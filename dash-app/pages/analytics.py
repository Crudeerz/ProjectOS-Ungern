import pandas as pd
import plotly.express as px 
from dash import Dash, html, dcc, callback, Input, Output, register_page
from dash.dash_table import DataTable
import dash_bootstrap_components as dbc


# Read in datasets to dataframes for visual overview on first page
df_events = pd.read_csv("../Data/athlete_events.csv")
df_regions = pd.read_csv("../Data/noc_regions.csv")



###################### DASH APP ########################
register_page(__name__)


layout = dbc.Container(fluid=False, children=[

###################### HEADING ########################
    dbc.Row(justify="center", children=[
        dbc.Col(
            children = [
            html.H2("Visualiseringar"),
            ],
            class_name="mt-5 text-center",
            xs=12,sm=12, md=12, lg=12

        )

    ]),

    dbc.Row(justify="center", children=[
        dbc.Col(
            children = [
                dbc.Label(id="label_1", children="Graph1"), 
                dbc.Input(id="input_1", placeholder="Antal länder: ", type="integer"),
                dcc.Graph(id="graph_1", className="mt-2", figure={})
            ],
            class_name="mt-2 mx-auto",
            xs=12,sm=12, md=6, lg=6

        ), 
        dbc.Col(
            children = [
                dbc.Label(id="label_2", children="Graph2"),
                dbc.Input(id="input_2", placeholder="Antal länder att visa: ", type="integer"),
                dcc.Graph(className="mt-2", id="graph_2", figure={})
            ],
            class_name="mt-2 mx-auto",
            xs=12,sm=12, md=6, lg=6

        ),
        
        

    ]),

    dbc.Row(justify="center", children=[
        dbc.Col(
            children = [
                dbc.Label(id="label_3", children="Graph3"),
                dcc.Dropdown(["Bronze","Silver","Gold"], "Total", 
                             id="drop_3",                              
                             className="text-secondary-emphasis"),
                dcc.Graph(className="mt-2", id="graph_3", figure={})
            ],
            class_name="mt-2 mx-auto",
            xs=12,sm=12, md=6, lg=6

        ), 
        dbc.Col(
            children = [
                dbc.Label(id="label_4", children="Graph4", class_name="text-center"),
                dbc.Input(id="input_4", placeholder="Antal länder: ", type="integer"),
                dcc.Graph(className="mt-2", id="graph_4", figure={})
            ],
            class_name="mt-2 mx-auto",
            xs=12,sm=12, md=6, lg=6

        ),
        
        

    ]),




])


@callback(
    Output("graph_1", "figure"),
    Input("input_1", "value"),

)
def set_num_of_countries(num):

    if num is None:
        num = 10
    num = int(num)
    
    countries = df_events.groupby("NOC").agg({"Medal": "count"}).sort_values(by="Medal", ascending=False)
    graph = px.bar(countries.head(num), y="Medal",
             template="seaborn",
             labels=dict(Medal = "Antal medaljer", Team = "Land"), 
             title=f"Flest medaljer tagna (Top {num})")

    return graph


@callback(
    Output("graph_2", "figure"),
    Input("input_2", "value"),
)
def set_num_of_countries_2(num):
    if num is None:
        num = 5
    num = int(num)
    countries = df_events.groupby("NOC").agg({"Medal": "count"}).sort_values(by="Medal", ascending=False)
    graph = px.bar(countries.head(num), y="Medal",
             template="seaborn",
             labels=dict(Medal = "Antal medaljer", Team = "Land"), 
             title=f"Flest medaljer tagna (Top {num})")

    return graph

@callback(
    Output("graph_3", "figure"),
    Input("drop_3", "value"),
)
def show_medal_dispersion(medal):
    medal_not_none = df_events[df_events["Medal"].notna()]
    medal_counts = medal_not_none.groupby(['NOC', 'Medal']).size().unstack().fillna(0)
    medal_counts['Total'] = medal_counts.sum(axis=1)


    graph_3 = px.bar(medal_counts, y=f"{medal}")
    
    return graph_3