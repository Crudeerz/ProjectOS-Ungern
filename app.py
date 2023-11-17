import pandas as pd
import plotly.express as px 
from dash import Dash, html, dcc, callback, Input, Output
from dash.dash_table import DataTable
import dash_bootstrap_components as dbc


# Read in datasets to dataframes for visual overview on first page
df_events = pd.read_csv("./Data/athlete_events.csv")
df_regions = pd.read_csv("./Data/noc_regions.csv")



###################### DASH APP ########################
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY], 
           meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])


app.layout = dbc.Container(fluid=False, children=[

###################### HEADING ########################
    dbc.Row(justify="center", children=[
        dbc.Col(
            children = [
            html.H1("Data Analys Olympiska Spelen"), 
            html.H2("Ungern")
            ],
            class_name="mt-5 text-center",
            xs=12,sm=12, md=12, lg=12

        )

    ]),

###################### SAMMANFATTNING ########################
    dbc.Row(justify="center", children=[
        dbc.Col(
            children = [
            html.H5("Välkommen till vår Dash-app! Vi har analyserat över 120 års olympisk data, med extra fokus på Ungern. Utforska våra visualiseringar för att få en djupare förståelse av Ungerns unika bidrag till OS-historien."), 
            dcc.Link(target="_blank", title="athletes_events.csv / noc_regions.csv", 
                    children="Länk till Dataseten (Kaggle)", 
                    href="https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results/data")
       
            
            ],
            class_name="mt-2 text-center",
            xs=12,sm=12, md=8, lg=8

        )

    ]),

###################### HEADING DATASET ########################
    dbc.Row(justify="center", children=[
        dbc.Col(
            children = [
            html.H4("Nedan kan du se en översikt över dataseten vi har arbetat med:"), 
            ],
            class_name="mt-5 text-center ",
            xs=12,sm=12, md=12, lg=12

        )

    ]),


###################### DATASET ÖVERSIKT ########################
    dbc.Row(justify="center", children=[
###################### EVENTS ########################
        dbc.Col(
            children = [
            dbc.Label("Fil: athletes_events.csv"),
            DataTable(
                df_events.drop(columns="ID").head(50).to_dict("records"),
                [{"name": i, "id": i} for i in df_events.drop(columns="ID").columns],
                sort_action="native",
                page_size=10, 
                style_cell={"overflow": "hidden", "text-overflow":"hidden", "maxWidth":"auto"},
                style_table={"overflowX":"auto"},
                style_header={"textAlign":"center", "backgroundColor": "rgb(30, 30, 30)", "color": "white"},
                style_data={"textAlign":"left", "backgroundColor": "rgb(50, 50, 50)", "color": "white"},
                
            ), 
            ],
            class_name="mt-2",
            xs=12,sm=12, md=12, lg=6

        ), 

###################### REGIONS ########################
        dbc.Col(
            children = [
            dbc.Label("Fil: noc_regions.csv"),
            DataTable(
                data=df_regions.head(50).to_dict("records"),
                columns=[{"name": col, "id": col} for col in df_regions.columns],
                sort_action="native",
                page_size=10, 
                style_cell={"overflow": "hidden", "text-overflow":"hidden", "maxWidth": "auto"},
                style_table={"overflowX":"auto"},
                style_header={"textTransform":"capitalize","textAlign":"center", "backgroundColor": "rgb(30, 30, 30)", "color": "white"},
                style_data={"textAlign":"left","backgroundColor": "rgb(50, 50, 50)", "color": "white"},
                
                            
            ), 
            ],
            class_name="mt-2",
            xs=12,sm=12, md=12, lg=6

        )

    ]),




])












if __name__ == "__main__":
    app.run(debug=True)