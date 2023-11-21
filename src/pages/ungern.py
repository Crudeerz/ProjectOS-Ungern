import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, callback, Input, Output, register_page
from dash.dash_table import DataTable
import dash_bootstrap_components as dbc


# Read in datasets to dataframes for visual overview on first page
df_events = pd.read_csv("../Data/athlete_events.csv")
df_regions = pd.read_csv("../Data/noc_regions.csv")

df_hungarian_events = df_events.loc[df_events["NOC"] == "HUN"]


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
                        html.H2("Visualiseringar Ungern"),
                    ],
                    class_name="mt-5 text-center",
                    xs=12,
                    sm=12,
                    md=12,
                    lg=12,
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
                    class_name="mt-0 mx-auto",
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
                                        dbc.Label("Filtrera på:", class_name="fw-bold"),
                                        dcc.Dropdown(
                                            ["Ungern", "Hela"],
                                            "Ungern",
                                            id="u_drop_1",
                                            className="text-secondary-emphasis",
                                        ),
                                    ],
                                    width=2,
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Årsperiod:", class_name="fw-bold"),
                                        dcc.RangeSlider(
                                            id="u_slider_1",
                                            step=10,
                                            min=1896,
                                            max=2023,
                                            marks={
                                                i: str(i) for i in range(1896, 2023, 20)
                                            },
                                            className="mt-3",
                                            value=[1896, 2024],
                                        ),
                                    ],
                                    width=10,
                                ),
                            ],
                            style={"justify-content": "center"},
                        ),
                        dcc.Graph(id="u_graph_1", className="mt-2", figure={}),
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
                    class_name="my-auto mx-auto",
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
                                        dbc.Label("Filtrera på:", class_name="fw-bold"),
                                        dcc.Dropdown(
                                            ["Ungern", "Alla"],
                                            "Ungern",
                                            id="u_drop_2a",
                                            className="text-secondary-emphasis",
                                        ),
                                    ]
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Medaljtyp:", class_name="fw-bold"),
                                        dcc.Dropdown(
                                            ["Alla", "Gold", "Silver", "Bronze"],
                                            "Alla",
                                            id="u_drop_2b",
                                            className="text-secondary-emphasis",
                                        ),
                                    ]
                                ),
                            ]
                        ),
                        dcc.Graph(className="mt-2", id="u_graph_2", figure={}),
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
                    md=2,
                    lg=2,
                ),
                dbc.Col(
                    children=[
                        dbc.Row(
                            children=[
                                dbc.Col(
                                    [
                                        dbc.Label("Filtrera på:", class_name="fw-bold"),
                                        dcc.Dropdown(
                                            ["Ungern", "Alla"],
                                            "Ungern",
                                            id="u_drop_3a",
                                            className="text-secondary-emphasis",
                                        ),
                                    ],
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label("Medaljtyp:", class_name="fw-bold"),
                                        dcc.Dropdown(
                                            ["Alla", "Bronze", "Silver", "Gold"],
                                            "Alla",
                                            id="u_drop_3b",
                                            className="text-secondary-emphasis",
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        dcc.Graph(className="my-3", id="u_graph_3", figure={}),
                    ],
                    class_name="mt-2 mx-auto",
                    xs=12,
                    sm=12,
                    md=10,
                    lg=10,
                ),
            ],
        ),
    ],
)

MEDAL_COLOR_MAP = {
    "Gold": "rgb(255, 200, 0)",
    "Silver": "rgb(180, 180, 180)",
    "Bronze": "rgb(180, 110, 0)",
}


@callback(
    Output("u_graph_1", "figure"),
    Input("u_drop_1", "value"),
    Input("u_slider_1", "value"),
)
def avergage_age_of_medal_winners(dataset_string, years):
    min_year, max_year = years

    dataset = df_hungarian_events if dataset_string == "Ungern" else df_events

    dataset = dataset.query("@min_year <= Year <= @max_year")

    fig = px.line(
        dataset.groupby("Year")["Age"].mean().reset_index(),
        x="Year",
        y="Age",
        title=f"Genomsnittlig ålder av medaljvinnare över tid ({min_year} - {max_year})",
    )
    fig.update_layout(
        xaxis_title="År",
        yaxis_title="Genomsnittlig ålder",
    )

    return fig


@callback(
    Output("u_graph_2", "figure"),
    Input("u_drop_2a", "value"),
    Input("u_drop_2b", "value"),
)
def number_of_medals_per_age(dataset_string, medal):
    dataset = df_hungarian_events if dataset_string == "Ungern" else df_events

    medals = ["Gold", "Silver", "Bronze"]
    df_medal = dataset if medal not in medals else dataset.query("Medal == @medal")

    fig = px.histogram(
        df_medal,
        x="Age",
        color="Medal",
        title="Antal medaljer per åldersgrupp",
        color_discrete_map=MEDAL_COLOR_MAP,
    )
    fig.update_layout(
        yaxis_title="Antal medaljer",
        xaxis_title="Ålder",
        legend_title_text="Medaljer",
    )

    return fig


@callback(
    Output("u_graph_3", "figure"),
    Input("u_drop_3a", "value"),
    Input("u_drop_3b", "value"),
)
def average_age_per_sport(dataset_string, medal):
    dataset = df_hungarian_events if dataset_string == "Ungern" else df_events

    medals = ["Gold", "Silver", "Bronze"]
    df_medal = dataset if medal not in medals else dataset.query("Medal == @medal")

    fig = px.bar(
        df_medal.groupby(["Sport", "Medal"])["Age"].mean().reset_index(),
        x="Sport",
        y="Age",
        color="Medal",
        title="Genomsnittlig ålder för medaljtyp per sport",
        color_discrete_map=MEDAL_COLOR_MAP,
    )
    fig.update_layout(
        yaxis_title="Genomsnittlig ålder" if medal in medals else "",
    )

    return fig
