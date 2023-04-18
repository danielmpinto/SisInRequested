import dash
from dash import html, dcc
from dash import Dash, dcc, html, Input, Output,State
import dash_bootstrap_components as dbc

dbc_css="https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/cyborg/bootstrap.min.css"
#app = Dash(__name__,external_stylesheets=[dbc_css])

app = dash.Dash(__name__, use_pages=True,external_stylesheets=[dbc_css] )

app.layout = html.Div(
       
    [
      dbc.Container(dbc.Alert(html.H5("Sis In", style={'fontSize':50, 'textAlign':'center'},
                        className="alert-heading"), color="success"),
          className="m-2"),
        html.Div([
            dcc.Link(page['name']+"  |  ", href=page['path'])
            for page in dash.page_registry.values()
        ]),
        html.Hr(),

        # content of each page
        dash.page_container
    ]
)


if __name__ == '__main__':
    app.run_server()
