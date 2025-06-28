from __future__ import annotations

import textwrap
from test.games.pokemonBattle.pokemonPackage.elemento import Elemento
from test.games.pokemonBattle.pokemonPackage.pokemon import Pokemon


class Allenatore(Elemento):
    """Un allenatore è un giocatore con un pokemon sul campo"""

    def __init__(self, name: str, pokemon: Pokemon):
        super().__init__(name)
        self.pokemon = pokemon

    def copy(self) -> Allenatore:
        """Restituisce una deep copy dell'Allenatore"""

        return Allenatore(
            self.name,
            self.pokemon.copy(),
        )

    def changeTo(self, other: Allenatore) -> None:
        """Metodo di comodo che rende un oggetto Allenatore già esistente uguale ad un allenatore in input"""
        self.name = other.name
        self.pokemon.changeTo(other.pokemon)

    def __str__(self) -> str:
        return f"{self.name} [\n{textwrap.indent(str(self.pokemon), "\t")}\n]"

    def __hash__(self) -> int:
        prime = 31
        result = 0
        result = result * prime + hash(self.name)
        result = result * prime + hash(self.pokemon)
        return result

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, Allenatore)
            and self.name == other.name
            and self.pokemon == other.pokemon
        )
