from __future__ import annotations

from enum import StrEnum


class Statistica(StrEnum):
    PUNTI_SALUTE = "Punti Salute"
    ATTACCO = "Attacco"
    DIFESA = "Difesa"
    ATTACCO_SPECIALE = "Attacco Speciale"
    DIFESA_SPECIALE = "Difesa Speciale"
    VELOCITA = "Velocità"
    # ELUSIONE = "Elusione"
    # PRECISIONE = "Precisione"


class Statistiche:
    def __init__(
        self,
        punti_salute: int,
        attacco: int = 20,
        difesa: int = 20,
        attacco_speciale: int = 20,
        difesa_speciale: int = 20,
        velocita: int = 20,
    ):
        self._stats = {
            Statistica.PUNTI_SALUTE: punti_salute,
            Statistica.ATTACCO: attacco,
            Statistica.DIFESA: difesa,
            Statistica.ATTACCO_SPECIALE: attacco_speciale,
            Statistica.DIFESA_SPECIALE: difesa_speciale,
            Statistica.VELOCITA: velocita,
        }

    def copy(self) -> Statistiche:
        return Statistiche(
            self._stats[Statistica.PUNTI_SALUTE],
            self._stats[Statistica.ATTACCO],
            self._stats[Statistica.DIFESA],
            self._stats[Statistica.ATTACCO_SPECIALE],
            self._stats[Statistica.DIFESA_SPECIALE],
            self._stats[Statistica.VELOCITA],
        )

    def __getitem__(self, statistica: Statistica) -> int:
        return self._stats[statistica]

    def __setitem__(self, statistica: Statistica, valore: int) -> None:
        self._stats[statistica] = valore

    def __hash__(self) -> int:
        prime = 31
        result = 0
        for key, value in self._stats.items():
            result = result * prime + hash(key)
            result = result * prime + hash(value)
        return result

    def __eq__(self, other) -> bool:
        return isinstance(other, Statistiche) and self._stats == other._stats
    
    def __str__(self) -> str:
        return f"PS: {self._stats[Statistica.PUNTI_SALUTE]}"
