import json
import os
import pika
from src import json_pars


class FrontReceiver:
    def __init__(self, rabbitmq_user, rabbitmq_pass, rabbitmq_server_name, rabbitmq_queue):
        """
        Инициализация объекта FrontReceiver.

        Args:
            rabbitmq_user (str): Имя пользователя RabbitMQ.
            rabbitmq_pass (str): Пароль пользователя RabbitMQ.
            rabbitmq_server_name (str): Имя сервера RabbitMQ.
            rabbitmq_queue (str): Имя очереди RabbitMQ.
        """
        self.rabbitmq_user = rabbitmq_user
        self.rabbitmq_pass = rabbitmq_pass
        self.rabbitmq_server_name = rabbitmq_server_name
        self.rabbitmq_queue = rabbitmq_queue
        self.channel = self.get_channel()

    def get_channel(self):
        """
        Создание канала RabbitMQ.

        Returns:
            channel (pika.channel.Channel): Канал RabbitMQ.
        """
        # Создание учетных данных для подключения к серверу RabbitMQ
        credentials = pika.PlainCredentials(self.rabbitmq_user, self.rabbitmq_pass)
        # Установка соединения с RabbitMQ сервером
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.rabbitmq_server_name, credentials=credentials))
        # Создание канала для взаимодействия с RabbitMQ
        channel = connection.channel()
        # Объявление очереди в RabbitMQ
        channel.queue_declare(queue=self.rabbitmq_queue)
        return channel

    def callback(self, ch, method, properties, body):
        """
        Callback функция для обработки полученных сообщений.

        Args:
            ch (pika.channel.Channel): Канал RabbitMQ.
            method (pika.spec.Basic.Deliver): Метод доставки.
            properties (pika.spec.BasicProperties): Свойства сообщения.
            body (bytes): Тело сообщения.
        """
        print(" [X] FRONT | Received JSON")

        try:
            # Декодирование сообщения
            new_data = body.decode('utf-8')
            new_data = json.loads(new_data)
            # Обновление или добавление данных в зависимости от наличия файла response.json
            if os.stat("response.json").st_size == 0:
                json_pars.add_data(new_data)
            else:
                json_pars.update_data(new_data)
        except Exception as e:
            print(f"Error processing message: {e}")

    def start_consuming(self):
        """
        Запуск процесса потребления сообщений из очереди RabbitMQ.
        """
        # Настройка потребителя для очереди
        self.channel.basic_consume(queue=self.rabbitmq_queue,
                                   on_message_callback=self.callback,
                                   auto_ack=True)
        print(' [x] FRONT | Waiting for messages. To exit press CTRL+C')
        # Запуск бесконечного цикла для ожидания сообщений
        self.channel.start_consuming()

