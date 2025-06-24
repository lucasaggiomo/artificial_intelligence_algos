import sys
from test.gameFormulations.pokemon.mossa import (
    CategoriaMossaOffensiva,
    Mossa,
    MossaOffensiva,
)
from test.gameFormulations.pokemon.pokemon import (
    Allenatore,
    Pokemon,
    PokemonEnvironment,
    PokemonGame,
    PokemonPlayerAI,
    PokemonState,
)
from test.gameFormulations.pokemon.statistiche import Statistiche
from test.gameFormulations.pokemon.tipo import Tipo

from agentPackage.taskSolvers.gameTheory import GameTheory


def getFromArgvOrDefault(index: int, default) -> int:
    try:
        return int(sys.argv[index])
    except:
        return default


def main():
    azione = MossaOffensiva(
        "Azione",
        Tipo.NORMALE,
        40,
        CategoriaMossaOffensiva.MOSSA_FISICA,
    )
    azione_elettrica = MossaOffensiva(
        "AzioneElettrica",
        Tipo.ELETTRO,
        35,
        CategoriaMossaOffensiva.MOSSA_SPECIALE,
    )
    graffio = MossaOffensiva(
        "Graffio",
        Tipo.NORMALE,
        35,
        CategoriaMossaOffensiva.MOSSA_FISICA,
    )

    pikachu = Pokemon(
        "Pikachu",
        {Tipo.ELETTRO},
        Statistiche(punti_salute=100, attacco_speciale=30),
        {azione, azione_elettrica},
    )
    bulbasaur = Pokemon("Bulbasaur", {Tipo.NORMALE}, Statistiche(punti_salute=120), {graffio})

    player1 = PokemonPlayerAI(
        "Allenatore1",
        1,
        pikachu,
        GameTheory.minimaxAlphaBetaDecision,
        limit=2,
    )
    player2 = PokemonPlayerAI(
        "Allenatore2",
        2,
        bulbasaur,
        GameTheory.minimaxAlphaBetaDecision,
        limit=2,
    )

    game = PokemonGame(player1, player2)
    solver = GameTheory(game)

    solver.startGame()


if __name__ == "__main__":
    main()
