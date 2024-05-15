from .layout import*
import dash
import dash.dash_table as dt
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

from .json_pars import parsing
import json

import pandas as pd
import plotly.graph_objs as go

import os


import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


# Инициализация приложения Dash
external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.title = "Данные метеостанции!"

data_frame_presents = pd.DataFrame(columns=['time',
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

# Заг(рузка JSON (в дальнейшем будет api запрос)

print(os.system("pwd"))
with open('response_example.json', 'r') as f:
    data = json.load(f)

# Макет приложения
app.layout = html.Div(children=[
    header(),
    dcc.Interval(
        id="interval-component",
        interval=500,  # в миллисекундах
        n_intervals=0
    ),
    charts(),
    data_table()
])

# Обновление данных каждые 5 секунд
@app.callback(
    [Output('temp-chart', 'figure'),
     Output('pressure-chart', 'figure'),
     Output('humidity-chart', 'figure'),
     Output('wind-speed-chart', 'figure'),
     Output('wind-direction-chart', 'figure'),
     Output('data-table', 'data')],
    [Input('interval-component', 'n_intervals')]
)

def update_charts(n_intervals):
    # Создание датафрейма внутри функции
    #data_frame_presents = update_data(data,data_frame_presents)
    df = parsing(data)


    temp_chart = go.Figure()
    temp_chart.add_trace(go.Scatter(x=df['time'], y=df['temperature_after'], mode='lines', name='Восстановленные данные', line=dict(color='red')))
    temp_chart.add_trace(go.Scatter(x=df['time'], y=df['temperature_before'], mode='lines+markers', name='Полученные данные', line=dict(color='blue')))
    temp_chart.update_layout(
        xaxis_tickformat='%Y-%m-%d %H:%M',
        title='Температура'
    )

    pressure_chart = go.Figure()
    pressure_chart.add_trace(go.Scatter(x=df['time'], y=df['pressure_after'], mode='lines', name='Восстановленные данные', line=dict(color='red')))
    pressure_chart.add_trace(go.Scatter(x=df['time'], y=df['pressure_before'], mode='lines+markers', name='Полученные данные', line=dict(color='blue')))
    pressure_chart.update_layout(
        xaxis_tickformat='%Y-%m-%d %H:%M',
        title='Давление'
    )

    humidity_chart = go.Figure()
    humidity_chart.add_trace(go.Scatter(x=df['time'], y=df['humidity_after'], mode='lines', name='Восстановленные данные', line=dict(color='red')))
    humidity_chart.add_trace(go.Scatter(x=df['time'], y=df['humidity_before'], mode='lines+markers', name='Полученные данные', line=dict(color='blue')))
    humidity_chart.update_layout(
        xaxis_tickformat='%Y-%m-%d %H:%M',
        title='Влажность'
    )

    wind_speed_chart = go.Figure()
    wind_speed_chart.add_trace(go.Scatter(x=df['time'], y=df['wind_speed_after'], mode='lines', name='Восстановленные данные', line=dict(color='red')))
    wind_speed_chart.add_trace(go.Scatter(x=df['time'], y=df['wind_speed_before'], mode='lines+markers', name='Полученные данные', line=dict(color='blue')))
    wind_speed_chart.update_layout(
        xaxis_tickformat='%Y-%m-%d %H:%M',
        title='Скорость ветра'
    )

    wind_direction_chart = go.Figure()
    wind_direction_chart.add_trace(go.Scatter(x=df['time'], y=df['wind_direction_after'], mode='lines', name='Востоновленные данные', line=dict(color='red')))
    wind_direction_chart.add_trace(go.Scatter(x=df['time'], y=df['wind_direction_before'], mode='lines+markers', name='Полученные данные', line=dict(color='blue')))
    wind_direction_chart.update_layout(
        xaxis_tickformat='%Y-%m-%d %H:%M',
        title='Направление ветра'
    )


    # Возвращение графиков и таблицы
    return temp_chart, pressure_chart, humidity_chart, wind_speed_chart, wind_direction_chart, df.to_dict('records')

if __name__ == '__main__':
    app.run_server(host="0.0.0.0", debug=True)