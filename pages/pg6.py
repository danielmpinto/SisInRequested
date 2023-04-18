import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import dash
from dash import Dash, dcc, html, Input, Output,State,callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import scipy.interpolate as interp


dash.register_page(__name__, name='FEBRE-Histórico de probabilidade')


df1=pd.read_excel('Febre_norm.xlsx')
df2=pd.read_excel('gripe.xlsx')
df1.drop(['Febre','febre_Google','febre_alta_Norm'],axis=1,inplace=True)

novo=np.linspace(df2['febre_Google'].min(),df2['febre_Google'].max(),364)
x = interp.interp1d(np.arange(df2['febre_alta_Norm'].size),df2['febre_alta_Norm'],kind='cubic')(novo)
df1['febre_alta_Norm']=pd.Series(x)

#df_grupo=df.groupby(['FebreNorm','febre_alta_Norm']).size().reset_index()
#df_grupo.drop([0],axis=1,inplace=True)

fig1=px.ecdf(df1)

fig1.update_layout(template="plotly_dark",showlegend=False,
                   title_text='Comparação com probabilidade histórica')

##########################################################################
layout = html.Div(children=[
    dbc.Container(dbc.Alert(html.H5("Compara (últimos 7 dias) com histórico SUS", className="alert-heading"), color="success"),
    className="m-2"),
     dcc.Graph(id='graph1',style={'width': '60vh', 'height': '50vh','display':'inline-block'},
        figure=fig1)
     
])    
     