import sys

import pika
from predictor import Predictor, ModelInputs
from pathlib import Path


if __name__ == '__main__':
    credentials = pika.PlainCredentials('xmasuser','xmaspassword')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='85.192.34.254', port='5672', credentials= credentials))
    channel = connection.channel()
    pred = Predictor(Path('./model'))

    def callbackFunctionForQueueA(ch,method,properties,body):
        try:
            result = pred.process(ModelInputs.parse_raw(body))
            print(result)
        except Exception as e:
            print(e, file=sys.stderr)
    channel.basic_consume(queue='predict', on_message_callback=callbackFunctionForQueueA, auto_ack=True)
    channel.start_consuming()
