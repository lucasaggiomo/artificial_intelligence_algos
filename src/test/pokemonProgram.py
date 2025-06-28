import threading as th
from test.gameFormulations.pokemon.game import PokemonGame
from test.gameFormulations.pokemon.mosse import (
    CategoriaMossaOffensiva,
    CategoriaMossaStato,
    MossaOffensiva,
    MossaStato,
)
from test.gameFormulations.pokemon.players import PokemonPlayerAI, PokemonPlayerUmano
from test.gameFormulations.pokemon.pokemon import Pokemon
from test.gameFormulations.pokemon.pokemonUI import BattleGUI
from test.gameFormulations.pokemon.statistiche import Statistica, Statistiche
from test.gameFormulations.pokemon.tipo import Tipo

from agentPackage.taskSolvers.gameTheory import GameTheory


def creaGame1() -> PokemonGame:
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
        {body_slam, pistolacqua, skull_bash, difesa_speciale},
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
    player1 = PokemonPlayerUmano(
        "Blastoise's Allenatore",
        blastoise,
    )
    player2 = PokemonPlayerAI(
        "Charizard's Allenatore",
        charizard,
        GameTheory.minimaxAlphaBetaDecision,
        limit=20,
    )
    player3 = PokemonPlayerUmano(
        "Venusaur's Allenatore",
        venusaur,
    )

    # battaglia pokemon
    game = PokemonGame(
        player3,
        player1,
    )

    return game


def creaGame2() -> PokemonGame:
    # Mosse offensive
    dragartigli = MossaOffensiva(
        "Dragartigli",
        Tipo.DRAGO,
        80,
        CategoriaMossaOffensiva.MOSSA_FISICA,
    )

    psicoraggio = MossaOffensiva(
        "Psicoraggio",
        Tipo.PSICO,
        65,
        CategoriaMossaOffensiva.MOSSA_SPECIALE,
    )

    zuffa = MossaOffensiva(
        "Zuffa",
        Tipo.LOTTA,
        120,
        CategoriaMossaOffensiva.MOSSA_FISICA,
    )

    metaltestata = MossaOffensiva(
        "Metaltestata",
        Tipo.ACCIAIO,
        90,
        CategoriaMossaOffensiva.MOSSA_FISICA,
    )

    morso = MossaOffensiva(
        "Morso",
        Tipo.BUIO,
        60,
        CategoriaMossaOffensiva.MOSSA_FISICA,
    )

    # Mosse di stato
    cura_totale = MossaStato(
        "Cura Totale",
        Tipo.NORMALE,
        categoria=CategoriaMossaStato.MOSSA_BUFF,
        modificheStatistiche={Statistica.PUNTI_SALUTE: 70},
    )

    sacrificio_potere = MossaStato(
        "Sacrificio di Potere",
        Tipo.LOTTA,
        categoria=CategoriaMossaStato.MOSSA_BUFF,
        modificheStatistiche={
            Statistica.ATTACCO: 25,
            Statistica.ATTACCO_SPECIALE: 25,
            Statistica.DIFESA: -10,
            Statistica.DIFESA_SPECIALE: -10,
        },
    )

    scudo_psichico = MossaStato(
        "Scudo Psichico",
        Tipo.PSICO,
        categoria=CategoriaMossaStato.MOSSA_BUFF,
        modificheStatistiche={
            Statistica.DIFESA: 20,
            Statistica.DIFESA_SPECIALE: 20,
        },
    )

    abbassa_morale = MossaStato(
        "Abbassa Morale",
        Tipo.BUIO,
        categoria=CategoriaMossaStato.MOSSA_DEBUFF,
        modificheStatistiche={
            Statistica.ATTACCO: -20,
            Statistica.ATTACCO_SPECIALE: -20,
        },
    )

    # Salamence - drago offensivo
    salamence = Pokemon(
        "Salamence",
        {Tipo.DRAGO, Tipo.VOLANTE},
        Statistiche(
            punti_salute=130,
            attacco=110,
            difesa=80,
            attacco_speciale=95,
            difesa_speciale=80,
        ),
        {dragartigli, zuffa, sacrificio_potere, morso},
    )

    # Metagross – tank misto
    metagross = Pokemon(
        "Metagross",
        {Tipo.ACCIAIO, Tipo.PSICO},
        Statistiche(
            punti_salute=140,
            attacco=100,
            difesa=110,
            attacco_speciale=80,
            difesa_speciale=100,
        ),
        {metaltestata, scudo_psichico, psicoraggio, cura_totale},
    )

    # Umbreon – difensore fastidioso
    umbreon = Pokemon(
        "Umbreon",
        {Tipo.BUIO},
        Statistiche(
            punti_salute=160,
            attacco=65,
            difesa=110,
            attacco_speciale=60,
            difesa_speciale=130,
        ),
        {morso, abbassa_morale, cura_totale, scudo_psichico},
    )

    player_salamence = PokemonPlayerAI(
        "Allenatore Salamence",
        salamence,
        GameTheory.minimaxAlphaBetaDecision,
        limit=20,
    )

    player_metagross = PokemonPlayerAI(
        "Allenatore Metagross",
        metagross,
        GameTheory.minimaxAlphaBetaDecision,
        limit=20,
    )

    player_umbreon = PokemonPlayerAI(
        "Allenatore Umbreon",
        umbreon,
        GameTheory.minimaxAlphaBetaDecision,
        limit=20,
    )

    # game
    game = PokemonGame(player_umbreon, player_metagross)
    return game


def main():

    game = creaGame1()

    def runTkinter(waitTurnEvent: th.Event):
        app = BattleGUI(game.initialState, waitTurnEvent)
        game.setUpdateCallback(app.update_callback)
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
