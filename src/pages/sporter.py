import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, callback, Input, Output, register_page
from dash.dash_table import DataTable
import dash_bootstrap_components as dbc
import plotly.graph_objects as go


# Read in datasets to dataframes for visual overview on first page
df_events = pd.read_csv("../Data/athlete_events.csv")
df_regions = pd.read_csv("../Data/noc_regions.csv")

df_events.dropna(subset=["Height", "Weight"], inplace=True)
df_events["BMI"] = df_events["Weight"] / (df_events["Height"] / 100) ** 2

###################### DASH APP ########################
register_page(__name__)


layout = dbc.Container(
    fluid=False,
    children=[
        ###################### HEADING ########################
        dbc.Row(
            justify="center",
            children=[
                dbc.Col(
                    children=[
                        html.H2("Ishockey, Fäktning och Freestyle"),
                    ],
                    class_name="my-5 text-center",
                    xs=12,
                    sm=12,
                    md=12,
                    lg=10,
                )
            ],
        ),
        dbc.Row(
            justify="center",
            children=[
                dbc.Col(
                    children=[
                        html.H3("Medaljer mellan länder i sporterna"),
                        html.P(
                            ['Fäktning:', html.Br(), 
                            'Tom. 1956: Ungern och Frankrike klar ledning', html.Br(), 
                            'Tom. 1976: Soviet och Ungern klar ledning', html.Br(), 
                            'Tom. 1996: Frankrike och Italien närmar sig ledarna', html.Br(), 
                            'Tom. 2016: Frankrike och Italien går om', html.Br(), 
                            'Ishockey:', html.Br(), 
                            'Tom. 1956: USA och Kanada klar ledning', html.Br(), 
                            'Tom. 1976: Soviet och Tjeckien går om', html.Br(), 
                            'Tom. 1996: Sverige går om USA', html.Br(), 
                            'Tom. 2016: USA går om Sverige, Finland fyra', html.Br(), 
                            'Freestyle:', html.Br(), 
                            'Tom. 1986: Inga medaljer eftersom grenen är ny', html.Br(), 
                            'Tom. 1996: Många har lika många medaljer', html.Br(), 
                            'Tom. 2016: Först här urskiljer sig en tydlig ranking. USA, Kanada och Frankrike top 3, Australien på plats 6.']
                        ),
                    ],
                    class_name="mt-2 mx-auto",
                    xs=12,
                    sm=12,
                    md=3,
                    lg=2,
                ),
                dbc.Col(
                    children=[
                        dcc.Dropdown(
                            ["Freestyle Skiing", "Ice Hockey", "Fencing"],
                            "Fencing",
                            id="s_drop_1",
                            className="text-secondary-emphasis",
                        ),
                        dcc.RangeSlider(
                            id="s_slider_1",
                            step=10,
                            min=1896,
                            max=2023,
                            marks={i: str(i) for i in range(1896, 2023, 20)},
                            className="mt-2",
                            value=[1936, 1950],
                        ),
                        dcc.Graph(className="mt-2", id="s_graph_1", figure={}),
                    ],
                    class_name="mt-2 mx-auto",
                    xs=12,
                    sm=12,
                    md=9,
                    lg=10,
                ),
            ],
        ),
        html.Hr(),
        dbc.Row(
            justify="center",
            children=[
                dbc.Col(
                    children=[
                        html.H3("Ålder mellan sporterna"),
                        html.P(
                            ['Tom. 1976: Fler tävlande och högre medelålder i fäktning än i Ishockey.', html.Br(), 
                            'Tom. 1996: Freestyle får sina första tävlande.', html.Br(),  
                            '1996 - 2016: Fäktning och ishockey ungefär lika många tävlande och liknande ålder till skillnad från tidigare.']
                        ),
                    ],
                    class_name="my-4 mx-auto",
                    xs=12,
                    sm=12,
                    md=3,
                    lg=2,
                ),
                dbc.Col(
                    children=[
                        dcc.RangeSlider(
                            id="s_slider_2",
                            step=10,
                            min=1896,
                            max=2023,
                            marks={i: str(i) for i in range(1896, 2023, 20)},
                            className="mt-2",
                            value=[1936, 1950],
                        ),
                        dcc.Graph(className="mt-2", id="s_graph_2", figure={}),
                    ],
                    class_name="mt-2 mx-auto",
                    xs=12,
                    sm=12,
                    md=9,
                    lg=10,
                ),
            ],
        ),
        html.Hr(),
        dbc.Row(
            justify="center",
            children=[
                dbc.Col(
                    children=[
                        html.H3("BMI mellan sporterna"),
                        html.P(
                             ['Tom. 1956: Ishockey och fäktning lika median BMI.', html.Br(),
                            'Första damerna till ishockey 2006. Fäktning har första damerna mycket tidigare.', html.Br(),
                            'Nyare tider tydlig skillnad på BMI mellan ishockey och fäktning till skillnad från äldre då de var lika.', html.Br(),
                            'Fäktning och freestyle liknande BMI.']
                        ),
                    ],
                    class_name="mt-2 mx-auto",
                    xs=12,
                    sm=12,
                    md=3,
                    lg=2,
                ),
                dbc.Col(
                    children=[
                        dcc.RangeSlider(
                            id="s_slider_3",
                            step=10,
                            min=1896,
                            max=2023,
                            marks={i: str(i) for i in range(1896, 2023, 20)},
                            className="mt-2",
                            value=[1936, 1950],
                        ),
                        dcc.Graph(className="mt-2", id="s_graph_3", figure={}),
                    ],
                    class_name="my-4 mx-auto",
                    xs=12,
                    sm=12,
                    md=9,
                    lg=10,
                ),
            ],
        ),
    ],
)


