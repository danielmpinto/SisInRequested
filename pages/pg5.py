import matplotlib.pyplot as fig
from pytrends.request import TrendReq #precisa instalar essa biblioteca usando pip install
import matplotlib.dates as mdates
import pandas as pd
from scipy.signal import find_peaks
import numpy as np
import matplotlib.ticker as ticker
import plotly.express as px
from plotly.subplots import make_subplots
import dash
from dash import Dash, dcc, html, Input, Output,State,callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import threading
import time

dash.register_page(__name__, name='Gripe Geral')


#++++++++++++++++++++++ conexao com o servidor ++++++++++++++++++++++++++++
pytrends=TrendReq(hl='en-US', tz=360)



#++++++++++++++++++++++ lista com palavra-chave +++++++++++++++++++++++++++
kw_list=['febre','tosse','garganta','hospital']

#++++++++++++++++++++++ lista de legenda para o grafico
leg=[kw_list[0],kw_list[1],kw_list[2],kw_list[3]]


## thread infinita

## deixa figuras globais

global fig1
global fig2
global fig3
global fig4
global fig5
global fig6
global fig7
global fig8
global fig9
global fig10
global fig11
global fig12

def atualizaResultado():
  while True:
    pytrends.build_payload(kw_list, timeframe='now 7-d',geo='BR',gprop='')
    #pytrends.build_payload(kw_list,  
    #                      timeframe='2023-01-01 2023-04-04',
    #                      geo='BR',gprop='')

    teste=pytrends.interest_over_time()

    teste['dias']=teste.index

    peaks1, _ = find_peaks(teste[kw_list[0]], height=60)
    peaks2, _ = find_peaks(teste[kw_list[1]], height=60)
    peaks3, _ = find_peaks(teste[kw_list[2]], height=60)
    peaks4, _ = find_peaks(teste[kw_list[3]], height=60)
    #peaks, _ = find_peaks(teste['febre'], distance=4)

    difer1=np.diff(peaks1)
    difer2=np.diff(peaks2)
    difer3=np.diff(peaks3)
    difer4=np.diff(peaks4)

    fig1 = px.line(teste,x='dias',y='febre')
    fig1.add_trace(go.Scatter(x=teste.index[peaks1],
                              y=teste[kw_list[0]].values[peaks1],
                              mode='markers'))
    fig1.add_trace(go.Scatter(x=teste.index,
                              y=60*np.ones_like(teste[kw_list[0]].values),
                              line = dict(color='firebrick', width=4, dash='dot')
                              ))
    fig1.update_layout(template="plotly_dark",showlegend=False,
                       title_text='Busca no Google por "febre"')

    fig2 = px.histogram(difer1,nbins=5)
    fig2.update_layout(template="plotly_dark",showlegend=False,
                       title_text='Histograma-distância entre picos"',
                       xaxis_title="horas")


    fig3 = px.line(difer1)
    fig3.update_layout(template="plotly_dark",showlegend=False,
                       title_text='Evolução da distância entre picos"',
                       yaxis_title="distância horas")

    fig4 = px.line(teste,x='dias',y='tosse')
    fig4.add_trace(go.Scatter(x=teste.index[peaks2],
                              y=teste[kw_list[1]].values[peaks2],
                              mode='markers'))
    fig4.add_trace(go.Scatter(x=teste.index,
                              y=60*np.ones_like(teste[kw_list[1]].values),
                              line = dict(color='firebrick', width=4, dash='dot')
                              ))
    fig4.update_layout(template="plotly_dark",showlegend=False,
                       title_text='Busca no Google por "tosse"')

    fig5 = px.histogram(difer2,nbins=5)
    fig5.update_layout(template="plotly_dark",showlegend=False,
                       title_text='Histograma-distância entre picos"',
                       xaxis_title="horas")


    fig6 = px.line(difer2)
    fig6.update_layout(template="plotly_dark",showlegend=False,
                       title_text='Evolução-distância entre picos"',
                       yaxis_title="distância horas")


    fig7 = px.line(teste,x='dias',y='garganta')
    fig7.add_trace(go.Scatter(x=teste.index[peaks3],
                              y=teste[kw_list[2]].values[peaks3],
                              mode='markers'))
    fig7.add_trace(go.Scatter(x=teste.index,
                              y=60*np.ones_like(teste[kw_list[2]].values),
                              line = dict(color='firebrick', width=4, dash='dot')
                              ))
    fig7.update_layout(template="plotly_dark",showlegend=False,
                       title_text='Busca no Google por "garganta"')

    fig8 = px.histogram(difer3,nbins=5)
    fig8.update_layout(template="plotly_dark",showlegend=False,
                       title_text='Histograma-distância entre picos"',
                       xaxis_title="horas")


    fig9 = px.line(difer3)
    fig9.update_layout(template="plotly_dark",showlegend=False,
                       title_text='Evolução-distância entre picos"',
                       yaxis_title="distância horas")


    fig10 = px.line(teste,x='dias',y='hospital')
    fig10.add_trace(go.Scatter(x=teste.index[peaks4],
                              y=teste[kw_list[3]].values[peaks4],
                              mode='markers'))
    fig10.add_trace(go.Scatter(x=teste.index,
                              y=60*np.ones_like(teste[kw_list[3]].values),
                              line = dict(color='firebrick', width=4, dash='dot')
                              ))
    fig10.update_layout(template="plotly_dark",showlegend=False,
                        title_text='Busca no Google por "hospital"')

    fig11 = px.histogram(difer4,nbins=5)
    fig11.update_layout(template="plotly_dark",showlegend=False,
                        title_text='Histograma-distância entre picos"',
                        xaxis_title="horas")


    fig12 = px.line(difer3)
    fig12.update_layout(template="plotly_dark",showlegend=False,
                        title_text='Evolução-distância entre picos"',
                        yaxis_title="distância horas")

    #df=pd.read_excel('Febre_norm.xlsx')
    #df.drop(['febre_Google','febre_alta_Norm'],axis=1,inplace=True)

    df=pd.DataFrame(columns=['febre_Google','febre_alta_Norm'])
    df['febre_Google']=teste['febre']

    z_normal=lambda x:(x-x.mean())/x.std()
    teste=teste.apply(z_normal)

    df['febre_alta_Norm']=teste['febre']

    df.to_excel('gripe.xlsx')
    time.sleep(100)

    
