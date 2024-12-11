FROM python:3.11.10-alpine3.20
COPY requirements.txt /
RUN pip install -r requirements.txt
WORKDIR /
COPY . /
EXPOSE 80
CMD ["python","-u","main.py"]

