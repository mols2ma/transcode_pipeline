# transcode_pipeline

### Run Docker Container

1. In the CLI run `docker-compose up --build --detach`. (`--build` can be omitted after the first run once images are built)

2. Go to `app` container in created `transcode pipeline` container stack in Docker Desktop.

Look at `app` container's logs to see real-time logging of app. Upon startup of `app` container, it should display in the **Logs** tab the following message:

```

2023-07-13 14:42:33 - Transcoder pipeline is ready...

2023-07-13 14:42:33 - Listening for folder changes in '/app/upload'...

```

3. Go to the **Files** tab and navigate to `/app/files/upload/`.

The transcoder pipeline app should be running and listening for video uploads to folder, `/app/files/upload`, within `app` container's file system.

## How To Use App

1. In Docker Desktop, go to `/app/upload` folder on `app` container's file system. This can be done by going to the `app` container > **Files**.

2. Import desired video in the format **<IMDB_ID>.<VIDEO_EXTENSION>**, i.e., `tt1234567.mp4` into the folder from Step 1.
   **Note**: File upload is only supported by import through Docker Desktop. This is to keep the application instance's scope within the container only, without needing a host folder. Also note that the file video name **_has_** to be the IMDB ID **_only_**.

3. Pipeline will detect new file, start pipeline, and display logs as pipeline runs. Logger will first display `----- PIPELINE STARTED... -----` once a file has been uploaded. Note that a logged error message `Pipeline error: <ERROR MESSAGE>` will stop the pipeline instance for that video upload.

4. Once the pipeline successfully runs, the transcoded video will be exported to the folder, `app/files/completed`, which is also within the `app` container's filesystem.

## Architecture and Implementation Choices

![Architectural Diagram](Architectural_Diagram.jpg "Architectural Diagram")

### Tech Stack:

Main Application: **_Python_**

Database: **PostgreSQL**

External Database: **TMDB**

External Libraries: **FFmpeg**

Python Libraries:

- [ffmpeg-python](https://github.com/kkroening/ffmpeg-python)

  - Utilizing a Python wrapper for FFmpeg allows for ease of implementation and readability in the code.

- [watchdog](https://github.com/gorakhargosh/watchdog)

  - Utilizing library to handle file detection for filesystem folders. It provides directory and single file detection.

- [tmdbsimple](https://github.com/celiao/tmdbsimple)

  - Initially utilized `requests` library, however, `tmdbsimple` showed to be a cleaner Python wrapper which utilized Python Objects to represent movies. This conformed better with using SQLAlchemy which is an orm.

- [sqlalchemy](https://www.sqlalchemy.org/)
  - `SQLAlchemy` is a common Python toolkit and ORM for SQL. It is easier to implement for a demo-level project, and it allows easier inserts into the db.
