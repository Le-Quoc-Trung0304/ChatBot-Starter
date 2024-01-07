# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# install app dependencies
RUN apt-get update && apt-get install -y python3=3.10.* python3-pip
RUN pip install flask==3.0.* requests


WORKDIR /app

# install app
COPY . /app

# final configuration
ENV FLASK_APP=app.py
EXPOSE 8000
# Run the application
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "8000"]