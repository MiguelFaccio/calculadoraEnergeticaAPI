from fastapi import APIRouter, Query, HTTPException
from models.dispositivo import DispositivoDB
from models.dependencia import DependenciaDB
from models.unidade_consumidora import UnidadeConsumidoraDB
from models.bandeira import BandeiraDB
from schemas.consumo import ConsumoRead
from services.consumo import calcular_consumo, aplicar_tarifa  # Importando as funções

router = APIRouter(prefix='/consumos', tags=['Consumos'])


@router.get('/unidade/{unidade_id}', response_model=ConsumoRead)
def calcular_consumo_por_unidade(unidade_id: int, bandeira_id: int):
    unidade = UnidadeConsumidoraDB.get_or_none(UnidadeConsumidoraDB.id == unidade_id)
    if not unidade:
        raise HTTPException(status_code=404, detail="Unidade consumidora não encontrada")

    bandeira = BandeiraDB.get_or_none(BandeiraDB.id == bandeira_id)
    if not bandeira:
        raise HTTPException(status_code=404, detail="Bandeira não encontrada")

    dispositivos_eletricos = list(DispositivoDB.select().where(DispositivoDB.unidade_consumidora == unidade))
    consumo_diario, consumo_mensal, consumo_anual = calcular_consumo(dispositivos_eletricos)
    consumo_diario, consumo_mensal, consumo_anual = aplicar_tarifa(consumo_diario, consumo_mensal, consumo_anual, bandeira.tarifa)

    return ConsumoRead(
        consumo_diario=consumo_diario,
        consumo_mensal=consumo_mensal,
        consumo_anual=consumo_anual,
    )

@router.get('/dependencia/{dependencia_id}', response_model=ConsumoRead)
def calcular_consumo_por_dependencia(unidade_id: int, dependencia_id: int, bandeira_id: int):
    unidade = UnidadeConsumidoraDB.get_or_none(UnidadeConsumidoraDB.id == unidade_id)
    if not unidade:
        raise HTTPException(status_code=404, detail="Unidade consumidora não encontrada")

    dependencia = DependenciaDB.get_or_none(DependenciaDB.id == dependencia_id, DependenciaDB.unidade_consumidora == unidade)
    if not dependencia:
        raise HTTPException(status_code=404, detail="Dependência não encontrada")

    bandeira = BandeiraDB.get_or_none(BandeiraDB.id == bandeira_id)
    if not bandeira:
        raise HTTPException(status_code=404, detail="Bandeira não encontrada")

    dispositivos_eletricos = list(DispositivoDB.select().where(DispositivoDB.dependencia == dependencia))
    consumo_diario, consumo_mensal, consumo_anual = calcular_consumo(dispositivos_eletricos)
    consumo_diario, consumo_mensal, consumo_anual = aplicar_tarifa(consumo_diario, consumo_mensal, consumo_anual, bandeira.tarifa)

    return ConsumoRead(
        consumo_diario=consumo_diario,
        consumo_mensal=consumo_mensal,
        consumo_anual=consumo_anual,
    )

@router.get('/dispositivo/{dispositivo_id}', response_model=ConsumoRead)
def calcular_consumo_por_dispositivo(unidade_id: int, dependencia_id: int, dispositivo_id: int, bandeira_id: int):
    unidade = UnidadeConsumidoraDB.get_or_none(UnidadeConsumidoraDB.id == unidade_id)
    if not unidade:
        raise HTTPException(status_code=404, detail="Unidade consumidora não encontrada")

    dependencia = DependenciaDB.get_or_none(DependenciaDB.id == dependencia_id, DependenciaDB.unidade_consumidora == unidade)
    if not dependencia:
        raise HTTPException(status_code=404, detail="Dependência não encontrada")

    dispositivo = DispositivoDB.get_or_none(DispositivoDB.id == dispositivo_id, DispositivoDB.dependencia == dependencia)
    if not dispositivo:
        raise HTTPException(status_code=404, detail="Dispositivo não encontrado")

    bandeira = BandeiraDB.get_or_none(BandeiraDB.id == bandeira_id)
    if not bandeira:
        raise HTTPException(status_code=404, detail="Bandeira não encontrada")

    consumo_diario, consumo_mensal, consumo_anual = calcular_consumo([dispositivo])
    consumo_diario, consumo_mensal, consumo_anual = aplicar_tarifa(consumo_diario, consumo_mensal, consumo_anual, bandeira.tarifa)

    return ConsumoRead(
        consumo_diario=consumo_diario,
        consumo_mensal=consumo_mensal,
        consumo_anual=consumo_anual,
    )
