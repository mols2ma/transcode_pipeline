from utils import *


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

        self.start_ingestion()

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
            transcoder = Transcoder(file_path)
            result = DataProcessor(file_path, session_db)
        except Exception as e:
            logging.info(f"Pipeline error: {e}\n{traceback.format_exc()}")

        logging.info("----- PIPELINE FINISHED.  -----")
