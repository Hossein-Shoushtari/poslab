##### Layout Home
###IMPORTS
# dash
from dash import html, dcc, Dash, Output, Input, State, no_update
import dash_bootstrap_components as dbc
# built in
import datetime
import os

class CopyBibtexText():
    def __init__(self):
        pass

    def copy_IVK_2023(self):
        return '''@article{IVK2023,
      title={Optimierte Trajektorie aus Smartphone-Sensoren und 5G UL-TDoA mit Cluster-Partikel-Filter},
      author={Shoushtari, Hossein and Harder, Dorian and Willemsen, Thomas and Sternberg, Harald},
      booktitle={Beiträge zum 20. Internationalen Ingenieurvermessungskurs - Zürich, 2023},
      pages={291 - 304},
      year={2023},
      publisher={Herbert Wichmann Verlag},
      address={Berlin}
    }'''
    def copy_ION_2023(self):
        return '''@article{ION2023,
      title={Data-Driven Inertial Navigation assisted by 5G UL-TDoA Positioning},
      author={Shoushtari, Hossein and Harder, Dorian and Kasparek, Maximilian and  Schäfer, Matthias and M{\"u}ller-Lietzkow, J{\"o}rg and Sternberg, Harald},
      booktitle={Proceedings of the 2023 International Technical Meeting of The Institute of Navigation}
      pages={1169 - 1183},
      year={2023},
    }'''
    def copy_2022_9_5_IPIN2022(self):
        return'''@article{shoushtari2022l5in+,
      title={L5IN+: From an Analytical Platform to Optimization of Deep Inertial Odometry},
      author={Shoushtari, Hossein and Kassawat, Firas and Harder, Dorian and Venzke, Korvin and M{\"u}ller-Lietzkow, J{\"o}rg and Sternberg, Harald},
      year={2022}
    }'''
    def copy_2022_4_25_sensors(self):
        return'''@article{harder2022real,
      title={Real-Time Map Matching with a Backtracking Particle Filter Using Geospatial Analysis},
      author={Harder, Dorian and Shoushtari, Hossein and Sternberg, Harald},
      journal={Sensors},
      volume={22},
      number={9},
      pages={3289},
      year={2022},
      publisher={MDPI}
    }'''
    def copy_2021_11_29_IPIN2021(self):
        return'''@inproceedings{shoushtari20213d,
      title={3D Indoor Localization using 5G-based Particle Filtering and CAD Plans},
      author={Shoushtari, Hossein and Askar, Cigdem and Harder, Dorian and Willemsen, Thomas and Sternberg, Harald},
      booktitle={2021 International Conference on Indoor Positioning and Indoor Navigation (IPIN)},
      pages={1--8},
      year={2021},
      organization={IEEE}
    }'''
    def copy_2021_2_5_electronics(self):
        return'''@article{shoushtari2021many,
      title={Many ways lead to the goal—Possibilities of autonomous and infrastructure-based indoor positioning},
      author={Shoushtari, Hossein and Willemsen, Thomas and Sternberg, Harald},
      journal={Electronics},
      volume={10},
      number={4},
      pages={397},
      year={2021},
      publisher={MDPI}
    }'''
    def copy_2023_DGON_ISS(self):
        return'''@article{shoushtari2023dgon,
      title={Supervised Learning Regression for Sensor Calibration},
      author={Shoushtari, Hossein and Willemsen, Thomas and Sternberg, Harald},
      year={2023},
      publisher={IEEE Xplore},
      address={Braunschweig}
    }'''


