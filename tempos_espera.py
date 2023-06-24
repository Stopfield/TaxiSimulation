import pandas as pd
import statistics as st
import matplotlib.pyplot as plt
from scipy.stats import lognorm
import numpy as np
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


# Histograma
k = round(1 + 3.3 * math.log10(len(tempos_viagem_sem_outliers)))
h = (max(tempos_viagem_sem_outliers) - min(tempos_viagem_sem_outliers)) / k

mu = st.mean(np.log(tempos_viagem_sem_outliers))
sigma = st.stdev(np.log(tempos_viagem_sem_outliers))

x = np.linspace(min(tempos_viagem_sem_outliers), max(tempos_viagem_sem_outliers), 100)
y = np.random.lognormal(mu, sigma, 100)
pdf = (np.exp(-(np.log(x) - mu)**2 / (2 * sigma**2)) / (x * sigma * np.sqrt(2 * np.pi)))


print(f"Média: {st.mean(tempos_viagem_sem_outliers)}")
print(f"Stdev: {st.stdev(tempos_viagem_sem_outliers)}")

print(mu, sigma)
print(np.random.lognormal(mean=mu, sigma=sigma))
