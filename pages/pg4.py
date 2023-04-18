import dash
from dash import dcc, html
import plotly.express as px
import dash_bootstrap_components as dbc

dash.register_page(__name__, name='Gripe')

sidebar = dbc.Nav(
            [
                dbc.NavLink([html.Div("Gripe Geral", className="ms-2")],
                             href="/pg5", active="exact"),
                dbc.NavLink([html.Div('FEBRE-Histórico de probabilidade', className="ms-2")],
                             href="/pg6", active="exact"),                  
             ],   
            vertical=True,
            pills=True,
            className="bg-light",
)
                
layout = html.Div(
       
    [     
    dbc.Row(
        [
            dbc.Col(
                [
                    sidebar
                ], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2),

      ]
    ),
        html.Hr(),
    ]
)


