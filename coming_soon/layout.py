##### Coming Soon Tab -- Layout
###IMPORTS
# dash
from dash import html, dcc, Dash, Output, Input, State, no_update
import dash_bootstrap_components as dbc
# built in
import datetime

def com_layout():
    return dbc.Card(
        [
            dbc.CardBody(
                [
                    html.P("Coming Soon", className="card-text")
                ]
            ),
            dbc.CardFooter(f"Copyright © {datetime.date.today().strftime('%Y')} Level 5 Indoor Navigation. All Rights Reserved", style={"textAlign": "center"})
        ]
    )