from dash import Dash, html, dcc, Input, Output
import CPI_Functions as cpi
import calendar
import plotly.express as px
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([dbc.Row([
        dbc.Col(html.H1('CPI Dashboard', className="text-center"), width=12)])])

if __name__ == '__main__':
    app.run_server(debug=True)