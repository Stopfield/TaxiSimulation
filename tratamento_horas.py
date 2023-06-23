import pandas as pd

ds = pd.read_csv("soma_horas.csv", parse_dates=["dias"])

# Trata as horas para inteiros e remove chaves
nova_lista_horas = []
for i in range(len(ds)):
    lista_horas = ds["soma_horas"][i]
    lista_horas = lista_horas.replace("[", " ")
    lista_horas = lista_horas.replace("]", " ")
    nova_lista = [int(hora) for hora in lista_horas.split(",")]
    nova_lista_horas.append(nova_lista)

# Gerar novo dataframe com os dados novos, separados em colunas
novo_df = pd.DataFrame()
novo_df["dias"] = ds["dias"]

for i in range(24):
    coluna = nova_lista_horas[i]

print(novo_df)
