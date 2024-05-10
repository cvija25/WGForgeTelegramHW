FROM python:3.10

WORKDIR /code

RUN apt-get update && \
    apt-get install -y ffmpeg

COPY . /code

RUN pip install -r requirements.txt

CMD [ "python3", "bot.py" ]
