FROM python:latest

WORKDIR /app

COPY requirements.txt ./
COPY ./src/app.py ./src/

RUN pip install --no-cache-dir --root-user-action=ignore -r requirements.txt
RUN rm requirements.txt
RUN apt-get update -qq && apt-get install ffmpeg -y

RUN mkdir upload

# CMD [ "python", "-u", "app.py"] # TODO MSA: uncomment for final submission: auto runs app at start of container
CMD ["sleep", "infinity"] # keeps container running indefinitely