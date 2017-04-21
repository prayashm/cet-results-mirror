FROM  python:2.7-slim

WORKDIR /

ADD . /

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "server.py"]
