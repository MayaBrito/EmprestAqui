FROM ubuntu:24.04
RUN apt-get update -y && \
    apt-get install -y python-pip python-dev
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
CMD ["python","main.py"]