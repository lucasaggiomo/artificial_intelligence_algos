from __future__ import annotations

import textwrap
from test.games.pokemonBattle.pokemonPackage.mosse import (
    CategoriaMossaOffensiva,
    CategoriaMossaStato,
    Mossa,
    MossaOffensiva,
    MossaStato,
)
from test.games.pokemonBattle.pokemonPackage.pokemon import Pokemon
from test.games.pokemonBattle.pokemonPackage.statistiche import Statistica
from test.games.pokemonBattle.pokemonPackage.tipo import get_moltiplicatore

from ai.action import Action


class PokemonAction(Action):
    """
    L'azione è rappresentata dalla mossa di un pokemon e dal pokemon che la effettua.
    Si potrebbero aggiungere in futuro come azioni possibili:
        - utilizzo di un rimedio (es: pozione) dalla borsa -> potrei farlo
        - utilizzo di un potenziamento dalla borsa -> non penso lo farò
        - cambia pokemon -> si complicherebbe molto aggiungere diversi pokemon
    """

    def __init__(
        self,
        pokemon: Pokemon,  # il pokemon che esegue la mossa
        mossa: Mossa,  # la mossa effettuata
        target: Pokemon,  # il pokemon che subisce la mossa
    ):
        self.pokemon = pokemon
        self.mossa = mossa
        self.target = target
        self.danno = -1
        self.moltiplicatorePuro = 1
        self.moltiplicatoreTotale = 1

    def calcolaDanno_(self) -> int:
        """
        STUB per semplificare, il danno è PARI alla potenza della mossa.
        Non tiene conto dei moltiplicatori in base ai tipi, né delle statistiche dei pokemon.
        """
        if not isinstance(self.mossa, MossaOffensiva):
            self.danno = 0
            return 0

        stringa = f"Calcolo del danno con pokemon:\n{self.pokemon}\nverso\n{self.target}\ncon la mossa {self.mossa}"
        # print(textwrap.indent(stringa, "\t----"))

        self.danno = (
            self.mossa.potenza
            + self.pokemon.statistiche[Statistica.ATTACCO]
            - self.target.statistiche[Statistica.DIFESA]
        )
        return self.danno

    def calcolaDanno(self) -> int:
        """Questa funzione calcola il danno solo se la mossa riferita da questa azione è una mossa offensiva"""
        if not isinstance(self.mossa, MossaOffensiva):
            self.danno = 0
            return 0

        # CALCOLO DANNO PURO

        # livello del pokemon attaccante
        livello = 50  # il livello è stato omesso per semplicità, viene assunto pari ad 50

        # in base alla categoria di mossa offensiva, cambia la statistica offensiva e difensiva da guardare (fisica o speciale)
        match self.mossa.categoria:
            case CategoriaMossaOffensiva.MOSSA_FISICA:
                attacco = self.pokemon.statistiche[Statistica.ATTACCO]
                difesa = self.target.statistiche[Statistica.DIFESA]
            case CategoriaMossaOffensiva.MOSSA_SPECIALE:
                attacco = self.pokemon.statistiche[Statistica.ATTACCO_SPECIALE]
                difesa = self.target.statistiche[Statistica.DIFESA_SPECIALE]

        danno = ((2 * livello / 5 + 2) * self.mossa.potenza * attacco / difesa) / 50 + 2
        # print(f"Danno con potenza {self.mossa.potenza}, attacco {attacco} e difesa {difesa}: {danno}")

        # CALCOLO MOLTIPLICATORE
        moltiplicatore = 1.0
        for tipoTarget in self.target.tipi:
            moltiplicatore *= get_moltiplicatore(self.mossa.tipo, tipoTarget)
        self.moltiplicatorePuro = moltiplicatore

        # il danno incrementato se il pokemon attaccante è dello stesso tipo della mossa
        if self.mossa.tipo in self.pokemon.tipi:
            moltiplicatore *= 1.5

        self.moltiplicatoreTotale = moltiplicatore

        # calcolo del danno arrotondato per difetto
        danno = int(danno * moltiplicatore)

        # se il danno è zero, il danno inflitto sarà:
        # - 0 se il moltiplicatore è 0 (ovvero la mossa non ha effetto sul tipo del pokemon target)
        # - 1 altrimenti

        if moltiplicatore == 0:
            self.danno = 0
            return 0

        if danno == 0:
            self.danno = 1
            return 1

        self.danno = danno
        return danno

    def changeTo(self, other: PokemonAction) -> None:
        """Metodo di comodo che rende un oggetto PokemonAction già esistente uguale ad un'azione in input"""
        self.pokemon.changeTo(other.pokemon)
        self.mossa = other.mossa
        self.target.changeTo(other.target)

    def __hash__(self) -> int:
        prime = 31
        result = 0
        result = result * prime + hash(self.pokemon)
        result = result * prime + hash(self.mossa)
        result = result * prime + hash(self.target)
        # result = result * prime + hash(self.danno)
        # result = result * prime + hash(self.moltiplicatorePuro)
        # result = result * prime + hash(self.moltiplicatoreTotale)
        return result

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, PokemonAction)
            and self.pokemon == other.pokemon
            and self.mossa == other.mossa
            and self.target == other.target
            # and self.danno == other.danno
            # and self.moltiplicatorePuro == other.moltiplicatorePuro
            # and self.moltiplicatoreTotale == other.moltiplicatoreTotale
        )

    def __str__(self) -> str:
        str = f"{self.pokemon.name} usa {self.mossa}!\n"
        if isinstance(self.mossa, MossaOffensiva):
            str += f"Infligge {self.danno} PS!\n"
        elif isinstance(self.mossa, MossaStato):
            if self.mossa.categoria == CategoriaMossaStato.MOSSA_BUFF:
                str += "Modifica il suo stato con le seguenti statistiche aumentate: [\n"
                str += textwrap.indent(
                    "\n".join(
                        f"{stat.name}: {incr}"
                        for stat, incr in self.mossa.modificheStatistiche.items()
                    ),
                    "\t- ",
                )
                str += "\n]\n"
            else:
                str += (
                    f"Modifica lo stato dell'avversario con le seguenti statistiche diminuite: [\n"
                )
                str += textwrap.indent(
                    "\n".join(
                        f"{stat.name}: {decr}"
                        for stat, decr in self.mossa.modificheStatistiche.items()
                    ),
                    "\t- ",
                )
                str += "\n]\n"
        str += _getTextFromMoltiplicatore(self.moltiplicatorePuro)
        str += f"(moltiplicatore totale: {self.moltiplicatoreTotale})"
        return str

    def __repr__(self) -> str:
        return self.__str__()


def _getTextFromMoltiplicatore(moltiplicatore: float) -> str:
    if moltiplicatore < 1:
        return "Non è molto efficace...\n"
    elif moltiplicatore > 1:
        return "È superefficace!\n"
    return ""
