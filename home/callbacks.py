##### Callbacks Home
#### IMPORTS
# dash
from dash import html, Output, Input, State, no_update, callback_context
# built in
import os



def home_calls(app):   
    @app.callback(
        Output("paper_carousel", "active_index"),
        [Input(f"{paper.split('.')[0]}_show_btn", "n_clicks") for paper in list(reversed([file for file in os.listdir("assets/images/papers")]))]
    )
    def show_slide(*show):
        button = [p["prop_id"] for p in callback_context.triggered][0]
        papers = [f"{paper.split('.')[0]}_show_btn" for paper in list(reversed([file for file in os.listdir("assets/images/papers")]))]
        if button != ".":
            return papers.index(button.split(".")[0])
        return no_update
        

    @app.callback(
        [Output(f"{paper.split('.')[0]}_pdf_sign", "src") for paper in list(reversed([file for file in os.listdir("assets/images/papers")]))],
        [Output(f"{paper.split('.')[0]}_show_btn", "style") for paper in list(reversed([file for file in os.listdir("assets/images/papers")]))],
        [Output(f"{paper.split('.')[0]}_paper", "style") for paper in list(reversed([file for file in os.listdir("assets/images/papers")]))],
        Input("paper_carousel", "active_index")
    )
    def mark_paper(slide):
        n_papers = len([file for file in os.listdir("assets/images/papers")])
        pdf_signs = ["assets/images/signs/pdf_sign1.svg" for _ in range(n_papers)]
        show_btns = [{"margin-left": "8px", "border": "0px", "background": "transparent", "height": "110px", "color": "silver", "text-align": "left", "padding": "0px"} for _ in range(n_papers)]
        papers = [{"padding": "0px", "color": "silver", "margin-left": "5px", "height": "110px", "width": "500px", "background-color": "#545454", "border-left": "4px solid silver", "border-radius": 0} for _ in range(n_papers)]
        if slide:
            pdf_signs[slide] = "assets/images/signs/pdf_sign2.svg"
            show_btns[slide] = {"margin-left": "8px", "border": "0px", "background": "transparent", "height": "110px", "color": "white", "text-align": "left", "padding": "0px"}
            papers[slide] = {"padding": "0px", "color": "white", "margin-left": "5px", "height": "110px", "width": "500px", "background-color": "#737373", "border-left": "4px solid white", "border-radius": 0}
        else:
            pdf_signs[0] = "assets/images/signs/pdf_sign2.svg"
            show_btns[0] = {"margin-left": "8px", "border": "0px", "background": "transparent", "height": "110px", "color": "white", "text-align": "left", "padding": "0px"}
            papers[0] = {"padding": "0px", "color": "white", "margin-left": "5px", "height": "110px", "width": "500px", "background-color": "#737373", "border-left": "4px solid white", "border-radius": 0}
        outputs = pdf_signs + show_btns + papers
        return outputs