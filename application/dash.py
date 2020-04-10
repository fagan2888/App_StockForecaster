###############################################################################
#                                MAIN                                         #
###############################################################################

# Setup
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px

from settings import config
from python.data import Data



# App Instance
app = dash.Dash(name=config.name, assets_folder=config.root+"/application/static", external_stylesheets=[dbc.themes.LUX, config.fontawesome])
app.title = config.name



# Navbar
navbar = dbc.Nav(className="nav nav-pills", children=[
    ## home
    dbc.NavItem(html.Img(src=app.get_asset_url("logo.PNG"), height="40px")),
    ## about
    dbc.NavItem(dbc.NavLink("About", href="#")),
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
    dbc.Button("Get Data", color="primary", size="sm")
]) 



# Input Model
inputs_model = dbc.Card(body=True, children=[
    dbc.FormGroup([
        dbc.Label("FORECASTER"),
        dbc.FormText("model complexity", color="secondary"), dcc.Slider(id="model-neurons", min=1, max=10, step=1, value=3),
        dbc.FormText("days ahead to forecast", color="secondary"), dbc.Input(id="model-ahead", placeholder=5)
    ]),
    dbc.Button("Forecast", color="primary", size="sm")
])



# App Layout
app.layout = dbc.Container(fluid=True, children=[

    ## App Name
    html.H1(config.name, id="nav-pills"),

    ## Top Nav
    navbar,

    # ## Logo + App Name in a Fixed Navbar
    # dbc.Navbar(children=[
    #     dbc.Row(align="center", children=[
    #         dbc.Col(html.Img(src=app.get_asset_url("logo.PNG"), height="40px")),
    #         dbc.Col(dbc.NavbarBrand(config.name, className="ml-2"))
    #     ])
    # ]),

    # html.Div(config.name, className="ml-2"),

    # ## Top Nav
    # dbc.Nav(className="nav nav-pills", children=[
    #     ### home
    #     dbc.NavItem(dbc.NavLink("Home", href="#")),
    #     ### about
    #     dbc.NavItem(dbc.NavLink("About", href="#")),
    #     ### links
    #     dbc.DropdownMenu(label="Links", nav=True, children=[
    #         dbc.DropdownMenuItem("Contact", href="https://www.linkedin.com/in/mauro-di-pietro-56a1366b/", target="_blank"), 
    #         dbc.DropdownMenuItem("Code", href="https://github.com/mdipietro09/FlaskApp_StockForecaster", target="_blank")
    #     ])
    # ]),

    
    # ## Top Navbar
    # dbc.Navbar(className="navbar navbar-expand-lg navbar-light bg-light", children=[
    #     dbc.Row(align="center", no_gutters=True, children=[
    #         ### logo
    #         dbc.Col(html.Img(src=app.get_asset_url("logo.PNG"), height="40px")),
    #         ### name
    #         dbc.Col(dbc.NavbarBrand(config.name, className="ml-2")),
    #         ### about
    #         dbc.NavItem(dbc.NavLink("About", href="#")),
    #         ### links
    #         dbc.DropdownMenu(nav=True, in_navbar=True, label="Links", className="nav-item active", children=[
    #             dbc.DropdownMenuItem("Contact", href="https://www.linkedin.com/in/mauro-di-pietro-56a1366b/", target="_blank"),
    #             dbc.DropdownMenuItem("Code", href="https://github.com/mdipietro09/FlaskApp_StockForecaster", target="_blank")
    #         ])
    #     ])
    # ]),
    html.Br(),

    ## Body
    dbc.Row(align="center", children=[
        ### inputs
        dbc.Col(dbc.Row([inputs_data, inputs_model]), md=3),
        ### plot
        dbc.Col(dcc.Graph(id="plot-output"), md=9)
    ])

])



# Callbacks
@app.callback(dash.dependencies.Output("plot-output", "figure"), [
    dash.dependencies.Input("stock-symbol", "value"),
    dash.dependencies.Input("stock-from", "value"),
    dash.dependencies.Input("stock-to", "value"),
    dash.dependencies.Input("stock-variable", "value")
])



# Python Instances
def make_graph(x, y, n_clusters):
    z = y + x * n_clusters

    fig = px.scatter(iris, x=x, y=y)

    layout = {"xaxis":{"title":x}, 
              "yaxis":{"title":y}}

    return fig