from __future__ import annotations

import textwrap
from test.games.pokemonBattle.core.elemento import Elemento
from test.games.pokemonBattle.core.mosse import Mossa, MossaError, MossaStato
from test.games.pokemonBattle.core.statistiche import Statistica, Statistiche
from test.games.pokemonBattle.core.tipo import Tipo


class Pokemon(Elemento):
    """
    Un pokemon ha uno o più tipi, al più quattro mosse e una serie di statistiche
    Per semplicità, è omesso il livello del pokemon e quindi:
    - l'incremento delle statistiche all'aumentare dei livelli
    - le mosse che impara il pokemon all'aumentare dei livelli
    """

    def __init__(
        self,
        name: str,
        tipi: set[Tipo],
        statistiche: Statistiche,
        mosse: set[Mossa],
        maxPS: int = -1,
    ):
        if len(tipi) == 0:
            raise ValueError("Un pokemon deve avere almeno un tipo")

        super().__init__(name)
        self.tipi = tipi
        self.statistiche = statistiche
        self.mosse = mosse

        # dizionario che indica il cooldown (quanti turni mancano) per eseguire ogni mossa
        # all'inizio sono tutte disponibili
        self.mosse_cooldown: dict[Mossa, int] = {mossa: 0 for mossa in mosse}

        self.maxPS: int = maxPS if maxPS >= 0 else self.statistiche[Statistica.PUNTI_SALUTE]

    def getMosseDisponibili(self) -> set[Mossa]:
        """Restituisce le mosse che il pokemon può fare (eliminando eventuali mosse disabilitate)"""
        return {mossa for mossa in self.mosse if self.mosse_cooldown[mossa] == 0}

    def getTurniDaAttendere(self, mossa: Mossa) -> int:
        """Restituisce il numero di turni rimanenti per poter rieseguire nuovamente la mossa richiesta"""
        if mossa not in self.mosse:
            raise MossaError("Questo pokemon non ha imparato questa mossa")

        return self.mosse_cooldown[mossa]

    def notificaTurnoPassato(self):
        """
        Notifica il pokemon che un turno COMPLETO è passato (ovvero che tocca di nuovo a lui).
        Quindi il pokemon decrementa i cooldown delle mosse
        """
        for mossa in self.mosse_cooldown:
            self.mosse_cooldown[mossa] = max(0, self.mosse_cooldown[mossa] - 1)

    def notificaUtilizzoMossa(self, mossa: Mossa):
        """Notifica il pokemon che ha utilizzato tale mossa, per poter resettare il cooldown associato"""
        if mossa not in self.mosse:
            raise MossaError("Questo pokemon non ha imparato questa mossa")

        if self.mosse_cooldown[mossa] > 0:
            raise MossaError("Mossa non ancora riutilizzabile")

        self.mosse_cooldown[mossa] = mossa.cooldown + 1

    def subisciDanno(self, danno: int) -> int:
        """
        Infligge il danno e restituisce il danno totale inflitto
        (in generale è diverso dal danno in input, in quanto i PS non possono scendere sotto 0)
        """

        vitaCorrente = self.statistiche[Statistica.PUNTI_SALUTE]

        vitaCorrente -= danno
        dannoInflitto = danno

        if vitaCorrente < 0:
            dannoInflitto += vitaCorrente
            vitaCorrente = 0

        self.statistiche[Statistica.PUNTI_SALUTE] = vitaCorrente

        return dannoInflitto

    def applicaEffetto(self, mossa: MossaStato) -> None:
        """Applica l'effetto di stato (per ora solo BUFF o DEBUFF)"""
        for statistica, valore in mossa.modificheStatistiche.items():
            # aumenta o decrementa le statistiche, considerando che i PS non possono scendere oltre 0 e salire oltre self.maxPS
            # e le altre statistiche non possonos scendere sotto il valore 1
            if statistica == Statistica.PUNTI_SALUTE:
                currPS = self.statistiche[statistica]
                newPS = max(0, min(self.maxPS, currPS + valore))
                self.statistiche[statistica] = newPS
            else:
                currValue = self.statistiche[statistica]
                newValue = max(1, currValue + valore)
                self.statistiche[statistica] = newValue

    def isKO(self) -> bool:
        return self.statistiche[Statistica.PUNTI_SALUTE] == 0

    def isAlive(self) -> bool:
        """True se il pokemon è K.O., False altrimenti"""
        # ps = self.statistiche[Statistica.PUNTI_SALUTE]
        # print(f">>>>>>Punti salute di {self.name} = {ps}, restituisco {self.statistiche[Statistica.PUNTI_SALUTE] == 0}")
        return self.statistiche[Statistica.PUNTI_SALUTE] > 0

    def __hash__(self) -> int:
        prime = 31
        result = 0
        result = result * prime + hash(self.name)
        for tipo in self.tipi:
            result = result * prime + hash(tipo)
        result = result * prime + hash(self.statistiche)
        return result

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, Pokemon)
            and self.name == other.name
            and self.tipi == other.tipi
            and self.statistiche == other.statistiche
        )

    def __str__(self) -> str:
        internalText = (
            f"Tipi = {[tipo.name for tipo in self.tipi]}\n"
            "Statistiche = [\n"
            f"{textwrap.indent("\n".join(str(self.statistiche).splitlines()), "\t- ")}"
            "\n]"
            f"\nMosse = [\n"
            f"{textwrap.indent("\n".join(f"{mossa.name}\t({self.getTurniDaAttendere(mossa)}, cd = {mossa.cooldown})" for mossa in self.mosse), "\t- ")}"
            "\n]"
        )
        return f"{self.name}: [\n" f"{textwrap.indent(internalText,"\t")}" f"\n]"
    
    def _copy(self) -> Pokemon:
        newPokemon = Pokemon(
            self.name,
            self.tipi.copy(),
            self.statistiche._copy(),
            self.mosse.copy(),
            self.maxPS,
        )
        newPokemon.mosse_cooldown = self.mosse_cooldown.copy()
        return newPokemon

    def _changeTo(self, other: Pokemon) -> None:
        """Metodo di comodo che rende un oggetto Pokemon già esistente uguale ad un pokemon in input"""
        self.name: str = other.name
        self.tipi = set(other.tipi)
        self.statistiche._changeTo(other.statistiche)
        self.mosse = set(other.mosse)
        self.maxPS = other.maxPS
        self.mosse_cooldown = other.mosse_cooldown.copy()
