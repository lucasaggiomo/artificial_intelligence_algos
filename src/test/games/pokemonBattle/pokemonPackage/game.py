from test.games.pokemonBattle.pokemonPackage.mosse import (
    CategoriaMossaStato,
    MossaOffensiva,
    MossaStato,
)
from test.games.pokemonBattle.pokemonPackage.players import PokemonPlayer
from test.games.pokemonBattle.pokemonPackage.pokemonAction import PokemonAction
from test.games.pokemonBattle.pokemonPackage.pokemonState import PokemonState
from typing import Callable, Optional

from ai.environment import Environment
from ai.tasks.game import Game


class PokemonEnvironment(Environment):
    def __init__(self, initialState: PokemonState):
        super().__init__(initialState)
        self.currentState = initialState
        self.updateCallback: Optional[
            Callable[[PokemonState, PokemonAction, PokemonState], None]
        ] = None

    def transitionModel(self, state: PokemonState, action: PokemonAction) -> PokemonState:
        return _transitionModel(state, action)

    def evolveState(self, action: PokemonAction) -> PokemonState:
        # evolve lo stato corrente, salvandosi una COPIA di quello precedente.
        # Il riferimento self.currentState viene preservato
        oldState = self.currentState.copy()
        self.currentState.changeTo(self.transitionModel(oldState, action))
        if self.updateCallback:
            self.updateCallback(oldState, action, self.currentState)
        return self.currentState


class PokemonGame(Game):
    def __init__(
        self,
        player1: PokemonPlayer,
        player2: PokemonPlayer,
    ):
        player1.numero = 1
        player2.numero = 2
        self.allenatore1 = player1
        self.allenatore2 = player2
        # self.campo = Campo(
        #     pokemon1=self.allenatore1.getFirstPokemon(),
        #     pokemon2=self.allenatore2.getFirstPokemon(),
        # )
        self.initialState = PokemonState(
            self.allenatore1,
            self.allenatore2,
            # self.campo,
        )
        self.environment = PokemonEnvironment(self.initialState)
        super().__init__(self.initialState, self.environment, [player1, player2])

    def setUpdateCallback(
        self, updateCallback: Callable[[PokemonState, PokemonAction, PokemonState], None]
    ):
        self.environment.updateCallback = updateCallback

    def terminalTest(self, state: PokemonState) -> bool:
        # pokemon1Ko = state.pokemon1.isKO()
        # pokemon2Ko = state.pokemon2.isKO()
        # print(">>>Verifico se qualcuno ha vinto...", pokemon1Ko, pokemon2Ko)
        return state.pokemon1.isKO() or state.pokemon2.isKO()

    def getActionsFromState(self, state: PokemonState) -> list[PokemonAction]:
        if state.turno % 2 == 0:
            sottoscritto = state.pokemon1
            avversario = state.pokemon2
        else:
            sottoscritto = state.pokemon2
            avversario = state.pokemon1

        mosse = sottoscritto.getMosseDisponibili()

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

    # Applica l'azione (la mossa di un pokemon ad un target) nel nuovo stato
    # Quindi individua il pokemon che esegue la mossa e il pokemon target
    # NOTA: il target (così come il pokemon 'esecutore') NON è action.target, ma la COPIA di action.target presente in nuovoStato
    # Questa cosa è importante per evitare di modificare il target associato allo stato corrente
    # Quindi trovo il target copiato, confrontandolo con action.target con "==" (opportunamente overridato in Pokemon.__eq__)
    if action.pokemon == nuovoStato.allenatore1.pokemon:
        pokemonEsecutore = nuovoStato.allenatore1.pokemon
        pokemonAvversario = nuovoStato.allenatore2.pokemon
    else:
        pokemonEsecutore = nuovoStato.allenatore2.pokemon
        pokemonAvversario = nuovoStato.allenatore1.pokemon

    # NOTA: target NON è necessariamente il pokemon avversario (esempio: MossaStato di categoria BUFF)
    if action.target == nuovoStato.allenatore1.pokemon:
        pokemonTarget = nuovoStato.allenatore1.pokemon
    else:
        pokemonTarget = nuovoStato.allenatore2.pokemon

    if isinstance(action.mossa, MossaOffensiva):
        danno = action.calcolaDanno()

        # effettua il danno sul pokemon target nel nuovoStato e aggiorna il danno dell'azione
        action.danno = pokemonTarget.infliggiDanno(danno)

    elif isinstance(action.mossa, MossaStato):
        # effettua la mossa stato sul pokemon target nel nuovoStato
        pokemonTarget.applicaEffetto(action.mossa)

    # notifica il pokemon che ha eseguito la mossa
    pokemonEsecutore.notificaUtilizzoMossa(action.mossa)

    nuovoStato.azione_precedente = action
    nuovoStato.turno += 1

    # notifica il pokemon avversario che il turno è passato e quindi che tocca di nuovo a lui
    # NON va notificato anche il pokemon esecutore. La notifica del turno ha lo scopo di decrementare
    # il cooldown, quindi deve avvenire solo quando è di nuovo il turno del pokemon da notificare
    pokemonAvversario.notificaTurnoPassato()

    # DEBUG
    # global stampatoUtility
    # if stampatoUtility:
    #     tabs = "\t\t\t\t" * (nuovoStato.turno - 1)
    #     stampatoUtility = False
    # else:
    #     tabs = "\t"
    # print(
    #     f"{tabs}{nuovoStato.turno} {nuovoStato.azione_precedente.mossa.name}: {nuovoStato.pokemon1.statistiche[Statistica.PUNTI_SALUTE]} - {nuovoStato.pokemon2.statistiche[Statistica.PUNTI_SALUTE]}\t",
    #     end="",
    # )

    return nuovoStato


# stampatoUtility = False
