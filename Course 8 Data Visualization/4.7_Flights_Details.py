# import the necessary libraries
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from dash import dash, dcc, html, Input, Output

# load the data
AIRLINE_DATA = pd.read_csv(
    filepath_or_buffer="datasets/airline.csv", index_col=0)

# create the app
app = dash.Dash(__name__)

# build the app layout
app.layout = html.Div(children=[
    # Title of the Dashboard
    html.H1(
        "Flight Details Statistics Dashboard",
        style={
            "text-align": "center",
            "color": "#503D36",
            "font-size": 35,
        }
    ),
    # First Component: User input
    html.Div(
        [
            "Input Year: ",
            dcc.Input(
                id="input-year",
                value=2010,
                type="number",
                style={
                    "height": "35px",
                    "font-size": 30
                }
            )
        ],
        style={"font-size": 30}
    ),
    html.Br(),
    html.Br(),
    # Second Component: first row of output
    html.Div(
        [
            # first graph
            html.Div(
                dcc.Graph(id="carrier-plot")
            ),
            # second graph
            html.Div(
                dcc.Graph(id="weather-plot")
            )
        ],
        style={"display": "flex"}
    ),
    # second row of Graphs
    html.Div(
        [
            html.Div(
                dcc.Graph(id="nas-plot")
            ),
            html.Div(
                dcc.Graph(id="security-plot")
            )
        ],
        style={"display": "flex"}
    ),
    html.Div(
        dcc.Graph(id="late-plot"),
        style={"width": "65%"}
    )
])

# compute the data for a given year


def get_data(data=AIRLINE_DATA, year=2010):
    return data[data["Year"] == year].groupby(["Month", "Reporting_Airline"])


@app.callback(
    [
        Output(component_id="carrier-plot", component_property="figure"),
        Output(component_id="weather-plot", component_property="figure"),
        Output(component_id="nas-plot", component_property="figure"),
        Output(component_id="security-plot", component_property="figure"),
        Output(component_id="late-plot", component_property="figure"),
    ],
    Input(component_id="input-year", component_property="value")
)
def get_graph(inputYear):
    # compute the values needed for the figures
    df = get_data(year=inputYear)

    # plot the first figure
    avg_carrier_delay = df["CarrierDelay"].mean().reset_index()
    carrier_fig = px.line(
        avg_carrier_delay,
        x="Month",
        y="CarrierDelay",
        color="Reporting_Airline",
        title="Average carrier delay time (in minutes) by airlines"
    )

    # plot the second figure
    avg_weather_delay = df["WeatherDelay"].mean().reset_index()
    weather_fig = px.line(
        avg_weather_delay,
        x="Month",
        y="WeatherDelay",
        color="Reporting_Airline",
        title="Average weather delay time (in minutes) by airlines"
    )

    # plot the third figure
    avg_NAS_delay = df["NASDelay"].mean().reset_index()
    nas_fig = px.line(
        avg_NAS_delay,
        x="Month",
        y="NASDelay",
        color="Reporting_Airline",
        title="Average NAS delay time (in minutes) by airlines"
    )
    avg_security_delay = df["SecurityDelay"].mean().reset_index()
    security_fig = px.line(
        avg_security_delay,
        x="Month",
        y="SecurityDelay",
        color="Reporting_Airline",
        title="Average security delay time (in minutes) by airlines"
    )

    avg_late_delay = df["LateAircraftDelay"].mean().reset_index()
    late_fig = px.line(
        avg_late_delay,
        x="Month",
        y="LateAircraftDelay",
        color="Reporting_Airline",
        title="Average late aircraft delay time (in minutes) by airlines"
    )

    return [carrier_fig, weather_fig, nas_fig, security_fig, late_fig]


    # run the app if this script is executed
if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=80)
