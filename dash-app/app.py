import pandas as pd
from dash import Dash, html, dcc, page_container
import dash_bootstrap_components as dbc
import socket


###################### DASH APP ########################
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY], 
           meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}], use_pages=True)


app.layout = dbc.Container(fluid=True, children=[

###################### HEADING ########################
    dbc.Row(justify="center", children=[
        dbc.Col(children=[
            dbc.NavbarSimple(children= [               
                dbc.NavItem(dbc.NavLink("Hem", href="/")),
                dbc.NavItem(dbc.NavLink("Visualiseringar", href="analytics"))

            ], 
            color="primary",
            dark=True,
            brand="Project OS - Ungern",
            style={"justify-content":"center"}
            ),
        ]),
        page_container
    ])
])



def set_dash_host(host=None, port=None):

    '''
    Set host adress for dash application

    Parameters: 
    host (string): public for hosting app on public IP-adress
     
    Example: 
    >>> Host = "public": Dash App is hosted on your public IP-adress. 
    >>> Host = None: Dash App is hosted on localhost 127.0.0.1
    '''

    if host == "public":
        host = socket.gethostname()
        ip = socket.gethostbyname(host)
        
    else:  
        ip = "127.0.0.1" 

    return ip

dash_host = set_dash_host("public")

if __name__ == "__main__":
    app.run(debug=True, host=dash_host)