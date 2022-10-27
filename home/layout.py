##### Home Tab -- Layout
###IMPORTS
# dash
from dash import html, dcc, Dash, Output, Input, State, no_update
import dash_bootstrap_components as dbc
# built in
import datetime
import os

def tooltips():
    # tooltips for more information
    tooltips = html.Div([
        dbc.Tooltip("open PDF", target="2022_9_5_IPIN2022_pdf_btn",      placement="left"),
        dbc.Tooltip("open PDF", target="2022_4_25_sensors_pdf_btn",      placement="left"),
        dbc.Tooltip("open PDF", target="2021_4_1_mobility_pdf_btn",      placement="left"),
        dbc.Tooltip("open PDF", target="2021_2_9_remotesensing_pdf_btn", placement="left"),
        dbc.Tooltip("open PDF", target="2021_2_5_electronics_pdf_btn",   placement="left"),
    ])
    return tooltips

def header():
    header = html.Div([
        html.H2(["L5IN", html.Sup("+"), ": Level 5 Indoor Navigation"], style={"color": "white", "text-align": "center"}),
        html.Br(),
        # html.Div(html.Iframe(
        #     src="https://www.youtube.com/embed/w7jk_1mhPY0",
        #     width="842",
        #     height="475" 
        # ), style={"textAlign": "center"}),
    ])
    return header

def about():
    about = html.Div([
        html.Div(
            html.H4("About this website",
                style={
                    "display": "inline-block",
                    "font-variant": "small-caps",
                    "color": "white",
                    "text-align": "center",
                    "padding-bottom": "5px",
                    "border-bottom": "3px solid silver"
                }),
        style={"text-align": "center"}
        ),
        html.Div(
            html.P("""This is a tool developed by Level 5 Indoor Navigation (L5IN) project with positioning focus.
                The L5IN project deals with real-time navigation inside buildings, using 5G and smartphone sensors.
                The project demonstrates the feasibility of the transition from outdoor to indoor environment in
                terms of navigation. The aim of the L5IN project is to use newly introduced 5G technology to demonstrate,
                based on a research-oriented model project, how indoor navigation systems can function. Such systems
                were previously only known in the outdoor segment (through GNSS) but can now also be integrated into
                existing smartphone systems and 5G as a ubiquitous alternative for the GNSS solutions in the context
                of indoor navigation.""",
                style={"color": "silver", "font-size": "16px", "padding-left": "10px", "padding-right": "10px"}),
            style={"width": "90%", "margin": "auto"}
        ),
        html.Div(
            html.P("""The positioning work package is one of the L5IN research areas. Autonomous pedestrian localization would make
                the navigation possible at any time. The positioning team uses the benefits of interdisciplinary technologies developed
                at L5IN and focuses on the approaches and methods such as Monte Carlo Simulation, state estimation filters, machine learning,
                deep learning and 5G positioning to develop a practice-oriented solution.""",
                style={"color": "silver", "width": "100%", "font-size": "16px", "padding-left": "10px", "padding-right": "10px"}),
            style={"width": "90%", "margin": "auto"}
        ),
    ])
    return about

