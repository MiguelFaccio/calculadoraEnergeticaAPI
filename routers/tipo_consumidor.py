from fastapi import APIRouter
from models.tipo_consumidor import TipoConsumidorDB
from schemas.tipo_consumidor import TipoConsumidorCreate, TipoConsumidorRead, TipoConsumidorReadList, TipoConsumidorUpdate

router = APIRouter(prefix='/tipos-consumidores', tags=['TIPOS CONSUMIDORES'])

@router.post(path='', response_model=TipoConsumidorRead)
def criar_tipo_de_consumidor(novo_tipo: TipoConsumidorCreate):
    tipo = TipoConsumidorDB.create(**novo_tipo.model_dump())
    return tipo

@router.get(path='', response_model=TipoConsumidorReadList)
def listar_tipo_de_consumidor():
    tipos = TipoConsumidorDB.select()
    return {'tipos_consumidores': tipos}

@router.get(path='/{tipo_id}', response_model=TipoConsumidorRead)
def listar_tipo_de_consumidor(tipo_id: int):
    tipo = TipoConsumidorDB.get_or_none(TipoConsumidorDB.id == tipo_id)
    return tipo

@router.patch(path='/{tipo_id}', response_model=TipoConsumidorRead)
def atualizar_tipo_de_consumidor(tipo_id: int, novo_tipo: TipoConsumidorUpdate):
    tipo = TipoConsumidorDB.get_or_none(TipoConsumidorDB.id == tipo_id)
    tipo.valor_kwh = novo_tipo.valor_kwh
    tipo.nome = novo_tipo.nome
    tipo.save()
    return tipo

@router.delete(path='/{tipo_id}', response_model=TipoConsumidorRead)
def excluir_tipo_de_consumidor(tipo_id: int):
    tipo = TipoConsumidorDB.get_or_none(TipoConsumidorDB.id == tipo_id)
    tipo.delete_instance()
    return tipo
