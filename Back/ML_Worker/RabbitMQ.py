
import pika
from predictor import Predictor, ModelInputs
from pathlib import Path


print(1)
#declaring the credentials needed for connection like host, port, username, password, exchange etc
credentials = pika.PlainCredentials('xmasuser','xmaspassword')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='85.192.34.254', port='5672', credentials= credentials))
channel = connection.channel()
#channel.exchange_declare('/', durable=True, exchange_type='topic')
#defining callback functions responding to corresponding queue callbacks
pred = Predictor(Path('./model'))
def callbackFunctionForQueueA(ch,method,properties,body):
    pred.process(ModelInputs(doc_path=Path(body["path"])))

channel.basic_consume(queue='predict', on_message_callback=callbackFunctionForQueueA, auto_ack=True)

channel.start_consuming()

