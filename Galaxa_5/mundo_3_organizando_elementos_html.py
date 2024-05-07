from dash import Dash, html, dcc, callback, Output, Input

app = Dash(__name__)

app.layout = html.Main(
    
    children = [html.Div(children = "Texto 1", 
                         style = {'background-color': 'red', 'grid-columns': '1', 'grid-row': '1', 'height': '50vh',
                                  'display': 'flex', 'justify-content': 'center'}), 
                


                html.Div(children = "Texto 2", style = {'background-color': 'blue', 'grid-columns': '1', 'grid-row': '2', 'height': '50vh'}),
                html.Div(children = "Texto 3", style = {'background-color': 'green', 'grid-columns': '2', 'grid-row': '1', 'height': '50vh'}),
                html.Div(children = "Texto 4", style = {'background-color': 'yellow', 'grid-columns': '2', 'grid-row': '2', 'height': '50vh'})  

                ], style = {'display': 'grid', 'gap': '25px', 'grid-template-columns': 'repeat(2 , 1fr)'}
                    )

if __name__ == '__main__': 
    app.run(debug=True)