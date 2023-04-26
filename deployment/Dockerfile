FROM python:3.8-buster

EXPOSE 8080

COPY /requirements.txt /requirements.txt

RUN apt update && \
    pip install --upgrade pip \
    && pip install -r requirements.txt


COPY /src ./src
COPY /static ./static

ENV PYTHONPATH "${PYTHONPATH}:/src"

CMD ["python", "static/start_bot.py"]