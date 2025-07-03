from __future__ import annotations

import textwrap
from test.games.pokemonBattle.pokemonPackage.allenatore import Allenatore
from test.games.pokemonBattle.pokemonPackage.pokemonAction import PokemonAction
from typing import Optional

from ai.state import State


class PokemonState(State):
    def __init__(
        self,
        allenatore1: Allenatore,
        allenatore2: Allenatore,
        turno: int = 0,
        azione_precedente: Optional[PokemonAction] = None,  # solo per debug
    ):
        self.allenatore1 = allenatore1
        self.allenatore2 = allenatore2
        self.turno = turno
        self.azione_precedente = azione_precedente

    def copy(self) -> PokemonState:
        return PokemonState(
            self.allenatore1.copy(),
            self.allenatore2.copy(),
            self.turno,
        )

    def changeTo(self, other: PokemonState) -> None:
        """Metodo di comodo che rende un oggetto PokemonState già esistente uguale ad uno stato in input"""
        self.allenatore1.changeTo(other.allenatore1)
        self.allenatore2.changeTo(other.allenatore2)
        self.turno = other.turno
        if not other.azione_precedente:
            self.azione_precedente = None
        elif self.azione_precedente:
            self.azione_precedente.changeTo(other.azione_precedente)  # l'azione non viene copiata
            # self.azione_precedente.changeTo(other.azione_precedente)

    # per accedere in maniera più semplice ai pokemon degli allenatori
    # sono property (per essere readonly)
    @property
    def pokemon1(self):
        return self.allenatore1.pokemon

    @property
    def pokemon2(self):
        return self.allenatore2.pokemon

    # il turno NON fa parte di ciò che caratterizza lo stato (quindi due stati sono considerati uguali anche se hanno turni diversi ma il resto identico)
    # questa scelta è volta ad intercettare stati già visitati negli algoritmi
    def __hash__(self) -> int:
        prime = 31
        result = 0
        result = result * prime + hash(self.allenatore1)
        result = result * prime + hash(self.allenatore2)
        return result

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, PokemonState)
            and self.allenatore1 == other.allenatore1
            and self.allenatore2 == other.allenatore2
        )

    def __str__(self) -> str:
        return (
            f"Mossa precedente: [\n{textwrap.indent(str(self.azione_precedente), '\t')}\n]\n"
            f"Allenatore1: {str(self.allenatore1)}\n"
            f"Allenatore2: {str(self.allenatore2)}\n"
            f"Turno di: {self.allenatore1.name if self.turno % 2 == 0 else self.allenatore2.name}"
        )
        # Campo: {self.campo}

    def __repr__(self) -> str:
        return str(self)
