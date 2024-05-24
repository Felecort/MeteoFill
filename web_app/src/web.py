from . import layout
from . import json_pars

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

import json

import pandas as pd
import plotly.graph_objs as go

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


class WeatherApp:
    def __init__(self):
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
                interval=5000,  # в миллисекундах
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
            with open("response.json", "r") as f:
                raw_json = json.load(f)
                if raw_json:
                    self.data = json_pars.parsing(raw_json)
                else:
                    return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

            temp_chart = self.create_temp_chart()
            pressure_chart = self.create_pressure_chart()
            humidity_chart = self.create_humidity_chart()
            wind_speed_chart = self.create_wind_speed_chart()
            wind_direction_chart = self.create_wind_direction_chart()

            return temp_chart, pressure_chart, humidity_chart, wind_speed_chart, wind_direction_chart, self.data.to_dict('records')

    def create_temp_chart(self):
        temp_chart = go.Figure()
        temp_chart.add_trace(go.Scatter(x=self.data['time'], y=self.data['temperature_after'], mode='lines', name='Восстановленные данные', line=dict(color='red')))
        temp_chart.add_trace(go.Scatter(x=self.data['time'], y=self.data['temperature_before'], mode='lines+markers', name='Полученные данные', line=dict(color='blue')))
        temp_chart.update_layout(
            xaxis_tickformat='%Y-%m-%d %H:%M',
            title='Температура'
        )
        return temp_chart

    def create_pressure_chart(self):
        pressure_chart = go.Figure()
        pressure_chart.add_trace(go.Scatter(x=self.data['time'], y=self.data['pressure_after'], mode='lines', name='Восстановленные данные', line=dict(color='red')))
        pressure_chart.add_trace(go.Scatter(x=self.data['time'], y=self.data['pressure_before'], mode='lines+markers', name='Полученные данные', line=dict(color='blue')))
        pressure_chart.update_layout(
            xaxis_tickformat='%Y-%m-%d %H:%M',
            title='Давление'
        )
        return pressure_chart

    def create_humidity_chart(self):
        humidity_chart = go.Figure()
        humidity_chart.add_trace(go.Scatter(x=self.data['time'], y=self.data['humidity_after'], mode='lines', name='Восстановленные данные', line=dict(color='red')))
        humidity_chart.add_trace(go.Scatter(x=self.data['time'], y=self.data['humidity_before'], mode='lines+markers', name='Полученные данные', line=dict(color='blue')))
        humidity_chart.update_layout(
            xaxis_tickformat='%Y-%m-%d %H:%M',
            title='Влажность'
        )
        return humidity_chart

    def create_wind_speed_chart(self):
        wind_speed_chart = go.Figure()
        wind_speed_chart.add_trace(go.Scatter(x=self.data['time'], y=self.data['wind_speed_after'], mode='lines', name='Восстановленные данные', line=dict(color='red')))
        wind_speed_chart.add_trace(go.Scatter(x=self.data['time'], y=self.data['wind_speed_before'], mode='lines+markers', name='Полученные данные', line=dict(color='blue')))
        wind_speed_chart.update_layout(
            xaxis_tickformat='%Y-%m-%d %H:%M',
            title='Скорость ветра'
        )
        return wind_speed_chart

    def create_wind_direction_chart(self):
        wind_direction_chart = go.Figure()
        wind_direction_chart.add_trace(go.Scatter(x=self.data['time'], y=self.data['wind_direction_after'], mode='lines', name='Востановленные данные', line=dict(color='red')))
        wind_direction_chart.add_trace(go.Scatter(x=self.data['time'], y=self.data['wind_direction_before'], mode='lines+markers', name='Полученные данные', line=dict(color='blue')))
        wind_direction_chart.update_layout(
            xaxis_tickformat='%Y-%m-%d %H:%M',
            title='Направление ветра'
        )
        return wind_direction_chart

    def run(self):
        self.app.run_server(host="0.0.0.0", debug=True)


if __name__ == '__main__':
    weather_app = WeatherApp()
    weather_app.run()
