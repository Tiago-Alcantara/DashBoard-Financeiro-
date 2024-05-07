from dash import Dash, html, dcc, callback, Output, Input, dash_table
import yfinance as yf
import datetime
import plotly.graph_objects as go
from bcb import sgs

ticker = ['WEGE3.SA', 'PETR4.SA', 'ABEV3.SA', 'VALE3.SA', 'MGLU3.SA', 'PCAR3.SA', 'ITUB4.SA', 'BBDC4.SA', 'BBAS3.SA']
cotacoes = yf.download(ticker, start = (datetime.date.today() - datetime.timedelta(days=5)))
cotacoes = cotacoes['Close']
cotacoes = cotacoes.iloc[-1, :]
cotacoes = cotacoes.to_frame()
cotacoes = cotacoes.reset_index()
cotacoes.columns = ['Ticker', 'Preço']
cotacoes['Preço'] = cotacoes['Preço'].astype(float).round(2)


cotacoes_candle = yf.download("WEGE3.SA", start= (datetime.date.today() - datetime.timedelta(days=5)))

layout = go.Layout(yaxis=dict(tickfont=dict(color="#D3D6DF"), showline = False),
                           xaxis=dict(tickfont=dict(color="#D3D6DF"), showline = False))

fig_candle = go.Figure(data=[go.Candlestick(x=cotacoes_candle.index,
                                            open=cotacoes_candle['Open'], 
                                            high=cotacoes_candle['High'],
                                            low=cotacoes_candle['Low'],
                                            close=cotacoes_candle['Close']), 
                            ], layout=layout)






app = Dash(__name__)

app.layout = html.Main(
    
    children = [html.Div(children = [
                                    html.Div(
                                        
                                        children= html.H1(children="Cotações de ontem", className='titulos-do-dash'),
                                        
                                        style={'display': 'flex', 'justify-content': 'center'}

                                    ),
                                    html.Div(

                                        children= dash_table.DataTable(cotacoes.to_dict('records'), id = 'tabela_teste',
                                                                       
                                                      style_header={
                                                                    'backgroundColor': '#333E66',
                                                                    'fontWeight': 'bold',
                                                                    'border': '0px',
                                                                    'font-size': "12px",
                                                                    'color': '#D3D6DF',
                                                                    "borderRadius": "8px"},

                                                      style_cell={'textAlign': 'center',
                                                                    'padding': '4px 4px',
                                                                    'backgroundColor': '#212946',
                                                                    "borderRadius": "8px",
                                                                    'color': '#D3D6DF'
                                                                    
                                                                    },    

                                                        style_data={ 'border': '0px',
                                                                    'font-size': "12px",
                                                                        }, 

                                                       style_table={
                                                                    
                                                                    'borderRadius': '8px',
                                                                    'overflow': 'hidden',
                                                                    
                                                                },

                                                         style_data_conditional=[
                                                                        {
                                                                        'if': {
                                                                                'filter_query': '{Preço} > 20',
                                                                                'column_id': 'Preço'
                                                                            }, 
                                                                            'color': '#19C819',
                                                                            
                                                                        },
                                                                        {
                                                                        'if': {
                                                                                'filter_query': '{Preço} < 20',
                                                                                'column_id': 'Preço'
                                                                            }, 
                                                                            'color': '#E50000'
                                                                        }
                                                                ]),         
                                        style={'margin-left': '100px', 'margin-right': '100px', 
                                               }

                                    )], 
                         
                         
                         
                         style = {'background-color': 'black', 'grid-columns': '1', 'grid-row': '1', 'height': '50vh'}),
                                  
                


                html.Div(children = [
                                    html.Div(
                                        
                                        children= html.H1(children="Gráfico de Candle", className='titulos-do-dash'),
                                        
                                        style={'display': 'flex', 'justify-content': 'center'}

                                    ),
                                    html.Div(

                                        children= dcc.Graph(figure=fig_candle, style= {'margin-left': '100px', 'margin-right': '100px',
                                                                                           'height': '400px'})
                                        

                                    )],
                         
                    
                         
                         style = {'background-color': 'black', 'grid-columns': '1', 'grid-row': '2', 'height': '50vh'}),



                html.Div(children = [html.P('Elementos do Dash'),
                                     dcc.Dropdown(['IPCA', 'IGP-M'], 'IPCA', id = 'escolher_inflacao', multi = True),
                                     html.Br(),
                                    dcc.Checklist(['IPCA', 'IGP-M'], id = 'checklist-padrao'),
                                    html.Br(),
                                    dcc.Slider(0, 30, 5)

                                     ], 
                         
                         style = {'background-color': 'white', 'grid-columns': '2', 'grid-row': '1', 'height': '50vh'}),



                html.Div(children =  [
                                    html.Div(
                                        
                                        children= html.H1(children="Gráfico de Inflação", className='titulos-do-dash'),
                                        
                                        style={'display': 'flex', 'justify-content': 'center'}

                                    ),

                                    html.Div(

                                        [dcc.Dropdown(['IPCA', 'IGP-M'], 'IPCA', id = 'drop_infla_callback'),
                                         dcc.Dropdown(['6', '12', '24'], '6', id = 'drop_infla_callback_periodo')]

                                    ),

                                    html.Div(

                                        children= dcc.Graph(id = 'grafico_com_callback')
                                        

                                    )],
                         
                         
                         style = {'background-color': 'black', 'grid-columns': '2', 'grid-row': '2', 'height': '50vh'})  

                ], style = {'display': 'grid', 'gap': '25px', 'grid-template-columns': 'repeat(2 , 1fr)'}
                    )


@app.callback(

    Output('grafico_com_callback', 'figure'),
    Input('drop_infla_callback', 'value'),
    Input('drop_infla_callback_periodo', 'value')

)
def criando_grafico_infla(valor_do_dropdown_indicador, valor_dropdown_periodo):

    dados_inflacao = sgs.get({'ipca': 433,
                        'igp-m': 189})

    dados_inflacao = dados_inflacao.dropna()

    dados_inflacao = dados_inflacao/100
    dados_inflacao = dados_inflacao.iloc[-(int(valor_dropdown_periodo)):, :]

    if valor_do_dropdown_indicador == "IPCA":

        dados_inflacao = dados_inflacao['ipca']

    elif valor_do_dropdown_indicador == 'IGP-M':

        dados_inflacao = dados_inflacao['igp-m']

    layout = go.Layout(yaxis=dict(tickformat=".1%", tickfont=dict(color="black")),
                            xaxis=dict(tickfont=dict(color="black")))

    fig_inflacao = go.Figure(layout = layout)

    fig_inflacao.add_trace(go.Bar(x=dados_inflacao.index, y=dados_inflacao.values,
                          marker_color = 'blue', name = 'IPCA'
                         ))        

    return fig_inflacao


if __name__ == '__main__': 
    app.run(debug=True)

