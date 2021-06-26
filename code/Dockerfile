FROM python:3.8-slim-buster

RUN apt-get update && apt-get install -y git

RUN git clone https://github.com/MSDS698/2021-product-analytics-group-project-group_8_fraud_bnb/tree/docker
COPY . /2021-product-analytics-group-project-group_8_fraud_bnb/tree/docker/code
WORKDIR /2021-product-analytics-group-project-group_8_fraud_bnb/tree/docker/code

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000
CMD flask run --host=0.0.0.0