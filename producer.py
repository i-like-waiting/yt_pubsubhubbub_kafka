from kafka import KafkaProducer

def send_json(topic, msg):
    producer = KafkaProducer(bootstrap_servers='localhost:9092')
    ack = producer.send(topic, msg)
    metadata = ack.get()
    print(metadata.topic)
    print(metadata.partition)
# producer.send('sample', key=b'message-two', value=b'This is Kafka-Python')