import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, callback, Input, Output, register_page
from dash.dash_table import DataTable
import dash_bootstrap_components as dbc
import hashlib as hl


# Read in datasets to dataframes for visual overview on first page
df_events = pd.read_csv("../Data/athlete_events.csv")
df_regions = pd.read_csv("../Data/noc_regions.csv")

df_events_table = df_events.drop(columns=["ID", "Name"]).head(50)


###################### DASH APP ########################
register_page(__name__, path="/")


layout = dbc.Container(
    fluid=False,
    children=[
        ###################### HEADING ########################
        dbc.Row(
            justify="center",
            children=[
                dbc.Col(
                    children=[
                        html.H1("Data-analys Olympiska Spelen"),
                    ],
                    class_name="mt-5 text-center",
                    xs=12,
                    sm=12,
                    md=12,
                    lg=12,
                )
            ],
        ),
        ###################### SAMMANFATTNING ########################
        dbc.Row(
            justify="center",
            children=[
                dbc.Col(
                    children=[
                        html.H5(
                            """Välkommen till vår Dash-app! 
                            Vi har analyserat över 120 års olympisk data, 
                            med extra fokus på Ungern. Utforska våra visualiseringar 
                            för att få en djupare förståelse av Ungerns unika bidrag till OS-historien."""
                        ),
                        dcc.Link(
                            target="_blank",
                            title="athletes_events.csv / noc_regions.csv",
                            children="Länk till Dataseten (Kaggle)",
                            href="https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results/data",
                        ),
                    ],
                    class_name="mt-2 text-center",
                    xs=12,
                    sm=12,
                    md=8,
                    lg=8,
                )
            ],
        ),
        ###################### HEADING DATASET ########################
        dbc.Row(
            justify="center",
            children=[
                dbc.Col(
                    children=[
                        html.H4(
                            """Nedan kan man se ett urval från 
                                dataseten vi har arbetat med """,
                        ),
                    ],
                    class_name="mt-5 text-center ",
                    xs=12,
                    sm=12,
                    md=12,
                    lg=12,
                )
            ],
        ),
        dbc.Row(
            justify="center",
            children=[
                ###################### EVENTS TABLE ########################
                dbc.Col(
                    children=[
                        dbc.Label(
                            "Kolumnerna Namn och ID, är bortfiltrerade från: athletes_events.csv",
                            class_name="fst-italic",
                        ),
                        DataTable(
                            df_events_table.to_dict("records"),
                            [{"name": i, "id": i} for i in df_events_table.columns],
                            sort_action="native",
                            page_size=12,
                            style_cell={
                                "overflow": "hidden",
                                "text-overflow": "hidden",
                                "maxWidth": "auto",
                            },
                            style_table={"overflowX": "auto"},
                            style_header={
                                "textAlign": "center",
                                "backgroundColor": "rgb(30, 30, 30)",
                                "color": "white",
                            },
                            style_data={
                                "textAlign": "left",
                                "backgroundColor": "rgb(50, 50, 50)",
                                "color": "white",
                            },
                        ),
                    ],
                    class_name="mt-2",
                    xs=12,
                    sm=12,
                    md=12,
                    lg=6,
                ),
                ###################### REGIONS TABLE ########################
                dbc.Col(
                    children=[
                        dbc.Label("noc_regions.csv"),
                        DataTable(
                            data=df_regions.head(50).to_dict("records"),
                            columns=[
                                {"name": col, "id": col} for col in df_regions.columns
                            ],
                            sort_action="native",
                            page_size=12,
                            style_cell={
                                "overflow": "hidden",
                                "text-overflow": "hidden",
                                "maxWidth": "auto",
                            },
                            style_table={"overflowX": "auto"},
                            style_header={
                                "textTransform": "capitalize",
                                "textAlign": "center",
                                "backgroundColor": "rgb(30, 30, 30)",
                                "color": "white",
                            },
                            style_data={
                                "textAlign": "left",
                                "backgroundColor": "rgb(50, 50, 50)",
                                "color": "white",
                            },
                        ),
                    ],
                    class_name="mt-2",
                    xs=12,
                    sm=12,
                    md=12,
                    lg=6,
                ),
            ],
        ),
    ],
)
