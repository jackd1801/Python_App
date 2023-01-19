# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output
import CPI_Functions as cpi
import calendar
import plotly.express as px

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
data = cpi.cpi_data('CPI_time_series_December_2022.xls')

##Layout section with components to be displayed
#Create list options for the data


app.layout = html.Div(children=[
    html.H1(children='CPI Dashboard'),
    html.Label('Select item'),
    dcc.Dropdown(Index, id='inflation', multi=False, value=Index[0]),
    html.Label('Select month'),
    dcc.Dropdown(Months, id='month', multi=False, placeholder="All"),
    html.Label('Select geography'),
    dcc.Checklist(options=data.Level.unique(),
                  value=data.Level.unique(),
                  inline=True,
                  id='geography'),
    html.Label('Select range'),
    dcc.RangeSlider(min=min(Years),
                    max=max(Years),
                    step=1,
                    value=[min(Years), max(Years)],
                    marks=Year_marks,
                    id='years_chosen'),
    dcc.Graph(
        id='fig',
        figure={}
    )
])


@app.callback(
    [Output(component_id='fig', component_property='figure')],
    [Input(component_id='inflation', component_property='value'),
     Input(component_id='month', component_property='value'),
     Input(component_id='years_chosen', component_property='value'),
     Input(component_id='geography', component_property='value')]
)
def update_graph(inflation, month, years_chosen, geography):
    dff = data.copy()
    if month not in Months:
        dff = dff
    else:
        dff = dff[dff['Month']==month]
    dff = dff[dff['Level'].isin(geography)]
    dff = dff.loc[dff["Index"] == inflation]
    fig = px.line(dff, x="Date", y="CPI", title="{}".format(inflation), color="Level",
                  labels={"Date": "", "CPI": "CPI", "Level": "Geography"})
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5
    ),
        title={'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'}
    )
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
