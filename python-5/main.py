from datetime import datetime

TAXA_NOTURNA = 0
TAXA_DIURNA = 0.09

FIXO_DIURNO = 0.36
FIXO_NOTURNO = 0.36

FIM_MANHA = 6
INICIO_NOITE = 22

records = [
    {'source': '48-996355555', 'destination': '48-666666666',
     'end': 1564610974, 'start': 1564610674},
    {'source': '41-885633788', 'destination': '41-886383097',
     'end': 1564506121, 'start': 1564504821},
    {'source': '48-996383697', 'destination': '41-886383097',
     'end': 1564630198, 'start': 1564629838},
    {'source': '48-999999999', 'destination': '41-885633788',
     'end': 1564697158, 'start': 1564696258},
    {'source': '41-833333333', 'destination': '41-885633788',
     'end': 1564707276, 'start': 1564704317},
    {'source': '41-886383097', 'destination': '48-996384099',
     'end': 1564505621, 'start': 1564504821},
    {'source': '48-999999999', 'destination': '48-996383697',
     'end': 1564505721, 'start': 1564504821},
    {'source': '41-885633788', 'destination': '48-996384099',
     'end': 1564505721, 'start': 1564504821},
    {'source': '48-996355555', 'destination': '48-996383697',
     'end': 1564505821, 'start': 1564504821},
    {'source': '48-999999999', 'destination': '41-886383097',
     'end': 1564610750, 'start': 1564610150},
    {'source': '48-996383697', 'destination': '41-885633788',
     'end': 1564505021, 'start': 1564504821},
    {'source': '48-996383697', 'destination': '41-885633788',
     'end': 1564627800, 'start': 1564626000}
]


def calcula_minutos(hora, minuto=0):

    return 60*hora + minuto


def verifica_manha(hora):

    if hora <= FIM_MANHA:
        return True
    else:
        False


def verifica_dia(hora):

    if FIM_MANHA < hora <= INICIO_NOITE:
        return True
    else:
        False


def calcula_periodo(hora_inicial, hora_final, minuto_inicial, minuto_final):
    return (hora_final - hora_inicial, minuto_final - minuto_inicial)

def calcula_tarifa(start, end):

    ''' Recebe os instantes iniciais e finais de uma ligação
    em timestamp e calcula a tarifa total a ser cobrada.
    Esta função considera que o início e o término da ligação
    ocorrem em um mesmo dia.

    TAXA_DIURNA vigora entre FIM_MANHA e INICIO_NOITE
    TAXA_NOTURNA vigora antes do FIM_MANHA ou
    após INICIO_NOITE

    '''

    inicio = datetime.fromtimestamp(start)
    fim = datetime.fromtimestamp(end)

    hora_inicial = inicio.hour
    minuto_inicial = inicio.minute
    hora_final = fim.hour
    minuto_final = fim.minute

    # ajuste para minuto quebrado andiantando
    # em uma unidade o inicio da ligação
    if inicio.second > fim.second:
        minuto_inicial += 1

    total = 0

    if verifica_manha(hora_inicial):
        total += FIXO_NOTURNO
        total -= calcula_minutos(hora_inicial, minuto_inicial) * TAXA_NOTURNA
        if verifica_manha(hora_final):
            total += calcula_minutos(hora_final, minuto_final) * TAXA_NOTURNA
        elif verifica_dia(hora_final):
            total += calcula_minutos(FIM_MANHA) * TAXA_NOTURNA
            total += calcula_minutos((hora_final-FIM_MANHA), minuto_final) * TAXA_DIURNA
        else:# hora_final > 22
            total += calcula_minutos(FIM_MANHA) * TAXA_NOTURNA
            total += calcula_minutos(INICIO_NOITE-FIM_MANHA) * TAXA_DIURNA
            total += calcula_minutos((hora_final-INICIO_NOITE), minuto_final) * TAXA_NOTURNA

    elif verifica_dia(hora_inicial):
        total += FIXO_DIURNO
        total -= calcula_minutos(hora_inicial, minuto_inicial) * TAXA_DIURNA
        if verifica_dia(hora_final):
            total += calcula_minutos(hora_final, minuto_final) * TAXA_DIURNA
        else:# hora_final > 22
            total += calcula_minutos(INICIO_NOITE) * TAXA_DIURNA
            total += calcula_minutos((hora_final-INICIO_NOITE), minuto_final) * TAXA_NOTURNA

    else:# hora_inicial > 22
        total += FIXO_NOTURNO
        total -= calcula_minutos(hora_inicial, minuto_inicial) * TAXA_NOTURNA
        total += calcula_minutos(hora_final, minuto_final) * TAXA_NOTURNA

    return total


def tarifa_para_ligacao(record):

    '''
    Recebe cada registro de ligação no formato de dicionário
    e retorna um novo dicionário contendo apenas o telefone
    de origem e a tarifa total gerada pela ligação.
    '''
    new_shape = {
        'source': record['source'],
        'total': calcula_tarifa(record['start'], record['end'])
        }

    return new_shape


def classify_by_phone_number(records):

    '''
    Recebe por parâmetro um relatório de ligações
    em forma de lista de dicionários, em que os horários
    de início de fim das ligações estão no formato timestamp
    e os números de telefone de origem e destino estão
    no formato de strings.

    Ex:
        records = [
    {'source': '48-996355555',
    'destination': '48-666666666',
    'end': 1564610974,
    'start': 1564610674},
    {'source': '41-885633788',
    'destination': '41-886383097',
    'end': 1564506121,
    'start': 1564504821}
    ]

    Retorna uma lista contendo dicionários com as chaves:
     - 'source' referente à origem da ligação; e
     - 'total' referente à tarifa total a ser paga na ligação.

    A lista resultante é ordenada pelo maior valor de 'total'.

    O valor de 'total' é arredondado em 2 casas decimais.

    '''

    lista_source_e_total = [tarifa_para_ligacao(item) for item in records]

    # conjunto com registro único para cada origem
    source_unique = set(item['source'] for item in lista_source_e_total)

    # dicionário com soma das tarifas das várias ligações
    totals = {}
    for source in source_unique:
        totals[source] = 0

    for item in lista_source_e_total:
        totals[item['source']] += item['total']

    # lista contendo dicionários com source e total agregado
    source_agregado = []
    for key, value in totals.items():
        source_agregado.append({
            'source': key,
            'total': round(value, 2)
            })

    # organizando em ordem decrescente
    source_agregado = sorted(source_agregado, key=lambda x: x['total'], reverse=True)

    return source_agregado
