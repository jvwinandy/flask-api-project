FROM python:3.11-slim-bullseye
LABEL manteiner="jvwinandy.com"

COPY requirements.txt /tmp/requirements.txt
COPY src /src
WORKDIR /src

EXPOSE 5000

RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt

ENV FLASK_APP=/src/flask_api/app.py
ENV PATH="/py/bin:$PATH"
RUN ls
