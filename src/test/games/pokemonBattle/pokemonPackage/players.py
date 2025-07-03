import threading as th
from test.games.pokemonBattle.pokemonPackage.allenatore import Allenatore
from test.games.pokemonBattle.pokemonPackage.mosse import (
    CategoriaMossaStato,
    Mossa,
    MossaOffensiva,
    MossaStato,
)
from test.games.pokemonBattle.pokemonPackage.pokemon import Pokemon
from test.games.pokemonBattle.pokemonPackage.pokemonAction import PokemonAction
from test.games.pokemonBattle.pokemonPackage.pokemonState import PokemonState
from test.games.pokemonBattle.pokemonPackage.statistiche import Statistica
from typing import Callable, Optional

from ai.core.sensor import Sensor, StateSensor
from ai.games.gameTheory import DecisionAlgorithmType, GameTheory
from ai.games.player import Player, PlayerAI

NUM_DIGITS = 6  # per l'approssimazione di getUtility


class PokemonPlayer(Allenatore, Player):
    """
    Un Player di pokemon estende la classe astratta Player ed è un allenatore.
    Si è voluto evitare che fondere questa classe con Allenatore. In questo modo, infatti,
    la classe Allenatore NON è un Player e non ha ciò che ne deriva (ad esempio un sensore).
    La classe Allenatore incapsula SOLO la logica dell'allenatore pokemon.
    La classe PokemonPlayer unisce la logica di Allenatore con quella di Player.
    """

    def __init__(self, sensor: Sensor, name: str, pokemon: Pokemon):
        Player.__init__(self, sensor, name)
        Allenatore.__init__(self, name, pokemon)
        self.numero: int = 0

    def getUtility(self, state: PokemonState) -> float:

        if self.numero == 1:
            mio_pokemon = state.pokemon1
            avversario = state.pokemon2
        else:
            mio_pokemon = state.pokemon2
            avversario = state.pokemon1

        # punti salute attuali
        ps_mio = mio_pokemon.statistiche[Statistica.PUNTI_SALUTE]
        ps_avversario = avversario.statistiche[Statistica.PUNTI_SALUTE]

        # penalizza il punteggio all'avanzare dei turni,
        # prediligendo una vittoria più rapida
        decay = 0.999**state.turno

        utility = 0.0

        # verifica se qualcuno è K.O.
        if ps_mio == 0 and ps_avversario > 0:
            utility = -1.0  # sconfitta
        elif ps_avversario == 0 and ps_mio > 0:
            utility = 1.0  # vittoria
        elif ps_mio == 0 and ps_avversario == 0:
            utility = 0.0
        else:
            # normalizza sulla somma totale degli HP
            total_ps = ps_mio + ps_avversario

            utility = (ps_mio - ps_avversario) / total_ps

            # print("Utility finale: " + str(utility))
            # global stampatoUtility
            # stampatoUtility = True

        utility *= decay
        return round(utility, NUM_DIGITS)


class PokemonPlayerUmano(PokemonPlayer):
    def __init__(self, name: str, pokemon: Pokemon):
        PokemonPlayer.__init__(self, StateSensor(), name, pokemon)
        self.chosenMove = None
        self._moveSelectedEvent: th.Event = th.Event()
        self._registerMoveCallback: Optional[Callable[[Pokemon, Callable[[Mossa], None]], None]] = (
            None
        )

    def registerMoveCallback(self, callback: Callable[[Pokemon, Callable[[Mossa], None]], None]):
        """
        La GUI userà questo per registrare una funzione che permette a questo player di mostrare le mosse
        e fornire una callback da chiamare una volta che l'utente ha scelto.
        """
        self._registerMoveCallback = callback

    def chooseAction(self, game: "PokemonGame") -> PokemonAction:  # type: ignore
        # azzera lo stato precedente
        self.mossaScelta = None
        self._moveSelectedEvent.clear()

        if self._registerMoveCallback:
            # mostra le mosse e passa la callback che riceverà la mossa scelta
            self._registerMoveCallback(self.pokemon, self._onMoveSelected)
        else:
            raise RuntimeError("Non c'è una callback per mostrare le mosse del player")

        # attende che l'utente selezioni una mossa
        self._moveSelectedEvent.wait()

        # genera l'azione capendo chi sia il target (per semplicità lo assume dal tipo di mossa anziché chiederlo all'utente)
        if self.numero == 1:
            pokemonAvversario = game.allenatore2.pokemon
        else:
            pokemonAvversario = game.allenatore1.pokemon

        if isinstance(self.mossaScelta, MossaOffensiva):
            target = pokemonAvversario
        elif isinstance(self.mossaScelta, MossaStato):
            if self.mossaScelta.categoria == CategoriaMossaStato.MOSSA_BUFF:
                target = self.pokemon
            else:
                target = pokemonAvversario

        azione = PokemonAction(self.pokemon, self.mossaScelta, target)  # type: ignore
        print(f"Danno calcolato: {azione.calcolaDanno()}, target = {target.name}")

        # restituisce l'azione scelta
        return azione

    def _onMoveSelected(self, mossa: Mossa):
        self.mossaScelta = mossa
        self._moveSelectedEvent.set()


class PokemonPlayerAI(
    PokemonPlayer,
    PlayerAI,
):
    def __init__(
        self,
        name: str,
        pokemon: Pokemon,
        decisionAlgorithm: DecisionAlgorithmType = GameTheory.minimaxAlphaBetaDecision,
        limit: float = float("+inf"),
    ):
        sensor = StateSensor()
        PlayerAI.__init__(self, sensor, name, decisionAlgorithm, limit)
        PokemonPlayer.__init__(self, sensor, name, pokemon)
