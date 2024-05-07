from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from mundo_1_import import contar_goiabas

'''
DADOS
APP
LAYOUT
CALLBACKS
RODAR O APP
'''

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

app = Dash(__name__) #esse name é o nome do seu código

app.layout = html.Div([
    html.H1(children='Titulo 2', style={'textAlign':'center'}),
    dcc.Dropdown(df.country.unique(), 'Canada', id='dropdown-selection'),
    dcc.Graph(id='graph-content')
])

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    dff = df[df.country==value]
    return px.line(dff, x='year', y='pop')

if __name__ == '__main__': #isso impede de rodar em imports
    app.run(debug=True)
    contar_goiabas(2)

























