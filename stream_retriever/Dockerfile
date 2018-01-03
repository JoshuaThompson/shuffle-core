FROM python:3.6.4-jessie

COPY requirements.txt .
COPY retrieve_streams.py .

RUN pip3 install -r requirements.txt

CMD [ "python3", "-u", "retrieve_streams.py" ]