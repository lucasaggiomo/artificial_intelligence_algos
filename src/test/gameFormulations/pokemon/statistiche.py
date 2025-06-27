from __future__ import annotations

from enum import StrEnum


class Statistica(StrEnum):
    PUNTI_SALUTE = "Punti Salute"
    ATTACCO = "Attacco"
    DIFESA = "Difesa"
    ATTACCO_SPECIALE = "Attacco Speciale"
    DIFESA_SPECIALE = "Difesa Speciale"
    # VELOCITA = "Velocità"
    # ELUSIONE = "Elusione"
    # PRECISIONE = "Precisione"


class Statistiche:
    def __init__(
        self,
        punti_salute: int,
        attacco: int = 50,
        difesa: int = 50,
        attacco_speciale: int = 50,
        difesa_speciale: int = 50,
    ):
        self._stats = {
            Statistica.PUNTI_SALUTE: punti_salute,
            Statistica.ATTACCO: attacco,
            Statistica.DIFESA: difesa,
            Statistica.ATTACCO_SPECIALE: attacco_speciale,
            Statistica.DIFESA_SPECIALE: difesa_speciale,
        }

    def copy(self) -> Statistiche:
        return Statistiche(
            self._stats[Statistica.PUNTI_SALUTE],
            self._stats[Statistica.ATTACCO],
            self._stats[Statistica.DIFESA],
            self._stats[Statistica.ATTACCO_SPECIALE],
            self._stats[Statistica.DIFESA_SPECIALE],
        )

    def changeTo(self, other: Statistiche) -> None:
        """Metodo di comodo che rende un oggetto Statistiche già esistente uguale a delle statistiche in input"""
        self._stats[Statistica.PUNTI_SALUTE] = other._stats[Statistica.PUNTI_SALUTE]
        self._stats[Statistica.ATTACCO] = other._stats[Statistica.ATTACCO]
        self._stats[Statistica.DIFESA] = other._stats[Statistica.DIFESA]
        self._stats[Statistica.ATTACCO_SPECIALE] = other._stats[Statistica.ATTACCO_SPECIALE]
        self._stats[Statistica.DIFESA_SPECIALE] = other._stats[Statistica.DIFESA_SPECIALE]

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
        return "\n".join(f"{stat.name}: {value}" for stat, value in self._stats.items())
