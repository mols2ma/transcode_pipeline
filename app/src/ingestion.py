from utils import logging
import ffmpeg
import mimetypes
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def get_metadata(path):
    try:
        return ffmpeg.probe(path, select_streams="V")['streams'][0]
    except:
        return None


def is_video(file_path):
    if "video" in mimetypes.guess_type(file_path)[0]:
        metadata = get_metadata(file_path)
        if metadata is not None:
            return metadata['codec_type'] == "video"
    return False


class Ingestor:

    upload_path = "../upload/"

    def __init__(self):

        event_handler = FileSystemEventHandler()
        event_handler.on_created = Ingestor.on_created

        observer = Observer()
        observer.schedule(event_handler, Ingestor.upload_path, recursive=True)
        observer.start()

        try:
            logging.info(
                "Listening for folder changes in '~/app/src/upload'...")
            while observer.is_alive():
                observer.join(1)
        finally:
            observer.stop()
            observer.join()

    def on_created(event):
        if is_video(event.src_path):
            logging.info("Video successfully detected...")
            logging.info("Transcoding video...")
            logging.info("Validating title...")
        else:
            logging.error("File type is not of video.")
