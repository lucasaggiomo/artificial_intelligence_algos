from abc import ABC
from enum import StrEnum
from test.gameFormulations.pokemon.elemento import Elemento
from test.gameFormulations.pokemon.statistiche import Statistica
from test.gameFormulations.pokemon.tipo import Tipo


class Mossa(Elemento, ABC):
    """
    Una mossa è l'azione principale che un Pokemon esegue durante una lotta
    Ogni mossa ha:
    - un tipo
    - una precisione (da 1 a 100, indica la probabilità di successo)
    - vari punti potenza (indica il numero di possibili esecuzioni) -> omesso per semplicità
    """

    def __init__(
        self,
        name: str,
        tipo: Tipo,
        precisione: int = 100,
        # punti_potenza: int,
    ):
        super().__init__(name)
        self.tipo = tipo
        self.precisione = precisione
        # self.punti_potenza = punti_potenza


class CategoriaMossaOffensiva(StrEnum):
    MOSSA_FISICA = "Fisica"
    MOSSA_SPECIALE = "Speciale"


class MossaOffensiva(Mossa):
    """
    Una mossa offensiva è una mossa che infligge danno.
    È caratterizzata, oltre dai parametri ereditati dalla Mossa, da:
    - un valore di potenza, utilizzato per il calcolo del danno inflitto
    - una categoria, che può essere Fisica o Speciale, determinante nel calcolo del danno
    """

    def __init__(
        self,
        name: str,
        tipo: Tipo,
        # punti_potenza: int,
        potenza: int,
        categoria: CategoriaMossaOffensiva,
        precisione: int = 100,
    ):
        super().__init__(
            name,
            tipo,
            precisione,
            # punti_potenza,
        )
        self.potenza = potenza
        self.categoria = categoria


class CategoriaMossaStato(StrEnum):
    MOSSA_BUFF = "Buff"
    MOSSA_DEBUFF = "Debuff"


class MossaStato(Mossa):
    """
    Una mossa di stato è una mossa che non infligge danno.
    Può ad esempio aumentare o diminuire una o più statistiche, infliggere o curare un problema di stato.
    La categoria indica se:
    - è una possa potenziante (buff) [ovvero il target sarà il pokemon che la effettua]
    - è una possa depotenziante (debuff) [ovvero il target sarà il pokemon avversario]
    """

    def __init__(
        self,
        name: str,
        tipo: Tipo,
        # punti_potenza: int,
        categoria: CategoriaMossaStato,
        modificheStatistiche: dict[Statistica, int],
        precisione: int = 100,
    ):
        super().__init__(
            name,
            tipo,
            precisione,
            # punti_potenza,
        )
        self.categoria = categoria
        self.modificheStatistiche = modificheStatistiche
