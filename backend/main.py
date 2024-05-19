
from backend.src import back_consumer

if __name__ == "__main__":
    channel = back_consumer.get_channel()
    # Consume messages from the 'data_queue'
    channel.basic_consume(queue='data_queue',
                        on_message_callback=back_consumer.callback,
                        auto_ack=True)

    print(' [x] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()