def publications():
    papers_list = ["2022_9_5_IPIN2022", "2022_4_25_sensors", "2021_4_1_mobility", "2021_2_9_remotesensing", "2021_2_5_electronics"]
    publications = html.Div([
        html.Div(
            html.H4("Publications",
                style={
                    "display": "inline-block",
                    "font-variant": "small-caps",
                    "color": "white",
                    "text-align": "center",
                    "padding-bottom": "5px",
                    "margin-bottom": "10px",
                    "border-bottom": "3px solid silver"
                }),
            style={"text-align": "center"}),
        dbc.Row(
            [
                # slide show
                dbc.Col([
                    dbc.Carousel(
                        items=list(reversed([
                            {
                                "src": f"assets/images/papers/{paper}.png"
                            } 
                            for paper in papers_list
                        ])),
                        variant="dark",
                        style={"width": "500px", "margin-left": "2px"},
                        id="paper_carousel"
                    )
                ], width=2, style={"width": "506px", "margin-top": "5px", "margin-bottom": "11px", "padding-left": "0px"}),
                # papers
                dbc.Col([
                    dbc.Alert(
                        [
                            html.Div(
                                html.A(
                                    target="_blank",
                                    href="https://www.researchgate.net/publication/362134877_L5IN_From_an_Analytical_Platform_to_Optimization_of_Deep_Inertial_Odometry",
                                    children=html.Button(
                                        html.Img(
                                            src="assets/images/signs/pdf_sign2.svg",
                                            id="2022_9_5_IPIN2022_pdf_sign",
                                            style={"margin-left": "-8px"}),
                                        id="2022_9_5_IPIN2022_pdf_btn",
                                        style={"margin-left": "8px", "width": "44px", "background": "transparent", "border": "0px"})
                                ),
                                style={"width": "44px"}
                            ),
                            html.Button(
                                [
                                    html.P(html.B(["L5IN", html.Sup("+"), ": From an Analytical Platform to Optimization of Deep Inertial Odometry (2022)"])),
                                    html.P("Hossein Shoushtari, Firas Kassawat, Dorian Harder, Korvin Venzke, Jörg Müller-Lietzkow, Harald Sternberg", style={"line-height": "120%"})
                                ],
                                id="2022_9_5_IPIN2022_show_btn",
                                style={"margin-left": "8px", "border": "0px", "background": "transparent", "height": "110px", "color": "white", "text-align": "left", "padding": "0px"}
                            ),
                        ],
                        id="2022_9_5_IPIN2022_paper",
                        className="d-flex align-items-center",
                        style={"padding": "0px", "color": "white", "height": "110px", "width": "500px", "background-color": "#737373", "border-left": "4px solid white", "border-radius": 0, "margin-left": "-10px"}
                    ),
                    dbc.Alert(
                        [
                            html.Div(
                                html.A(
                                    target="_blank",
                                    href="https://www.mdpi.com/1424-8220/22/9/3289",
                                    children=html.Button(
                                        html.Img(
                                            src="assets/images/signs/pdf_sign1.svg",
                                            id="2022_4_25_sensors_pdf_sign",
                                            style={"margin-left": "-8px"}),
                                        id="2022_4_25_sensors_pdf_btn",
                                        style={"margin-left": "8px", "width": "44px", "background": "transparent", "border": "0px"})
                                ),
                                style={"width": "44px"}
                            ),
                            html.Button(
                                [
                                    html.P(html.B("Real-Time Map Matching with a Backtracking Particle Filter Using Geospatial Analysis (2022)")),
                                    html.P("Dorian Harder, Hossein Shoushtari, Harald Sternberg", style={"line-height": "120%"})
                                ],
                                id="2022_4_25_sensors_show_btn",
                                style={"margin-left": "8px", "border": "0px", "background": "transparent", "height": "110px", "color": "silver", "text-align": "left", "padding": "0px"}
                            ),
                        ],
                        id="2022_4_25_sensors_paper",
                        className="d-flex align-items-center",
                        style={"padding": "0px", "color": "silver", "height": "110px", "width": "500px", "background-color": "#545454", "border-left": "4px solid silver", "border-radius": 0, "margin-left": "-10px"}
                    ),
                    dbc.Alert(
                        [
                            html.Div(
                                html.A(
                                    target="_blank",
                                    href="https://www.researchgate.net/publication/351234064_A_Conceptual_Digital_Twin_for_5G_Indoor_Navigation", 
                                    children=html.Button(
                                        html.Img(
                                            src="assets/images/signs/pdf_sign1.svg",
                                            id="2021_4_1_mobility_pdf_sign",
                                            style={"margin-left": "-8px"}),
                                        id="2021_4_1_mobility_pdf_btn",
                                        style={"margin-left": "8px", "width": "44px", "background": "transparent", "border": "0px"})
                                ),
                                style={"width": "44px"}
                            ),
                            html.Button(
                                [
                                    html.P(html.B("A Conceptual Digital Twin for 5G Indoor Navigation (2021)")),
                                    html.P("Vladeta Stojanovic, Hossein Shoushtari, Cigdem Askar, Annette Scheider, Caroline Schuldt, Nils Hellweg, Harald Sternberg", style={"line-height": "120%"})
                                ],
                                id="2021_4_1_mobility_show_btn",
                                style={"margin-left": "8px", "border": "0px", "background": "transparent", "height": "110px", "color": "silver", "text-align": "left", "padding": "0px"}
                            ),
                        ],
                        id="2021_4_1_mobility_paper",
                        className="d-flex align-items-center",
                        style={"padding": "0px", "color": "silver", "height": "110px", "width": "500px", "background-color": "#545454", "border-left": "4px solid silver", "border-radius": 0, "margin-left": "-10px"}
                    ),
                    dbc.Alert(
                        [
                            html.Div(
                                html.A(
                                    target="_blank",
                                    href="https://www.mdpi.com/2072-4292/13/4/624",
                                    children=html.Button(
                                        html.Img(
                                            src="assets/images/signs/pdf_sign1.svg",
                                            id="2021_2_9_remotesensing_pdf_sign",
                                            style={"margin-left": "-8px"}),
                                        id="2021_2_9_remotesensing_pdf_btn",
                                        style={"margin-left": "8px", "width": "44px", "background": "transparent", "border": "0px"})
                                ),
                                style={"width": "44px"}
                            ),
                            html.Button(
                                [
                                    html.P(html.B("L5IN: Overview of an Indoor Navigation Pilot Project (2021)")),
                                    html.P("Caroline Schuldt, Hossein Shoushtari, Nils Hellweg, Harald Sternberg", style={"line-height": "120%"})
                                ],
                                id="2021_2_9_remotesensing_show_btn",
                                style={"margin-left": "8px", "border": "0px", "background": "transparent", "height": "110px", "color": "silver", "text-align": "left", "padding": "0px"}
                            ),
                        ],
                        id="2021_2_9_remotesensing_paper",
                        className="d-flex align-items-center",
                        style={"padding": "0px", "color": "silver", "height": "110px", "width": "500px", "background-color": "#545454", "border-left": "4px solid silver", "border-radius": 0, "margin-left": "-10px"}
                    ),
                    dbc.Alert(
                        [
                            html.Div(
                                html.A(
                                    target="_blank",
                                    href="https://www.mdpi.com/2079-9292/10/4/397",
                                    children=html.Button(
                                        html.Img(
                                            src="assets/images/signs/pdf_sign1.svg",
                                            id="2021_2_5_electronics_pdf_sign",
                                            style={"margin-left": "-8px"}),
                                        id="2021_2_5_electronics_pdf_btn",
                                        style={"margin-left": "8px", "width": "44px", "background": "transparent", "border": "0px"})
                                ),
                                style={"width": "44px"}
                            ),
                            html.Button(
                                [
                                    html.P(html.B("Many Ways Lead to the Goal — Possibilities of Autonomous and Infrastructure-Based Indoor Positioning (2021)")),
                                    html.P("Hossein Shoushtari, Thomas Willemsen, Harald Sternberg", style={"line-height": "120%"})
                                ],
                                id="2021_2_5_electronics_show_btn",
                                style={"margin-left": "8px", "border": "0px", "background": "transparent", "height": "110px", "color": "silver", "text-align": "left", "padding": "0px"}
                            ),
                        ],
                        id="2021_2_5_electronics_paper",
                        className="d-flex align-items-center",
                        style={"padding": "0px", "color": "silver", "height": "110px", "width": "500px", "background-color": "#545454", "border-left": "4px solid silver", "border-radius": 0, "margin-left": "-10px"}
                    )
                ], width=2, style={"width": "506px", "margin-top": "5px", "margin-bottom": "11px"})
            ], justify="center"
        ),
    ])
    return publications

