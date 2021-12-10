# Librerías que por ahora no he necesitado
from datetime import datetime, timedelta

import pandas_datareader as pdr
import numpy as np
import plotly.express as px
import requests
import time
from time import sleep
import dash
from dash import dcc  # dash_core_components
from dash import html  # dash_html_components
from dash import Input, Output

# Importamos todas las librerías necesarias para poder llevar a cabo el proyecto:

import pandas as pd
import plotly.graph_objects as go
import krakenex
from pykrakenapi import KrakenAPI

# Acceder a los datos
api = krakenex.API()
k = KrakenAPI(api)

# Solicitamos al usuario qué par de monedas quiere representar
print(
    "Escriba el par de cotizaciones que quiera visualizar (introduzca las siglas).\n\nElija la primera moneda:\n   BTC - Bitcoin\n   ETH - Ethereum\n   USDT - Tether\n   SOL - Solana\n   ADA - Cardano\n   USDC - USD Coin\n   DOGE - Dogecoin\n")

c1 = input('PRIMERA MONEDA: ')

print(
    "\nElija la segunda moneda:\n   USD - Dólar\n   EUR - Euro\n   BTC - Bitcoin\n   ETH - Ethereum\n   USDT - Tether\n   SOL - Solana\n   ADA - Cardano\n   USDC - USD Coin\n   DOGE - Dogecoin\n")
c2 = input('SEGUNDA MONEDA: ')

# Unimos el str de las monedas para poder trabajar con dicho par de cotizaciones
comp_coin = c1 + c2

# get historical data, ojo el resultado que obtenemos es una tupla.
ohlc = k.get_ohlc_data(comp_coin, interval=1, ascending=True)
ohlc[0].head()

# convertimos la tupla a un dataFrame
df = ohlc[0]


# calculate vwap value
def c_w(df):
    df = df.sort_values('dtime', ascending=False)
    df_vwap = []
    for j in range(0, df.shape[0] - 3):
        n = 4 + j
        total_sum = 0.0
        volume_sum = 0
        for i in range(j, n):
            h_p = df.iloc[i, 2]
            l_p = df.iloc[i, 3]
            c_p = df.iloc[i, 4]
            p = (h_p + l_p + c_p) / 3
            v = df.iloc[i, 6]
            total_sum += p * v
            volume_sum += v
        sol = total_sum / volume_sum
        df_vwap.append(sol)
    for k in range(df.shape[0] - 3, df.shape[0]):
        for m in range(k, df.shape[0]):
            h_p = df.iloc[m, 2]
            l_p = df.iloc[m, 3]
            c_p = df.iloc[m, 4]
            p = (h_p + l_p + c_p) / 3
            v = df.iloc[m, 6]
            total_sum += p * v
            volume_sum += v
        sol = total_sum / volume_sum
        df_vwap.append(sol)
    r = pd.DataFrame(df_vwap, index=df.index, columns=['calc_vwap'])
    return r.sort_values('dtime', ascending=True)


calc_vwap = c_w(df)

# unimos al df el vwap calculado
df_c = pd.concat([df, calc_vwap], join="outer", axis=1)

# Graficar el par PRIMERA MONEDA - SEGUNDA MONEDA
fig = go.Figure(data=[go.Candlestick(x=df_c.index,
                                     open=df_c['open'],
                                     high=df_c['high'],
                                     low=df_c['low'],
                                     close=df_c['close'],
                                     ),
                      ])
fig.update_layout(title_text='Gráfico de cotizaciones: ' + comp_coin, title_x=0.5)
fig.show()

# graficar VWAP
fig = go.Figure(
    data=[go.Scatter(x=df_c.index, y=df_c['calc_vwap'], line=dict(color='purple', width=1), name='VWAP Calculado'),
          go.Scatter(x=df_c.index, y=df_c['vwap'], line=dict(color='red', width=1), name='VWAP')])
fig.update_layout(title_text='Gráfico de cotizaciones: VWAP (' + comp_coin + ')', title_x=0.5)
fig.show()

# Graficar el par PRIMERA MONEDA - SEGUNDA MONEDA y el VWAP
fig = go.Figure(data=[go.Candlestick(x=df_c.index,
                                     open=df_c['open'],
                                     high=df_c['high'],
                                     low=df_c['low'],
                                     close=df_c['close'],
                                     name='Cotización ' + comp_coin),
                      go.Scatter(x=df_c.index, y=df_c['calc_vwap'], line=dict(color='purple', width=1), name='VWAP')])
fig.update_layout(title_text='Gráfico de cotizaciones: ' + comp_coin, title_x=0.5)
fig.show()

