import statistics as st
import pandas as pd

"""
for j, dia in enumerate(count["dias"]):
    for i in range(len(my_df)):
        print(i, dia)
        if my_df["dia"][i] == dia:
            contador[my_df["hora"][i]] += 1
    count["soma_horas"][j] = contador
    contador = [0 for i in range(24)]

print(count)
count.to_csv("data_e_hora.csv", index=False)
"""
def contar_ocorrencia(chunk):
    """
    Conta a ocorrência de viagens em cada hora do dia (0 ... 24).
    Parameters:
        chunk: Quais dias procurar no dataframe
    Returns:
        contador: 
    """
    count = pd.DataFrame()
    count["dias"] = chunk
    contador = [0 for i in range(24)]
    for dia in chunk:
        # Procura em todo o dataset pelo dia tal
        for i in range(len(my_df)):
            if my_df["dia"][i] == dia:
                contador[my_df["hora"][i]] += 1
        count["soma_horas"][j] = contador
        contador = [0 for i in range(24)]
    return count

def contador_multiprocessing(dias, num_processos=4):
    """
    Conta o número de viagens por hora em todo o dataset.
    Parameters:
        dias: Dataframe com os dias e horários
        num_processos: Número de processos para criar
    """
    counter_df = pd.DataFrame()
    counter_df["dias"] = dias
    pool = multiprocessing.Pool(processes=num_processos)
    tamanho_chunk = len(dias) // num_processos
    resultados = []
    for i in range(num_processos):
        inicio = i * tamanho_chunk
        fim = (i + 1) * tamanho_chunk
        chunk = dias[inicio:fim]
        result = pool.apply_async(contar_ocorrencia, (chunk, ))
        resultados.append(result)
    contador_total = []
    for res in resultados:
        contador_total.append(res.get())
    contador_total = pd.Series(contador_total)
    counter_df["lista_contagem"] = contador_total
    return counter_df

if __name__ == "__main__":
    multiprocessing.freeze_support()
    ds = pd.read_csv("train.csv", parse_dates=["pickup_datetime"])
    print(ds)
    horario = ds["pickup_datetime"]

    # Tratamento - Pegar número de pessoas por hora
    # Num mesmo dia, na mesma hora, 
    my_df = pd.DataFrame()
    print(horario)
    horario = horario.dt.hour
    print(horario)
    contagem_horarios = horario.value_counts()

    # Mas quero para cada dia, não no total
    my_df["dia"] = ds["pickup_datetime"].dt.date
    my_df["hora"] = ds["pickup_datetime"].dt.hour

    # São esses dias
    dias = my_df["dia"].unique()
    print(dias)
    count = pd.DataFrame()
    count["dias"] = dias
    count["soma_horas"] = pd.Series([ [] for i in range(len(dias)) ])

    contador = [0 for i in range(24)]
    contador_multiprocessing(dias)

    ...
