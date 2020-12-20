FROM python:3.8.5

RUN apt-get update && apt-get install -y python3-dev
WORKDIR ./
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
WORKDIR /bot
COPY . .

CMD python3 bot.py