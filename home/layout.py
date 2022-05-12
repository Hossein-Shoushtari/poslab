##### Home Tab -- Layout
###IMPORTS
# dash
from dash import html, dcc, Dash, Output, Input, State, no_update
import dash_bootstrap_components as dbc

def home_layout():
    return dbc.Card([
        dbc.CardBody(
            [
                html.H3("Level 5 Indoor Navigation", style={"color": "silver"}),

                html.Br(),

                dbc.Row(
                    [
                        dbc.Col([
                            html.P("""This is a tool developed by Level 5 Indoor navigation (L5IN) project with positioning focus.
                                The L5IN project deals with real-time navigation inside buildings, using 5G and smartphone sensors.
                                The project demonstrates the feasibility of the transition from outdoor to indoor environment in
                                terms of navigation. The aim of the L5IN project is to use newly introduced 5G technology to demonstrate,
                                based on a research-oriented model project, how in door navigation systems can function. Such systems
                                were previously only known in the outdoor segment (through GNSS) but can now also be integrated into
                                existing smartphone systems and 5G as a ubiquitous alternative for the GNSS solutions within the context
                                of indoor navigation.""",
                                style={"color": "silver", "font-size": "16px"}),
                            html.P("""The positioning work package is one of the L5IN research area. Autonomous pedestrian localization would make
                                the navigation possible at any time. The positioning team use the benefits of interdisciplinary technologies developed
                                at L5IN and focus on the approaches and methods such as Monte Carlo Simulation, state estimation filters, machine learning,
                                deep learning, 5G Positioning to develop a practice-oriented solution.""",
                                style={"color": "silver", "width": "100%", "font-size": "16px"})
                        ]),
                        dbc.Col([
                            html.Div(html.Img(src="assets/images/L5IN_app_photo.png"),
                                style={"textAlign": "center"})
                        ])
                    ]),

                html.Br(),

                html.Hr(style={"width": "40%"}),

                dbc.Row(
                    [
                        dbc.Col([
                            html.B("Responsible for the project:",
                                style={"color": "silver", "font-size": "16px"}),

                            html.P("Prof. Dr. Jörg Müller-Litzkow",
                                style={"color": "silver", "marginTop": "5px", "font-size": "13px", "text-indent": "10px"}),
                            html.P("President of Hafencity University Hamburg (HCU) and Univ. Prof. for Economics and Digitalization",
                                style={"line-height": "110%", "color": "silver", "marginTop": "-20px", "font-size": "12px", "paddingLeft": "10px"}),

                            html.P("Prof. Dr. Harald Sternberg",
                                style={"color": "silver", "marginTop": "-12px", "font-size": "13px", "text-indent": "10px"}),
                            html.P("""Vice President for Teaching and Digitalization of Hafencity University Hamburg (HCU)
                                and Univ. Prof. for Hydrography and Engineering Geodesy""",
                                style={"line-height": "110%", "color": "silver", "marginTop": "-20px", "font-size": "12px", "paddingLeft": "10px"}),

                            html.P("Nils Hellweg",
                                style={"color": "silver", "marginTop": "-12px", "font-size": "13px", "text-indent": "10px"}),
                            html.P("""Project Manager and PhD Student at Hafencity University Hamburg (HCU)""",
                                style={"line-height": "110%", "color": "silver", "marginTop": "-20px", "font-size": "12px", "paddingLeft": "10px"}),
                        ],
                        width=2),

                        dbc.Col([
                            html.B("Positioning Contact Persons:",
                                style={"color": "silver", "font-size": "16px"}),

                            html.P("Hossein Shoushtari",
                                style={"color": "silver", "marginTop": "5px", "font-size": "11px", "text-indent": "10px"}),
                            html.P("Research assistant and PhD Student at Hafencity University Hamburg (HCU)",
                                style={"line-height": "110%", "color": "silver", "marginTop": "-18px", "font-size": "10px", "paddingLeft": "10px"}),
                            html.P("hossein.shoushtari@hcu-hamburg.de",
                                style={"color": "silver", "marginTop": "-18px", "font-size": "10px", "paddingLeft": "10px"}),

                            html.P("Dorian Harder",
                                style={"color": "silver", "marginTop": "-12px", "font-size": "11px", "text-indent": "10px"}),
                            html.P("Research assistant at Hafencity University Hamburg (HCU)",
                                style={"line-height": "110%", "color": "silver", "marginTop": "-18px", "font-size": "10px", "paddingLeft": "10px"}),
                            html.P("dorian.harder@hcu-hamburg.de",
                                style={"color": "silver", "marginTop": "-18px", "font-size": "10px", "paddingLeft": "10px"}),

                            html.P("Georg Fjodorow",
                                style={"color": "silver", "marginTop": "-12px", "font-size": "11px", "text-indent": "10px"}),
                            html.P("Master Student at Hafencity University Hamburg (HCU)",
                                style={"line-height": "110%", "color": "silver", "marginTop": "-18px", "font-size": "10px", "paddingLeft": "10px"}),
                            html.P("georg.fjodorow@hcu-hamburg.de",
                                style={"color": "silver", "marginTop": "-18px", "font-size": "10px", "paddingLeft": "10px"}),
                                
                            html.P("Korvin Venzke",
                                style={"color": "silver", "marginTop": "-12px", "font-size": "11px", "text-indent": "10px"}),
                            html.P("Bachelor Student at Hafencity University Hamburg (HCU)",
                                style={"line-height": "110%", "color": "silver", "marginTop": "-18px", "font-size": "10px", "paddingLeft": "10px"}),
                            html.P("korvin.venzke@hcu-hamburg.de",
                                style={"color": "silver", "marginTop": "-18px", "font-size": "10px", "paddingLeft": "10px"}),
                        ],
                        width=2)
                    ])                
            ]),
        dbc.CardFooter("Copyright © 2022 Level 5 Indoor Navigation. All Rights Reserved", style={"textAlign": "center"})
    ])