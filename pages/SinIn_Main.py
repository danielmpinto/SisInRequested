# Run this app with `python app.py` and
# visit http://127.0.0.1:8049/ in your web browser.

from dash import Dash, dcc, html, Input, Output,State
import dash_table
from dash_table.Format import Format, Scheme
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots
import os
import glob
import dash
import plotly.graph_objects as go
import networkx as nx
import numpy as np
import socket


dbc_css="https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/cyborg/bootstrap.min.css"
app = dash.Dash(__name__, use_pages=True,external_stylesheets=[dbc_css] )

################ S. Sebastiao Geral ######################################
df=pd.read_excel('SSeb2022_23.xlsx')
previsao=pd.read_excel('previsaoDash.xlsx')

df['valorMedida'] = df['valorMedida'].shift(-10)
df['Hazard_2dias']=df['Hazard_2dias'].round(decimals=2)
df['maxmov']=df['maxmov'].round(decimals=2)
df.dropna(inplace=True)
df_PIE=df

fig1 = px.line(df,x='dia',y='valorMedida')
fig2 = px.line(df,x='dia',y='Hazard_2dias')
fig2.update_traces(line_color='red', line_width=5)

fig2.update_traces(yaxis="y2")

subfig = make_subplots(specs=[[{"secondary_y": True}]])

fig3=subfig.add_traces(fig1.data + fig2.data)

fig3.update_layout(template="plotly_dark",title_text='S.Sebastião (todos bairros)')
######################################################################### 
################ Enseada ######################################
df=pd.read_excel('Enseada2022_23.xlsx')
df['valorMedida'] = df['valorMedida'].shift(-10)
fig4 = px.line(df,x='dia',y='valorMedida')
fig5 = px.line(df,x='dia',y='Hazard_2dias')
fig5.update_traces(line_color='yellow', line_width=5)

fig5.update_traces(yaxis="y2")

subfig = make_subplots(specs=[[{"secondary_y": True}]])

fig6=subfig.add_traces(fig4.data + fig5.data)

fig6.update_layout(template="plotly_dark",title_text='Bairro Enseada')
#########################################################################

fig_PIE1 = px.pie(df_PIE, values='Hazard_2dias',names='Hazard_2dias', hole=0.4)
fig_PIE1.update_traces(textposition='inside')
fig_PIE1.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
subfig = make_subplots(specs=[[{"secondary_y": True}]])
fig13=subfig.add_traces(fig_PIE1.data) 
fig13.update_layout(template="plotly_dark",title_text='Probabilidade')

########################################################################

fig_PIE2 = px.pie(df_PIE, values='maxmov',names='maxmov', hole=0.4)
fig_PIE2.update_traces(textposition='inside')
fig_PIE2.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
subfig = make_subplots(specs=[[{"secondary_y": True}]])
fig14=subfig.add_traces(fig_PIE2.data) 
fig14.update_layout(template="plotly_dark",title_text='Máximo Móvel')

################ Praia Grande ######################################
df=pd.read_excel('PraiaGrande2022_23.xlsx')
df['valorMedida'] = df['valorMedida'].shift(-10)
fig7 = px.line(df,x='dia',y='valorMedida')
fig8 = px.line(df,x='dia',y='Hazard_2dias')
fig8.update_traces(line_color='white', line_width=5)

fig8.update_traces(yaxis="y2")

subfig = make_subplots(specs=[[{"secondary_y": True}]])

fig9=subfig.add_traces(fig7.data + fig8.data)

fig9.update_layout(template="plotly_dark",title_text='Bairro Praia Grande')
######################################################################### 
################ Toque Toque Pequeno ######################################
df=pd.read_excel('Toque2022_23.xlsx')
df['valorMedida'] = df['valorMedida'].shift(-10)
fig10 = px.line(df,x='dia',y='valorMedida')
fig11 = px.line(df,x='dia',y='Hazard_2dias')
fig11.update_traces(line_color='orange', line_width=5)

fig11.update_traces(yaxis="y2")

subfig = make_subplots(specs=[[{"secondary_y": True}]])

fig12=subfig.add_traces(fig10.data + fig11.data)

fig12.update_layout(template="plotly_dark",title_text='Bairro Toque Toque Pequeno')
######################################################################### 
fig15 = px.line(previsao,x='Pluviosidade',y='previsao')
fig15.update_traces(line_color='green', line_width=2)

fig15.update_layout(template="plotly_dark",title_text='Previsão Machine Learning')

################## grafico e redes complexas #################################
df=pd.read_excel('nodos_chuva.xlsx')

G=nx.from_pandas_edgelist(df, source='De', target='Para')

#pos = nx.spring_layout(G)
pos = nx.circular_layout(G)


listaTraces = []
    # edges trace
edge_x = []
edge_y = []
for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(color='white', width=1),
        hoverinfo='none',
        showlegend=False,
        mode='lines')

listaTraces.append(edge_trace)

    # nodes trace
node_x = []
node_y = []
text = []
for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        text.append(node)

node_trace = go.Scatter(
        x=node_x, y=node_y, text=text,
        mode='markers+text',
        showlegend=False,
        hoverinfo='none')
