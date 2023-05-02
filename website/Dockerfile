FROM python:3.10-alpine

WORKDIR /usr/src/app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT [ "gunicorn", "--bind", "0.0.0.0:8000", "--log-level=debug", "wsgi:app" ]