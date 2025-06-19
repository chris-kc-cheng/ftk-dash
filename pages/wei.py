import dash
from dash import html, dcc, callback, Input, Output, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

regions = ["Global", "Asia", "Europe", "North America", "South America"]
indices = pd.read_csv("data/indices.csv")

px = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vQt8DWz4crJb_GoKyzYS64Pb6L1WQMsTg_YuNhiu1o5l5DBwJ65m75SNMc0ViaLHoVY3L-wGOVVOopk/pub?gid=1924551939&single=true&output=csv')
px = px.set_index("Ticker").T
px.index.name = "Date"
px.index = pd.to_datetime(px.index).normalize()
px = px.groupby(pd.Grouper(freq="ME")).last()

curr = px.index[-1].month
lastM = -1
lastQ = -((curr - 1) % 3 + 1)
lastY = -curr

rtn = pd.concat([
    px.iloc[-1] / px.iloc[lastM - 1] - 1,
    px.iloc[-1] / px.iloc[lastQ - 1] - 1,
    px.iloc[-1] / px.iloc[lastY - 1] - 1
], axis=1, keys=["MTD", "QTD", "YTD"])

df = rtn.merge(indices, left_index=True, right_on="Ticker", how='left')


def region_tab(region):
    return dbc.Tab(
        label=region,
        tab_id=region,
        children=dbc.Container([
            # dbc.Table.from_dataframe(df),
            dash_table.DataTable(df.to_dict('records'),
                                 [{"name": i, "id": i} for i in df.columns]),
            dbc.Row(
                dbc.Col(
                    dbc.ButtonGroup([
                        dbc.Button("Map", outline=True, color="primary"),
                        dbc.Button("Table", outline=True, color="primary"),
                        dbc.Button("Chart", outline=True, color="primary"),
                    ])
                )
            )
        ])
    )


dash.register_page(__name__)

layout = html.Div([
    html.H1('World Equity Indices'),
    dbc.Tabs(
        [region_tab(r) for r in regions]
    )
])
