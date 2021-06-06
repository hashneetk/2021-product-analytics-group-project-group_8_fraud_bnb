FROM python:3.7-alpine
RUN apk add git

COPY . /2021-product-analytics-group-project-group_8_fraud_bnb/code
WORKDIR /2021-product-analytics-group-project-group_8_fraud_bnb/code

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000
CMD flask run --host=0.0.0.0