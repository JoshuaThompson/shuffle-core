FROM python:3.6.4-jessie

ENV FLASK_APP src/app.py

COPY requirements.txt .
COPY src src

RUN pip3 install -r requirements.txt

CMD [ "flask", "run", "--host=0.0.0.0" ]