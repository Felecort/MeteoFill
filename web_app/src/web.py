
# from .layout import *
# from .json_pars import parsing, update_data
# from .front_receiver import json_data
from . import layout
from . import json_pars
from . import front_receiver


import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

import json

import pandas as pd
import plotly.graph_objs as go


import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


class WebInterface:
    def __init__(self):
        # Инициализация приложения Dash
        self.external_stylesheets = [
            {
                "href": "https://fonts.googleapis.com/css2?"
                        "family=Lato:wght@400;700&display=swap",
                "rel": "stylesheet",
            },
        ]

        self.app = dash.Dash(__name__, external_stylesheets=self.external_stylesheets)

        self.app.title = "Данные метеостанции!"

        self.data_frame_presents = pd.DataFrame(columns=['time',
                                                        'temperature_before',
                                                        'temperature_after',
                                                        'wind_speed_before',
                                                        'wind_speed_after',
                                                        'wind_direction_before',
                                                        'wind_direction_after',
                                                        'pressure_before',
                                                        'pressure_after',
                                                        'humidity_before',
                                                        'humidity_after'])

        # Макет приложения
        self.app.layout = html.Div(children=[
            layout.header(),
            dcc.Interval(
                id="interval-component",
                interval=5000,  # в миллисекундах
                n_intervals=0
            ),
            layout.charts(),
            layout.data_table()
        ])


        self.callback_charts = ([Output('temp-chart', 'figure'),
            Output('pressure-chart', 'figure'),
            Output('humidity-chart', 'figure'),
            Output('wind-speed-chart', 'figure'),
            Output('wind-direction-chart', 'figure'),
            Output('data-table', 'data')],
            [Input('interval-component', 'n_intervals')])

    def __call__(self):
        @self.app.callback(self.callback_charts)
        def update_charts():
            global data_frame_presents
            
            # Use the global JSON data directly
            if json_pars.json_data:
                data = json.loads(json_pars.json_data)

                # Создание датафрейма внутри функции
                data_frame_presents = json_pars.update_data(data, data_frame_presents)

                temp_chart = go.Figure()
                temp_chart.add_trace(go.Scatter(x=data_frame_presents['time'], y=data_frame_presents['temperature_after'], mode='lines', name='Восстановленные данные', line=dict(color='red')))
                temp_chart.add_trace(go.Scatter(x=data_frame_presents['time'], y=data_frame_presents['temperature_before'], mode='lines+markers', name='Полученные данные', line=dict(color='blue')))
                temp_chart.update_layout(
                    xaxis_tickformat='%Y-%m-%d %H:%M',
                    title='Температура'
                )

                pressure_chart = go.Figure()
                pressure_chart.add_trace(go.Scatter(x=data_frame_presents['time'], y=data_frame_presents['pressure_after'], mode='lines', name='Восстановленные данные', line=dict(color='red')))
                pressure_chart.add_trace(go.Scatter(x=data_frame_presents['time'], y=data_frame_presents['pressure_before'], mode='lines+markers', name='Полученные данные', line=dict(color='blue')))
                pressure_chart.update_layout(
                    xaxis_tickformat='%Y-%m-%d %H:%M',
                    title='Давление'
                )

                humidity_chart = go.Figure()
                humidity_chart.add_trace(go.Scatter(x=data_frame_presents['time'], y=data_frame_presents['humidity_after'], mode='lines', name='Восстановленные данные', line=dict(color='red')))
                humidity_chart.add_trace(go.Scatter(x=data_frame_presents['time'], y=data_frame_presents['humidity_before'], mode='lines+markers', name='Полученные данные', line=dict(color='blue')))
                humidity_chart.update_layout(
                    xaxis_tickformat='%Y-%m-%d %H:%M',
                    title='Влажность'
                )

                wind_speed_chart = go.Figure()
                wind_speed_chart.add_trace(go.Scatter(x=data_frame_presents['time'], y=data_frame_presents['wind_speed_after'], mode='lines', name='Восстановленные данные', line=dict(color='red')))
                wind_speed_chart.add_trace(go.Scatter(x=data_frame_presents['time'], y=data_frame_presents['wind_speed_before'], mode='lines+markers', name='Полученные данные', line=dict(color='blue')))
                wind_speed_chart.update_layout(
                    xaxis_tickformat='%Y-%m-%d %H:%M',
                    title='Скорость ветра'
                )

                wind_direction_chart = go.Figure()
                wind_direction_chart.add_trace(go.Scatter(x=data_frame_presents['time'], y=data_frame_presents['wind_direction_after'], mode='lines', name='Востановленные данные', line=dict(color='red')))
                wind_direction_chart.add_trace(go.Scatter(x=data_frame_presents['time'], y=data_frame_presents['wind_direction_before'], mode='lines+markers', name='Полученные данные', line=dict(color='blue')))
                wind_direction_chart.update_layout(
                    xaxis_tickformat='%Y-%m-%d %H:%M',
                    title='Направление ветра'
                )

                # Возвращение графиков и таблицы
                return temp_chart, pressure_chart, humidity_chart, wind_speed_chart, wind_direction_chart, data_frame_presents.to_dict('records')
            else:
                return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

        return update_charts()


# if __name__ == '__main__':
#     app.run_server(host="0.0.0.0", debug=True)
