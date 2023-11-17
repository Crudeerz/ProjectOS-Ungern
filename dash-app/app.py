import pandas as pd
from dash import Dash, html, dcc, page_container
import dash_bootstrap_components as dbc


# Read in datasets to dataframes for visual overview on first page
df_events = pd.read_csv("./Data/athlete_events.csv")
df_regions = pd.read_csv("./Data/noc_regions.csv")



###################### DASH APP ########################
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY], 
           meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}], use_pages=True)


app.layout = dbc.Container(fluid=False, children=[

###################### HEADING ########################
    dbc.Row(justify="center", children=[
        dbc.Col(
            dbc.DropdownMenu(label="Menu",
                children=[
                        dbc.DropdownMenuItem("Hem", href="/"),
                        dbc.DropdownMenuItem("Analytics", href="analytics")
                        ]),
        ),
        page_container
    ])
])






if __name__ == "__main__":
    app.run(debug=True)