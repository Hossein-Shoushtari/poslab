from dash import html, dcc, Dash, Output, Input, State, no_update
import dash_bootstrap_components as dbc

def coming_soon_card():
    return dbc.Card(
        dbc.CardBody(
            [
                html.P("Coming Soon", className="card-text")
            ]
        ),
        className="mt-3",
    )