# Busca de comunidades

#-------------------------------------------------------
cliques=nx.find_cliques(G)
#+++++++++++++ separacao dos cliques acima de um valor ++++
cliques3 = [clq for clq in cliques if len(clq) >= 4]
#+++++++++++++ ordenacao dos nodos com cliques acima de um valor+++
nodes_cliq = set(n for clq in cliques3 for n in clq)
#++++++++++++ separacao e identificacao dos nodos com maiores graus
grau=nx.degree(G)
nod=[n for n in nodes_cliq if grau[n] >= 25]
#cores_arestas=[(v, w) for v, w in G.edges if v in nod]
    # edges trace
edgecor_x = []
edgecor_y = []
for edgeC in G.edges():
    if edgeC[0] in nod:
        x0, y0 = pos[edgeC[0]]
        x1, y1 = pos[edgeC[1]]
        edgecor_x.append(x0)
        edgecor_x.append(x1)
        edgecor_x.append(None)
        edgecor_y.append(y0)
        edgecor_y.append(y1)
        edgecor_y.append(None)

edge_traceC = go.Scatter(
        x=edgecor_x, y=edgecor_y,
        line=dict(color='red', width=2),
        hoverinfo='none',
        showlegend=False,
        mode='lines')

    # nodes trace colorido
nodecor_x = []
nodecor_y = []
textcor = []
for nodeC in G.nodes():
      if nodeC in nod:
        x, y = pos[nodeC]
        nodecor_x.append(x)
        nodecor_y.append(y)
        textcor.append(nodeC)

node_traceC = go.Scatter(
        x=nodecor_x, y=nodecor_y, text=textcor,
        mode='markers+text',
        showlegend=False,
        hoverinfo='none',
        marker=dict(
            color='black',
            size=50,
            line=dict(color='white', width=1)))

#listaTraces.append(edge_traceC)
#------------------------------------------------------

    # layout
layout = dict(plot_bgcolor='black',
                  paper_bgcolor='black',
                  margin=dict(t=10, b=10, l=10, r=10, pad=0),
                  xaxis=dict(linecolor='black',
                             showgrid=False,
                             showticklabels=False,
                             mirror=True),
                  yaxis=dict(linecolor='black',
                             showgrid=False,
                             showticklabels=False,
                             mirror=True))

    # figure
fig_redes=go.Figure(data=[edge_trace,node_trace,edge_traceC,node_traceC], layout=layout)    
fig_redes.update_layout(template="plotly_dark",
                        title_text='Rede complexa - Autocorrelação Pluviometrica (lag = 10 dias)',
                        font=dict(size=12),
                        margin=dict(l=20, r=20, t=50, b=20))

##########################################################################
app.layout = html.Div(children=[
    dbc.Container(dbc.Alert(html.H5("Pluviosidade São Sebastião 2021-2023", className="alert-heading"), color="success"),
    className="m-2"),
     dcc.Graph(id='graph1',style={'width': '60vh', 'height': '30vh','display':'inline-block'},
        figure=fig3),
    dcc.Graph(id='graph2',style={'width': '30vh', 'height': '30vh','display':'inline-block'},
        figure=fig13),
    dcc.Graph(id='graph3',style={'width': '30vh', 'height': '30vh','display':'inline-block'},
        figure=fig14),
    html.Div(children=''),
    dcc.Graph(id='graph_redes',style={'width': '60vh', 'height': '30vh','display':'inline-block'},
               figure=fig_redes),  
    dcc.Graph(id='graph4',style={'width': '60vh', 'height': '30vh','display':'inline-block'},
        figure=fig6), 
    html.Div(children=''), 
    dcc.Graph(id='graph5',style={'width': '60vh', 'height': '30vh','display':'inline-block'},
        figure=fig9),
    dcc.Graph(id='graph6',style={'width': '60vh', 'height': '30vh','display':'inline-block'},
        figure=fig12),
    html.Div(children=''), 
    dbc.Container(dbc.Alert(html.H5("Previsão de Probabilidade de Evento Extremo - Machine Learning", className="alert-heading"), color='warning'),
    className="m-1"),
    dcc.Graph(id='graph_machine',style={'width': '120vh', 'height': '50vh','display':'inline-block'},
        figure=fig15),
    html.Div(children=''),
    html.I("Entre com a pluviosidade"),
    html.Div(children=''),
    dcc.Input(id='input1', value=None,type='number'),
    html.Div([ html.Span("Probabilidade estimada de chover acima de 250 mm após 10 dias: "),
             html.H5( 
                 html.Span(id="prob-estimada", style={"color": "red"})
                     )
            ])
])    
#df['ret'].iloc[(df['close']-x).abs().argsort()[:1]].values

@app.callback(
    Output("prob-estimada", 'children'),
    Input("input1", "value")
)

def update_output(value):
        # Verifica se o valor é válido
    if value is None:
        return ''
    prob_estimada=previsao['previsao'].iloc[(previsao['Pluviosidade']-value).abs().argsort()[:1]].values
    return np.round(prob_estimada,2)



