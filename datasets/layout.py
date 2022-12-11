##### Datasets Tab -- Layout
###IMPORTS
# dash
from dash import html, dcc, Dash, Output, Input, State, no_update
import dash_bootstrap_components as dbc
# built in
import datetime

def ds_layout():
    return dbc.Card(
        [
            dbc.CardBody(
                [
                    html.Br(),
                    html.H2(["L5IN", html.Sup("+"), " Dataset: Release 26.02.2023"], style={"color": "white", "text-align": "center"})
                ]
            ),
            dbc.CardFooter(f"Copyright © {datetime.date.today().strftime('%Y')} Level 5 Indoor Navigation. All Rights Reserved", style={"textAlign": "center"})
        ]
    )