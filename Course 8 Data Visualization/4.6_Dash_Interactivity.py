import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from dash import dash, dcc, html, Input, Output

# import the dataset
airline_data = pd.read_csv(
    filepath_or_buffer="datasets/airline.csv", index_col=0)

# create a dash application
app = dash.Dash(__name__)

# fill the layout
app.layout = html.Div(
    children=[
        html.H1(
            children="Airline Dash Interactivity",
            style={
                "textAlign": "center",
                "color": "#503D36",
                "font-size": 40
            }
        ),
        html.Div(
            [
                "Input Year",
                dcc.Input(
                    id="input-year",
                    value=2015,
                    type="number",
                    style={
                        "height": "40px",
                        "font-size": 40
                    }
                ),
            ],
            style={"font-size": 35}
        ),
        html.Br(),
        html.Br(),
        html.Div(
            [
                dcc.Graph(id="line-plot")
            ]
        ),
    ]
)

# add a callback decorator


@app.callback(
    Output(component_id="line-plot", component_property="figure"),
    Input(component_id="input-year", component_property="value")
)
# add computation to callback function and return Graph-output
def getGraph(inputYear=2010):
    # select the data from the given year
    df = airline_data[airline_data["Year"] == int(inputYear)]

    # group the data by month and compute average arrival delay
    lineData = df.groupby("Month")["ArrDelay"].mean().reset_index()

    # plot the figure
    fig = px.scatter(
        data_frame=lineData,
        x="Month",
        y="ArrDelay",
        #   mode="lines",
        #   marker={"color": "green"}
    )

    fig.update_layout(
        title="Month vs. Average Flight Delay Time",
        xaxis_title="Month",
        yaxis_title="Average Delay"
    )

    return fig


if __name__ == "__main__":
    app.run_server()
