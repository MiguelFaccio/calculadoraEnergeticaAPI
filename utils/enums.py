from enum import Enum

class EnumGetEletrodomesticos(Enum):
    dependencia = 'dependencia'  # Reflete o modelo DependenciaDB
    dispositivo = 'dispositivo_eletrico'  # Reflete o modelo DispositivoDB
    unidade_consumidora = 'unidade_consumidora'  # Reflete o modelo UnidadeConsumidoraDB

class EnumGetDependencias(Enum):
    dependencia = 'dependencia'  # Reflete o modelo DependenciaDB
    unidade_consumidora = 'unidade_consumidora'  # Reflete o modelo UnidadeConsumidoraDB

class EnumOrigemDoConsumo(Enum):
    dispositivo = 'dispositivo_eletrico'  # Reflete o modelo DispositivoDB
    dependencia = 'dependencia'  # Reflete o modelo DependenciaDB
    unidade_consumidora = 'unidade_consumidora'  # Reflete o modelo UnidadeConsumidoraDB
