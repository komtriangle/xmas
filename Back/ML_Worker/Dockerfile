FROM python:3.9
RUN apt-get update && apt-get -y install git make automake gcc g++ subversion default-jre
RUN pip3 install git+https://github.com/mrapplexz/tika-python scikit-learn catboost numpy pandas pydantic pika
WORKDIR /opt
#COPY Back/ML_Worker/model ./model
COPY Back/ML_Worker .
WORKDIR /opt
ENTRYPOINT ["python3", "listener.py"]