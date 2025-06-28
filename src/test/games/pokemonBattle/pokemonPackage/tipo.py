from enum import StrEnum


class Tipo(StrEnum):
    NORMALE = "Normale"
    FUOCO = "Fuoco"
    ACQUA = "Acqua"
    ERBA = "Erba"
    ELETTRO = "Elettro"
    GHIACCIO = "Ghiaccio"
    LOTTA = "Lotta"
    VELENO = "Veleno"
    TERRA = "Terra"
    VOLANTE = "Volante"
    PSICO = "Psico"
    COLEOTTERO = "Coleottero"
    ROCCIA = "Roccia"
    SPETTRO = "Spettro"
    DRAGO = "Drago"
    BUIO = "Buio"
    ACCIAIO = "Acciaio"


MATRICE_TIPI: dict[Tipo, dict[Tipo, float]] = {
    Tipo.NORMALE: {
        Tipo.ROCCIA: 0.5,
        Tipo.SPETTRO: 0,
        Tipo.ACCIAIO: 0.5,
    },
    Tipo.FUOCO: {
        Tipo.FUOCO: 0.5,
        Tipo.ACQUA: 0.5,
        Tipo.ERBA: 2,
        Tipo.GHIACCIO: 2,
        Tipo.COLEOTTERO: 2,
        Tipo.ROCCIA: 0.5,
        Tipo.DRAGO: 0.5,
        Tipo.ACCIAIO: 2,
    },
    Tipo.ACQUA: {
        Tipo.FUOCO: 2,
        Tipo.ACQUA: 0.5,
        Tipo.ERBA: 0.5,
        Tipo.TERRA: 2,
        Tipo.ROCCIA: 2,
        Tipo.DRAGO: 0.5,
    },
    Tipo.ELETTRO: {
        Tipo.ACQUA: 2,
        Tipo.ELETTRO: 0.5,
        Tipo.ERBA: 0.5,
        Tipo.TERRA: 0,
        Tipo.VOLANTE: 2,
        Tipo.DRAGO: 0.5,
    },
    Tipo.ERBA: {
        Tipo.FUOCO: 0.5,
        Tipo.ACQUA: 2,
        Tipo.ERBA: 0.5,
        Tipo.VELENO: 0.5,
        Tipo.TERRA: 2,
        Tipo.VOLANTE: 0.5,
        Tipo.COLEOTTERO: 0.5,
        Tipo.ROCCIA: 2,
        Tipo.DRAGO: 0.5,
        Tipo.ACCIAIO: 0.5,
    },
    Tipo.GHIACCIO: {
        Tipo.FUOCO: 0.5,
        Tipo.ACQUA: 0.5,
        Tipo.ERBA: 2,
        Tipo.GHIACCIO: 0.5,
        Tipo.TERRA: 2,
        Tipo.VOLANTE: 2,
        Tipo.DRAGO: 2,
        Tipo.ACCIAIO: 0.5,
    },
    Tipo.LOTTA: {
        Tipo.NORMALE: 2,
        Tipo.GHIACCIO: 2,
        Tipo.VELENO: 0.5,
        Tipo.VOLANTE: 0.5,
        Tipo.PSICO: 0.5,
        Tipo.COLEOTTERO: 0.5,
        Tipo.ROCCIA: 2,
        Tipo.SPETTRO: 0,
        Tipo.BUIO: 2,
        Tipo.ACCIAIO: 2,
    },
    Tipo.VELENO: {
        Tipo.ERBA: 2,
        Tipo.VELENO: 0.5,
        Tipo.TERRA: 0.5,
        Tipo.ROCCIA: 0.5,
        Tipo.SPETTRO: 0.5,
        Tipo.ACCIAIO: 0,
    },
    Tipo.TERRA: {
        Tipo.FUOCO: 2,
        Tipo.ELETTRO: 2,
        Tipo.ERBA: 0.5,
        Tipo.VELENO: 2,
        Tipo.VOLANTE: 0,
        Tipo.COLEOTTERO: 0.5,
        Tipo.ROCCIA: 2,
        Tipo.ACCIAIO: 2,
    },
    Tipo.VOLANTE: {
        Tipo.ELETTRO: 0.5,
        Tipo.ERBA: 2,
        Tipo.LOTTA: 2,
        Tipo.COLEOTTERO: 2,
        Tipo.ROCCIA: 0.5,
        Tipo.ACCIAIO: 0.5,
    },
    Tipo.PSICO: {
        Tipo.LOTTA: 2,
        Tipo.VELENO: 2,
        Tipo.PSICO: 0.5,
        Tipo.BUIO: 0,
        Tipo.ACCIAIO: 0.5,
    },
    Tipo.COLEOTTERO: {
        Tipo.FUOCO: 0.5,
        Tipo.ERBA: 2,
        Tipo.LOTTA: 0.5,
        Tipo.VELENO: 0.5,
        Tipo.VOLANTE: 0.5,
        Tipo.PSICO: 2,
        Tipo.SPETTRO: 0.5,
        Tipo.BUIO: 2,
        Tipo.ACCIAIO: 0.5,
    },
    Tipo.ROCCIA: {
        Tipo.FUOCO: 2,
        Tipo.GHIACCIO: 2,
        Tipo.LOTTA: 0.5,
        Tipo.TERRA: 0.5,
        Tipo.VOLANTE: 2,
        Tipo.COLEOTTERO: 2,
        Tipo.ACCIAIO: 0.5,
    },
    Tipo.SPETTRO: {
        Tipo.NORMALE: 0,
        Tipo.PSICO: 2,
        Tipo.SPETTRO: 2,
        Tipo.BUIO: 0.5,
        Tipo.ACCIAIO: 0.5,
    },
    Tipo.DRAGO: {
        Tipo.DRAGO: 2,
        Tipo.ACCIAIO: 0.5,
    },
    Tipo.BUIO: {
        Tipo.LOTTA: 0.5,
        Tipo.PSICO: 2,
        Tipo.SPETTRO: 2,
        Tipo.BUIO: 0.5,
        Tipo.ACCIAIO: 0.5,
    },
    Tipo.ACCIAIO: {
        Tipo.FUOCO: 0.5,
        Tipo.ACQUA: 0.5,
        Tipo.ELETTRO: 0.5,
        Tipo.GHIACCIO: 2,
        Tipo.ROCCIA: 2,
        Tipo.ACCIAIO: 0.5,
    },
}


def get_moltiplicatore(tipo_attaccante: Tipo, tipo_difensore: Tipo) -> float:
    """
    Restituisce il moltiplicatore del danno in base al tipo di partenza e al tipo di destinazione
    """
    return MATRICE_TIPI[tipo_attaccante].get(tipo_difensore, 1.0)