def contact():
    contact = html.Div([
        html.Div(
            html.H4("Contact",
                style={
                    "display": "inline-block",
                    "font-variant": "small-caps",
                    "color": "white",
                    "text-align": "center",
                    "padding-bottom": "5px",
                    "border-bottom": "3px solid silver"
                }),
            style={"text-align": "center"}
        ),
        html.H5("Responsible for the project", style={"color": "silver", "text-align": "center"}),
        dbc.Row(
            [
                dbc.Col([
                    html.P(html.B("Prof. Dr. Jörg Müller-Litzkow", style={"color": "silver", "margin-top": "5px"})),
                    html.P("President of HafenCity University Hamburg (HCU) and University Professor for Economics and Digitization",
                        style={"line-height": "110%", "color": "silver", "margin-top": "-18px"}),
                    html.P(
                        html.A("praesident@vw.hcu-hamburg.de", href="mailto: praesident@vw.hcu-hamburg.de", style={"color": "silver"}),
                        style={"color": "silver", "margin-top": "-18px"}
                    )
                ], width=3, style={"height": "136px", "width": "337px"}),
                dbc.Col([
                    html.P(html.B("Prof. Dr. Harald Sternberg", style={"color": "silver", "margin-top": "-12px"})),
                    html.P("""Vice President for Teaching and Digitization of HafenCity University Hamburg (HCU)
                        and University Professor for Hydrography and Engineering Geodesy""",
                        style={"line-height": "110%", "color": "silver", "margin-top": "-18px"}),
                    html.P(
                        html.A("harald.sternberg@hcu-hamburg.de", href="mailto: harald.sternberg@hcu-hamburg.de", style={"color": "silver"}),
                        style={"color": "silver", "margin-top": "-18px"}
                    )
                ], width=3, style={"height": "136px", "width": "337px"}),
                dbc.Col([
                    html.P(html.B("Nils Hellweg", style={"color": "silver", "margin-top": "-12px"})),
                    html.P("""Project Manager and PhD Student at HafenCity University Hamburg (HCU)""",
                        style={"line-height": "110%", "color": "silver", "margin-top": "-18px"}),
                    html.P(
                        html.A("nils.hellweg@hcu-hamburg.de", href="mailto: nils.hellweg@hcu-hamburg.de", style={"color": "silver"}),
                        style={"color": "silver", "margin-top": "-18px"}
                    )
                ], width=3, style={"height": "136px", "width": "337px"})
            ], justify="center"
        ),
        html.H5("Positioning contact persons", style={"color": "silver", "text-align": "center"}),
        dbc.Row(
            [
                dbc.Col([
                    html.P(html.B("Hossein Shoushtari", style={"color": "silver", "margin-top": "5px"})),
                    html.P("Research assistant and PhD Student at HafenCity University Hamburg (HCU)",
                        style={"line-height": "110%", "color": "silver", "margin-top": "-18px"}),
                    html.P(
                        html.A("hossein.shoushtari@hcu-hamburg.de", href="mailto: hossein.shoushtari@hcu-hamburg.de", style={"color": "silver"}),
                        style={"color": "silver", "margin-top": "-18px"}
                    )
                ], width=3, style={"height": "101px", "width": "337px"}),
                dbc.Col([
                    html.P(html.B("Dorian Harder", style={"color": "silver", "margin-top": "-12px"})),
                    html.P("Research assistant at HafenCity University Hamburg (HCU)",
                        style={"line-height": "110%", "color": "silver", "margin-top": "-18px"}),
                    html.P(
                        html.A("dorian.harder@hcu-hamburg.de", href="mailto: dorian.harder@hcu-hamburg.de", style={"color": "silver"}),
                        style={"color": "silver", "margin-top": "-18px"}
                    )
                ], width=3, style={"height": "101px", "width": "337px"})
            ], justify="center"
        ),
        dbc.Row(
            [
                dbc.Col([
                    html.P(html.B("Georg Fjodorow", style={"color": "silver", "margin-top": "-12px"})),
                    html.P("Master Student at HafenCity University Hamburg (HCU)",
                        style={"line-height": "110%", "color": "silver", "margin-top": "-18px"}),
                    html.P(
                        html.A("georg.fjodorow@hcu-hamburg.de", href="mailto: georg.fjodorow@hcu-hamburg.de", style={"color": "silver"}),
                        style={"color": "silver", "margin-top": "-18px"}
                    )
                ], width=3, style={"height": "101px", "width": "337px"}),
                dbc.Col([  
                    html.P(html.B("Korvin Venzke", style={"color": "silver", "margin-top": "-12px"})),
                    html.P("Bachelor Student at HafenCity University Hamburg (HCU)",
                        style={"line-height": "110%", "color": "silver", "margin-top": "-18px"}),
                    html.P(
                        html.A("korvin.venzke@hcu-hamburg.de", href="mailto: korvin.venzke@hcu-hamburg.de", style={"color": "silver"}),
                        style={"color": "silver", "margin-top": "-18px"}
                    ),
                ], width=3, style={"height": "101px", "width": "337px"})
            ], justify="center"
        )
    ])
    return contact

def home_layout():
    return dbc.Card([
        dbc.CardBody(
            [
                tooltips(),
                html.Br(),
                header(),
                html.Br(),
                about(),
                html.Br(),
                publications(),
                html.Br(),
                contact()
            ]
        ),
        dbc.CardFooter(f"Copyright © {datetime.date.today().strftime('%Y')} Level 5 Indoor Navigation. All Rights Reserved", style={"textAlign": "center"})
    ])