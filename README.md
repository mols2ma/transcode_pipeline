# transcode_pipeline

## How to run app in Docker

### One-Time Initial Environment Set-up

1. Rename `variables.env.template` to `variables.env`.

1. Retrieve environment variables from developer (Monica Andres).

1. Fill in environment variables with respective values.

### Run Docker Container

1. In the CLI run `docker-compose up --build --detach`. (`--build` can be omitted after the first run once images are built)

2. Go to `app` container in created `transcode pipeline` container stack in Docker Desktop.

Transcoder pipeline app should be running and listening for video uploads to folder `/app/upload` folder within `app` container's file system.

Look at `app` container's logs to see real-time logging of app. It should display

```
Transcoder pipeline is ready...
Listening for folder changes in '~/app/src/upload'...
```

## How To Use App

1. Go to `/app/upload` folder on `app` container's file system. This can be accessed in Docker Desktop.

1. Import desired video in the format <IMDB_ID>.movie file, i.e., `tt1234567.mp4`

1. Pipeline will detect new file, start pipeline, and display logs as pipeline runs. Logger will display `----- PIPELINE STARTED... -----`. Note that a logged error message `Pipeline error: <ERROR MESSAGE>` will stop the pipeline instance for that video upload.
