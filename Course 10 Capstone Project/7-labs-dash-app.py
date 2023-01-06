# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("datasets/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create the options for the dropdown
dropdownOptions = [{"label": "All Sites", "value": "All"}]
sites = pd.unique(spacex_df.loc[:, "Launch Site"])
# loop through the sites options
for site in sites:
    newSite = {"label": site, "value": site}
    dropdownOptions.append(newSite)
del sites

# Create an app layout
app.layout = html.Div(children=[
    html.H1(
        'SpaceX Launch Records Dashboard',
        style={
            'textAlign': 'center', 'color': '#503D36',
            'font-size': 40
        }
    ),
    # TASK 1: Add a dropdown list to enable Launch Site selection
    # The default select value is for ALL sites
    dcc.Dropdown(
        id='site-dropdown',
        options=dropdownOptions,
        value="All",
        placeholder="Select a launch Site",
        searchable=True
    ),

    html.Br(),

    # TASK 2: Add a pie chart to show the total successful launches count for all sites
    # If a specific launch site was selected, show the Success vs. Failed counts for the site
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),
    # TASK 3: Add a slider to select payload range
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        marks={0: "0", 2500: "2500", 5000: "5000",
               7500: "7500", 10000: "10000"},
        value=[
            spacex_df.loc[:, "Payload Mass (kg)"].min(),
            spacex_df.loc[:, "Payload Mass (kg)"].max()
        ]
    ),

    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    html.Div(
        dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output


@app.callback(
    Output(
        component_id="success-pie-chart",
        component_property="figure"
    ),
    Input(
        component_id="site-dropdown",
        component_property="value"
    )
)
def renderPieChart(launchSite):
    if launchSite == "All":
        pieChart = px.pie(
            data_frame=spacex_df,
            values="class",
            names="Launch Site",
            title="Successful launches for all sites"
        )

    else:
        pieChart = px.pie(
            data_frame=spacex_df.loc[
                spacex_df.loc[:, "Launch Site"] == launchSite, :
            ],
            names="class",
            title=f"Success Rate for {launchSite}"
        )

    return pieChart


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id="success-payload-scatter-chart",
           component_property="figure"),
    [
        Input(component_id="site-dropdown", component_property="value"),
        Input(component_id="payload-slider", component_property="value")
    ]
)
def renderScatterPlot(launchSite, payloadRange):
    if launchSite == "All":
        df = spacex_df
    else:
        df = spacex_df.loc[
            spacex_df.loc[:, "Launch Site"] == launchSite, :
        ]
    df = df.loc[
        df.loc[:, "Payload Mass (kg)"].between(left=payloadRange[0], right=payloadRange[1]), :
    ]
    scatterPlot = px.scatter(
        data_frame=df,
        title="Correlation between Payload and launch succes",
        color="Booster Version Category",
        x="Payload Mass (kg)",
        y="class",
        labels={
            "class": "Outcome of the launch",
            "Payload Mass (kg)": "Payload Mass (in kg)"
        }
    )

    scatterPlot.update_yaxes(
        nticks=2,
        tickvals=[0, 1],
        ticktext=["Failed Lauch", "Successfull launch"]
    )

    return scatterPlot


# Run the app
if __name__ == '__main__':
    app.run_server()
