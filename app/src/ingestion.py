from utils import *

class IngestionHandler(FileSystemEventHandler):

    def __init__(self, session):
        self.database_session = session

    upload_path = "../upload/"

    def on_created(self, event): # TODO MSA: watch if on_created gets called twice when adding video to folder
        """Overrides on_created class within FileSystemEventHandler. Called when a file or directory is created.
        Assumes event represents a single file creation."""

        trigger_pipeline(event.src_path, self.database_session)

class Pipeline:

    def __init__(self, session_db):

        event_handler = IngestionHandler(session_db)

        observer = Observer()
        observer.schedule(event_handler, IngestionHandler.upload_path, recursive=True)
        observer.start()

        try:
            logging.info("Listening for folder changes in '~/app/src/upload'...")
            while observer.is_alive():
                observer.join(1)
        finally:
            observer.stop()
            observer.join()