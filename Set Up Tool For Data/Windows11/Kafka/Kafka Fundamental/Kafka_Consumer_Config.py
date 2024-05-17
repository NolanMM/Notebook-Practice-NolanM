from confluent_kafka import Consumer, KafkaError, KafkaException

consumer_config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'my_consumer_group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(consumer_config)

consumer.subscribe(['first_topic'])

try:
    while True:
        msg = consumer.poll(1.0)  # Timeout of 1 second

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                print('End of partition reached {}/{}'.format(msg.topic(), msg.partition()))
            elif msg.error():
                raise KafkaException(msg.error())
        else:
            print('Received message: {}'.format(msg.value().decode('utf-8')))
finally:
    consumer.close()
