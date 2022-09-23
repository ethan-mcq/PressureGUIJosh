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
            ], body="true"), width={"size": 6, "offset": 3})
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
                    style={'margin': '15px', 'display': 'inline-block'}),
                dbc.Button("Query Site", id="query", color="primary", style={"margin": "5px"},
                           n_clicks=0)
            ], body="true"),
            html.Hr(),
            dbc.Card([
                html.P("Selected Outlier"),
                dcc.Markdown("""
                    **Click Data**

                    Click on points in the graph.
                """),
                html.Pre(id='selected')
            ], body="true")
        ], width=3),
        dbc.Col(
            dbc.Card(
                dcc.Graph(id='indicator-graphic')), width=6)
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
