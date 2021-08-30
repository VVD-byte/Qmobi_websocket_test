FROM python:3.9.6
WORKDIR /app
RUN apt-get update
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 3306
EXPOSE 8000
COPY . /app
