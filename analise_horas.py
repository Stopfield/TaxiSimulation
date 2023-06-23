import pandas as pd
import matplotlib.pyplot as plt
import statistics as st
ds = pd.read_csv("soma_horas_melhorado.csv", parse_dates=["dias"])
# Tratar outliers
for i in range(24):
    # Retirar outliers extremos
    q1, q2, q3 = st.quantiles(ds[f"{i}"])
    A = q3 - q1
    col_sem_outliers = []
    col = ds[f"{i}"]
    for tempo in col:
        if tempo < q1 - 1.5 * A or tempo > q3 + 1.5 * A:
            print(f"Outlier: {tempo}")
            continue
        if tempo < q1 - 3 * A or tempo > q3 + 3 * A:
            print(f"Outlier: {tempo}")
            continue
        col_sem_outliers.append(tempo)
test = pd.DataFrame()
test["a"] = col_sem_outliers
test["a"].hist()
plt.show()

