FROM python:3.8-buster

EXPOSE 8080

COPY /requirements.txt /requirements.txt

RUN apt update && \
    pip install --upgrade pip \
    && pip install -r requirements.txt

WORKDIR nometa_bot

COPY /src ./src
COPY /static ./static

ENV PYTHONPATH "${PYTHONPATH}:/nometa_bot/src"

CMD ["python", "static/start_bot.py"]