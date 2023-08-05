##### Callbacks Home
#### IMPORTS
# dash
from dash import Output, Input, no_update, callback_context



def home_calls(app):

    papers_list = ["IVK2023", "ION2023", "2022_9_5_IPIN2022", "2022_4_25_sensors", "2021_11_29_IPIN2021", "2021_2_5_electronics"]

    @app.callback(
        Output("paper_carousel", "active_index"),
        [Input(f"{paper}_show_btn", "n_clicks") for paper in papers_list]
    )
    def show_slide(*show):
        """
        Callback function that changes the active index of a carousel element when a button is clicked.
        
        Parameters:
        show (tuple) : A tuple of n_clicks values for each button corresponding to a paper in the list `papers_list`.
        
        Returns:
        int : The index of the active slide in the carousel element.
        """
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
        """
        This function updates the style of the show buttons and papers based on the active index of the paper carousel.
        
        Parameters:
        slide (int): The index of the active slide in the carousel.
        
        Returns:
        list: A list of dictionaries containing the updated styles for the show buttons and papers.
        """
        n_papers = len(papers_list)
        show_btns = [{
            "margin-left": "8px",
            "border": "0px",
            "background": "transparent",
            "height": "130px",
            "color": "silver",
            "text-align": "left",
            "padding": "0px"
            } for _ in range(n_papers)]
        papers = [{
            "margin-bottom": "14px",
            "padding": "5px",
            "color": "silver",
            "height": "130px",
            "width": "475px",
            "background-color": "#737373",
            "border-left": "4px solid silver",
            "border-radius": 0,
            "margin-left": "-10px"
            } for _ in range(n_papers)]
        outputs = show_btns + papers
        if slide:
            show_btns[slide] = {
                "margin-left": "8px",
                "border": "0px",
                "background": "transparent",
                "height": "130px",
                "color": "white",
                "text-align": "left",
                "padding": "0px"
            }
            papers[slide] = {
                "margin-bottom": "14px",
                "padding": "5px",
                "color": "white",
                "height": "130px",
                "width": "475px",
                "background-color": "#737373",
                "border-left": "4px solid white",
                "border-radius": 0,
                "margin-left": "-10px"
            }
        else:
            show_btns[0] = {
                "margin-left": "8px",
                "border": "0px",
                "background": "transparent",
                "height": "130px",
                "color": "white",
                "text-align": "left",
                "padding": "0px"
            }
            papers[0] = {
                "margin-bottom": "14px",
                "padding": "5px",
                "color": "white",
                "height": "130px",
                "width": "475px",
                "background-color": "#737373",
                "border-left": "4px solid white",
                "border-radius": 0,
                "margin-left": "-10px"
            }
        outputs = show_btns + papers
        return outputs


    @app.callback(
        [Output(f"{paper}_bibtex_modal", "is_open") for paper in papers_list],
        [Input(f"{paper}_bibtex_btn", "n_clicks") for paper in papers_list]
    )
    def modals(*bibtex):
        """
        This callback function opens the bibtex modal for the selected paper.

        Parameters:
        *bibtex : variable length argument list
                  contains the number of clicks for each paper's bibtex button

        Returns:
        list : a list of booleans indicating whether the corresponding paper's 
               bibtex modal should be open or not
        """
        return_string = [p["prop_id"] for p in callback_context.triggered][0]
        output = [False for _ in range(len(papers_list))]
        if return_string == ".":
            return output
        else:
            paper_title = return_string.split('_bibtex_btn')[0]
            index = papers_list.index(paper_title)
            output[index] = True
            return output