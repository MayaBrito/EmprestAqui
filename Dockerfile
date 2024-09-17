FROM python:3.11.10-alpine3.20
WORKDIR /
COPY . /
EXPOSE 80
RUN pip install -r requirements.txt
CMD ["python","main.py"]

