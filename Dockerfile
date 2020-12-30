FROM python:3.8

RUN mkdir -p /home/bot
WORKDIR /home/bot

ENV BOT_TOKEN=""
ENV TZ=Europe/Minsk
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY . /home/bot
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "server.py"]
