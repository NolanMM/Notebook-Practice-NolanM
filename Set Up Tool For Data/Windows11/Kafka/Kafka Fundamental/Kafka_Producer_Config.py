from confluent_kafka import Producer

producer_config = {
    'bootstrap.servers': 'localhost:9092'
}

producer = Producer(producer_config)


def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))


while True:
    message = input("Enter message to send to Kafka (or 'exit' to quit): ")
    if message.lower() == 'exit':
        break
    producer.produce('first_topic', value=message, callback=delivery_report)
    producer.flush()
