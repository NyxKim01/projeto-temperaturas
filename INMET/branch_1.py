#Aqui foi criado uma função que limpa e padroniza os dados dos últimos 20 anos.

import pandas as pd

#Limpa o dataset
def limpar(caminho):
    #Tira colunas irrelevantes
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

    #Transforma todos os dados em números
    colunas = ["Temperatura", "Orvalho", "Max", "Min", "O_max", "O_min", "U_max", "U_min", "Umidade"]
    df[colunas] = df[colunas].replace(",", ".", regex=True).astype(float)
    df["Hora"] = df["Hora"].replace(" UTC", "", regex=True).replace(":", "", regex=True)
    df["Data"] = df["Data"].replace("/", "", regex=True).replace("-", "", regex=True)
    tempo = ["Data", "Hora"]
    df[tempo] = df[tempo].astype(int)

    #Remove valores com -9999
    for col in colunas:
        media = df.loc[df[col] != -9999, col].mean()
        df[col] = df[col].replace(-9999, media)
    
    #Arredonda os valores para duas casas decimais 
    df[colunas] = df[colunas].round(2)

    #Retorna o data frame limpo
    return df

#Acha os mínimos e máximos de uma determinada coluna
def min_max(caminho, coluna_1, coluna_2):
    df = pd.read_csv(caminho)

    #Cria um dataframe com os mínimos e máximos, por coluna_1, usando os valores da coluna_2
    df_min_max = df.groupby([coluna_1])[coluna_2].agg(["min", "max"])

    #Retorna um dataframe com os mínimos e máximos
    return df_min_max

#Divide o dataframe por estações do ano
def estacoes(caminho):
    lista = []
    df = pd.read_csv(caminho)

    #Separa com base nos últimos quatro dígitos da data
    outono = df[df["Data"]%10000 >= 320]
    outono = outono[outono["Data"]%10000 <= 620]
    df = df.drop(outono.index)
    inverno = df[df["Data"]%10000 >= 621]
    inverno = inverno[inverno["Data"]%10000 <= 921]
    df = df.drop(inverno.index)
    primavera = df[df["Data"]%10000 >= 922]
    primavera = primavera[primavera["Data"]%10000 <= 1220]
    df = df.drop(primavera.index)
    verao = df

    #Coloca os dataframes em uma lista
    lista.append(outono)
    lista.append(inverno)
    lista.append(primavera)
    lista.append(verao)

    #Retorna uma lista com os dataframes de cada estação do ano
    return lista

