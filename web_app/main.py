#main.py

from src import WebInterface
from src import front_receiver, callback
from time import sleep
from multiprocessing import Process


def run_web():
    app = WebInterface()
    app.run(host="0.0.0.0", debug=True)


def run_receiver():
    print("Waiting...")
    sleep(10)
    channel = front_receiver.get_channel()

    channel.basic_consume(queue='gui_queue',
                            on_message_callback=callback,
                            auto_ack=True)
    print(' [x] FRONT | Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == "__main__":

    p1 = Process(target=run_web)
    p1.start()
    p2 = Process(target=run_receiver)
    p2.start()