@callback(
    Output("s_graph_1", "figure"),
    Input("s_drop_1", "value"),
    Input("s_slider_1", "value"),
)
def choose_sport(sport, year):
    min_year, max_year = year

    df_top_performers = (
        df_events.query("Sport == @sport and @min_year <= Year <= @max_year")
        .groupby("Team")
        .agg({"Medal": "count"})
        .sort_values("Medal", ascending=True)
        .tail(10)
    )

    s_graph_1 = px.bar(
        df_top_performers.query("Medal > 0"),
        title=f"Flest antal medaljer för {sport}, mellan {min_year}-{max_year}",
        template="seaborn",
        labels={"value": "Antal medaljer", "Team": "Land", "variable": ""},
        orientation="h",
    )

    s_graph_1.update_layout(showlegend=False)

    return s_graph_1


@callback(
    Output("s_graph_2", "figure"),
    # Input("s_input_2", "value"),
    Input("s_slider_2", "value"),
)
def choose_years_2(year):
    min_year, max_year = year

    s_graph_2 = go.Figure()
    s_graph_2.add_trace(
        go.Histogram(
            x=df_events.query('Sport == "Fencing" and @min_year <= Year <= @max_year')[
                "Age"
            ]
        )
    )
    s_graph_2.add_trace(
        go.Histogram(
            x=df_events.query(
                'Sport == "Ice Hockey" and @min_year <= Year <= @max_year'
            )["Age"]
        )
    )
    s_graph_2.add_trace(
        go.Histogram(
            x=df_events.query(
                'Sport == "Freestyle Skiing" and @min_year <= Year <= @max_year'
            )["Age"]
        )
    )

    s_graph_2.update_layout(
        barmode="overlay",
        title=f"Antal tävlande (y) och ålder (x) per sport mellan {min_year}-{max_year}",
        template="seaborn",
    )

    s_graph_2.data[0].name = "Fencing"
    s_graph_2.data[1].name = "Ice Hockey"
    s_graph_2.data[2].name = "Freestyle Skiing"

    s_graph_2.update_traces(opacity=0.75)

    return s_graph_2


@callback(
    Output("s_graph_3", "figure"),
    Input("s_slider_3", "value"),
)
def choose_years_3(year):
    min_year, max_year = year

    s_graph_3 = px.box(
        df_events.query(
            '(Sport == "Ice Hockey" or Sport == "Fencing" or Sport == "Freestyle Skiing") and @min_year <= Year <= @max_year'
        ),
        x="Sport",
        y="BMI",
        color="Sex",
        title=f"BMI per sport och kön mellan {min_year}-{max_year}",
        template="seaborn",
    )

    return s_graph_3
