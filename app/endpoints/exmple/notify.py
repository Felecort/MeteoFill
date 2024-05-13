import json 
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

queue = channel.queue_declare("order_notify")
queue_name = queue.method.queue


channel.queue_bind(
    exchange="order",
    queue=queue_name,
    routing_key="order.notify"
)

def callback(ch, method, properties, body):
    playload = json.loads(body)
    print(f"[x] Notifying {playload['user_email']}")
    print(f"[x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(on_message_callback=callback, queue=queue_name)

print("[x] Waiting for notify messages. To exit press ctrl + C")

channel.start_consuming()