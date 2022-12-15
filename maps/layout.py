##### Maps -- Layout
###IMPORTS
# dash
import dash_bootstrap_components as dbc
from dash import html, dcc

def storage():
    ### STORAGE
    # dcc.Store to store and share data between callbacks
    storage = html.Div([
        dcc.Store(id="unlocked", data={"unlocked": False,"date": 0}, storage_type="memory"),
        dcc.Store(id="layers", data=[], storage_type="memory")
    ])
    return storage


def modals():
    ### MODALs
    modals = html.Div(
        [
            # upload and map display done
            dbc.Modal(
                dbc.ModalHeader(
                    dbc.Alert(
                        [
                            html.Div(html.Img(src="assets/images/signs/done_sign.svg"), style={"margin-right": "30px"}),
                            "Successful!"
                        ],
                        className="d-flex align-items-center",
                        style={"padding-top": "20px", "margin-top": "12px", "margin-left": "-6px", "width": "500px", "color": "silver", "background": "transparent"}
                    ),
                    style={"background": "rgba(0, 179, 0, 0.3)", "border-radius": 5, "border": "1px solid #146d2c", "height": "70px"}
                ),
                id="display_done",
                is_open=False
            ),
            # trajectory 500 points limit reached
            dbc.Modal(
                dbc.ModalHeader(
                    dbc.Alert(
                        [
                            html.Div(html.Img(src="assets/images/signs/caution_sign.svg"), style={"margin-right": "30px"}),
                            "Over 500 pts! Not displaying, but still in system."
                        ],
                        className="d-flex align-items-center",
                        style={"padding-top": "20px", "margin-top": "12px", "margin-left": "-6px", "width": "500px", "color": "silver", "background": "transparent"}
                    ),
                    style={"background": "rgba(243, 156, 18, 0.3)", "border-radius": 5, "border": "1px solid #F39C12", "height": "70px"}
                ),
                id="overflow",
                is_open=False
            ),
            # unlock hcu maps
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Researcher Login")),
                    dbc.ModalBody(
                        html.Div(
                            [
                                dbc.Label("Password"),
                                dbc.Input(id="hcu_pw", type="password", placeholder="Enter password", style={"color": "white"}),
                                dbc.FormFeedback("Access granted", type="valid"),
                                dbc.FormFeedback("Access denied", type="invalid")
                            ]
                        )
                    ),
                    dbc.ModalFooter(
                        dbc.Button("Unlock", color="primary", id="unlock")
                    ),
                ],
                id="research",
                backdrop="static",
                is_open=False,
            )
        ]
    )
    return modals

def maps_layout():
    return html.Div(
        [
            storage(),
            modals()
        ]
    )