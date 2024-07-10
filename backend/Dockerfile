FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

ADD . .

RUN pip install -r requirements.txt
RUN python manage.py collectstatic --noinput