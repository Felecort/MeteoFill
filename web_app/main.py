
from src import app
from time import sleep
from multiprocessing import Process
<<<<<<< HEAD
=======
from src import front_consumer

>>>>>>> 3c097709b153093cad58b4f8f397d3c5f11b7024

def run_web():
    app.run(host="0.0.0.0", debug=True)


<<<<<<< HEAD
def run_receiver():
    print("Waiting...")
    sleep(10)
    channel = front_receiver.get_channel()

    channel.basic_consume(queue='gui_queue',
                            on_message_callback=callback,
=======
def run_consumer():
    print("Waiting...")
    sleep(10)
    channel = front_consumer.get_channel()

    channel.basic_consume(queue='gui_queue',
                            on_message_callback=front_consumer.callback,
>>>>>>> 3c097709b153093cad58b4f8f397d3c5f11b7024
                            auto_ack=True)
    print(' [x] FRONT | Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == "__main__":
<<<<<<< HEAD

    p1 = Process(target=run_web)
    p1.start()
    p2 = Process(target=run_receiver)
    p2.start()

=======
    p1 = Process(target=run_web)
    p1.start()
    p2 = Process(target=run_consumer)
    p2.start()
>>>>>>> 3c097709b153093cad58b4f8f397d3c5f11b7024
