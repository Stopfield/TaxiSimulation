# Calcula a média das horas e plota o gráfico
import pandas as pd
import matplotlib.pyplot as plt
import statistics as st
ds = pd.read_csv("soma_horas_melhorado.csv")

# Tratar outliers
def tratar_outliers(lista):
    # Retirar outliers extremos
    q1, q2, q3 = st.quantiles(lista)
    A = q3 - q1
    print(A, q1, q2, q3)
    lista_sem_outliers = []
    for valor in lista:
        if valor < q1 - 1.5 * A or valor > q3 + 1.5 * A:
            print(f"Outlier: {valor}")
            continue
        if valor < q1 - 3 * A or valor > q3 + 3 * A:
            print(f"Outlier: {valor}")
            continue
        lista_sem_outliers.append(valor)
    return lista_sem_outliers

def to_list(string):
    string = string.replace("[", " ")
    string = string.replace("]", " ")
    nova_lista = [int(hora) for hora in string.split(",")]
    return nova_lista

novo_df = pd.DataFrame()
medias = []
for i in range(24):
    medias.append(st.mean(ds[f"{i}"].tolist()))
print(medias)
plt.plot(range(24), medias)
plt.show()
