FROM ubuntu:20.04

# Timezone Configuration
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt update && apt install -y    apt-utils \
    wget \
    unzip \
    curl \
    git \
    nano \
    iputils-ping \
    psmisc \
    python3-pip \
    python3-dev

RUN pip3 install flask pika requests
RUN pip3 install pandas pickle5 statistics numpy
RUN pip3 install seaborn scipy scikit-learn
RUN pip3 install numpy  tqdm
RUN pip3 install git+https://github.com/mrapplexz/tika-python
RUN pip3 install scikit-learn
RUN pip3 install  catboost
RUN pip3 install  numpy
RUN pip3 install  pandas
RUN pip3 install  pydantic

WORKDIR /app