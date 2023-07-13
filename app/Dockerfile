FROM python:latest

WORKDIR /app

COPY requirements.txt ./
COPY ./src/app.py ./src/

RUN pip install --no-cache-dir --root-user-action=ignore -r requirements.txt
RUN rm requirements.txt
RUN apt-get update -qq && apt-get install ffmpeg -y

RUN mkdir upload
RUN mkdir completed

WORKDIR /app/src

CMD [ "python", "-u", "app.py"]