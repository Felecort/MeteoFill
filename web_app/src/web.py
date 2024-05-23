
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


external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.title = "Данные метеостанции!"

data = pd.DataFrame(columns=['time',
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
app.layout = html.Div(children=[
    layout.header(),
    dcc.Interval(
        id="interval-component",
        interval=5000,  # в миллисекундах
        n_intervals=0
    ),
    layout.charts(),
    layout.data_table()
])

callback_args = ([Output('temp-chart', 'figure'),
                Output('pressure-chart', 'figure'),
                Output('humidity-chart', 'figure'),
                Output('wind-speed-chart', 'figure'),
                Output('wind-direction-chart', 'figure'),
                Output('data-table', 'data')],
                [Input('interval-component', 'n_intervals')])


@app.callback(*callback_args)
def update_charts(n_intervals):
    with open("response.json", "r") as f:
        raw_json = json.load(f)
        if raw_json:
            data = json_pars.parsing(raw_json)
        else:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update


    # with open("actual_data.json", "r") as f:
    #     raw_data = json.load(f)
    #     data = json_pars.parsing(raw_data)
    # with open("past_data.json", "r") as f:
    #     data_frame_presents = json_pars.parsing(json.load(f))
    
    # data_frame_presents = json_pars.update_data(data, data_frame_presents)

    # with open("past_data.json", "w") as f: 
    #     json.dump(raw_data, f)

    
    temp_chart = go.Figure()
    temp_chart.add_trace(go.Scatter(x=data['time'], y=data['temperature_after'], mode='lines', name='Восстановленные данные', line=dict(color='red')))
    temp_chart.add_trace(go.Scatter(x=data['time'], y=data['temperature_before'], mode='lines+markers', name='Полученные данные', line=dict(color='blue')))
    temp_chart.update_layout(
        xaxis_tickformat='%Y-%m-%d %H:%M',
        title='Температура'
    )

    pressure_chart = go.Figure()
    pressure_chart.add_trace(go.Scatter(x=data['time'], y=data['pressure_after'], mode='lines', name='Восстановленные данные', line=dict(color='red')))
    pressure_chart.add_trace(go.Scatter(x=data['time'], y=data['pressure_before'], mode='lines+markers', name='Полученные данные', line=dict(color='blue')))
    pressure_chart.update_layout(
        xaxis_tickformat='%Y-%m-%d %H:%M',
        title='Давление'
    )

    humidity_chart = go.Figure()
    humidity_chart.add_trace(go.Scatter(x=data['time'], y=data['humidity_after'], mode='lines', name='Восстановленные данные', line=dict(color='red')))
    humidity_chart.add_trace(go.Scatter(x=data['time'], y=data['humidity_before'], mode='lines+markers', name='Полученные данные', line=dict(color='blue')))
    humidity_chart.update_layout(
        xaxis_tickformat='%Y-%m-%d %H:%M',
        title='Влажность'
    )

    wind_speed_chart = go.Figure()
    wind_speed_chart.add_trace(go.Scatter(x=data['time'], y=data['wind_speed_after'], mode='lines', name='Восстановленные данные', line=dict(color='red')))
    wind_speed_chart.add_trace(go.Scatter(x=data['time'], y=data['wind_speed_before'], mode='lines+markers', name='Полученные данные', line=dict(color='blue')))
    wind_speed_chart.update_layout(
        xaxis_tickformat='%Y-%m-%d %H:%M',
        title='Скорость ветра'
    )

    wind_direction_chart = go.Figure()
    wind_direction_chart.add_trace(go.Scatter(x=data['time'], y=data['wind_direction_after'], mode='lines', name='Востановленные данные', line=dict(color='red')))
    wind_direction_chart.add_trace(go.Scatter(x=data['time'], y=data['wind_direction_before'], mode='lines+markers', name='Полученные данные', line=dict(color='blue')))
    wind_direction_chart.update_layout(
        xaxis_tickformat='%Y-%m-%d %H:%M',
        title='Направление ветра'
    )

    # Возвращение графиков и таблицы
    return temp_chart, pressure_chart, humidity_chart, wind_speed_chart, wind_direction_chart, data.to_dict('records')


if __name__ == '__main__':
    app.run_server(host="0.0.0.0", debug=True)