def modals():
    bibtex_text = CopyBibtexText()
    modals = html.Div([
        dbc.Modal(
            dbc.ModalHeader(
                html.Div(
                    [
                        html.P("@article{dgon2023,", style={"color": "silver", "margin-bottom": "0px"}),
                        html.P(
                            "      title={Supervised Learning Regression for Sensor Calibration},",
                            style={"color": "silver", "margin-bottom": "0px", "text-indent": "15px"}),
                        html.P(
                            "author={Shoushtari, Hossein and Willemsen, Thomas and Sternberg, Harald},",
                            style={"color": "silver", "margin-bottom": "0px", "text-indent": "15px"}),
                        html.P("year={2023}", style={"color": "silver", "margin-bottom": "0px", "text-indent": "15px"}),
                        html.P("}", style={"color": "silver", "margin-bottom": "0px"}),
                        dcc.Clipboard(
                            content=bibtex_text.copy_2023_DGON_ISS(),
                            style={
                                "color": "#9B9B9B",
                                "position": "absolute",
                                "top": 11,
                                "right": 16,
                                "fontSize": 20,
                            },
                        ),
                    ], style={"padding": "0px", "height": "90%", "width": "95%", "margin": "auto"}
                ),
                style={"padding-left": "14px", "background": "#585858", "border-radius": 5,
                       "border": "1px solid silver"}
            ),
            id="DGON2023_bibtex_modal",
            size="xl",
            is_open=False,
            backdrop="static"
        ),
        dbc.Modal(
            dbc.ModalHeader(
                html.Div(
                    [
                        html.P("@article{IVK2023,", style={"color": "silver", "margin-bottom": "0px"}),
                        html.P("      title={Optimierte Trajektorie aus Smartphone-Sensoren und 5G UL-TDoA mit Cluster-Partikel-Filter}," ,style={"color": "silver", "margin-bottom": "0px", "text-indent": "15px"}),
                        html.P( "author={Shoushtari, Hossein and Harder, Dorian and Willemsen, Thomas and Sternberg, Harald},",
                            style={"color": "silver", "margin-bottom": "0px", "text-indent": "15px"}),
                        html.P("year={2023}", style={"color": "silver", "margin-bottom": "0px", "text-indent": "15px"}),
                        html.P("}", style={"color": "silver", "margin-bottom": "0px"}),
                        dcc.Clipboard(
                            content=bibtex_text.copy_IVK_2023(),
                            style={
                                "color": "#9B9B9B",
                                "position": "absolute",
                                "top": 11,
                                "right": 16,
                                "fontSize": 20,
                            },
                        ),
                    ], style={"padding": "0px", "height": "90%", "width": "95%", "margin": "auto"}
                ),
                style={"padding-left": "14px", "background": "#585858", "border-radius": 5,
                       "border": "1px solid silver"}
            ),
            id="IVK2023_bibtex_modal",
            size="xl",
            is_open=False,
            backdrop="static"
        ),
        dbc.Modal(
            dbc.ModalHeader(
                html.Div(
                    [
                        html.P("@article{ION2023,", style={"color": "silver", "margin-bottom": "0px"}),
                        html.P("      title={Data-Driven Inertial Navigation assisted by 5G UL-TDoA Positioning}," ,style={"color": "silver", "margin-bottom": "0px", "text-indent": "15px"}),
                        html.P( "author={Shoushtari, Hossein and Harder, Dorian and Kasparek, Maximilian and  Schäfer, Matthias and M{\"u}ller-Lietzkow, J{\"o}rg and Sternberg, Harald},",
                            style={"color": "silver", "margin-bottom": "0px", "text-indent": "15px"}),
                        html.P("year={2023}", style={"color": "silver", "margin-bottom": "0px", "text-indent": "15px"}),
                        html.P("}", style={"color": "silver", "margin-bottom": "0px"}),
                        dcc.Clipboard(
                            content=bibtex_text.copy_ION_2023(),
                            style={
                                "color": "#9B9B9B",
                                "position": "absolute",
                                "top": 11,
                                "right": 16,
                                "fontSize": 20,
                            },
                        ),
                    ], style={"padding": "0px", "height": "90%", "width": "95%", "margin": "auto"}
                ),
                style={"padding-left": "14px", "background": "#585858", "border-radius": 5,
                       "border": "1px solid silver"}
            ),
            id="ION2023_bibtex_modal",
            size="xl",
            is_open=False,
            backdrop="static"
        ),
        dbc.Modal(
            dbc.ModalHeader(
                html.Div(
                    [
                        html.P("@article{shoushtari2022l5in+,", style={"color": "silver", "margin-bottom": "0px"}),
                        html.P("title={L5IN+: From an Analytical Platform to Optimization of Deep Inertial Odometry},", style={"color": "silver", "margin-bottom": "0px", "text-indent": "15px"}),
                        html.P("author={Shoushtari, Hossein and Kassawat, Firas and Harder, Dorian and Venzke, Korvin and M{\"u}ller-Lietzkow, J{\"o}rg and Sternberg, Harald},", style={"color": "silver", "margin-bottom": "0px", "text-indent": "15px"}),
                        html.P("year={2022}", style={"color": "silver", "margin-bottom": "0px", "text-indent": "15px"}),
                        html.P("}", style={"color": "silver", "margin-bottom": "0px"}),
                        dcc.Clipboard(
                            content=bibtex_text.copy_2022_9_5_IPIN2022(),
                            style={
                                "color": "#9B9B9B",
                                "position": "absolute",
                                "top": 11,
                                "right": 16,
                                "fontSize": 20,
                            },
                        ),
                    ], style={"padding": "0px", "height": "90%", "width": "95%", "margin": "auto"}
                ),
                style={"padding-left": "14px", "background": "#585858", "border-radius": 5, "border": "1px solid silver"}
            ),
            id="2022_9_5_IPIN2022_bibtex_modal",
            size="xl",
            is_open=False,
            backdrop="static"
        ),
        dbc.Modal(
            dbc.ModalHeader(
                html.Div(
                    [
                        html.P("@article{harder2022real,", style={"color": "silver", "margin-bottom": "0px"}),
                        html.P("title={Real-Time Map Matching with a Backtracking Particle Filter Using Geospatial Analysis},", style={"color": "silver", "margin-bottom": "0px", "text-indent": "15px"}),
                        html.P("author={Harder, Dorian and Shoushtari, Hossein and Sternberg, Harald},", style={"color": "silver", "margin-bottom": "0px", "text-indent": "15px"}),
                        html.P("journal={Sensors},", style={"color": "silver", "margin-bottom": "0px", "text-indent": "15px"}),
                        html.P("volume={22},", style={"color": "silver", "margin-bottom": "0px", "text-indent": "15px"}),
                        html.P("number={9},", style={"color": "silver", "margin-bottom": "0px", "text-indent": "15px"}),
                        html.P("pages={3289},", style={"color": "silver", "margin-bottom": "0px", "text-indent": "15px"}),
                        html.P("year={2022},", style={"color": "silver", "margin-bottom": "0px", "text-indent": "15px"}),
                        html.P("publisher={MDPI}", style={"color": "silver", "margin-bottom": "0px", "text-indent": "15px"}),
                        html.P("}", style={"color": "silver", "margin-bottom": "0px"}),
                        dcc.Clipboard(
                            content=bibtex_text.copy_2022_4_25_sensors(),
                            style={
                                "color": "#9B9B9B",
                                "position": "absolute",
                                "top": 11,
                                "right": 16,
                                "fontSize": 20,
                            },
                        ),
                    ], style={"padding": "0px", "height": "90%", "width": "95%", "margin": "auto"}
                ),
                style={"padding-left": "14px", "background": "#585858", "border-radius": 5, "border": "1px solid silver"}
            ),
            id="2022_4_25_sensors_bibtex_modal",
            size="xl",
            is_open=False,
            backdrop="static"
        ),
        dbc.Modal(
            dbc.ModalHeader(
                html.Div(
                    [
                        html.P("@inproceedings{shoushtari20213d,", style={"color": "silver", "margin-bottom": "0px"}),
                        html.P("title={3D Indoor Localization using 5G-based Particle Filtering and CAD Plans},", style={"color": "silver", "margin-bottom": "0px", "text-indent": "15px"}),
                        html.P("author={Shoushtari, Hossein and Askar, Cigdem and Harder, Dorian and Willemsen, Thomas and Sternberg, Harald},", style={"color": "silver", "margin-bottom": "0px", "text-indent": "15px"}),
                        html.P("booktitle={2021 International Conference on Indoor Positioning and Indoor Navigation (IPIN)},", style={"color": "silver", "margin-bottom": "0px", "text-indent": "15px"}),
                        html.P("pages={1--8},", style={"color": "silver", "margin-bottom": "0px", "text-indent": "15px"}),
                        html.P("year={2021},", style={"color": "silver", "margin-bottom": "0px", "text-indent": "15px"}),
                        html.P("organization={IEEE}", style={"color": "silver", "margin-bottom": "0px", "text-indent": "15px"}),
                        html.P("}", style={"color": "silver", "margin-bottom": "0px"}),
                        dcc.Clipboard(
                            content=bibtex_text.copy_2021_11_29_IPIN2021(),
                            style={
                                "color": "#9B9B9B",
                                "position": "absolute",
                                "top": 11,
                                "right": 16,
                                "fontSize": 20,
                            },
                        ),
                    ], style={"padding": "0px", "height": "90%", "width": "95%", "margin": "auto"}
                ),
                style={"padding-left": "14px", "background": "#585858", "border-radius": 5, "border": "1px solid silver"}
            ),
            id="2021_11_29_IPIN2021_bibtex_modal",
            size="xl",
            is_open=False,
            backdrop="static"
        ),
        dbc.Modal(
            dbc.ModalHeader(
                html.Div(
                    [
                        html.P("@article{shoushtari2021many,", style={"color": "silver", "margin-bottom": "0px"}),
                        html.P("title={Many ways lead to the goal—Possibilities of autonomous and infrastructure-based indoor positioning},", style={"color": "silver", "margin-bottom": "0px", "text-indent": "15px"}),
                        html.P("author={Shoushtari, Hossein and Willemsen, Thomas and Sternberg, Harald},", style={"color": "silver", "margin-bottom": "0px", "text-indent": "15px"}),
                        html.P("journal={Electronics},", style={"color": "silver", "margin-bottom": "0px", "text-indent": "15px"}),
                        html.P("volume={10},", style={"color": "silver", "margin-bottom": "0px", "text-indent": "15px"}),
                        html.P("number={4},", style={"color": "silver", "margin-bottom": "0px", "text-indent": "15px"}),
                        html.P("pages={397},", style={"color": "silver", "margin-bottom": "0px", "text-indent": "15px"}),
                        html.P("year={2021},", style={"color": "silver", "margin-bottom": "0px", "text-indent": "15px"}),
                        html.P("publisher={MDPI}", style={"color": "silver", "margin-bottom": "0px", "text-indent": "15px"}),
                        html.P("}", style={"color": "silver", "margin-bottom": "0px"}),
                        dcc.Clipboard(
                            content=bibtex_text.copy_2021_2_5_electronics(),
                            style={
                                "color": "#9B9B9B",
                                "position": "absolute",
                                "top": 11,
                                "right": 16,
                                "fontSize": 20,
                            },
                        ),
                    ], style={"padding": "0px", "height": "90%", "width": "95%", "margin": "auto"}
                ),
                style={"padding-left": "14px", "background": "#585858", "border-radius": 5, "border": "1px solid silver"}
            ),
            id="2021_2_5_electronics_bibtex_modal",
            size="xl",
            is_open=False,
            backdrop="static"
        )
    ])
    return modals
    

