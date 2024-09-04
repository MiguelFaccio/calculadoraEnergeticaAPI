from fastapi import APIRouter
from models.tipo_consumidor import TipoConsumidorDB
from models.unidade_consumidora import UnidadeConsumidoraDB
from schemas.unidade_consumidora import UnidadeConsumidoraCreate, UnidadeConsumidoraRead, UnidadeConsumidoraReadList, UnidadeConsumidoraUpdate

router = APIRouter(prefix='/unidades-consumidoras', tags=['UNIDADES CONSUMIDORAS'])

@router.post(path='', response_model=UnidadeConsumidoraRead)
def criar_unidade_de_consumo(nova_unidade: UnidadeConsumidoraCreate):
    unidade = UnidadeConsumidoraDB.create(**nova_unidade.model_dump())
    return unidade

@router.get(path='', response_model=UnidadeConsumidoraReadList)
def listar_unidades_de_consumo():
    unidades = UnidadeConsumidoraDB.select()
    return {'unidades_consumidoras': unidades}

@router.get(path='/{unidade_id}', response_model=UnidadeConsumidoraRead)
def listar_unidade_de_consumo(unidade_id: int):
    unidade = UnidadeConsumidoraDB.get_or_none(UnidadeConsumidoraDB.id == unidade_id)
    return unidade

@router.patch(path='/{unidade_id}', response_model=UnidadeConsumidoraRead)
def atualizar_unidade_de_consumo(unidade_id: int, nova_unidade: UnidadeConsumidoraUpdate):
    unidade = UnidadeConsumidoraDB.get_or_none(UnidadeConsumidoraDB.id == unidade_id)
    unidade.tipo = nova_unidade.tipo
    unidade.nome = nova_unidade.nome
    unidade.save()
    return unidade

@router.delete(path='/{unidade_id}', response_model=UnidadeConsumidoraRead)
def excluir_unidade_de_consumo(unidade_id: int):
    unidade = UnidadeConsumidoraDB.get_or_none(UnidadeConsumidoraDB.id == unidade_id)
    unidade.delete_instance()
    return unidade
