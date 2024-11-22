FROM python:latest

RUN mkdir /transcode_pipeline_app

WORKDIR /transcode_pipeline_app

COPY requirements.txt ./
COPY ./src/ ./src/

RUN pip install --no-cache-dir --root-user-action=ignore -r requirements.txt
RUN rm requirements.txt
RUN apt-get update -qq && apt-get install ffmpeg -y

RUN mkdir files
RUN mkdir files/upload
RUN mkdir files/completed

# CMD [ "python", "-u", "src/app.py"]
CMD ["sleep", "infinity"] # TODO MSA: remove before final sub, keeps container running indefinitely TODO MSA: remove before final sub