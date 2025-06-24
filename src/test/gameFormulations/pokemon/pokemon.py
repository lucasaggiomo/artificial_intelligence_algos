from __future__ import annotations

import textwrap
from abc import ABC
from enum import StrEnum
from test.gameFormulations.pokemon.elemento import Elemento
from test.gameFormulations.pokemon.mossa import (
    CategoriaMossaOffensiva,
    CategoriaMossaStato,
    Mossa,
    MossaOffensiva,
    MossaStato,
)
from test.gameFormulations.pokemon.statistiche import Statistica, Statistiche
from test.gameFormulations.pokemon.tipo import Tipo, get_moltiplicatore

from agentPackage.action import Action
from agentPackage.environment import Environment
from agentPackage.player import Player
from agentPackage.playerAI import PlayerAI
from agentPackage.sensor import Sensor, StateSensor
from agentPackage.state import State
from agentPackage.tasks.game import Game
from agentPackage.taskSolvers.gameTheory import DecisionAlgorithmType


class Allenatore(Elemento):
    """Un allenatore è un giocatore con un pokemon sul campo"""

    def __init__(self, name: str, pokemon: Pokemon):
        super().__init__(name)
        self.pokemon = pokemon

    def copy(self) -> Allenatore:
        """Restituisce una deep copy dell'Allenatore"""

        return Allenatore(
            self.name,
            self.pokemon.copy(),
        )

    def __str__(self) -> str:
        return f"{self.name}\n" + textwrap.indent(str(self.pokemon), "\t")


class PokemonPlayer(Player, Allenatore):
    """
    Un Player di pokemon estende la classe astratta Player ed è un allenatore.
    Si è voluto evitare che fondere questa classe con Allenatore. In questo modo, infatti,
    la classe Allenatore NON è un Player e non ha ciò che ne deriva (ad esempio un sensore).
    La classe Allenatore incapsula SOLO la logica dell'allenatore pokemon.
    La classe PokemonPlayer unisce la logica di Allenatore con quella di Player.
    """

    def __init__(self, sensor: Sensor, name: str, numero: int, pokemon: Pokemon):
        Player.__init__(self, sensor, name)
        Allenatore.__init__(self, name, pokemon)
        self.numero = numero

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

        # verifica se qualcuno è K.O.
        if ps_mio == 0 and ps_avversario > 0:
            return -1.0  # sconfitta
        elif ps_avversario == 0 and ps_mio > 0:
            return 1.0  # vittoria
        elif ps_mio == 0 and ps_avversario == 0:
            return 0.0  # pareggio

        # normalizza sulla somma totale degli HP
        total_ps = ps_mio + ps_avversario

        utility = (ps_mio - ps_avversario) / total_ps
        return utility

    # def chooseAction(self, game: PokemonGame) -> PokemonAction:
    #     return None


class PokemonPlayerAI(
    PokemonPlayer,
    PlayerAI,
):
    def __init__(
        self,
        name: str,
        numero: int,
        pokemon: Pokemon,
        decisionAlgorithm: DecisionAlgorithmType,
        limit: float = float("+inf"),
    ):
        sensor = StateSensor()
        PlayerAI.__init__(self, sensor, name, decisionAlgorithm, limit)
        PokemonPlayer.__init__(self, sensor, name, numero, pokemon)


class Pokemon(Elemento):
    """
    Un pokemon ha uno o più tipi, al più quattro mosse e una serie di statistiche
    Per semplicità, è omesso il livello del pokemon e quindi:
    - l'incremento delle statistiche all'aumentare dei livelli
    - le mosse che impara il pokemon all'aumentare dei livelli
    """

    def __init__(
        self,
        name: str,
        tipi: set[Tipo],
        statistiche: Statistiche,
        # allenatore: Optional[Allenatore],
        mosse: set[Mossa],
    ):
        if len(tipi) == 0:
            raise ValueError("Un pokemon deve avere almeno un tipo")

        super().__init__(name)
        self.tipi = tipi
        self.statistiche = statistiche
        # self.allenatore = allenatore
        self.mosse = mosse

    def copy(self) -> Pokemon:
        return Pokemon(
            self.name,
            self.tipi.copy(),
            self.statistiche.copy(),
            self.mosse.copy(),
        )

    def infliggiDanno(self, danno: int) -> None:
        vitaCorrente = self.statistiche[Statistica.PUNTI_SALUTE]
        vitaCorrente -= danno
        if vitaCorrente < 0:
            vitaCorrente = 0

        self.statistiche[Statistica.PUNTI_SALUTE] = vitaCorrente

    def applicaEffetto(self, mossa: MossaStato) -> None:
        """Applica l'effetto di stato (per ora solo BUFF o DEBUFF)"""
        for statistica, valore in mossa.modificheStatistiche.items():
            self.statistiche[statistica] += valore

    def isKO(self) -> bool:
        return not self.isAlive()

    def isAlive(self) -> bool:
        """True se il pokemon è K.O., False altrimenti"""
        ps = self.statistiche[Statistica.PUNTI_SALUTE]
        # print(f">>>>>>Punti salute di {self.name} = {ps}, restituisco {self.statistiche[Statistica.PUNTI_SALUTE] == 0}")
        return self.statistiche[Statistica.PUNTI_SALUTE] > 0

    def __hash__(self) -> int:
        prime = 31
        result = 0
        result = result * prime + hash(self.name)
        for tipo in self.tipi:
            result = result * prime + hash(tipo)
        # result = result * prime + hash(self.allenatore)
        result = result * prime + hash(self.statistiche)
        return result

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, Pokemon)
            and self.name == other.name
            and self.tipi == other.tipi
            # and self.allenatore == other.allenatore
            and self.statistiche == other.statistiche
        )

    def __str__(self) -> str:
        return f"{self.name}\n\tTipi = {[tipo.name for tipo in self.tipi]}\n\tStatistiche = {self.statistiche}\n"


