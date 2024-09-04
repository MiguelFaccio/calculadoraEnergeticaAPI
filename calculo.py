from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from peewee import fn
from config import database, shutdown_db
from models.dispositivo import DispositivoDB
from models.tipo_dispositivo import TipoDispositivoDB
from models.tipo_consumidor import TipoConsumidorDB
from models.unidade_consumidora import UnidadeConsumidoraDB
from models.bandeira import BandeiraDB
from models.dependencia import DependenciaDB

app = FastAPI()


class DispositivoResponse(BaseModel):
    consumo_diario: float
    consumo_mensal: float
    consumo_anual: float
    custo_diario: float
    custo_mensal: float
    custo_anual: float


@app.get("/calcular/{id_dispositivo}", response_model=DispositivoResponse)
async def calcular_consumo(id_dispositivo: int):
    # Conectar ao banco de dados
    database.connect()

    try:
        dispositivo = DispositivoDB.get(DispositivoDB.id == id_dispositivo)
        unidade_consumidora = UnidadeConsumidoraDB.get(UnidadeConsumidoraDB.id == dispositivo.unidade_consumidora)
        tipo_consumidor = TipoConsumidorDB.get(TipoConsumidorDB.id == unidade_consumidora.tipo_consumidor)
        bandeira = BandeiraDB.get(BandeiraDB.tipo_bandeira == 'Amarela')  # Ajuste conforme necessário

        # Cálculos
        potencia = dispositivo.potencia  # em W
        tempo_diario = dispositivo.tempo_diario  # em horas
        tarifa = tipo_consumidor.tarifa
        adicional = bandeira.adicional

        consumo_diario = (potencia / 1000) * tempo_diario
        consumo_mensal = consumo_diario * 30
        consumo_anual = consumo_diario * 365

        custo_diario = consumo_diario * (tarifa + adicional)
        custo_mensal = consumo_mensal * (tarifa + adicional)
        custo_anual = consumo_anual * (tarifa + adicional)

        return DispositivoResponse(
            consumo_diario=consumo_diario,
            consumo_mensal=consumo_mensal,
            consumo_anual=consumo_anual,
            custo_diario=custo_diario,
            custo_mensal=custo_mensal,
            custo_anual=custo_anual
        )

    except (DispositivoDB.DoesNotExist, UnidadeConsumidoraDB.DoesNotExist, TipoConsumidorDB.DoesNotExist,
            BandeiraDB.DoesNotExist) as e:
        raise HTTPException(status_code=404, detail=str(e))

    finally:
        # Fechar a conexão ao banco de dados
        shutdown_db()
