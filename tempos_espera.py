import pandas as pd
import statistics as st
import matplotlib.pyplot as plt
import math

ds = pd.read_csv("train.csv")
tempos_viagem = ds["trip_duration"]

# Retirar outliers extremos
q1, q2, q3 = st.quantiles(tempos_viagem)
A = q3 - q1
print(q1, q2, q3)

tempos_viagem_sem_outliers = []

for tempo in tempos_viagem:
    if tempo < q1 - 1.5 * A or tempo > q3 + 1.5 * A:
        # print(f"Outlier: {tempo}")
        continue
    if tempo < q1 - 3 * A or tempo > q3 + 3 * A:
        # print(f"Outlier: {tempo}")
        continue
    tempos_viagem_sem_outliers.append(tempo)

print(len(tempos_viagem_sem_outliers))
print(st.mean(tempos_viagem_sem_outliers))
print(st.mean(tempos_viagem))

# Análise de correlação
x = [tempos_viagem_sem_outliers[x] for x in range(len(tempos_viagem_sem_outliers)) if x % 2 == 0]
y = [tempos_viagem_sem_outliers[x] for x in range(len(tempos_viagem_sem_outliers)) if x % 2 != 0]
plt.plot(x, y, 'o')
plt.show()

# Histograma
k = round(1 + 3.3 * math.log10(len(tempos_viagem_sem_outliers)))
h = (max(tempos_viagem_sem_outliers) - min(tempos_viagem_sem_outliers)) / k
plt.hist(tempos_viagem_sem_outliers, bins=k)
plt.show()

# Teste de aderência
