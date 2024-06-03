from . import layout
from . import json_pars

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

import json

import pandas as pd
import plotly.graph_objs as go

import os

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


class WeatherApp:
    def __init__(self):
        with open("response.json", "w") as f:
            f.write("")

        self.external_stylesheets = [
            {
                "href": "https://fonts.googleapis.com/css2?"
                        "family=Lato:wght@400;700&display=swap",
                "rel": "stylesheet",
            },
        ]
        self.app = dash.Dash(__name__, external_stylesheets=self.external_stylesheets)
        self.app.title = "Данные метеостанции!"

        self.app.layout = self.create_layout()
        self.register_callbacks()

        

    def create_layout(self):
        return html.Div(children=[
            layout.header(),
            dcc.Interval(
                id="interval-component",
                interval=20000,  # в миллисекундах
                n_intervals=0
            ),
            layout.charts(),
            layout.data_table()
        ])

    def register_callbacks(self):
        callback_args = ([Output('temp-chart', 'figure'),
                          Output('pressure-chart', 'figure'),
                          Output('humidity-chart', 'figure'),
                          Output('wind-speed-chart', 'figure'),
                          Output('wind-direction-chart', 'figure'),
                          Output('data-table', 'data')],
                         [Input('interval-component', 'n_intervals')])

        @self.app.callback(*callback_args)
        def update_charts(n_intervals):
            if os.stat("response.json").st_size == 0:
                return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
            else:
                with open("response.json", "r") as f:
                    raw_json = json.load(f)
                    if raw_json:
                        self.data = json_pars.parsing(raw_json)
                    else:
                        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update    

            temp_chart = self.create_chart( name = "Температура", id_before = "temperature_2m_before",id_after = "temperature_2m_after")
            pressure_chart = self.create_chart(name = "Атмосферное давление",id_before =  "surface_pressure_before",id_after = "surface_pressure_after")
            humidity_chart = self.create_chart(name = "Относительная влажность",id_before =  "relative_humidity_2m_before",id_after = "relative_humidity_2m_after")
            wind_speed_chart = self.create_chart(name = "Скорость ветра",id_before =  "wind_speed_10m_before",id_after = "wind_speed_10m_after")
            wind_direction_chart = self.create_chart(name = "Направление ветра",id_before =  "wind_direction_10m_before",id_after = "wind_direction_10m_after")

            return temp_chart, pressure_chart, humidity_chart, wind_speed_chart, wind_direction_chart, self.data.to_dict('records')

    def create_chart(self, name, id_before, id_after):
        temp_chart = go.Figure()
        temp_chart.add_trace(go.Scatter(x=self.data['time'], y=self.data[id_after], mode='lines', name='Восстановленные данные', line=dict(color='red')))
        temp_chart.add_trace(go.Scatter(x=self.data['time'], y=self.data[id_before], mode='lines+markers', name='Полученные данные', line=dict(color='blue')))
        temp_chart.update_layout(
            xaxis_tickformat='%Y-%m-%d %H:%M',
            title=name
        )
        return temp_chart

    def run(self):
        self.app.run_server(host="0.0.0.0", debug=True)


if __name__ == '__main__':
    weather_app = WeatherApp()
    weather_app.run()
