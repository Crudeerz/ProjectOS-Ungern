import pandas as pd
import plotly.express as px 
from dash import Dash, html, dcc, callback, Input, Output, register_page
from dash.dash_table import DataTable
import dash_bootstrap_components as dbc


# Read in datasets to dataframes for visual overview on first page
df_events = pd.read_csv("./Data/athlete_events.csv")
df_regions = pd.read_csv("./Data/noc_regions.csv")



###################### DASH APP ########################
register_page(__name__)


layout = dbc.Container(fluid=False, children=[

###################### HEADING ########################
    dbc.Row(justify="center", children=[
        dbc.Col(
            children = [
            html.H1("Visualiseringar"),
            ],
            class_name="mt-5 text-center",
            xs=12,sm=12, md=12, lg=12

        )

    ])
])