def header():
    header = html.Div([
        html.H2(["L5IN", html.Sup("+"), ": Level 5 Indoor-Navigation Plus"], style={"color": "white", "text-align": "center"}),
        html.Br(),
        html.Div(html.Iframe(
            src="https://www.youtube.com/embed/soP7hb5o_D8",
            width="900px",
            height="508px",
            style={"border-radius": "10px"}
        ), style={"textAlign": "center"}),
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
            html.P("""This is a tool developed by Level 5 Indoor-Navigation (L5IN) project with positioning focus.
                The L5IN project deals with real-time navigation inside buildings, using 5G and smartphone sensors.
                The project demonstrates the feasibility of the transition from outdoor to indoor environment in
                terms of navigation. The aim of the L5IN project is to use newly introduced 5G technology to demonstrate,
                based on a research-oriented model project, how indoor navigation systems can function. Such systems
                were previously only known in the outdoor segment (through GNSS) but can now also be integrated into
                existing smartphone systems and 5G as a ubiquitous alternative for the GNSS solutions in the context
                of indoor navigation.""",
                style={"color": "silver", "font-size": "18px", "padding-left": "10px", "padding-right": "10px"}),
            style={"width": "80%", "margin": "auto"}
        ),
        html.Div(
            html.P("""The positioning work package is one of the L5IN research areas. Autonomous pedestrian localization would make
                the navigation possible at any time. The positioning team uses the benefits of interdisciplinary technologies developed
                at L5IN and focuses on the approaches and methods such as Monte Carlo Simulation, state estimation filters, machine learning,
                deep learning and 5G positioning to develop a practice-oriented solution.""",
                style={"color": "silver", "width": "100%", "font-size": "18px", "padding-left": "10px", "padding-right": "10px"}),
            style={"width": "80%", "margin": "auto"}
        ),
        html.Br(),
        html.Div(
            html.Img(
                src="assets/images/L5INp_Workflow.png",
                style={"width": "850px"}),
            style={"textAlign": "center"}
        ),
    ])
    return about

