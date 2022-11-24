# import the necessary libraries
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from dash import dash, dcc, html, Input, Output

# Add Dataframe
df = pd.read_csv(filepath_or_buffer="/Users/sylvain/Data Science/Coursera IBM-Data-Science-Professional-Certificate/Course 8 Data Visualization/4.8_practice_assigment/assets/automobileEDA.csv")
# Clean the DataFrame
df = df[df.loc[:, "price"] != "?"]
df["price"] = df["price"].astype(int)

# create a dash application
app = dash.Dash(__name__)

# fill the layout
app.layout = html.Div(
    children=[
        # title of the app
        html.H1(
            children="Car Automobile Components",
            style={"text-align": "center"}
        ),
        html.P(
            "This is a Dashboard that I made myself!",
            id="testID"
        ),
        # dropdown
        html.Div(
            dcc.Dropdown(
                id="wheel-drive",
                options=[
                    {"label": "Rear wheel Drive", "value": "rwd"},
                    {"label": "Four wheel Drive", "value": "4wd"},
                    {"label": "Front wheel Drive", "value": "fwd"}
                ],
                value="fwd"
            )),

        # the two graphs
        html.Div(
            children=[
                dcc.Graph(id="pie-chart"),
                dcc.Graph(id="bar-plot")
            ],
            id="flex-graph"
        )
    ]
)


# create the callback function
@ app.callback(
    [
        Output(component_id="pie-chart", component_property="figure"),
        Output(component_id="bar-plot", component_property="figure")
    ],
    Input(component_id="wheel-drive", component_property="value")
)
def getGraph(wd="fwd"):

    data = df.groupby(["drive-wheels", "body-style"]).mean().reset_index()
    pie_fig = px.pie(
        data_frame=data[data.loc[:, "drive-wheels"] == wd],
        values="price",
        names="body-style",
        title="Pie Chart"
    )

    bar_fig = px.bar(
        data_frame=data[data.loc[:, "drive-wheels"] == wd],
        x="body-style",
        y="price",
        title="Bar plot"
    )
    # return the fig
    return [pie_fig, bar_fig]


# run the app
if __name__ == "__main__":
    app.run_server()
