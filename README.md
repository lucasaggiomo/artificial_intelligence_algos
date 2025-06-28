# artificial_intelligence_algos

Alcuni algoritmi del corso di Elementi di Intelligenza Artificiale, basati sul libro **Artificial Intelligence - A Modern Approach (Stuart J. Russell, Peter Norvig)**.

## Struttura repository
La cartella (package) [src](./src) contiene i package e i moduli in cui sono implementati gli algoritmi. In particolare contiene il package [agentPackage](./src/agentPackage/) in cui sono presenti:
- l'implementazione di alcuni algoritmi di ricerca nella classe [ProblemSolving](./src/agentPackage/taskSolvers/problemSolving.py)
- l'implementazione di alcuni algoritmi legati alla Teoria dei Giochi nella classe [GameTheory](./src/agentPackage/taskSolvers/gameTheory.py).
- una serie di classi astratte che possono essere implementate per realizzare i *problemi*/*giochi* desiderati, sulla base degli algoritmi implementati citati in precedenza.

La cartella (package) [test](./src/test) contiene alcune implementazioni basilari di problemi e giochi.
In particolare, è possibile eseguire, **a partire dalla cartella [src](./src)** della repository:
- i test dei problemi (ProblemSolving, con l'utilizzo degli algoritmi di ricerca) eseguendo il modulo desiderato con:
    
    ```
    python -m test.problems.[NOME_PROBLEMA].program
    ```
    
    dove NOME_PROBLEMA è il nome del problema (es: nPuzzle, googleMaps, vacuumCleaner)
- i test dei giochi (GameTheory, con l'utilizzo dell'algoritmo minimax) eseguendo il modulo desiderato con:
    
    ```
    python -m test.games.[NOME_GIOCO].program
    ```
    
    dove NOME_GIOCO è il nome del gioco (es: pokemonBattle, ticTacToe)

### PokemonBattle
Nel caso del gioco della battaglia pokemon, è possibile istanziare le mosse e i pokemon desiderati, con l'unica accortezza di dover aggiungere le rispettive immagini per i pokemon nella cartella [img](./src/test/games/pokemonBattle/img).

Per ogni pokemon inserito vanno aggiunte due immagini in tale cartella:
- [NOME_POKEMON]_front.png
- [NOME_POKEMON]_back.png

Dove NOME_POKEMON è il nome assegnato al pokemon (attributo *name* della classe **Pokemon**)

È possibile creare allenatori umani con la classe **PokemonPlayerUmano**, oppure allenatori AI con la classe **PokemonPlayerAI**.

Per ora ogni allenatore può possedere un solo pokemon.