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
                {"name": "Температура при получении", "id": "temperature_2m_before"},
                {"name": "Температура после обработки", "id": "temperature_2m_after"},
                {"name": "Давление при получении", "id": "surface_pressure_before"},
                {"name": "Давление после обработки", "id": "surface_pressure_after"},
                {"name": "Влажность при получении", "id": "relative_humidity_2m_before"},
                {"name": "Влажность после обработки", "id": "relative_humidity_2m_after"},
                {"name": "Скорость ветра при получении", "id": "wind_speed_10m_before"},
                {"name": "Скорость ветра после обработки", "id": "wind_speed_10m_after"},
                {"name": "Направление ветра при получении", "id": "wind_direction_10m_before"},
                {"name": "Направление ветра после обработки", "id": "wind_direction_10m_after"},
            ],
            style_cell={"textAlign": "center", "whiteSpace": "normal"},
        ),
        className="table",
    )
