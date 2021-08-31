FROM python:3.9.6
WORKDIR /usr/src/app
RUN apt-get update
COPY requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 8000
COPY . /usr/src/app
