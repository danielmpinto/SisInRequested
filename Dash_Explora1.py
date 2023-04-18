# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Maçã", "Laranja", "Banana", "Maçã", "Laranja", "Banana"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig1 = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = html.Div(children=[
    html.H1(children='Explorando mais ferramentas'),

    html.Div(children='''
        explorando tamanho das mensagens
    '''),
    dcc.Markdown(
       '''
            # Olá Mundo, SOU EU!
       '''
       ),               

    dcc.Graph(
        id='grafico1',
        figure=fig1
    ),
  dcc.Dropdown(['NYC', 'MTL', 'SF'], value='NYC', id='demo-dropdown'),
    html.Div(id='dd-output-container')           
])

@app.callback(
    Output('grafico1', 'figure'),
    Input('demo-dropdown', 'value')
)
def update_output(value):
    if value=='NYC':
             fig1 = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
    else:
             tab_escolha=df.loc[ df['City']==value,:]         
             fig1 = px.bar(tab_escolha, x="Fruit", y="Amount", color="City", barmode="group")
    return fig1


if __name__ == '__main__':
    app.run_server(debug=True)

