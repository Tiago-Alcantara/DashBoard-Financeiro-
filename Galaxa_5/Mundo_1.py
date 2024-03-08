from dash import Dash,html,dcc,callback,Output,Input
import plotly.express as px
import pandas as pd
from mundo_1_import import *


df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')


app = Dash(__name__) #nome do codigo


app.layout = html.Div([
    html.H1(children='Title teste ',style={'textAlign': 'center'}),
    dcc.Dropdown(df.country.unique(),'Canada', id='dropdown-selection'),
    dcc.Graph(id='graph-content')
])

@callback(
    Output('graph-content','figure'),
    Input('dropdown-selection','value')
)
def updateGraph(value):
    dff = df[df.country==value]
    return px.line(dff, x='year',y='pop')

if __name__ == '__main__': #rodar os imports
    app.run(debug=True)
    contar_goiabas(2)