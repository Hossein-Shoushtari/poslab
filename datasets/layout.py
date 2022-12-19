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
                    html.Br(),
                    html.Br(),
                    html.Iframe(
                        src="https://docs.google.com/forms/d/e/1FAIpQLScn4-3eV_mh1giia81LE1S_gk-WJoEPVJnYwkBZzug3UP3TMw/viewform?embedded=true",
                        style={
                            "width": "100%",
                            "height": "1300px"
                        }
                    )
                ],
                style={
                    "padding": "0px",
                    "background": "#FAE7D9"
                }
            ),
            dbc.CardFooter(
                f"Copyright © {datetime.date.today().strftime('%Y')} Level 5 Indoor Navigation. All Rights Reserved",
                class_name="ds-footer"
            )
        ],
        class_name="ds-card"
    )