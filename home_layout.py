from dash import html, dcc, Dash, Output, Input, State, no_update
import dash_bootstrap_components as dbc

def home_card():
    return dbc.Card(
        dbc.CardBody(
            [
                html.H3('Space for descriptions...', style={'textAlign': 'center'})
            ]
        ),
        className="mt-3",
)