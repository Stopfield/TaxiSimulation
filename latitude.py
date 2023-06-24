import statistics as st
import pandas as pd
import multiprocessing
import time

if __name__ == "__main__":
    multiprocessing.freeze_support()
    ds = pd.read_csv("train.csv")

    # Tratamento - Pegar número de pessoas por hora
    # Num mesmo dia, na mesma hora, 
    final_df = pd.DataFrame()
    my_df = pd.DataFrame()
    # Mas quero para cada dia, não no total
    my_df["latitude"] = ds["pickup_latitude"]
    my_df["longitude"] = ds["pickup_longitude"]

    # São esses dias
    inicio_lat, inicio_long = 40.77, -73.99
    fim_lat, fim_long = 40.76, -73.98
    
    # Contar quantos tem entre isso

    final_df = my_df[my_df["latitude"].between(fim_lat, inicio_lat) & my_df["longitude"].between(inicio_long, fim_long)]
    print(final_df)

    # dias = my_df["dia"].unique()
    # print(len(dias))
    # contador_multiprocessing(dias, my_df)