def publications():
    papers_list = ["DGON2023","IVK2023", "ION2023", "2022_9_5_IPIN2022", "2022_4_25_sensors", "2021_11_29_IPIN2021", "2021_2_5_electronics"]
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
                        items=[
                            {
                                "src": f"assets/images/papers/{paper}.jpg"
                            } 
                            for paper in papers_list
                        ],
                        variant="dark",
                        style={"width": "500px", "margin-left": "2px"},
                        id="paper_carousel"
                    )
                ], width=2, style={"width": "506px", "margin-top": "5px", "margin-bottom": "11px", "padding-left": "0px"}),
                # papers
                dbc.Col([
                    html.Div([
                        html.Div(
                            html.Div(
                                html.Button(html.Div(
                                    [
                                        html.P(html.B([
                                                          "Supervised Learning Regression for Sensor Calibration (2023)"]),
                                               style={"margin-bottom": "7px"}),
                                        html.P(
                                            "Hossein Shoushtari, Thomas Willemsen, Harald Sternberg",
                                            style={"line-height": "120%", "margin-bottom": "0px"}),
                                        html.P(
                                            [
                                                html.P("|", style={"display": "inline-block"}),
                                                html.Button(
                                                    "bibtex",
                                                    id="DGON2023_bibtex_btn",
                                                    style={"background": "transparent", "border": "0px",
                                                           "text-decoration": "underline", "color": "#00BC8C",
                                                           "padding": "0px", "width": "50px", "margin-left": "-1px",
                                                           "margin-right": "-1px"}
                                                ),
                                                html.P("|", style={"display": "inline-block"}),
                                                html.A(
                                                    "code",
                                                    target="_blank",
                                                    href="https://github.com/Hossein-Shoushtari/ISSDGON2023",
                                                    style={"display": "inline-block", "margin-left": "2px",
                                                           "margin-right": "2px"}),
                                                html.P("|", style={"display": "inline-block"}),
                                                html.A(
                                                    "arxiv",
                                                    target="_blank",
                                                    href="https://ieeexplore.ieee.org/abstract/document/10361922/",  # !#############################################
                                                    style={"display": "inline-block"}),
                                                html.P("|", style={"display": "inline-block", "margin-left": "2px",
                                                                   "margin-right": "2px"}),
                                                html.A(
                                                    "pdf",
                                                    target="_blank",
                                                    href="https://www.researchgate.net/publication/376766834_Supervised_Learning_Regression_for_Sensor_Calibration",
                                                    style={"display": "inline-block"}),
                                                html.P("|", style={"display": "inline-block", "margin-left": "2px",
                                                                   "margin-right": "2px"}),
                                            ],
                                            style={"line-height": "120%", "margin-bottom": "0px", "text-align": "right"}
                                        )
                                    ]),
                                    id="IVK2023_show_btn",
                                    style={"margin-left": "8px", "border": "0px", "background": "transparent",
                                           "height": "130px", "color": "white", "text-align": "left", "padding": "0px"}
                                ),
                                style={"margin": "auto"}
                            ),
                            id="DGON2023_paper",
                            className="d-flex align-items-center",
                            style={
                                "margin-bottom": "14px",
                                "padding": "5px",
                                "color": "white",
                                "height": "130px",
                                "width": "465px",
                                "background-color": "#737373",
                                "border-radius": "10px",
                                "border-left": "4px solid white",
                                "margin-left": "0px",
                                "padding-left": "5px",
                                "padding-right": "5px"
                            }
                        ),
                        html.Div(
                            html.Div(
                                html.Button(html.Div(
                                    [
                                        html.P(html.B(["Optimierte Trajektorie aus Smartphone-Sensoren und 5G UL-TDoA mit Cluster-Partikel-Filter (2023)"]),
                                            style={"margin-bottom": "7px"}),
                                        html.P(
                                            "Hossein Shoushtari, Dorian Harder, Thomas Willemsen, Harald Sternberg",
                                            style={"line-height": "120%", "margin-bottom": "0px"}),
                                        html.P(
                                            [
                                                html.P("|", style={"display": "inline-block"}),
                                                html.Button(
                                                    "bibtex",
                                                    id="IVK2023_bibtex_btn",
                                                    style={"background": "transparent", "border": "0px",
                                                        "text-decoration": "underline", "color": "#00BC8C",
                                                        "padding": "0px", "width": "50px", "margin-left": "-1px",
                                                        "margin-right": "-1px"}
                                                ),
                                                html.P("|", style={"display": "inline-block"}),
                                                html.A(
                                                    "code",
                                                    target="_blank",
                                                    href="https://github.com/Hossein-Shoushtari/poslab",
                                                    style={"display": "inline-block", "margin-left": "2px","margin-right": "2px"}),
                                                html.P("|", style={"display": "inline-block"}),
                                                html.A(
                                                    "arxiv",
                                                    target="_blank",
                                                    href="", #!#############################################
                                                    style={"display": "inline-block"}),
                                                html.P("|", style={"display": "inline-block", "margin-left": "2px",
                                                                "margin-right": "2px"}),
                                                html.A(
                                                    "pdf",
                                                    target="_blank",
                                                    href="https://www.researchgate.net/publication/373255308_Optimierte_Trajektorie_aus_Smartphone-Sensoren_und_5G_UL-TDOA_mit_Cluster-Partikel-Filter",
                                                    style={"display": "inline-block"}),
                                                html.P("|", style={"display": "inline-block", "margin-left": "2px",
                                                                "margin-right": "2px"}),
                                            ],
                                            style={"line-height": "120%", "margin-bottom": "0px", "text-align": "right"}
                                        )
                                    ]),
                                    id="IVK2023_show_btn",
                                    style={"margin-left": "8px", "border": "0px", "background": "transparent",
                                        "height": "130px", "color": "white", "text-align": "left", "padding": "0px"}
                                ),
                                style={"margin": "auto"}
                            ),
                            id="IVK2023_paper",
                            className="d-flex align-items-center",
                            style={
                                "margin-bottom": "14px",
                                "padding": "5px",
                                "color": "white",
                                "height": "130px",
                                "width": "465px",
                                "background-color": "#737373",
                                "border-radius": "10px",
                                "border-left": "4px solid white",
                                "margin-left": "0px",
                                "padding-left": "5px",
                                "padding-right": "5px"
                            }
                        ),
                        html.Div(
                            html.Div(
                                html.Button(html.Div(
                                    [
                                        html.P(html.B(["Data-Driven Inertial Navigation assisted by 5G UL-TDoA Positioning (2023)"]),
                                            style={"margin-bottom": "7px"}),
                                        html.P(
                                            "Hossein Shoushtari, Dorian Harder, Maximilian Kasparek, Matthias Schäfer, Jörg Müller-Lietzkow, Harald Sternberg",
                                            style={"line-height": "120%", "margin-bottom": "0px"}),
                                        html.P(
                                            [
                                                html.P("|", style={"display": "inline-block"}),
                                                html.Button(
                                                    "bibtex",
                                                    id="ION2023_bibtex_btn",
                                                    style={"background": "transparent", "border": "0px",
                                                        "text-decoration": "underline", "color": "#00BC8C",
                                                        "padding": "0px", "width": "50px", "margin-left": "-1px",
                                                        "margin-right": "-1px"}
                                                ),
                                                html.P("|", style={"display": "inline-block"}),
                                                html.A(
                                                    "code",
                                                    target="_blank",
                                                    href="https://github.com/Hossein-Shoushtari/poslab",
                                                    style={"display": "inline-block", "margin-left": "2px","margin-right": "2px"}),
                                                html.P("|", style={"display": "inline-block"}),
                                                html.A(
                                                    "arxiv",
                                                    target="_blank",
                                                    href="https://www.ion.org/publications/abstract.cfm?articleID=18645",
                                                    style={"display": "inline-block"}),
                                                html.P("|", style={"display": "inline-block", "margin-left": "2px",
                                                                "margin-right": "2px"}),
                                                html.A(
                                                    "pdf",
                                                    target="_blank",
                                                    href="https://www.researchgate.net/publication/368501717_Data-Driven_Inertial_Navigation_assisted_by_5G_UL-TDoA_Positioning",
                                                    style={"display": "inline-block"}),
                                                html.P("|", style={"display": "inline-block", "margin-left": "2px",
                                                                "margin-right": "2px"}),
                                            ],
                                            style={"line-height": "120%", "margin-bottom": "0px", "text-align": "right"}
                                        )
                                    ]),
                                    id="ION2023_show_btn",
                                    style={"margin-left": "8px", "border": "0px", "background": "transparent",
                                        "height": "130px", "color": "silver", "text-align": "left", "padding": "0px"}
                                ),
                                style={"margin": "auto"}
                            ),
                            id="ION2023_paper",
                            className="d-flex align-items-center",
                            style={
                                "margin-bottom": "14px",
                                "padding": "5px",
                                "color": "silver",
                                "height": "130px",
                                "width": "465px",
                                "background-color": "#737373",
                                "border-radius": "10px",
                                "border-left": "4px solid silver",
                                "margin-left": "0px",
                                "padding-left": "5px",
                                "padding-right": "5px"
                            }
                        ),
                        html.Div(
                            html.Div(
                                html.Button(html.Div(
                                    [
                                        html.P(html.B(["L5IN", html.Sup("+"), ": From an Analytical Platform to Optimization of Deep Inertial Odometry (2022)"]), style={"margin-bottom": "7px"}),
                                        html.P("Hossein Shoushtari, Firas Kassawat, Dorian Harder, Korvin Venzke, Jörg Müller-Lietzkow, Harald Sternberg", style={"line-height": "120%", "margin-bottom": "0px"}),
                                        html.P(
                                            [
                                                html.P("|", style={"display": "inline-block"}),
                                                html.Button(
                                                    "bibtex",
                                                    id="2022_9_5_IPIN2022_bibtex_btn",
                                                    style={"background": "transparent", "border": "0px", "text-decoration": "underline", "color": "#00BC8C", "padding": "0px", "width": "50px", "margin-left": "-1px", "margin-right": "-1px"}
                                                ),
                                                html.P("|", style={"display": "inline-block"}),
                                                html.A(
                                                    "code",
                                                    target="_blank",
                                                    href="https://github.com/Hossein-Shoushtari/poslab",
                                                    style={"display": "inline-block", "margin-left": "2px", "margin-right": "2px"}),
                                                html.P("|", style={"display": "inline-block"}),
                                                html.A(
                                                    "arxiv",
                                                    target="_blank",
                                                    href="https://ceur-ws.org/Vol-3248/",
                                                    style={"display": "inline-block"}),
                                                html.P("|", style={"display": "inline-block", "margin-left": "2px", "margin-right": "2px"}),
                                                html.A(
                                                    "pdf",
                                                    target="_blank",
                                                    href="https://ceur-ws.org/Vol-3248/paper24.pdf",
                                                    style={"display": "inline-block"}),
                                                html.P("|", style={"display": "inline-block", "margin-left": "2px", "margin-right": "2px"}),
                                            ],
                                            style={"line-height": "120%", "margin-bottom": "0px", "text-align": "right"}
                                        )
                                    ]),
                                    id="2022_9_5_IPIN2022_show_btn",
                                    style={"margin-left": "8px", "border": "0px", "background": "transparent", "height": "130px", "color": "silver", "text-align": "left", "padding": "0px"}
                                ),
                                style={"margin": "auto"}                           
                            ),
                            id="2022_9_5_IPIN2022_paper",
                            className="d-flex align-items-center",
                            style={
                                "margin-bottom": "14px",
                                "padding": "5px",
                                "color": "silver",
                                "height": "130px",
                                "width": "465px",
                                "background-color": "#737373",
                                "border-radius": "10px",
                                "border-left": "4px solid silver",
                                "margin-left": "0px",
                                "padding-left": "5px",
                                "padding-right": "5px"
                            }
                        ),
                        html.Div(
                            html.Div(
                                html.Button(html.Div(
                                    [
                                        html.P(html.B("Real-Time Map Matching with a Backtracking Particle Filter Using Geospatial Analysis (2022)"), style={"margin-bottom": "7px"}),
                                        html.P("Dorian Harder, Hossein Shoushtari, Harald Sternberg", style={"line-height": "120%", "margin-bottom": "0px"}),
                                        html.P(
                                            [
                                                html.P("|", style={"display": "inline-block"}),
                                                html.Button(
                                                    "bibtex",
                                                    id="2022_4_25_sensors_bibtex_btn",
                                                    style={"background": "transparent", "border": "0px", "text-decoration": "underline", "color": "#00BC8C", "padding": "0px", "width": "50px", "margin-left": "-1px", "margin-right": "-1px"}
                                                ),
                                                html.P("|", style={"display": "inline-block"}),
                                                html.A(
                                                    "code",
                                                    target="_blank",
                                                    href="https://github.com/DorianHarder/PF_backtracking_cluster",
                                                    style={"display": "inline-block", "margin-left": "2px", "margin-right": "2px"}),
                                                html.P("|", style={"display": "inline-block"}),
                                                html.A(
                                                    "arxiv",
                                                    target="_blank",
                                                    href="https://www.mdpi.com/1424-8220/22/9/3289",
                                                    style={"display": "inline-block"}),
                                                html.P("|", style={"display": "inline-block", "margin-left": "2px", "margin-right": "2px"}),
                                                html.A(
                                                    "pdf",
                                                    target="_blank",
                                                    href="https://www.mdpi.com/1424-8220/22/9/3289",
                                                    style={"display": "inline-block"}),
                                                html.P("|", style={"display": "inline-block", "margin-left": "2px", "margin-right": "2px"}),
                                            ],
                                            style={"line-height": "120%", "margin-bottom": "0px", "text-align": "right"}
                                        )
                                    ]),
                                    id="2022_4_25_sensors_show_btn",
                                    style={"margin-left": "8px", "border": "0px", "background": "transparent", "height": "130px", "color": "silver", "text-align": "left", "padding": "0px"}
                                ),
                                style={"margin": "auto"}                           
                            ),
                            id="2022_4_25_sensors_paper",
                            className="d-flex align-items-center",
                            style={
                                "margin-bottom": "14px",
                                "padding": "5px",
                                "color": "silver",
                                "height": "130px",
                                "width": "465px",
                                "background-color": "#737373",
                                "border-radius": "10px",
                                "border-left": "4px solid silver",
                                "margin-left": "0px",
                                "padding-left": "5px",
                                "padding-right": "5px"
                            }
                        ),
                        html.Div(
                            html.Div(
                                html.Button(html.Div(
                                    [
                                        html.P(html.B("3D Indoor Localization using 5G-based Particle Filtering and CAD Plans (2021)"), style={"margin-bottom": "7px"}),
                                        html.P("Hossein Shoushtari, Cigdem Askar, Dorian Harder, Thomas Willemsen, Harald Sternberg", style={"line-height": "120%", "margin-bottom": "0px"}),
                                        html.P(
                                            [
                                                html.P("|", style={"display": "inline-block"}),
                                                html.Button(
                                                    "bibtex",
                                                    id="2021_11_29_IPIN2021_bibtex_btn",
                                                    style={"background": "transparent", "border": "0px", "text-decoration": "underline", "color": "#00BC8C", "padding": "0px", "width": "50px", "margin-left": "-1px", "margin-right": "-1px"}
                                                ),
                                                html.P("|", style={"display": "inline-block"}),
                                                html.A(
                                                    "code",
                                                    target="_blank",
                                                    href="https://github.com/Hossein-Shoushtari/IPIN21Data",
                                                    style={"display": "inline-block", "margin-left": "2px", "margin-right": "2px"}),
                                                html.P("|", style={"display": "inline-block"}),
                                                html.A(
                                                    "arxiv",
                                                    target="_blank",
                                                    href="https://ieeexplore.ieee.org/document/9662636",
                                                    style={"display": "inline-block"}),
                                                html.P("|", style={"display": "inline-block", "margin-left": "2px", "margin-right": "2px"}),
                                                html.A(
                                                    "pdf",
                                                    target="_blank",
                                                    href="https://www.researchgate.net/publication/357594689_3D_Indoor_Localization_using_5G-based_Particle_Filtering_and_CAD_Plans",
                                                    style={"display": "inline-block"}),
                                                html.P("|", style={"display": "inline-block", "margin-left": "2px", "margin-right": "2px"}),
                                            ],
                                            style={"line-height": "120%", "margin-bottom": "0px", "text-align": "right"}
                                        )
                                    ]),
                                    id="2021_11_29_IPIN2021_show_btn",
                                    style={"margin-left": "8px", "border": "0px", "background": "transparent", "height": "130px", "color": "silver", "text-align": "left", "padding": "0px"}
                                ),
                                style={"margin": "auto"}                           
                            ),
                            id="2021_11_29_IPIN2021_paper",
                            className="d-flex align-items-center",
                            style={
                                "margin-bottom": "14px",
                                "padding": "5px",
                                "color": "silver",
                                "height": "130px",
                                "width": "465px",
                                "background-color": "#737373",
                                "border-radius": "10px",
                                "border-left": "4px solid silver",
                                "margin-left": "0px",
                                "padding-left": "5px",
                                "padding-right": "5px"
                            }
                        ),
                        html.Div(
                            html.Div(
                                html.Button(html.Div(
                                    [
                                        html.P(html.B("Many Ways Lead to the Goal — Possibilities of Autonomous and Infrastructure-Based Indoor Positioning (2021)"), style={"margin-bottom": "7px"}),
                                        html.P("Hossein Shoushtari, Thomas Willemsen, Harald Sternberg", style={"line-height": "120%", "margin-bottom": "0px"}),
                                        html.P(
                                            [
                                                html.P("|", style={"display": "inline-block"}),
                                                html.Button(
                                                    "bibtex",
                                                    id="2021_2_5_electronics_bibtex_btn",
                                                    style={"background": "transparent", "border": "0px", "text-decoration": "underline", "color": "#00BC8C", "padding": "0px", "width": "50px", "margin-left": "-1px", "margin-right": "-1px"}
                                                ),
                                                html.P("|", style={"display": "inline-block"}),
                                                html.A(
                                                    "code",
                                                    target="_blank",
                                                    href="https://github.com/Hossein-Shoushtari/ElectronicsData",
                                                    style={"display": "inline-block", "margin-left": "2px", "margin-right": "2px"}),
                                                html.P("|", style={"display": "inline-block"}),
                                                html.A(
                                                    "arxiv",
                                                    target="_blank",
                                                    href="https://www.mdpi.com/1424-8220/22/9/3289",
                                                    style={"display": "inline-block"}),
                                                html.P("|", style={"display": "inline-block", "margin-left": "2px", "margin-right": "2px"}),
                                                html.A(
                                                    "pdf",
                                                    target="_blank",
                                                    href="https://www.mdpi.com/2079-9292/10/4/397",
                                                    style={"display": "inline-block"}),
                                                html.P("|", style={"display": "inline-block", "margin-left": "2px", "margin-right": "2px"}),
                                            ],
                                            style={"line-height": "120%", "margin-bottom": "0px", "text-align": "right"}
                                        )
                                    ]),
                                    id="2021_2_5_electronics_show_btn",
                                    style={"margin-left": "8px", "border": "0px", "background": "transparent", "height": "130px", "color": "silver", "text-align": "left", "padding": "0px"}
                                ),
                                style={"margin": "auto"}                           
                            ),
                            id="2021_2_5_electronics_paper",
                            className="d-flex align-items-center",
                            style={
                                "margin-bottom": "14px",
                                "padding": "5px",
                                "color": "silver",
                                "height": "130px",
                                "width": "465px",
                                "background-color": "#737373",
                                "border-radius": "10px",
                                "border-left": "4px solid silver",
                                "margin-left": "0px",
                                "padding-left": "5px",
                                "padding-right": "5px"
                            }
                        )],
                    id="scrollable_paper_list",
                    style={"height": "706px", "overflow": "hidden", "overflow-y": "auto"})
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
        html.H5("Responsible for the L5IN project", style={"color": "silver", "text-align": "center"}),
        dbc.Row(
            [
                dbc.Col([
                    html.P(html.B("Prof. Dr. Jörg Müller-Litzkow", style={"color": "silver", "margin-top": "5px"})),
                    html.P("President of HafenCity University Hamburg (HCU) and University Professor for Economics and Digitization",
                        style={"line-height": "110%", "color": "silver", "margin-top": "-18px"})
                ], width=3, style={"height": "136px", "width": "337px"}),
                dbc.Col([
                    html.P(html.B("Prof. Dr. Harald Sternberg", style={"color": "silver", "margin-top": "-12px"})),
                    html.P("""University Professor for Hydrography and Engineering Geodesy""",
                        style={"line-height": "110%", "color": "silver", "margin-top": "-18px"})
                ], width=3, style={"height": "136px", "width": "337px"}),
                # dbc.Col([
                #     html.P(html.B("Nils Hellweg", style={"color": "silver", "margin-top": "-12px"})),
                #     html.P("""Project Manager and PhD Student at HafenCity University Hamburg (HCU)""",
                #         style={"line-height": "110%", "color": "silver", "margin-top": "-18px"})
                # ], width=3, style={"height": "136px", "width": "337px"})
            ], justify="center"
        ),
        html.H5(["L5IN", html.Sup("+"), " project contact persons"] , style={"color": "silver", "text-align": "center"}),
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

                    html.P(html.B("Korvin Venzke", style={"color": "silver", "margin-top": "-12px"})),
                    html.P("Bachelor Student at HafenCity University Hamburg (HCU)",
                        style={"line-height": "110%", "color": "silver", "margin-top": "-18px"}),
                   
                ], width=3, style={"height": "101px", "width": "337px"})
            ], justify="center"
        ),
        dbc.Row(
            [


                dbc.Col([
                    html.P(html.B("Dorian Harder", style={"color": "silver", "margin-top": "-12px"})),
                    html.P("Research assistant at HafenCity University Hamburg (HCU)",
                           style={"line-height": "110%", "color": "silver", "margin-top": "-18px"}),
                ], width=3, style={"height": "101px", "width": "337px"}),

                dbc.Col([
                    html.P(html.B("Georg Fjodorow", style={"color": "silver", "margin-top": "-12px"})),
                    html.P("Former Master Student at HafenCity University Hamburg (HCU)",
                           style={"line-height": "110%", "color": "silver", "margin-top": "-18px"}),
                ], width=3, style={"height": "101px", "width": "337px"})
            ], justify="center"
        )
    ], style={"margin-bottom": "20px"})
    return contact

