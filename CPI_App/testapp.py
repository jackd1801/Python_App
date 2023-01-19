import calendar

import plotly.express as px
from dash import Dash, html, dcc, Input, Output

import CPI_Functions as cpi
import dash_bootstrap_components as dbc

# Import data - use the latest version of the CPI time series data found here:


# Pre-define the drop-down values


app = Dash(__name__)

data = cpi.cpi_data('CPI_time_series_December_2022.xls')
Index = data.Index.unique()
Months = calendar.month_name[1:]
Years = data['Date'].dt.year.unique().tolist()
Year_marks = {i: str(i) for i in Years}

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

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1('CPI Dashboard', className="text-center"))]),
    dbc.Row([
        dbc.Col(index_dropdown, width=6),
        dbc.Col(months_dropdown, width=6)
    ]),
    dbc.Row([
        geography_checklist,
        years_slider,
        dcc.Graph(id='fig')])
])


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
