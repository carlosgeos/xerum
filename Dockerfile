# syntax=docker/dockerfile:1

FROM python:3.9-slim as base
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .

FROM base as dev
ENV FLASK_ENV=development
ENTRYPOINT ["flask", "run"]
CMD ["--host=0.0.0.0"]

FROM base as prod
CMD gunicorn --bind 0.0.0.0:$PORT app:app --timeout 600
