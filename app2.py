import dash
from dash import html, dcc
from dash import Dash, dcc, html, Input, Output,State
import dash_bootstrap_components as dbc

dbc_css="https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/cyborg/bootstrap.min.css"
#app = Dash(__name__,external_stylesheets=[dbc_css])

app = dash.Dash(__name__, use_pages=True,external_stylesheets=[dbc_css] )

sidebar = dbc.Nav(
            [
                dbc.NavLink([html.Div("Home",className="ms-2")],
                             href="/", active="exact"),
                dbc.NavLink([html.Div("Chuvas Extremas", className="ms-2")],
                             href="/pg2", active="exact"),
#                dbc.NavLink([html.Div("São Sebastião Geral", className="ms-2")],
#                             href="/pg3", active="exact"),
                dbc.NavLink([html.Div("Gripe",className="ms-2")],
                             href="/pg4", active="exact")
             ],   
            vertical=True,
            pills=True,
            className="bg-light",
)
                
app.layout = html.Div(
       
    [     
      dbc.Container(dbc.Alert(html.H5("SisIn", style={'fontSize':70, 'textAlign':'center'},
                        className="alert-heading"), color="success"),
          className="m-2"),
       html.Hr(),
       
        html.Div("Eventos Extremos", style={'fontSize':30, 'textAlign':'left'}),

    dbc.Row(
        [
            dbc.Col(
                [
                    sidebar
                ], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2),

            dbc.Col(
                [
                    dash.page_container
                ], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10)
        ]
    ),
        html.Hr(),
    ]
)


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080)
