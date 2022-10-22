##### Home Tab -- Layout
###IMPORTS
# dash
from dash import html, dcc, Dash, Output, Input, State, no_update
import dash_bootstrap_components as dbc
# built in
import datetime

def home_layout():
    return dbc.Card([
        dbc.CardBody(
            [
                html.Br(),
                html.H3("L5IN: Level 5 Indoor Navigation", style={"color": "silver", "text-align": "center"}),

                html.Br(),

                html.Div(html.Iframe(
                    src="https://www.youtube.com/embed/w7jk_1mhPY0",
                    width="842",
                    height="475" 
                ), style={"textAlign": "center"}),

                html.Br(),

                html.Div(
                    html.H4("About this website",
                        style={
                            "display": "inline-block",
                            "font-variant": "small-caps",
                            "color": "silver",
                            "text-align": "center",
                            "padding-bottom": "5px",
                            "border-bottom": "3px solid silver"
                        }),
                    style={"text-align": "center"}),
                html.Div(
                    html.P("""This is a tool developed by Level 5 Indoor navigation (L5IN) project with positioning focus.
                        The L5IN project deals with real-time navigation inside buildings, using 5G and smartphone sensors.
                        The project demonstrates the feasibility of the transition from outdoor to indoor environment in
                        terms of navigation. The aim of the L5IN project is to use newly introduced 5G technology to demonstrate,
                        based on a research-oriented model project, how indoor navigation systems can function. Such systems
                        were previously only known in the outdoor segment (through GNSS) but can now also be integrated into
                        existing smartphone systems and 5G as a ubiquitous alternative for the GNSS solutions within the context
                        of indoor navigation.""",
                        style={"color": "silver", "font-size": "16px", "padding-left": "10px", "padding-right": "10px"}),
                    style={"width": "90%", "margin": "auto"}),
                html.Div(
                    html.P("""The positioning work package is one of the L5IN research area. Autonomous pedestrian localization would make
                        the navigation possible at any time. The positioning team use the benefits of interdisciplinary technologies developed
                        at L5IN and focus on the approaches and methods such as Monte Carlo Simulation, state estimation filters, machine learning,
                        deep learning, 5G Positioning to develop a practice-oriented solution.""",
                        style={"color": "silver", "width": "100%", "font-size": "16px", "padding-left": "10px", "padding-right": "10px"}),
                    style={"width": "90%", "margin": "auto"}),

                html.Br(),

                html.Div(
                    html.H4("Publications",
                        style={
                            "display": "inline-block",
                            "font-variant": "small-caps",
                            "color": "silver",
                            "text-align": "center",
                            "padding-bottom": "5px",
                            "border-bottom": "3px solid silver"
                        }),
                    style={"text-align": "center"}),

                html.Br(),

                html.Div(
                    html.H4("Contact",
                        style={
                            "display": "inline-block",
                            "font-variant": "small-caps",
                            "color": "silver",
                            "text-align": "center",
                            "padding-bottom": "5px",
                            "border-bottom": "3px solid silver"
                        }),
                    style={"text-align": "center"}),
                dbc.Row(
                    [
                        dbc.Col([
                            html.H5("Responsible for the project:", style={"color": "silver"}),

                            html.P(html.B("Prof. Dr. Jörg Müller-Litzkow", style={"color": "silver", "marginTop": "5px"})),
                            html.P("President of HafenCity University Hamburg (HCU) and University Professor for Economics and Digitalization",
                                style={"line-height": "110%", "color": "silver", "marginTop": "-18px"}),
                            html.P(
                                html.A("praesident@vw.hcu-hamburg.de", href="mailto: praesident@vw.hcu-hamburg.de", style={"color": "silver"}),
                                style={"color": "silver", "marginTop": "-18px"}
                            ),

                            html.P(html.B("Prof. Dr. Harald Sternberg", style={"color": "silver", "marginTop": "-12px"})),
                            html.P("""Vice President for Teaching and Digitalization of HafenCity University Hamburg (HCU)
                                and University Professor for Hydrography and Engineering Geodesy""",
                                style={"line-height": "110%", "color": "silver", "marginTop": "-18px"}),
                            html.P(
                                html.A("harald.sternberg@hcu-hamburg.de", href="mailto: harald.sternberg@hcu-hamburg.de", style={"color": "silver"}),
                                style={"color": "silver", "marginTop": "-18px"}
                            ),

                            html.P(html.B("Nils Hellweg", style={"color": "silver", "marginTop": "-12px"})),
                            html.P("""Project Manager and PhD Student at HafenCity University Hamburg (HCU)""",
                                style={"line-height": "110%", "color": "silver", "marginTop": "-18px"}),
                            html.P(
                                html.A("nils.hellweg@hcu-hamburg.de", href="mailto: nils.hellweg@hcu-hamburg.de", style={"color": "silver"}),
                                style={"color": "silver", "marginTop": "-18px"}
                            ),
                        ], width=3),
                        dbc.Col([
                            html.H5("Positioning contact persons:", style={"color": "silver"}),

                            html.P(html.B("Hossein Shoushtari", style={"color": "silver", "marginTop": "5px"})),
                            html.P("Research assistant and PhD Student at HafenCity University Hamburg (HCU)",
                                style={"line-height": "110%", "color": "silver", "marginTop": "-18px"}),
                            html.P(
                                html.A("hossein.shoushtari@hcu-hamburg.de", href="mailto: hossein.shoushtari@hcu-hamburg.de", style={"color": "silver"}),
                                style={"color": "silver", "marginTop": "-18px"}
                            ),

                            html.P(html.B("Dorian Harder", style={"color": "silver", "marginTop": "-12px"})),
                            html.P("Research assistant at HafenCity University Hamburg (HCU)",
                                style={"line-height": "110%", "color": "silver", "marginTop": "-18px"}),
                            html.P(
                                html.A("dorian.harder@hcu-hamburg.de", href="mailto: dorian.harder@hcu-hamburg.de", style={"color": "silver"}),
                                style={"color": "silver", "marginTop": "-18px"}
                            ),

                            html.P(html.B("Georg Fjodorow", style={"color": "silver", "marginTop": "-12px"})),
                            html.P("Master Student at HafenCity University Hamburg (HCU)",
                                style={"line-height": "110%", "color": "silver", "marginTop": "-18px"}),
                            html.P(
                                html.A("georg.fjodorow@hcu-hamburg.de", href="mailto: georg.fjodorow@hcu-hamburg.de", style={"color": "silver"}),
                                style={"color": "silver", "marginTop": "-18px"}
                            ),
                                
                            html.P(html.B("Korvin Venzke", style={"color": "silver", "marginTop": "-12px"})),
                            html.P("Bachelor Student at HafenCity University Hamburg (HCU)",
                                style={"line-height": "110%", "color": "silver", "marginTop": "-18px"}),
                            html.P(
                                html.A("korvin.venzke@hcu-hamburg.de", href="mailto: korvin.venzke@hcu-hamburg.de", style={"color": "silver"}),
                                style={"color": "silver", "marginTop": "-18px"}
                            ),
                        ], width=3)
                    ], justify="center")
            ]),
        dbc.CardFooter(f"Copyright © {datetime.date.today().strftime('%Y')} Level 5 Indoor Navigation. All Rights Reserved", style={"textAlign": "center"})
    ])