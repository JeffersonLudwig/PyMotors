import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

# 1. Base de Dados Fictícia para Treino (No TCC real, você usaria milhares de dados)
# Aqui ensinamos a IA: [Ano, KM] -> Preço
dados_treino = {
    'ano': [2010, 2012, 2015, 2018, 2020, 2022, 2010, 2015],
    'km':  [120000, 100000, 70000, 40000, 20000, 5000, 130000, 80000],
    'preco': [25000, 32000, 45000, 70000, 90000, 110000, 24000, 44000]
}

# 2. Criar e Treinar o Modelo
def treinar_modelo():
    df = pd.DataFrame(dados_treino)
    X = df[['ano', 'km']] # Features (O que define o preço)
    y = df['preco']       # Target (O que queremos descobrir)
    
    modelo = LinearRegression()
    modelo.fit(X, y)
    return modelo

modelo_ia = treinar_modelo()

# 3. Função para Prever Preço
def prever_preco(ano, km):
    # A IA recebe o Ano e KM e calcula o preço provável
    entrada = pd.DataFrame([[ano, km]], columns=['ano', 'km'])
    preco_estimado = modelo_ia.predict(entrada)[0]
    return round(preco_estimado, 2)