import threading as th
from test.gameFormulations.pokemon.mossa import (
    CategoriaMossaOffensiva,
    CategoriaMossaStato,
    MossaOffensiva,
    MossaStato,
)
from test.gameFormulations.pokemon.pokemon import Pokemon, PokemonGame, PokemonPlayerAI
from test.gameFormulations.pokemon.pokemonUI import BattleGUI
from test.gameFormulations.pokemon.statistiche import Statistica, Statistiche
from test.gameFormulations.pokemon.tipo import Tipo

from agentPackage.taskSolvers.gameTheory import GameTheory


def main():
    # mosse
    azione = MossaOffensiva(
        "Azione",
        Tipo.NORMALE,
        50,
        CategoriaMossaOffensiva.MOSSA_FISICA,
    )
    breccia = MossaOffensiva(
        "Breccia",
        Tipo.LOTTA,
        40,
        CategoriaMossaOffensiva.MOSSA_SPECIALE,
    )
    graffio = MossaOffensiva(
        "Graffio",
        Tipo.NORMALE,
        35,
        CategoriaMossaOffensiva.MOSSA_FISICA,
    )
    cura = MossaStato(
        "Cura",
        Tipo.NORMALE,
        categoria=CategoriaMossaStato.MOSSA_BUFF,
        modificheStatistiche={Statistica.PUNTI_SALUTE: 40},
    )

    # Pokemon
    pikachu = Pokemon(
        "Pikachu",
        {Tipo.ELETTRO},
        Statistiche(punti_salute=100, attacco_speciale=30),
        {azione, breccia, cura},
    )
    bulbasaur = Pokemon(
        "Bulbasaur",
        {Tipo.NORMALE},
        Statistiche(punti_salute=200),
        {graffio, cura},
    )

    # allenatori (player)
    player1 = PokemonPlayerAI(
        "Allenatore1",
        1,
        pikachu,
        GameTheory.minimaxAlphaBetaDecision,
        limit=5,
    )
    player2 = PokemonPlayerAI(
        "Allenatore2",
        2,
        bulbasaur,
        GameTheory.minimaxAlphaBetaDecision,
        limit=5,
    )

    # battaglia pokemon
    game = PokemonGame(
        player1,
        player2,
    )

    def runTkinter(waitTurnEvent: th.Event):
        app = BattleGUI(game.initialState, waitTurnEvent)
        game.setUpdateCallback(app.update_callback)
        app.runMainLoop()

    waitTurnEvent = th.Event()
    tkThread = th.Thread(target=runTkinter, args=(waitTurnEvent,))
    tkThread.start()

    def solve():
        solver = GameTheory(game, waitTurnEvent)
        solver.startGame()

    solverThread = th.Thread(target=solve, args=())
    solverThread.start()

    tkThread.join()
    waitTurnEvent.set()
    solverThread.join()


if __name__ == "__main__":
    main()
