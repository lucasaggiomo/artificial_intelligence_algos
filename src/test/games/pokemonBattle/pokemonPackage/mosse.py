from abc import ABC
from enum import StrEnum
from test.games.pokemonBattle.pokemonPackage.elemento import Elemento
from test.games.pokemonBattle.pokemonPackage.statistiche import Statistica
from test.games.pokemonBattle.pokemonPackage.tipo import Tipo


class MossaError(Exception):
    pass


class Mossa(Elemento, ABC):
    """
    Una mossa è l'azione principale che un Pokemon esegue durante una lotta
    Ogni mossa ha:
    - un tipo
    - una precisione (da 1 a 100, indica la probabilità di successo)
    - vari punti potenza (indica il numero di possibili esecuzioni) -> omesso per semplicità
    - un eventuale 'cooldown', che indica il numero di turni in cui la mossa è disabilitata dopo la sua esecuzione (default 0)

    NOTA:   questa classe non ha uno "stato" interno. Ogni istanza può essere utilizzata per associare una stessa mossa
            a diversi Pokemon contemporaneamente. L'idea che sia il Pokémon ad avere lo stato, non la mossa.
    """

    def __init__(
        self,
        name: str,
        tipo: Tipo,
        cooldown: int = 0,
    ):
        super().__init__(name)
        self.tipo = tipo
        self.cooldown = cooldown

    def __hash__(self) -> int:
        prime = 31
        result = 0
        result = result * prime + hash(self.name)
        result = result * prime + hash(self.tipo)
        result = result * prime + hash(self.cooldown)
        return result

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, Mossa)
            and self.name == other.name
            and self.tipo == other.tipo
            and self.cooldown == other.cooldown
        )


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
        potenza: int,
        categoria: CategoriaMossaOffensiva,
        cooldown: int = 0,
    ):
        super().__init__(
            name,
            tipo,
            cooldown,
        )
        self.potenza = potenza
        self.categoria = categoria

    def __hash__(self) -> int:
        prime = 31
        result = super().__hash__()
        result = result * prime + hash(self.potenza)
        result = result * prime + hash(self.categoria)
        return result

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, MossaOffensiva)
            and self.name == other.name
            and self.tipo == other.tipo
            and self.potenza == other.potenza
            and self.categoria == other.categoria
            and self.cooldown == other.cooldown
        )


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
        categoria: CategoriaMossaStato,
        modificheStatistiche: dict[Statistica, int],
        cooldown: int = 0,
    ):
        super().__init__(
            name,
            tipo,
            cooldown,
        )
        self.categoria = categoria
        self.modificheStatistiche = modificheStatistiche

    def __hash__(self) -> int:
        prime = 31
        result = super().__hash__()
        result = result * prime + hash(self.categoria)
        for statistica, value in self.modificheStatistiche.items():
            result = result * prime + hash(statistica)
            result = result * prime + hash(value)
        return result

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, MossaStato)
            and self.name == other.name
            and self.tipo == other.tipo
            and self.categoria == other.categoria
            and self.modificheStatistiche == other.modificheStatistiche
            and self.cooldown == other.cooldown
        )
