##### Callbacks Home
#### IMPORTS
# dash
from dash import Output, Input, no_update, callback_context



def home_calls(app):

    papers_list = ["2022_9_5_IPIN2022", "2022_4_25_sensors", "2021_11_29_IPIN2021", "2021_2_5_electronics"]

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
        [Output(f"{paper}_show_btn", "style") for paper in papers_list],
        [Output(f"{paper}_paper", "style") for paper in papers_list],
        Input("paper_carousel", "active_index")
    )
    def mark_paper(slide):
        n_papers = len(papers_list)
        show_btns = [{"margin-left": "8px", "border": "0px", "background": "transparent", "height": "130px", "color": "silver", "text-align": "left", "padding": "0px"} for _ in range(n_papers)]
        papers = [{"margin-bottom": "15px", "padding": "5px", "color": "silver", "height": "130px", "width": "500px", "background-color": "#737373", "border-left": "4px solid silver", "border-radius": 0, "margin-left": "-10px"} for _ in range(n_papers)]
        outputs = show_btns + papers
        if slide:
            show_btns[slide] = {"margin-left": "8px", "border": "0px", "background": "transparent", "height": "130px", "color": "white", "text-align": "left", "padding": "0px"}
            papers[slide] = {"margin-bottom": "15px", "padding": "5px", "color": "white", "height": "130px", "width": "500px", "background-color": "#737373", "border-left": "4px solid white", "border-radius": 0, "margin-left": "-10px"}
        else:
            show_btns[0] = {"margin-left": "8px", "border": "0px", "background": "transparent", "height": "130px", "color": "white", "text-align": "left", "padding": "0px"}
            papers[0] = {"margin-bottom": "15px", "padding": "5px", "color": "white", "height": "130px", "width": "500px", "background-color": "#737373", "border-left": "4px solid white", "border-radius": 0, "margin-left": "-10px"}
        outputs = show_btns + papers
        return outputs

    @app.callback(
        [Output(f"{paper}_bibtex_modal", "is_open") for paper in papers_list],
        [Input(f"{paper}_bibtex_btn", "n_clicks") for paper in papers_list]
    )
    def modals(*bibtex):
        button = [p["prop_id"] for p in callback_context.triggered][0]
        output = [False for _ in range(len(papers_list))]
        if papers_list[0] in button:
            output[0] = True
            return output
        if papers_list[1] in button:
            output[1] = True
            return output
        if papers_list[2] in button:
            output[2] = True
            return output
        if papers_list[3] in button:
            output[3] = True
            return output
        else:
          return output