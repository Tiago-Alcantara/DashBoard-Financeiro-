from dash import Dash, html, dcc, callback, Output, Input

app = Dash(__name__)

app.layout = html.Main(
    
    children = [html.H1("Hello World"),
                html.H2("Subtitulo"),
                html.H3("sub do sub titulo"),
                html.P("Texto normal"),
                html.A("Link do google", href = '"https://www.google.com.br'),
                html.A("Link do globo.com", href= "https://www.globo.com", target = '_blank', style={'display': 'block'}),
                
                ]
)

if __name__ == '__main__': 
    app.run(debug=True)