# executa thread
threading.Thread(target=atualizaResultado).start()
    ##########################################################################
layout = html.Div(children=[
        dbc.Container(dbc.Alert(html.H5("Situação de Gripe (últimos 7 dias)", className="alert-heading"), color="success"),
        className="m-2"),
         dcc.Graph(id='graph1',style={'width': '40vh', 'height': '30vh','display':'inline-block'},
            figure=fig1),
         dcc.Graph(id='graph2',style={'width': '40vh', 'height': '30vh','display':'inline-block'},
            figure=fig2),
         dcc.Graph(id='graph3',style={'width': '40vh', 'height': '30vh','display':'inline-block'},
            figure=fig3),
        html.Div(children=''),
        dcc.Graph(id='graph4',style={'width': '40vh', 'height': '30vh','display':'inline-block'},
            figure=fig4),   
        dcc.Graph(id='graph5',style={'width': '40vh', 'height': '30vh','display':'inline-block'},
            figure=fig5),   
        dcc.Graph(id='graph6',style={'width': '40vh', 'height': '30vh','display':'inline-block'},
            figure=fig6),  
        html.Div(children=''),
        dcc.Graph(id='graph7',style={'width': '40vh', 'height': '30vh','display':'inline-block'},
            figure=fig7),   
        dcc.Graph(id='graph8',style={'width': '40vh', 'height': '30vh','display':'inline-block'},
            figure=fig8),   
        dcc.Graph(id='graph9',style={'width': '40vh', 'height': '30vh','display':'inline-block'},
            figure=fig9),  
        html.Div(children=''),
        dcc.Graph(id='graph10',style={'width': '40vh', 'height': '30vh','display':'inline-block'},
            figure=fig10),   
        dcc.Graph(id='graph11',style={'width': '40vh', 'height': '30vh','display':'inline-block'},
            figure=fig11),   
        dcc.Graph(id='graph12',style={'width': '40vh', 'height': '30vh','display':'inline-block'},
            figure=fig12),                 
    ])        
    
    

