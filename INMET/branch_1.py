#Aqui foi criado uma função para limpar e padronizar os dados dos últimos 20 anos.

import pandas as pd

def limpar(caminho):
    #Tirar colunas irrelevantes
    df = pd.read_csv(caminho, skiprows=8, encoding="latin1", sep=";")
    df.columns = [
        "Data",
        "Hora",
        "1",
        "2",
        "3",
        "4",
        "5",
        "Temperatura",
        "Orvalho",
        "Max",
        "Min",
        "O_max",
        "O_min",
        "U_max",
        "U_min",
        "Umidade",
        "6",
        "7",
        "8",
        "9",
        ]
    df = df.drop(columns=["1", "2", "3", "4", "5", "6", "7", "8", "9"])
    df = df.dropna()
    df = df.reset_index(drop=True)

    #Transformar todos os dados em números
    colunas = ["Temperatura", "Orvalho", "Max", "Min", "O_max", "O_min", "U_max", "U_min", "Umidade"]
    df[colunas] = df[colunas].replace(",", ".", regex=True).astype(float)
    df["Hora"] = df["Hora"].replace(" UTC", "", regex=True).replace(":", "", regex=True)
    df["Data"] = df["Data"].replace("/", "", regex=True).replace("-", "", regex=True)
    tempo = ["Data", "Hora"]
    df[tempo] = df[tempo].astype(int)

    #Remover valores com -9999
    for col in colunas:
        media = df.loc[df[col] != -9999, col].mean()
        df[col] = df[col].replace(-9999, media)
    
    #Retorna o data frame limpo
    return df