# class Campo:
#     """Rappresenta il campo di battaglia che contiene due pokemon"""

#     def __init__(self, pokemon1: Pokemon, pokemon2: Pokemon):
#         self.pokemon1 = pokemon1
#         self.pokemon2 = pokemon2

#     def __eq__(self, other) -> bool:
#         return (
#             isinstance(other, Campo)
#             and self.pokemon1 == other.pokemon1
#             and self.pokemon2 == other.pokemon2
#         )

#     def __hash__(self) -> int:
#         prime = 31
#         result = 0
#         result = result * prime + hash(self.pokemon1)
#         result = result * prime + hash(self.pokemon2)
#         return result

#     def __str__(self) -> str:
#         return (
#             f"Pokemon1: " + textwrap.indent(str(self.pokemon1), "\t") + "\n"
#             "\t\tvs\n"
#             "Pokemon2: " + textwrap.indent(str(self.pokemon2), "\t")
#         )


class PokemonState(State):
    def __init__(
        self,
        allenatore1: Allenatore,
        allenatore2: Allenatore,
        # campo: Campo,
        turno: int = 1,  # 1 o 2
    ):
        self.allenatore1 = allenatore1
        self.allenatore2 = allenatore2
        # self.campo = campo
        self.turno = turno

    def copy(self) -> PokemonState:
        return PokemonState(
            self.allenatore1.copy(),
            self.allenatore2.copy(),
            # self.campo,
            self.turno,
        )

    # per accedere in maniera più semplice ai pokemon degli allenatori
    # sono property (per essere readonly)
    @property
    def pokemon1(self):
        return self.allenatore1.pokemon

    @property
    def pokemon2(self):
        return self.allenatore2.pokemon

    def commutaTurno(self):
        self.turno = 1 if self.turno == 2 else 2

    def __hash__(self) -> int:
        prime = 31
        result = 0
        result = result * prime + hash(self.allenatore1)
        result = result * prime + hash(self.allenatore2)
        # result = result * prime + hash(self.campo)
        result = result * prime + hash(self.turno)
        return result

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, PokemonState)
            and self.allenatore1 == other.allenatore1
            and self.allenatore2 == other.allenatore2
            # and self.campo == other.campo
            and self.turno == other.turno
        )

    def __str__(self) -> str:
        return (
            f"Allenatore1: {self.allenatore1}\n"
            f"Allenatore2: {self.allenatore2}\n"
            f"Turno di: {self.allenatore1.name if self.turno == 1 else self.allenatore2.name}"
        )
        # Campo: {self.campo}

    def __repr__(self) -> str:
        return str(self)


class PokemonAction(Action):
    """
    L'azione è rappresentata dalla mossa di un pokemon e dal pokemon che la effettua.
    Si potrebbero aggiungere in futuro come azioni possibili:
        - utilizzo di un rimedio (es: pozione) dalla borsa -> potrei farlo
        - utilizzo di un potenziamento dalla borsa -> non penso lo farò
        - cambia pokemon -> si complicherebbe molto aggiungere diversi pokemon
    """

    def __init__(
        self,
        pokemon: Pokemon,  # il pokemon che esegue la mossa
        mossa: Mossa,  # la mossa effettuata
        target: Pokemon,  # il pokemon che subisce la mossa
    ):
        self.pokemon = pokemon
        self.mossa = mossa
        self.target = target

    def calcolaDanno(self) -> int:
        """Questa funzione calcola il danno solo se la mossa riferita da questa azione è una mossa offensiva"""
        if not isinstance(self.mossa, MossaOffensiva):
            return 0

        # CALCOLO DANNO PURO

        # livello del pokemon attaccante
        livello = 50  # il livello è stato omesso per semplicità, viene assunto pari ad 1

        # in base alla categoria di mossa offensiva, cambia la statistica offensiva e difensiva da guardare (fisica o speciale)
        match self.mossa.categoria:
            case CategoriaMossaOffensiva.MOSSA_FISICA:
                attacco = self.pokemon.statistiche[Statistica.ATTACCO]
                difesa = self.target.statistiche[Statistica.DIFESA]
            case CategoriaMossaOffensiva.MOSSA_SPECIALE:
                attacco = self.pokemon.statistiche[Statistica.ATTACCO_SPECIALE]
                difesa = self.target.statistiche[Statistica.DIFESA_SPECIALE]

        danno = ((2 * livello / 5 + 2) * self.mossa.potenza * attacco / difesa) / 50 + 2

        # CALCOLO MOLTIPLICATORE
        moltiplicatore = 1.0
        for tipoTarget in self.target.tipi:
            moltiplicatore *= get_moltiplicatore(self.mossa.tipo, tipoTarget)

        # il danno incrementato se il pokemon attaccante è dello stesso tipo della mossa
        if self.mossa.tipo in self.pokemon.tipi:
            moltiplicatore *= 1.5

        # calcolo del danno arrotondato per difetto
        danno = int(danno * moltiplicatore)

        # se il danno è zero, il danno inflitto sarà:
        # - 0 se il moltiplicatore è 0 (ovvero la mossa non ha effetto sul tipo del pokemon target)
        # - 1 altrimenti

        if moltiplicatore == 0:
            return 0

        if danno == 0:
            return 1

        return danno

    def __hash__(self) -> int:
        prime = 31
        result = 0
        result = result * prime + hash(self.pokemon)
        result = result * prime + hash(self.mossa)
        return result

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, PokemonAction)
            and self.pokemon == other.pokemon
            and self.mossa == other.mossa
        )

    def __str__(self) -> str:
        return f"{self.pokemon.name} usa {self.mossa}!"

    def __repr__(self) -> str:
        return self.__str__()


