
from src import app
from time import sleep
from multiprocessing import Process
from web_app.src import front_consumer


def run_web():
    app.run(host="0.0.0.0", debug=True)


def run_consumer():
    print("Waiting...")
    sleep(10)
    channel = front_consumer.get_channel()

    channel.basic_consume(queue='gui_queue',
                            on_message_callback=front_consumer.callback,
                            auto_ack=True)
    print(' [x] FRONT | Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == "__main__":
    p1 = Process(target=run_web)
    p1.start()
    p2 = Process(target=run_consumer)
    p2.start()
