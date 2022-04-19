from dash import html, dcc, Dash, Output, Input, State, no_update
import dash_bootstrap_components as dbc

def evaluator_card():
    return dbc.Card(
        [
            dbc.CardBody(
                [
                    html.P("EVALUATOR", className="card-text"),
                    dbc.Button("Don't click here", color="danger"),
                ]
            ),
            dbc.CardFooter("Copyright © 2022 Level 5 Indoor Navigation. All Rights Reserved", style={"textAlign": "center"})
        ]
    )