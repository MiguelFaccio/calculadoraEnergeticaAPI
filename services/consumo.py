from models.dispositivo import DispositivoDB


def calcular_consumo(dispositivos: list[DispositivoDB]):
    """
    Calcula o consumo de energia de uma lista de dispositivos.

    :param dispositivos: Lista de instâncias de DispositivoDB
    :return: Tuple com consumo diário, mensal e anual
    """
    consumo_diario = sum(
        dispositivo.consumo * dispositivo.uso_diario
        for dispositivo in dispositivos
    )
    consumo_mensal = consumo_diario * 30
    consumo_anual = consumo_diario * 365

    return consumo_diario, consumo_mensal, consumo_anual


def calcular_consumo_dispositivos_unidade(id_unidade_consumidora: int):
    """
    Calcula o consumo de todos os dispositivos que pertencem a uma unidade consumidora específica.

    :param id_unidade_consumidora: ID da unidade consumidora
    :return: Tuple com consumo diário, mensal e anual
    """
    # Consulta todos os dispositivos que pertencem à unidade consumidora fornecida
    dispositivos = DispositivoDB.select().where(DispositivoDB.unidade_consumidora == id_unidade_consumidora)

    # Calcula o consumo dos dispositivos
    consumo_diario, consumo_mensal, consumo_anual = calcular_consumo(dispositivos)

    return consumo_diario, consumo_mensal, consumo_anual


# Exemplo de uso
if __name__ == '__main__':
    id_unidade = int(input("Digite o ID da unidade consumidora: "))
    consumo_diario, consumo_mensal, consumo_anual = calcular_consumo_dispositivos_unidade(id_unidade)

    print(f"Consumo Diário: {consumo_diario} kWh")
    print(f"Consumo Mensal: {consumo_mensal} kWh")
    print(f"Consumo Anual: {consumo_anual} kWh")