class PokemonEnvironment(Environment):
    def __init__(self, initialState: PokemonState):
        super().__init__(initialState)

    def transitionModel(self, state: PokemonState, action: PokemonAction) -> PokemonState:
        return _transitionModel(state, action)


class PokemonGame(Game):
    def __init__(
        self,
        player1: PokemonPlayer,
        player2: PokemonPlayer,
    ):
        self.allenatore1 = player1
        self.allenatore2 = player2
        # self.campo = Campo(
        #     pokemon1=self.allenatore1.getFirstPokemon(),
        #     pokemon2=self.allenatore2.getFirstPokemon(),
        # )
        initialState = PokemonState(
            self.allenatore1,
            self.allenatore2,
            # self.campo,
        )
        self.environment = PokemonEnvironment(initialState)
        super().__init__(initialState, self.environment, [player1, player2])

    def terminalTest(self, state: PokemonState) -> bool:
        # print(">>>Verifico se qualcuno ha vinto...")
        # pokemon1Ko = state.pokemon1.isKO()
        # pokemon2Ko = state.pokemon2.isKO()
        return state.pokemon1.isKO() or state.pokemon2.isKO()

    def getActionsFromState(self, state: PokemonState) -> list[PokemonAction]:
        if state.turno == 1:
            mosse = state.pokemon1.mosse
            sottoscritto = state.pokemon1
            avversario = state.pokemon2
        else:
            mosse = state.pokemon2.mosse
            sottoscritto = state.pokemon2
            avversario = state.pokemon1

        # da ogni mossa possibile genera le possibili azioni
        azioni = []

        for mossa in mosse:
            if isinstance(mossa, MossaOffensiva):
                # se è una mossa offensiva, aggiunge l'azione di attaccare l'avversario
                nuovaAzione = PokemonAction(sottoscritto, mossa, avversario)

            elif isinstance(mossa, MossaStato):
                # se è una mossa di stato, aggiunge l'azione di usarla, in base alla categoria, su se stessa o sull'avversario
                match mossa.categoria:
                    case CategoriaMossaStato.MOSSA_BUFF:
                        target = sottoscritto
                    case CategoriaMossaStato.MOSSA_DEBUFF:
                        target = avversario

                nuovaAzione = PokemonAction(sottoscritto, mossa, target)

            azioni.append(nuovaAzione)

        return azioni

    def transitionModel(self, state: PokemonState, action: PokemonAction) -> PokemonState:
        return _transitionModel(state, action)


def _transitionModel(state: PokemonState, action: PokemonAction) -> PokemonState:
    """
    A partire da uno stato di partenza e da un'azione, restituisce lo stato successivo applicando la mossa associata all'azione
    """

    # crea una copia esatta (deep copy) dello stato corrente
    nuovoStato = state.copy()

    # applica l'azione (la mossa di un pokemon ad un target) nel nuovo stato
    # NOTA: il target NON è action.target, ma la COPIA di action.target presente in nuovoStato
    # Quindi trovo il target copiato, confrontandolo con action.target con "==" (opportunamente overridato in Pokemon.__eq__)
    if action.target == nuovoStato.allenatore1.pokemon:
        targetCopy = nuovoStato.allenatore1.pokemon
    else:
        targetCopy = nuovoStato.allenatore2.pokemon

    if isinstance(action.mossa, MossaOffensiva):
        danno = action.calcolaDanno()

        # effettua il danno sul pokemon target nel nuovoStato
        targetCopy.infliggiDanno(danno)

    elif isinstance(action.mossa, MossaStato):
        # effettua la mossa stato sul pokemon target nel nuovoStato
        targetCopy.applicaEffetto(action.mossa)

    nuovoStato.commutaTurno()

    return nuovoStato
