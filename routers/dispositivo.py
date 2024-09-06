from fastapi import APIRouter

from models.dependencia import DependenciaDB
from models.dispositivo import DispositivoDB
from models.unidade_consumidora import UnidadeConsumidoraDB
from schemas.dispositivos import (
    DispositivoCreate,
    DispositivoRead,
    DispositivoReadList,
    DispositivoUpdate,
)

router = APIRouter(prefix='/dispositivos', tags=['DISPOSITIVOS'])


@router.post(path='', response_model=DispositivoRead)
def criar_dispositivo(novo_dispositivo: DispositivoCreate):
    dispositivo = DispositivoDB.create(**novo_dispositivo.model_dump())
    return dispositivo


@router.get(
    path='/unidades-consumidoras/{unidade_consumidora_id}',
    response_model=DispositivoReadList,
)
def listar_dispositivos(unidade_consumidora_id):
    unidade_consumidora = UnidadeConsumidoraDB.get_or_none(
        UnidadeConsumidoraDB.id == unidade_consumidora_id
    )
    dispositivos = DispositivoDB.select().where(
        DispositivoDB.unidade_consumidora == unidade_consumidora
    )
    return {'dispositivos': dispositivos}


@router.get(
    path='/dependencias/{dependencia_id}', response_model=DispositivoReadList
)
def listar_dispositivos(dependencia_id):
    dependencia = DependenciaDB.get_or_none(DependenciaDB.id == dependencia_id)
    dispositivos = DispositivoDB.select().where(
        DispositivoDB.dependencia == dependencia
    )
    return {'dispositivos': dispositivos}


@router.get(path='/{dispositivo_id}', response_model=DispositivoRead)
def listar_dispositivo(dispositivo_id: int):
    dispositivo = DispositivoDB.get_or_none(DispositivoDB.id == dispositivo_id)
    return dispositivo


@router.patch(path='/{dispositivo_id}', response_model=DispositivoRead)
def atualizar_dispositivo(
    id_dispositivo: int, dispositivo_autualizado: DispositivoUpdate
):
    dispositivo = DispositivoDB.get_or_none(DispositivoDB.id == id_dispositivo)
    dispositivo.nome = dispositivo_autualizado.nome
    dispositivo.consumo = dispositivo_autualizado.consumo
    dispositivo.uso_diario = dispositivo_autualizado.uso_diario
    dispositivo.tipo_id = dispositivo_autualizado.tipo_id
    dispositivo.save()
    return dispositivo


@router.delete(path='/{dispostivo_id}', response_model=DispositivoRead)
def eliminar_dispositivo(dispositivo_id: int):
    dispositivo = DispositivoDB.get_or_none(DispositivoDB.id == dispositivo_id)
    dispositivo.delete_instance()
    return dispositivo