import pandas as pd
import numpy as np
import plotly.express as px
import calendar


def cpi_data(file):
    level = ["Urban", "Rural", "All Rwanda"]
    df_list = []
    for i in level:
        df = pd.read_excel(file, sheet_name=i, skiprows=3)
        df = df.rename(
            columns={"Unnamed: 0": "Province", "Unnamed: 1": "U_R", "Unnamed: 2": "COICOP", "Unnamed: 3": "Index"})
        df = df.drop([0, 19])
        df['Index'] = df['Index'].str.replace('v', '')
        df['Index'] = df['Index'].str.strip()
        df = df.melt(id_vars=['Province', 'U_R', 'COICOP', 'Index', 'Weights'], var_name='Date', value_name='CPI')
        df['Level'] = i
        df['Month'] = df['Date'].dt.month_name(locale='English')
        df['Year'] = df['Date'].dt.year
        df_list.append(df)
    df = pd.concat(df_list)
    return df


def cpi_clean(df, month, geography, years, inflation):
    options = calendar.month_name[1:]
    if month in options:
        df = df[df['Month'] == month]
    else:
        df = df
    df = df[df['Level'].isin(geography)]
    df = df[(df.Year >= min(years)) & (df.Year <= max(years))]
    df = df.loc[df["Index"] == inflation]
    return df


def cpi_plot(df, inflation):
    fig = px.line(df, x="Date", y="CPI", title="{}".format(inflation), color="Level",
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
