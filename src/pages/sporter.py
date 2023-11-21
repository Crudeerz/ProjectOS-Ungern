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
                dcc.Dropdown(["Freestyle Skiing","Ice Hockey", "Fencing"], "Fencing", 
                             id="s_drop_1",                              
                             className="text-secondary-emphasis"),

                dcc.RangeSlider(id="s_slider_1", step=10, min=1896, max=2023, 
                           marks={i: str(i) for i in range(1896,2023,20)},
                           className="mt-2", 
                           value=[1936, 1950]),

                dcc.Graph(className="mt-2", id="s_graph_1", figure={})
            ],

            class_name="mt-2 mx-auto",
            xs=12,sm=12, md=6, lg=6

        ), 
        dbc.Col(
            children = [                
                dbc.Input(id="s_input_2", placeholder="Antal länder att visa: ", type="integer"),
                dcc.Graph(className="mt-2", id="s_graph_2", figure={})
            ],
            class_name="mt-2 mx-auto",
            xs=12,sm=12, md=6, lg=6

        ),
        
        

    ]),

    dbc.Row(justify="center", children=[
        dbc.Col(
            children = [
                # dbc.Label(id="label_3", children="Graph3"),
                dcc.Dropdown(["Bronze","Silver","Gold"], "Total", 
                             id="s_drop_3",                              
                             className="text-secondary-emphasis"),
                dcc.Graph(className="mt-2", id="s_graph_3", figure={})
            ],
            class_name="mt-2 mx-auto",
            xs=12,sm=12, md=6, lg=6

        ), 
        dbc.Col(
            children = [
                dbc.Label(id="s_label_4", children="Graph4", class_name="text-center"),
                dbc.Input(id="s_input_4", placeholder="Antal länder: ", type="integer"),
                dcc.Graph(className="mt-2", id="s_graph_4", figure={})
            ],
            class_name="mt-2 mx-auto",
            xs=12,sm=12, md=6, lg=6

        ),
        
        

    ]),




])


@callback(
    Output("s_graph_1", "figure"),
    Input("s_drop_1", "value"),
    Input("s_slider_1", "value"),

)
def choose_sport(sport, year):
    # sport = 'Freestyle Skiing' # Valbara sporter: Fencing, Ice Hockey, Freestyle Skiing
    min_year, max_year = year


    df_top_performers = (df_events.query('Sport == @sport and @min_year <= Year <= @max_year') 
                        .groupby('Team').agg({'Medal': 'count'})
                        .sort_values('Medal', ascending=False)
                        .head(10)
                        .sort_values('Medal', ascending=True)
    )

    s_graph_1 = px.bar(df_top_performers.query('Medal > 0'),
                title=f'Länder med flest antal medaljer för {sport}, mellan {min_year}-{max_year}',
                template='seaborn',
                labels={'value': 'Antal medaljer', 'Team': 'Land', 'variable': ''},
                orientation='h'
                
    )
    return s_graph_1


@callback(
    Output("s_graph_2", "figure"),
    Input("s_input_2", "value"),
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
    Output("s_graph_3", "figure"),
    Input("s_drop_3", "value"),
)
def show_medal_dispersion(medal):
    medal_not_none = df_events[df_events["Medal"].notna()]
    medal_counts = medal_not_none.groupby(['NOC', 'Medal']).size().unstack().fillna(0)
    medal_counts['Total'] = medal_counts.sum(axis=1)


    graph_3 = px.bar(medal_counts, y=f"{medal}")
    
    return graph_3