import dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import time
import dash.dash_table as dt

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

# Тестовые данные
time = [
    "2024-04-13T00:00", "2024-04-13T01:00", "2024-04-13T02:00", "2024-04-13T03:00", 
    "2024-04-13T04:00", "2024-04-13T05:00", "2024-04-13T06:00", "2024-04-13T07:00", 
    "2024-04-13T08:00", "2024-04-13T09:00", "2024-04-13T10:00", "2024-04-13T11:00", 
    "2024-04-13T12:00", "2024-04-13T13:00", "2024-04-13T14:00", "2024-04-13T15:00", 
    "2024-04-13T16:00", "2024-04-13T17:00", "2024-04-13T18:00", "2024-04-13T19:00"
]
temperature_error = [
    0.8, 0.4, -0.5, "NaN", 1.6, 3.6, "NaN", 7.1, 9.8, 0.8, 0.4, -0.5, "NaN", 
    1.6, 3.6, "NaN", 7.1, 9.8, 0.8, 0.4
]
pressure_error = [
    1013.7, 1013.7, "NaN", 1013.1, 1013.4, 1013.1, "NaN", 1012.5, 1012.2, 
    1013.7, 1013.7, "NaN", 1013.1, 1013.4, 1013.1, "NaN", 1012.5, 1012.2, 
    1013.7, 1013.7
]
humidity_error = [
    98, "NaN", 99, 98, 96, 90, 82, 79, 72, 
    98, "NaN", 99, 98, 96, 90, 82, 79, 72, 
    98, "NaN"
]
wind_speed_error = [
    6.2, 6.2, 7.7, 7.4, "NaN", "NaN", 4.4, "NaN", 5.2, 
    6.2, 6.2, 7.7, 7.4, "NaN", "NaN", 4.4, "NaN", 5.2, 
    6.2, 6.2
]
wind_direction_error = [
    249, 234, "NaN", 194, 190, 180, 215, 185, 192, 
    249, 234, "NaN", 194, 190, 180, 215, 185, 192, 
    249, 234
]
temperature = [
    0.8, 0.4, -0.5, -0.4, 1.6, 3.6, 6.1, 7.1, 9.8, 
    0.8, 0.4, -0.5, -0.4, 1.6, 3.6, 6.1, 7.1, 9.8, 
    0.8, 0.4
]
pressure = [
    1013.7, 1013.7, 1013.3, 1013.1, 1013.4, 1013.1, 1012.8, 1012.5, 1012.2, 
    1013.7, 1013.7, 1013.3, 1013.1, 1013.4, 1013.1, 1012.8, 1012.5, 1012.2, 
    1013.7, 1013.7
]
humidity = [
    98, 99, 99, 98, 96, 90, 82, 79, 72, 
    98, 99, 99, 98, 96, 90, 82, 79, 72, 
    98, 99
]
wind_speed = [
    6.2, 6.2, 7.7, 7.4, 4, 5.4, 4.4, 4, 5.2, 
    6.2, 6.2, 7.7, 7.4, 4, 5.4, 4.4, 4, 5.2, 
    6.2, 6.2
]
wind_direction = [
    249, 234, 208, 194, 190, 180, 215, 185, 192, 
    249, 234, 208, 194, 190, 180, 215, 185, 192, 
    249, 234
]

# Define the function to create DataFrame
def create_data_frame():
    data = {
        'time': time,
        'temperature_error': temperature_error,
        'temperature': temperature,
        'pressure_error': pressure_error,
        'pressure': pressure,
        'humidity_error': humidity_error,
        'humidity': humidity,   
        'wind_speed_error': wind_speed_error,
        'wind_speed': wind_speed,
        'wind_direction_error': wind_direction_error,
        'wind_direction': wind_direction
    }
    return pd.DataFrame(data)

