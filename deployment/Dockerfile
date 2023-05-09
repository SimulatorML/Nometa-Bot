FROM python:3.8-buster

EXPOSE 8080

COPY /requirements.txt /requirements.txt

RUN apt update && \
    pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu

COPY /src ./src
COPY /static ./static

ENV PYTHONPATH "${PYTHONPATH}:/src"

CMD ["python", "static/start_bot.py"]