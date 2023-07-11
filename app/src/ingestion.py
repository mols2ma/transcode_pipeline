from utils import *

class IngestionHandler(FileSystemEventHandler):

    def on_created(self, event):
        """Overrides on_created class within FileSystemEventHandler. Called when a file or directory is created.
        Assumes event represents a single file creation."""

        trigger_pipeline(event.src_path)

class Ingestor:

    upload_path = "../upload/"

    def __init__(self):

        event_handler = IngestionHandler()

        observer = Observer()
        observer.schedule(event_handler, Ingestor.upload_path, recursive=True)
        observer.start()

        try:
            logging.info("Listening for folder changes in '~/app/src/upload'...")
            while observer.is_alive():
                observer.join(1)
        finally:
            observer.stop()
            observer.join()
