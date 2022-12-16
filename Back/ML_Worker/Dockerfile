FROM python:3.9
RUN apt-get update && apt-get install git make automake gcc g++ subversion
RUN pip3 install git+https://github.com/mrapplexz/tika-python scikit-learn catboost numpy pandas pydantic pika
WORKDIR /opt
COPY model ./model
COPY *.py .
WORKDIR /opt
ENTRYPOINT ["python3", "listener.py"]