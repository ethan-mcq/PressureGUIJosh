# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html, dash_table
from dash.dependencies import Output, Input, State
import dash_bootstrap_components as dbc
import plotly.express as px
import json
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import sqlite3
from run_query import get_pressure, get_discharge

# Declare the database file name here
db_name = "copy.db"

app = Dash(external_stylesheets=[dbc.themes.FLATLY])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            dbc.Card([
                html.H2("Abbott Lab GUI"),
                html.H5("Coolness overload")
            ], body="true", color="light"), width={"size": 10, "offset": 1})
    ]),
    html.Hr(),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.H5("Run Site Query"),
                html.P("Site ID:"),
                dcc.Dropdown(
                    options=['BEN', 'BLI', 'BSL', 'CLE', 'CRB', 'DAI', 'DFF', 'DFL', 'DFM', 'DFU', 'HCL',
                             'HCN', 'HCS', 'IND', 'LAK', 'LDF', 'MIT', 'NEB', 'PBC', 'SBL', 'SFL', 'SHE',
                             'SOL', 'STR', 'TCU', 'TIE', 'WAN'],
                    value='BEN',
                    id='site_id',
                    style={'display': 'inline-block',"margin": "5px"}),
                dbc.Button("Query Site", id="query", color="primary", style={'display': 'inline-block', "margin": "5px"},
                           n_clicks=0)
            ], body="true", color="light"),
            html.Hr(),
            dbc.Card([
                dbc.Button("Delete", id="delete", color="primary",
                           style={'display': 'inline-block', "margin": "5px"},
                           n_clicks=0),
                dbc.Button("Move Up", id="moveUp", color="primary",
                           style={'display': 'inline-block', "margin": "5px"},
                           n_clicks=0),
                dbc.Button("Move Down", id="moveDown", color="primary",
                           style={'display': 'inline-block', "margin": "5px"},
                           n_clicks=0),
                dbc.Button("Export Data", id="exportDF", color="primary",
                           style={'display': 'inline-block', "margin": "5px"},
                           n_clicks=0),
            ], body="true", color="light")
        ], width=2),
        dbc.Col(
            dbc.Card(
                dcc.Graph(id='indicator-graphic'), body='True', color="light"), width=10)
    ]),
    html.Hr(),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dcc.Markdown("""
                    **Click Data**
            
                    Click on a point from the graph to display more about that observation.
                """),
                html.Pre(id='selected'),
            ], body="true", color="light")
        ], width=2),
        dbc.Col([
            dbc.Card([
                dcc.Markdown("""
                    *TABLE HERE*
                """),
            ], body="true", color="light")
        ], width=10)
    ])
])


@app.callback(
    Output('indicator-graphic', 'figure'),
    Input('query', 'n_clicks'),
    State('site_id', 'value'))
def main_query(n_clicks, site_id):
    # Opening the database file
    print(f"button clicked {n_clicks} times")
    if db_name.endswith(".db"):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()  # This object will allow queries to be ran on the database
    else:
        print("Cannot open database file")

    # SQL query on the database -- Depending on your database, this will need to be formatted
    # to fit your system requirements
    pressure_data = get_pressure(cursor, site_id)
    # discharge_data = get_discharge(cursor, site_id)

    figure = px.scatter(pressure_data, x=pressure_data.datetime, y=pressure_data.pressure_hobo,
                        color=pressure_data.batch_id)

    return figure

@app.callback(
    Output('selected', 'children'),
    Input('indicator-graphic', 'clickData'))
def display_selected(clickData):
    return json.dumps(clickData, indent=1)

if __name__ == '__main__':
    app.run_server(debug=True)
