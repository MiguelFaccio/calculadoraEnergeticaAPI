from fastapi import APIRouter
from models.dependencia import DependenciaDB
from models.dispositivo import DispositivoDB
from models.unidade_consumidora import UnidadeConsumidoraDB
from schemas.dispositivos import DispositivoCreate, DispositivoRead, DispositivoReadList, DispositivoUpdate

router = APIRouter(prefix='/dispositivos', tags=['DISPOSITIVOS'])

@router.post(path='', response_model=DispositivoRead)
def criar_dispositivo(novo_dispositivo: DispositivoCreate):
    dispositivo = DispositivoDB.create(**novo_dispositivo.model_dump())
    return dispositivo

@router.get(path='', response_model=DispositivoReadList)
def listar_dispositivo():
    dispositivos = DispositivoDB.select()
    return {'dispositivos': dispositivos}

@router.get(path='/{dispositivo_id}', response_model=DispositivoRead)
def listar_dispositivo(dispositivo_id: int):
    dispositivo = DispositivoDB.get_or_none(DispositivoDB.id == dispositivo_id)
    return dispositivo

@router.patch(path='/{dispositivo_id}', response_model=DispositivoRead)
def atualizar_dispositivo(dispositivo_id: int, novo_dispositivo: DispositivoUpdate):
    dispositivo = DispositivoDB.get_or_none(DispositivoDB.id == dispositivo_id)
    dispositivo.consumo = novo_dispositivo.consumo
    dispositivo.uso_diario = novo_dispositivo.uso_diario
    dispositivo.nome = novo_dispositivo.nome
    dispositivo.dependencia = novo_dispositivo.dependencia
    dispositivo.unidade_consumidora = novo_dispositivo.unidade_consumidora
    dispositivo.save()
    return dispositivo

@router.delete(path='/{dispositivo_id}', response_model=DispositivoRead)
def excluir_dispositivo(dispositivo_id: int):
    dispositivo = DispositivoDB.get_or_none(DispositivoDB.id == dispositivo_id)
    dispositivo.delete_instance()
    return dispositivo
