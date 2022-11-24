# import the necessary libraries
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from dash import dash, dcc, html, Input, Output

# import the dataset
# data = pd.read_csv(
#     filepath_or_buffer="XXX", index_col=0)

# create a dash application
app = dash.Dash(__name__)

# fill the layout
app.layout = html.Div(
    children=[
        html.H1(
            children="APP Title",
            style={}
        ),
        html.Div(
            [],
            style={}
        ),
        html.Br(),
        html.Br(),
        # graph
        html.Div(
            [
                dcc.Graph(id="plot-id")
            ]
        ),
    ]
)
# create the callback function to plot the graph


@ app.callback(
    Output(component_id="plot-id", component_property="figure"),
    Input()
)
def getGraph():
    # select the data

    # plot the figure

    # return the fig
    return


# run the app
if __name__ == "__main__":
    app.run_server()
