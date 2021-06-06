# FROM python:3.7-alpine
FROM python:3.8-slim-buster

RUN apt-get update && apt-get install -y git

# RUN apk update
# RUN apk add chromium
# RUN apk add xvfb
# RUN apk add chromium-chromedriver
# RUN apk add python3

#RUN git clone https://github.com/MSDS698/2021-product-analytics-group-project-group_8_fraud_bnb

COPY . /2021-product-analytics-group-project-group_8_fraud_bnb/code
WORKDIR /2021-product-analytics-group-project-group_8_fraud_bnb/code

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN apt-get install -y wget
RUN apt-get install -y unzip

# RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o /chrome.deb
# RUN dpkg -i /chrome.deb || apt-get install -yf
# RUN rm /chrome.deb
#
#
# RUN wget https://chromedriver.storage.googleapis.com/2.31/chromedriver_linux64.zip -o /usr/local/bin/chromedriver


RUN wget -O /2021-product-analytics-group-project-group_8_fraud_bnb/code/chromedriver.zip https://chromedriver.storage.googleapis.com/91.0.4472.19/chromedriver_linux64.zip
RUN unzip /2021-product-analytics-group-project-group_8_fraud_bnb/code/chromedriver.zip chromedriver -d /2021-product-analytics-group-project-group_8_fraud_bnb/code/
RUN chmod +x /2021-product-analytics-group-project-group_8_fraud_bnb/code/chromedriver

EXPOSE 80
CMD flask run --host=0.0.0.0 --port=80