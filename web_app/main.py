from src import app
from src import front_receiver, callback
import os
from time import sleep
# from multiprocessing import Process

if __name__ == "__main__":

    # app.run(host="0.0.0.0", debug=True)

    pid=os.fork()
    if pid:
        app.run(host="0.0.0.0", debug=True)
    else:
        print("Waiting...")
        sleep(7)
        channel = front_receiver.get_channel()

        channel.basic_consume(queue='gui_queue',
                             on_message_callback=callback,
                             auto_ack=True)
        print(' [x] FRONT | Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()


    # p1 = Process(target=app.run, kwargs={"host":"0.0.0.0", "debug":True})
    # p1.start()
    # # p2 = Process(target=channel.basic_consume, kwargs={"queue":"gui_queue", "on_message_callback":callback, "auto_ack":True})


