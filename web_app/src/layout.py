from dash import dcc
from dash import html
import dash.dash_table as dt


def header():
    return html.Div(
        children=[
            html.P(children="🌤️", className="header-emoji"),
            html.H1(children="Данные метеостанции", className="header-title"),
            html.P(
                children="Визуализация восстановленных данных, которые были потеряны при передаче нам от метеостанции.\n Графики обновляются каждые 5 секунд, выводя результаты последних 100 временных меток.",
                className="header-description",
            ),
        ],
        className="header",
    )


def charts():
    return html.Div(
        children=[
            html.Div(
                children=dcc.Graph(id="temp-chart", style={"marginTop": "30px"}),
                className="card",
            ),
            html.Div(
                children=dcc.Graph(id="pressure-chart", style={"marginTop": "30px"}),
                className="card",
            ),
            html.Div(
                children=dcc.Graph(id="humidity-chart", style={"marginTop": "30px"}),
                className="card",
            ),
            html.Div(
                children=dcc.Graph(id="wind-speed-chart", style={"marginTop": "30px"}),
                className="card",
            ),
            html.Div(
                children=dcc.Graph(
                    id="wind-direction-chart", style={"marginTop": "30px"}
                ),
                className="card",
            ),
        ],
        className="wrapper",
    )


def data_table():
    return html.Div(
        children=dt.DataTable(
            id="data-table",
            columns=[
                {"name": "Время", "id": "time"},
                {"name": "Температура", "id": "temperature"},
                {"name": "Давление", "id": "pressure"},
                {"name": "Влажность", "id": "humidity"},
                {"name": "Скорость ветра", "id": "wind_speed"},
                {"name": "Направление ветра", "id": "wind_direction"},
            ],
            style_cell={"textAlign": "center", "whiteSpace": "normal"},
        ),
        className="table-container",
    )

