import pandas as pd
import plotly.express as px
import dash
from dash import html
import dash_core_components as dcc

# import the dataset
airline_data = pd.read_csv(
    filepath_or_buffer="datasets/airline.csv", index_col=0)

# randomly select 500 data points from this dataset
data = airline_data.sample(n=500, random_state=42)

# create the plotly figure
fig = px.pie(
    data_frame=data,
    values="Flights",
    names="DistanceGroup",
    title="Distance group proportion by flights"
)

# create the dash application
app = dash.Dash(__name__)

# personalize the layout of the application (title, description, graph)
app.layout = html.Div(
    children=[
        html.H1(
            "Airline Dashboard",
            style={
                "textAlign": "center",
                "color": "#503D36",
                "font-size": 40
            }
        ),
        html.P(
            "Proportion of distance group (250 Miles distance group) by flights.",
            style={
                "textAlign": "center",
                "color": "#F57241"
            }
        ),
        dcc.Graph(
            figure=fig
        )
    ]
)

# run the application
if __name__ == "__main__":
    app.run_server()
