from utils import *
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from transcoder import Transcoder
from data_processor import DataProcessor


class IngestionHandler(FileSystemEventHandler):

    def __init__(self, pipeline, session):
        self.pipeline = pipeline
        self.database_session = session

    upload_path = "../upload/"

    def on_created(self, event):
        """Assumes event represents a single file creation."""

        self.pipeline.trigger_pipeline(event.src_path, self.database_session)


class Pipeline:

    def __init__(self, session_db):
        self.sesssion_db = session_db

    def start_ingestion(self):
        event_handler = IngestionHandler(self, self.sesssion_db)

        observer = Observer()
        observer.schedule(
            event_handler, IngestionHandler.upload_path, recursive=True)
        observer.start()

        try:
            logging.info(
                "Listening for folder changes in '~/app/src/upload'...")
            while observer.is_alive():
                observer.join(1)
        finally:
            observer.stop()
            observer.join()

    def trigger_pipeline(self, file_path, session_db):
        logging.info("----- PIPELINE STARTED... -----")

        try:
            validate_video(file_path)
            logging.info(f"Detected and validated video file at {file_path}")

            t = Transcoder(file_path)
            t.transcode()

            d = DataProcessor(file_path, session_db)
            d.insert_tmdb_metadata(d.fetch_tmdb_metadata())
            d.insert_video_log()

        except Exception as e:
            logging.info(f"Pipeline error: {e}\n{traceback.format_exc()}")

        logging.info("----- PIPELINE FINISHED.  -----")
