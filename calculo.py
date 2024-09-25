from typing import List
from models.dispositivo import DispositivoDB

def calcular_consumo(dispositivos: List[DispositivoDB]):
    consumo_diario = sum(
        dispositivo.consumo * dispositivo.uso_diario
        for dispositivo in dispositivos
    )
    consumo_mensal = consumo_diario * 30
    consumo_anual = consumo_diario * 365

    return consumo_diario, consumo_mensal, consumo_anual

def aplicar_tarifa(consumo_diario, consumo_mensal, consumo_anual, tarifa):
    if tarifa == 0:
        return consumo_diario, consumo_mensal, consumo_anual
    return (
        consumo_diario * tarifa,
        consumo_mensal * tarifa,
        consumo_anual * tarifa
    )
