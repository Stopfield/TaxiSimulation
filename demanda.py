import statistics as st
import pandas as pd

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


for j, dia in enumerate(count["dias"]):
    for i in range(len(my_df)):
        print(i, dia)
        if my_df["dia"][i] == dia:
            contador[my_df["hora"][i]] += 1
    count["soma_horas"][j] = contador
    contador = [0 for i in range(24)]

print(count)
count.to_csv("data_e_hora.csv", index=False)
