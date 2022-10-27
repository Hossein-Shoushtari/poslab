##### Callbacks Home
#### IMPORTS
# dash
from dash import html, Output, Input, State, no_update, callback_context
# built in
import os



def home_calls(app):

    papers_list = ["2022_9_5_IPIN2022", "2022_4_25_sensors", "2021_4_1_mobility", "2021_2_9_remotesensing", "2021_2_5_electronics"]  

    @app.callback(
        Output("paper_carousel", "active_index"),
        [Input(f"{paper}_show_btn", "n_clicks") for paper in papers_list]
    )
    def show_slide(*show):
        button = [p["prop_id"] for p in callback_context.triggered][0]
        papers = [f"{paper}_show_btn" for paper in papers_list]
        if button != ".":
            return papers.index(button.split(".")[0])
        return no_update
        

    @app.callback(
        [Output(f"{paper}_pdf_sign", "src") for paper in papers_list],
        [Output(f"{paper}_show_btn", "style") for paper in papers_list],
        [Output(f"{paper}_paper", "style") for paper in papers_list],
        Input("paper_carousel", "active_index")
    )
    def mark_paper(slide):
        n_papers = len(papers_list)
        pdf_signs = ["assets/images/signs/pdf_sign1.svg" for _ in range(n_papers)]
        show_btns = [{"margin-left": "8px", "border": "0px", "background": "transparent", "height": "110px", "color": "silver", "text-align": "left", "padding": "0px"} for _ in range(n_papers)]
        papers = [{"padding": "0px", "color": "silver", "margin-left": "5px", "height": "110px", "width": "500px", "background-color": "#545454", "border-left": "4px solid silver", "border-radius": 0, "margin-left": "-10px"} for _ in range(n_papers)]
        if slide:
            pdf_signs[slide] = "assets/images/signs/pdf_sign2.svg"
            show_btns[slide] = {"margin-left": "8px", "border": "0px", "background": "transparent", "height": "110px", "color": "white", "text-align": "left", "padding": "0px"}
            papers[slide] = {"padding": "0px", "color": "white", "margin-left": "5px", "height": "110px", "width": "500px", "background-color": "#737373", "border-left": "4px solid white", "border-radius": 0, "margin-left": "-10px"}
        else:
            pdf_signs[0] = "assets/images/signs/pdf_sign2.svg"
            show_btns[0] = {"margin-left": "8px", "border": "0px", "background": "transparent", "height": "110px", "color": "white", "text-align": "left", "padding": "0px"}
            papers[0] = {"padding": "0px", "color": "white", "margin-left": "5px", "height": "110px", "width": "500px", "background-color": "#737373", "border-left": "4px solid white", "border-radius": 0, "margin-left": "-10px"}
        outputs = pdf_signs + show_btns + papers
        return outputs