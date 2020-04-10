###############################################################################
#                                MAIN                                         #
###############################################################################

# Setup
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from settings import config
from python.data import Data



# App Instance
app = dash.Dash(name=config.name, assets_folder=config.root+"/application/static", external_stylesheets=[dbc.themes.LUX, config.fontawesome])
app.title = config.name



# Navbar
navbar = dbc.Nav(className="nav nav-pills", children=[
    ## logo/home
    dbc.NavItem(html.Img(src=app.get_asset_url("logo.PNG"), height="40px")),
    ## about
    dbc.NavItem(dbc.NavLink("How it works", href="/about", id="link-about")),
    ## links
    dbc.DropdownMenu(label="Links", nav=True, children=[
        dbc.DropdownMenuItem([html.I(className="fa fa-linkedin"), "  Contacts"], href=config.contacts, target="_blank"), 
        dbc.DropdownMenuItem([html.I(className="fa fa-github"), "  Code"], href=config.code, target="_blank")
    ])
])



# Input Data
inputs_data = dbc.Card(body=True, children=[
    dbc.FormGroup([
        dbc.Label("STOCK"),
        dbc.FormText("Yahoo Finance Symbol", color="secondary"), dbc.Input(id="stock-symbol", placeholder="AAPL"),
        dbc.FormText("Variable", color="secondary"), dcc.Dropdown(id="stock-variable", options=[{"label":col, "value":col} for col in ["Open","High","Low","Close","Volume"]], value="Close"),
        dbc.FormText("From Date", color="secondary"), dbc.Input(id="stock-from", placeholder="2020-01-31"),
        dbc.FormText("To Date", color="secondary"), dbc.Input(id="stock-to", placeholder="YYYY-MM-DD")
    ]),
    dbc.Button("Get Data", color="primary", size="sm", id="button-data", n_clicks=0)
]) 



# Input Model
inputs_model = dbc.Card(body=True, children=[
    dbc.FormGroup([
        dbc.Label("FORECASTER"),
        dbc.FormText("model complexity", color="secondary"), dcc.Slider(id="model-neurons", min=1, max=10, step=1, value=3),
        dbc.FormText("days ahead to forecast", color="secondary"), dbc.Input(id="model-ahead", placeholder=5)
    ]),
    dbc.Button("Forecast", color="primary", size="sm", id="button-model", n_clicks=0)
])



# App Layout
app.layout = dbc.Container(fluid=True, children=[
    ## Top
    html.H1(config.name, id="nav-pills"),
    navbar,
    html.Br(),

    ## Body
    dbc.Row(align="center", children=[
        ### inputs
        dbc.Col(dbc.Row([inputs_data, inputs_model]), md=3),
        ### plot
        dbc.Col(dcc.Graph(id="output-plot"), md=9)
    ])
])



# Python Function
@app.callback(output=Output("output-plot","figure"), 
              inputs=[Input("button-data","n_clicks")], 
              state=[State("stock-symbol","value"), State("stock-variable","value"), State("stock-from","value"), State("stock-to","value")])
def plot_output(n_clicks, symbol, variable, from_str, to_str):
    ## when app starts
    if (n_clicks == 0):
        if (symbol is None) and (from_str is None) and (to_str is None):
            symbol, variable, from_str, to_str = "AAPL", "Close", "2020-01-31", ""
            data = Data(symbol, variable, from_str, to_str)
            data.get_data()
            return data.plot_data()

    ## when button is clicked
    elif (n_clicks > 0):
        data = Data(symbol, variable, from_str, to_str)
        data.get_data()
        return data.plot_data()



