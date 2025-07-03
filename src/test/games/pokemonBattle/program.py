import threading as th
from test.games.pokemonBattle.ai_impl.game import PokemonGame
from test.games.pokemonBattle.ai_impl.players import PokemonPlayerAI, PokemonPlayerUmano
from test.games.pokemonBattle.core.mosse import (
    CategoriaMossaOffensiva,
    CategoriaMossaStato,
    MossaOffensiva,
    MossaStato,
)
from test.games.pokemonBattle.core.pokemon import Pokemon
from test.games.pokemonBattle.core.statistiche import Statistica, Statistiche
from test.games.pokemonBattle.core.tipo import Tipo
from test.games.pokemonBattle.ui.pokemonUI import BattleGUI

from ai.games.gameTheory import GameTheory


def creaGame() -> PokemonGame:
    # mosse
    body_slam = MossaOffensiva(
        "Body Slam",
        Tipo.NORMALE,
        80,
        CategoriaMossaOffensiva.MOSSA_FISICA,
    )
    pistolacqua = MossaOffensiva(
        "Pistolacqua",
        Tipo.ACQUA,
        40,
        CategoriaMossaOffensiva.MOSSA_SPECIALE,
    )
    skull_bash = MossaOffensiva(
        "Skull Bash",
        Tipo.NORMALE,
        100,
        CategoriaMossaOffensiva.MOSSA_FISICA,
    )
    bruciatutto = MossaOffensiva(
        "Bruciatutto",
        Tipo.FUOCO,
        90,
        CategoriaMossaOffensiva.MOSSA_SPECIALE,
    )
    slash = MossaOffensiva(
        "Slash",
        Tipo.NORMALE,
        70,
        CategoriaMossaOffensiva.MOSSA_FISICA,
    )
    fire_spin = MossaOffensiva(
        "Fire Spin",
        Tipo.FUOCO,
        35,
        CategoriaMossaOffensiva.MOSSA_SPECIALE,
    )
    foglielama = MossaOffensiva(
        "Foglielama",
        Tipo.ERBA,
        55,
        CategoriaMossaOffensiva.MOSSA_SPECIALE,
    )
    azione = MossaOffensiva(
        "Azione",
        Tipo.NORMALE,
        50,
        CategoriaMossaOffensiva.MOSSA_FISICA,
    )
    solarraggio = MossaOffensiva(
        "Solarraggio",
        Tipo.ERBA,
        120,
        CategoriaMossaOffensiva.MOSSA_SPECIALE,
        cooldown=1,
    )
    cura = MossaStato(
        "Cura",
        Tipo.NORMALE,
        categoria=CategoriaMossaStato.MOSSA_BUFF,
        modificheStatistiche={Statistica.PUNTI_SALUTE: 40},
    )
    cuordileone_speciale = MossaStato(
        "Cuordileone",
        Tipo.NORMALE,
        categoria=CategoriaMossaStato.MOSSA_BUFF,
        modificheStatistiche={Statistica.ATTACCO: 15, Statistica.ATTACCO_SPECIALE: 20},
    )
    difesa_speciale = MossaStato(
        "Difesa",
        Tipo.NORMALE,
        categoria=CategoriaMossaStato.MOSSA_BUFF,
        modificheStatistiche={Statistica.DIFESA: 15, Statistica.DIFESA_SPECIALE: 15},
    )
    prepotenza_speciale = MossaStato(
        "Prepotenza",
        Tipo.NORMALE,
        categoria=CategoriaMossaStato.MOSSA_DEBUFF,
        modificheStatistiche={Statistica.DIFESA: -10, Statistica.DIFESA_SPECIALE: -10},
    )

    # Pokemon
    blastoise = Pokemon(
        "Blastoise",
        {Tipo.ACQUA},
        Statistiche(
            punti_salute=150, attacco=60, difesa=120, attacco_speciale=65, difesa_speciale=130
        ),
        {body_slam, pistolacqua, skull_bash, prepotenza_speciale},
    )
    charizard = Pokemon(
        "Charizard",
        {Tipo.FUOCO},
        Statistiche(
            punti_salute=120, attacco=85, difesa=70, attacco_speciale=90, difesa_speciale=75
        ),
        {bruciatutto, slash, fire_spin, prepotenza_speciale},
    )
    venusaur = Pokemon(
        "Venusaur",
        {Tipo.ERBA},
        Statistiche(
            punti_salute=135, attacco=75, difesa=90, attacco_speciale=80, difesa_speciale=95
        ),
        {foglielama, azione, solarraggio, cuordileone_speciale},
    )

    # allenatori (player)
    player1 = PokemonPlayerAI(
        "Blastoise's Allenatore",
        blastoise,
        # limit=20,
    )
    player2 = PokemonPlayerAI(
        "Charizard's Allenatore",
        charizard,
        limit=20,
    )
    player3 = PokemonPlayerAI(
        "Venusaur's Allenatore",
        venusaur,
        limit=20,
    )

    # battaglia pokemon
    game = PokemonGame(
        player1,
        player3,
    )

    return game


def main():

    game = creaGame()

    def runTkinter(waitTurnEvent: th.Event):
        app = BattleGUI(game.initialState, waitTurnEvent)
        game.environment._updateCallback = app.update_callback
        app.runMainLoop()

    def solve():
        try:
            solver = GameTheory(game, waitTurnEvent)
            solver.startGame()
        except Exception as e:
            print(
                f"Eccezione non gestita nel solver (probabilmente hai chiuso senza terminare la battaglia): {e}"
            )

    waitTurnEvent = th.Event()
    solverThread = th.Thread(name="solverThread", target=solve, args=())
    solverThread.start()

    # tkThread = th.Thread(name="tkinterThread", target=runTkinter, args=(waitTurnEvent,))
    # tkThread.start()
    runTkinter(waitTurnEvent)

    # tkThread.join()
    print("Attendo la terminazione del solver thread...")
    waitTurnEvent.set()
    solverThread.join()


if __name__ == "__main__":
    main()
