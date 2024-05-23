import time
import json
from threading import Thread, Event

import pandas as pd
import pika

from weather_api_calls import get_weather

"""
При инициализации:
1. Проверяет связь с фронтом и бэком, если нет, то пробует снова и если не получается, то прекращает работу
2. Проверяет связь с БД, если нет, то пробует снова и если не получается, то прекращает работу
3. Отправляет последние N значений на фронт для инициализации

Логика работы:
1. Запрашивает данные о погоде
2. Распаковывает их в словарь
3. Формирует запрос и посылает данные на обработку на бэкенд
4. Ждет ответ
5. Формирует запрос на фронтенд и посылает данные
6. Сохраняет данные в БД
7. Отправляет заполненные данные во внешнюю систему
"""


class BusinessLogic:
    def __init__(self, request_frequency_sec: int):
        self._request_timeout = request_frequency_sec
        self._name_mapping = {
            'temperature_2m': 'Температура',
            'relative_humidity_2m': 'Относительная влажность',
            'surface_pressure': 'Атмосферное давление',
            'wind_speed_10m': 'Скорость ветра',
            'wind_direction_10m': 'Направление ветра'
        }
        self._backend_conn, self._system2backend_channel = self.__set_backend_connection()
        self._evnt = Event()
        self._evnt.clear()
        self._backend_answer = None
        self.__start_consuming_from_backend()
        self._frontend_conn, self._system2frontend_channel = self.__set_frontend_connection()

    def __set_backend_connection(
            self, tries_num: int = 10
    ) -> (pika.adapters.blocking_connection.BlockingChannel, pika.adapters.blocking_connection.BlockingChannel):
        i = 0
        done_flag = False
        backend_conn = None
        system2backend_channel = None
        while i < tries_num and not done_flag:
            i += 1
            done_flag = True
            try:
                backend_conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
                system2backend_channel = backend_conn.channel()
                system2backend_channel.queue_declare(queue='system2backend')
            except:
                done_flag = False
                print(f'Cant connect. Try again #{i}')
                if i >= tries_num:
                    raise ConnectionError
                time.sleep(1)

        return backend_conn, system2backend_channel

    def __set_frontend_connection(
            self, tries_num: int = 10
    ) -> (pika.adapters.blocking_connection.BlockingChannel, pika.adapters.blocking_connection.BlockingChannel):
        i = 0
        done_flag = False
        frontend_conn = None
        system2frontend_channel = None
        while i < tries_num and not done_flag:
            i += 1
            done_flag = True
            try:
                frontend_conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
                system2frontend_channel = frontend_conn.channel()
                system2frontend_channel.queue_declare(queue='system2frontend')
            except:
                done_flag = False
                print(f'Cant connect. Try again #{i}')
                if i >= tries_num:
                    raise ConnectionError
                time.sleep(1)

        return frontend_conn, system2frontend_channel

    def __start_consuming_from_backend(self):

        def system_consumer(ch, method, properties, body):
            print(f'Data collected at {time.time()}')
            self._backend_answer = body
            self._evnt.set()

        self._backend2system_channel = self._backend_conn.channel()
        self._backend2system_channel.queue_declare(queue='backend2system')
        self._backend2system_channel.basic_consume(
            queue='backend2system',
            on_message_callback=system_consumer,
            auto_ack=True
        )

        self._consumer_thread = Thread(target=self._backend2system_channel.start_consuming)
        self._consumer_thread.start()
        self._consumer_thread.join(0)

    def __get_weather_data(self):
        data = get_weather()
        data = self.__input_adapter(data)
        return data

    def __input_adapter(self, data):
        # TODO: Реализовать адаптор
        return data

    def __output_adapter(self, data):
        # TODO: Реализовать адаптор
        return data

    def __add_timeout(self, start_time):
        now = time.time()
        if now - start_time < self._request_timeout:
            print('Timeout:', self._request_timeout - (now - start_time))
            time.sleep(self._request_timeout - (now - start_time))
        return time.time()

    def __create_backend_request(self, weather_data: pd.DataFrame) -> dict:
        backend_request = {}
        date_start = str(min(weather_data.index).to_datetime64())
        date_end = str(max(weather_data.index).to_datetime64())
        backend_request['timestamps'] = {}
        backend_request['timestamps']['start'] = date_start
        backend_request['timestamps']['end'] = date_end

        delay = (weather_data.index[1] - weather_data.index[0]).seconds
        backend_request['delay'] = delay

        backend_request['data'] = []
        for column_name in weather_data.columns:
            sensor_data = {}
            sensor_data['name'] = column_name   # Выставляем name по умолчанию равным id
            if column_name in self._name_mapping.keys():
                sensor_data['name'] = self._name_mapping[column_name]
            sensor_data['id'] = column_name
            sensor_data['values'] = weather_data[column_name].values.tolist()
            backend_request['data'].append(sensor_data)
        return backend_request

    def __send_and_wait_data_backend(self, raw_weather_data: pd.DataFrame):
        backend_request = self.__create_backend_request(raw_weather_data)
        self._system2backend_channel.basic_publish(
            exchange='',
            routing_key='system2backend',
            body=json.dumps(backend_request)
        )
        print(f'Data send to backend at {time.time()}')
        self._evnt.wait()
        self._evnt.clear()
        backend_response = json.loads(self._backend_answer)
        self._backend_answer = None
        return backend_request, backend_response

    def __create_frontend_request(self, unfilled_weather_data: dict, filled_weather_data: dict) -> dict:
        frontend_request = {
            'timestamps': unfilled_weather_data['timestamps'],
            'delay': unfilled_weather_data['delay'],
            'data': []
        }

        for raw_data, filled_data in zip(unfilled_weather_data['data'], filled_weather_data['data']):
            assert(raw_data['id'] == filled_data['id'])
            weather_data = {'name': raw_data['name'], 'id': raw_data['id'], 'values': {}}
            weather_data['values']['before'] = raw_data['values']
            weather_data['values']['after'] = filled_data['values']

            frontend_request['data'].append(weather_data)
        return frontend_request

    def __send_data_to_frontend(self, unfilled_weather_data: dict, filled_weather_data: dict):
        frontend_request = self.__create_frontend_request(unfilled_weather_data, filled_weather_data)
        self._system2frontend_channel.basic_publish(
            exchange='',
            routing_key='system2backend',
            body=json.dumps(frontend_request)
        )
        print(f'Data send to frontend at {time.time()}')

    def __save_data_to_database(self, unfilled_data: dict, filled_data: dict):
        # TODO: Реализовать сохранение в БД PostgreSQL
        pass

    def __send_filled_data_to_external_system(self, filled_data: dict):
        filled_data = self.__output_adapter(filled_data)
        # TODO: Реализовать отправку данных
        pass

    def run(self):
        start_time = time.time() - self._request_timeout - 1
        while True:
            # Добавляем задержку при запросах
            start_time = self.__add_timeout(start_time)

            # Запрашиваем данные о погоде
            raw_weather_data = self.__get_weather_data()
            # Формируем запрос и посылаем сырые данные на обработку на бэкенд
            unfilled_weather_data, filled_weather_data = self.__send_and_wait_data_backend(raw_weather_data)
            # Формируем запрос и посылаем заполненные данные на фронтенд
            self.__send_data_to_frontend(unfilled_weather_data, filled_weather_data)
            # Сохраняем данные в БД
            self.__save_data_to_database(unfilled_weather_data, filled_weather_data)
            # Отправляем заполненные данные во внешнюю систему
            self.__send_filled_data_to_external_system(filled_weather_data)


if __name__ == '__main__':
    bl = BusinessLogic(10)
    bl.run()
