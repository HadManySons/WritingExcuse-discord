FROM python:3.9.1-buster

WORKDIR /app

COPY BotCreds.py .
COPY requirements.txt .
COPY WritingExcuse-discord.py .
COPY Excuses.txt .

RUN pip install -r requirements.txt

CMD ["python", "WritingExcuse-discord.py"]
