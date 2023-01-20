import calendar

import plotly.express as px
from dash import Dash, html, dcc, Input, Output
import CPI_Functions as cpi
import dash_bootstrap_components as dbc

# Import data - use the latest version of the CPI time series data found here:


# Pre-define the drop-down values


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

data = cpi.cpi_data('CPI_time_series_December_2022.xls')
Index = data.Index.unique()
Months = calendar.month_name[1:]
Years = data['Date'].dt.year.unique().tolist()
Year_marks = {i: str(i) for i in Years}

description_text = "This dashboard presents the trend of Consumer Prices Index (CPI). <br><br> 1. Use Select Item to see the CPI for a specific product. <br> 2. Use Select Month to visualise monthly or yearly trends for each item. <br> 3. Select Location to visualize different regions of Rwanda."

intro_text = "This dashboard presents the trend of Consumer Prices Index (CPI)."

intro_text1 = "1. Use Select Item to see the CPI for a specific product."

intro_text2 = "2. Use Select Month to visualise monthly or yearly trends for each item."

intro_text3 = "3. Select Location to visualize different regions of Rwanda."

index_dropdown = dcc.Dropdown(Index,
                              id='inflation',
                              multi=False,
                              value=Index[0],
                              clearable=False)

months_dropdown = dcc.Dropdown(Months,
                               id='month',
                               multi=False,
                               placeholder="All")

geography_checklist = dcc.Checklist(options=data.Level.unique(),
                                    value=data.Level.unique(),
                                    inline=True,
                                    id='geography')

years_slider = dcc.RangeSlider(min=min(Years),
                               max=max(Years),
                               step=1,
                               value=[min(Years), max(Years)],
                               marks=Year_marks,
                               id='years_chosen')

##Create app layout and callback functions

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1('CPI Dashboard', className="text-center"), width=12)]),
    dbc.Row([
        dbc.Col([html.Div(intro_text),
                html.Div(intro_text1),
                html.Div(intro_text2),
                html.Div(intro_text3)], width=6),
        dbc.Col([index_dropdown, 
                 months_dropdown, 
                 geography_checklist,
                years_slider], 
                    width=6)]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='fig'), width=12)])
], fluid=False)

@app.callback(
    Output('fig', 'figure'),
    Input('inflation', 'value'),
    Input('month', 'value'),
    Input('geography', 'value'),
    Input('years_chosen', 'value'))
def update_graph(inflation, month, geography, years_chosen):
    dff = cpi.cpi_clean(data, month, geography, years_chosen, inflation)
    fig = cpi.cpi_plot(dff, inflation)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