# Макет приложения
app.layout = html.Div(children=[
        html.Div(children=[
            html.P(children="🌤️", className="header-emoji"),
            html.H1(children="Данные метеостанции",className="header-title"),
            html.P(children="Визуализация востановленных данных, которые были потеряны при передаче нам от метеостанции.\n Графики обновляются каждые 5 секунд, выводя результаты последних 100 временных меток.",
                className="header-description"),
            ],   
            className="header",
        ),
        dcc.Interval(
            id='interval-component',
            interval=5000,  # в миллисекундах
            n_intervals=0
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(id='temp-chart', style={'marginTop': '30px'}),
                className="card",
                ),
                html.Div(
                    children=dcc.Graph(id='pressure-chart', style={'marginTop': '30px'}),
                className="card",
                ),
                html.Div(
                    children=dcc.Graph(id='humidity-chart', style={'marginTop': '30px'}),
                className="card",
                ),
                html.Div(
                    children=dcc.Graph(id='wind-speed-chart', style={'marginTop': '30px'}),
                className="card",
                ),
                html.Div(
                    children=dcc.Graph(id='wind-direction-chart', style={'marginTop': '30px'}),
                className="card",
                ),
            ],
    className="wrapper",
    ),
    html.Div(children=dt.DataTable(
                        id='data-table',
                        columns=[
                            {"name": "Время", "id": "time"},
                            {"name": "Температура при получении", "id": "temperature_error"},
                            {"name": "Температура после обработки", "id": "temperature"},
                            {"name": "Давление при получении", "id": "pressure_error"},
                            {"name": "Давление после обработки", "id": "pressure"},
                            {"name": "Влажность при получении", "id": "humidity_error"},
                            {"name": "Влажность после обработки", "id": "humidity"},
                            {"name": "Скорость ветра при получении", "id": "wind_speed_error"},
                            {"name": "Скорость ветра после обработки", "id": "wind_speed"},
                            {"name": "Направление ветра при получении", "id": "wind_direction_error"},
                            {"name": "Направление ветра после обработки", "id": "wind_direction"}
                        ],
                        data=create_data_frame().to_dict('records'),
                        style_cell={'textAlign': 'center', 'whiteSpace': 'normal'},
                        style_data_conditional=[
                            {
                                'if': {'column_type': 'text', 'filter_query': '{} eq "NaN"'},
                                'backgroundColor': 'crimson',
                                'color': 'white'
                            }
                        ],
                    ),
                className="table",
                ),
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
    df = create_data_frame()

    temp_chart = go.Figure()
    temp_chart.add_trace(go.Scatter(x=df['time'], y=df['temperature'], mode='lines', name='Восстановленные данные', line=dict(color='red')))
    temp_chart.add_trace(go.Scatter(x=df['time'], y=df['temperature_error'], mode='lines+markers', name='Полученные данные', line=dict(color='blue')))
    temp_chart.update_layout(
        xaxis_tickformat='%Y-%m-%dT%H:%M',
        title='Температура'
    )

    pressure_chart = go.Figure()
    pressure_chart.add_trace(go.Scatter(x=df['time'], y=df['pressure'], mode='lines', name='Восстановленные данные', line=dict(color='red')))
    pressure_chart.add_trace(go.Scatter(x=df['time'], y=df['pressure_error'], mode='lines+markers', name='Полученные данные', line=dict(color='blue')))
    pressure_chart.update_layout(
        xaxis_tickformat='%Y-%m-%dT%H:%M',
        title='Давление'
    )

    humidity_chart = go.Figure()
    humidity_chart.add_trace(go.Scatter(x=df['time'], y=df['humidity'], mode='lines', name='Восстановленные данные', line=dict(color='red')))
    humidity_chart.add_trace(go.Scatter(x=df['time'], y=df['humidity_error'], mode='lines+markers', name='Полученные данные', line=dict(color='blue')))
    humidity_chart.update_layout(
        xaxis_tickformat='%Y-%m-%dT%H:%M',
        title='Влажность'
    )

    wind_speed_chart = go.Figure()
    wind_speed_chart.add_trace(go.Scatter(x=df['time'], y=df['wind_speed'], mode='lines', name='Восстановленные данные', line=dict(color='red')))
    wind_speed_chart.add_trace(go.Scatter(x=df['time'], y=df['wind_speed_error'], mode='lines+markers', name='Полученные данные', line=dict(color='blue')))
    wind_speed_chart.update_layout(
        xaxis_tickformat='%Y-%m-%dT%H:%M',
        title='Скорость ветра'
    )

    wind_direction_chart = go.Figure()
    wind_direction_chart.add_trace(go.Scatter(x=df['time'], y=df['wind_direction'], mode='lines', name='Востоновленные данные', line=dict(color='red')))
    wind_direction_chart.add_trace(go.Scatter(x=df['time'], y=df['wind_direction_error'], mode='lines+markers', name='Полученные данные', line=dict(color='blue')))
    wind_direction_chart.update_layout(
        xaxis_tickformat='%Y-%m-%dT%H:%M',
        title='Направление ветра'
    )


    # Возвращение графиков и таблицы
    return temp_chart, pressure_chart, humidity_chart, wind_speed_chart, wind_direction_chart, df.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)