def popup():
    return html.Div(
        className="popup-menu",
        children=[
            html.Ol(
                [
                    html.Li(
                        className="popup-open-item",
                        children=[
                            html.Div(
                                html.Button(
                                    html.Img(
                                        src="assets/images/svg/signs/bulb_sign.svg",
                                        style={"margin-left": "-4px"}
                                    ),
                                    className="popup-icon"
                                )
                            ),
                            html.Ol(
                                className="sub-popup-menu",
                                children=[
                                    html.Li(
                                        className="popup-item",
                                        children=html.Div(
                                            html.A(
                                                target="_blank",
                                                href="https://github.com/Hossein-Shoushtari/poslab",
                                                children=html.Button(
                                                    children=html.Img(
                                                        src="assets/images/svg/signs/github_sign.svg",
                                                        style={"margin-left": "-4px"}
                                                    ),
                                                    className="popup-icon"
                                                )
                                            ),
                                            className="popup-icon-div"
                                        )
                                    ),
                                    html.Li(
                                        className="popup-item",
                                        children=html.Div(
                                            html.A(
                                                target="_blank",
                                                href="https://www.youtube.com/channel/UChIY2hB7pU8V2Sq577tYQ2w",
                                                children=html.Button(
                                                    children=html.Img(
                                                        src="assets/images/svg/signs/youtube_sign.svg",
                                                        style={"margin-left": "-4px"}
                                                    ),
                                                    className="popup-icon"
                                                )
                                            ),
                                            className="popup-icon-div"
                                        )
                                    ),
                                    html.Li(
                                        className="popup-item",
                                        children=html.Div(
                                            html.A(
                                                target="_blank",
                                                href="https://www.hcu-hamburg.de/research/forschungsprojekte/level-5-indoor-navigation",
                                                children=html.Button(
                                                    children=html.Img(
                                                        src="assets/images/svg/signs/www_sign.svg",
                                                        style={"margin-left": "-4px"}
                                                    ),
                                                    className="popup-icon"
                                                )
                                            ),
                                            className="popup-icon-div"
                                        )
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )

def home_layout():
    return dbc.Card([
        dbc.CardBody(
            [
                modals(),
                html.Br(),
                html.Br(),
                header(),
                html.Br(),
                html.Br(),
                about(),
                html.Br(),
                html.Br(),
                publications(),
                html.Br(),
                html.Br(),
                contact()
            ]
        ),
        dbc.CardFooter(
            children=[
                dbc.Row(
                    [
                        dbc.Col(popup(), className="popup-col1", width=3),
                        dbc.Col(
                            html.P(
                                f"© {datetime.date.today().strftime('%Y')} Level 5 Indoor Navigation Plus. All Rights Reserved",
                                className="popup-p"
                            ),
                            className="popup-col2",
                            width=3
                        )
                    ],
                    className="popup-row"
                )
            ],
            class_name="home-footer"
        )
    ])
