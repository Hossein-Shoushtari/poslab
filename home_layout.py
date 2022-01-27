from dash import html, dcc, Dash, Output, Input, State, no_update
import dash_bootstrap_components as dbc

def home_card():
    return dbc.Card([
        dbc.CardBody(
            [
                html.H3("Level 5 Indoor Navigation", style={"color": "silver"}),

                html.Br(),

                html.P("""This is a tool developed by Level 5 Indoor navigation (L5IN) project with positioning focus.
                    The L5IN project deals with real-time navigation inside buildings, using 5G and smartphone sensors.""",
                    style={"color": "silver", "width": "50%", "font-size": "20px"}),
                html.P("""The project demonstrates the feasibility of the transition from outdoor to indoor environment in terms of navigation.
                    The aim of the L5IN project is to use newly introduced 5G technology to demonstrate, based on a research-oriented model
                    project, how in door navigation systems can function. Such systems were previously only known in the outdoor segment
                    (through GNSS) but can now also be integrated into existing smartphone systems and 5G as a ubiquitous alternative for
                    the GNSS solutions within the context of indoor navigation.""",
                    style={"color": "silver", "width": "50%", "font-size": "20px", "marginTop": "-10px", "text-indent": "15px"}),
                html.P("""The positioning work package is one of the L5IN research area. Autonomous pedestrian localization would make
                    the navigation possible at any time.""",
                    style={"color": "silver", "width": "50%", "font-size": "20px", "marginTop": "25px"}),
                html.P("""The positioning team use the benefits of interdisciplinary technologies developed
                    at L5IN and focus on the approaches and methods such as Monte Carlo Simulation, state estimation filters, machine learning,
                    deep learning, 5G Positioning to develop a practice-oriented solution.""",
                    style={"color": "silver", "width": "50%", "font-size": "20px", "marginTop": "-10px", "text-indent": "15px"}),

                html.Br(),

                html.Hr(style={"width": "25%"}),

                html.B("Responsible for the project:",

                    style={"color": "gray", "font-size": "18px"}),
                html.P("Prof. Dr. Jörg Müller-Litzkow",
                    style={"color": "gray", "width": "50%", "marginTop": "5px", "font-size": "18px", "text-indent": "10px"}),
                html.P("President of Hafencity University Hamburg (HCU) and Univ. Prof. for Economics and Digitalization",
                    style={"color": "gray", "width": "50%", "marginTop": "-20px", "font-size": "16px", "paddingLeft": "10px"}),

                html.P("Prof. Dr. Harald Sternberg",
                    style={"color": "gray", "width": "50%", "marginTop": "-12px", "font-size": "18px", "text-indent": "10px"}),
                html.P("""Vice President for Teaching and Digitalization of Hafencity University Hamburg (HCU)
                    and Univ. Prof. for Hydrography and Engineering Geodesy""",
                    style={"color": "gray", "width": "50%", "marginTop": "-20px", "font-size": "16px", "paddingLeft": "10px"}),
                

                html.B("Positioning Contact Persons:",
                
                    style={"color": "gray", "font-size": "18px"}),
                html.P("Hossein Shoushtari",
                    style={"color": "gray", "width": "50%", "marginTop": "5px", "font-size": "18px", "text-indent": "10px"}),
                html.P("Research assistant and PhD Student at Hafencity University Hamburg (HCU)",
                    style={"color": "gray", "width": "50%", "marginTop": "-20px", "font-size": "16px", "paddingLeft": "10px"}),
                html.P("hossein.shoushtari@hcu-hamburg.de",
                    style={"color": "gray", "width": "50%", "marginTop": "-20px", "font-size": "16px", "paddingLeft": "10px"}),

                html.P("Dorian Harder",
                    style={"color": "gray", "width": "50%", "marginTop": "-12px", "font-size": "18px", "text-indent": "10px"}),
                html.P("Research assistant at Hafencity University Hamburg (HCU)",
                    style={"color": "gray", "width": "50%", "marginTop": "-20px", "font-size": "16px", "paddingLeft": "10px"}),
                html.P("dorian.harder@hcu-hamburg.de",
                    style={"color": "gray", "width": "50%", "marginTop": "-20px", "font-size": "16px", "paddingLeft": "10px"}),

                html.P("Georg Fjodorow",
                    style={"color": "gray", "width": "50%", "marginTop": "-12px", "font-size": "18px", "text-indent": "10px"}),
                html.P("Master Student at Hafencity University Hamburg (HCU)",
                    style={"color": "gray", "width": "50%", "marginTop": "-20px", "font-size": "16px", "paddingLeft": "10px"}),
                html.P("georg.fjodorow@hcu-hamburg.de",
                    style={"color": "gray", "width": "50%", "marginTop": "-20px", "font-size": "16px", "paddingLeft": "10px"}),
                    
                html.P("Korvin Venzke",
                    style={"color": "gray", "width": "50%", "marginTop": "-12px", "font-size": "18px", "text-indent": "10px"}),
                html.P("Bachelor Student at Hafencity University Hamburg (HCU)",
                    style={"color": "gray", "width": "50%", "marginTop": "-20px", "font-size": "16px", "paddingLeft": "10px"}),
                html.P("korvin.venzke@hcu-hamburg.de",
                    style={"color": "gray", "width": "50%", "marginTop": "-20px", "font-size": "16px", "paddingLeft": "10px"}),
            ]),
        dbc.CardFooter("Copyright © 2022 Level 5 Indoor Navigation. All Rights Reserved")
    ])