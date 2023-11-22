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
                        html.H2("Ishockey, Fäktning och Freestyle - analys"),
                    ],
                    class_name="my-5 text-center",
                    xs=12,
                    sm=12,
                    md=12,
                    lg=10,
                )
            ],
        ),
        html.Hr(),
        dbc.Row(
            justify="center",
            children=[
                dbc.Col(
                    children=[
                        html.H3("Lorem ipsum"),
                        html.P(
                            """Lorem ipsum används ofta som exempeltext 
                       inom trycksaksframställning och grafisk design 
                       för att visa hur till exempel ett dokument kommer 
                       att se ut när väl den riktiga texten är på plats"""
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
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dcc.Dropdown(
                                            [
                                                "Freestyle Skiing",
                                                "Ice Hockey",
                                                "Fencing",
                                            ],
                                            "Fencing",
                                            id="s_drop_1",
                                            className="text-secondary-emphasis",
                                        ),
                                    ],
                                    width=2,
                                ),
                                dbc.Col(
                                    dcc.RangeSlider(
                                        id="s_slider_1",
                                        step=10,
                                        min=1896,
                                        max=2023,
                                        marks={
                                            i: str(i) for i in range(1896, 2023, 20)
                                        },
                                        className="mt-2",
                                        value=[1936, 1950],
                                    ),
                                    width=10,
                                ),
                            ]
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
                        html.H3("Lorem ipsum"),
                        html.P(
                            """Lorem ipsum används ofta som exempeltext 
                                inom trycksaksframställning och grafisk design 
                                för att visa hur till exempel ett dokument kommer 
                                att se ut när väl den riktiga texten är på plats"""
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
                        html.H3("Lorem ipsum"),
                        html.P(
                            """Lorem ipsum används ofta som exempeltext 
                                inom trycksaksframställning och grafisk design 
                                för att visa hur till exempel ett dokument kommer 
                                att se ut när väl den riktiga texten är på plats"""
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
