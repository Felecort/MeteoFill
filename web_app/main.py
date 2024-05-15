from src import app
from src import channel, callback
from multiprocessing import Process

if __name__ == "__main__":
    threads = []
    p1 = Process(target=app.run_server, kwargs={"host":"0.0.0.0", "debug":True})
    p2 = Process(target=channel.basic_consume, kwargs={"queue":"gui_queue", "on_message_callback":callback, "auto_ack":True})

    p1.run()
    p2.run()
