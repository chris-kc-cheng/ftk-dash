from dash import html, dcc, callback, register_page, Input, Output, State
import plotly.express as px
import pandas as pd
import time
import datetime
import requests
import json

countries = pd.Series({
    "USA": "USA",
    "Canada": "CAN",
    "Mexico": "MEX",
    "Brazil": "BRA",
    "UNITED KINGDOM IMI": "GBR",
    "Switzerland": "CHE",
    "Japan": "JPN",
    "China": "CHN",
    "Australia": "AUS",
    "MSCI India Domestic": "IND",
}, name="ISO")


def from_percent(x):
    return float(x.strip('%')) / 100


def get_rt_quotes():
    epoch = int(time.time() // 60 * 60 * 1000)
    res = requests.get(
        f"https://www.msci.com/webapp/indexperf/GetDelayedRealTime?callback=json_rt_callback&cachebuster={epoch}")
    text = res.text.replace("json_rt_callback(", "")[:-1]
    data = json.loads(text)
    values = [i["index"] for i in data["xmfIndices"]]
    df = pd.DataFrame(values)
    df.date = pd.to_datetime(df["date"], format="%d, %b %H:%M")
    df.date = df.date.apply(lambda x: x.replace(
        year=datetime.datetime.now().year))
    df.yearToDate = df.yearToDate.apply(from_percent)
    df = df.astype({
        "previousClose": "float",
        "yearToDate": "float",
        "level": "float",
        "change": "float",
        "id": "int"
    })
    return df.merge(countries, left_on='name', right_index=True, how='left')


register_page(__name__, path='/')

layout = html.Div([
    html.H1('Equity'),
    dcc.Graph(id="my-choropleth", figure={}),
    dcc.Store(id="storage", storage_type="session", data={}),
    dcc.Interval(id="timer", interval=1000 * 60, n_intervals=0),
])


@callback(
    Output("my-choropleth", "figure"),
    Input("timer", "n_intervals"),
    Input("switch", "value"),
)
def update_graph(_, mode):
    fig = px.choropleth(
        data_frame=get_rt_quotes(),
        locations="ISO",
        color="yearToDate",
        hover_name="name",
        color_continuous_scale=px.colors.sequential.RdBu,
        color_continuous_midpoint=0,
        labels={
            "name": "Country",
            "date": "Date",
            "yearToDate": "YTD",
            "previousClose": "Previous Close",
        },
        hover_data={
            "yearToDate": ":,.2%",
            "date": "|%Y-%m-%d %H:%M",
            "ISO": False
        },
        template="plotly" + ("" if mode else "_dark")
    )
    fig.update_traces(
        marker_line_width=0,
    )
    fig.update_layout(
        geo={
            "bgcolor": "rgba(0,0,0,0)",
            "showframe": False,
            "showcoastlines": False,
            "showcountries": False,
            "showlakes": False,
            "landcolor": "#EEEEEE",
            "projection_type": "natural earth",
            "scope": "world",  # world, europe,  asia, africa, north america, south america
        },
        coloraxis_colorbar={
            "tickformat": ",.0%"
        },
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)'
    )
    return fig
