#### IMPORTS
# dash
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc

# ---------------- HTML ---------------- #
# designing the webpage using dash
ex_ss = [dbc.themes.DARKLY]
app = Dash(__name__, external_stylesheets=ex_ss)
server = app.server
# title
app.title = "Test" 

div = html.Div([])

# putting all together
app.layout = html.Div(
    [  
        div
    ]
)

# pushing the page to the web
if __name__ == "__main__":
    app.run_server(debug=True)
