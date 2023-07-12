import time
import logging
import mimetypes
import ffmpeg
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from transcoder import Transcoder
from data_processor import DataProcessor
import traceback

logger = logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

def get_file_metadata(file_path):
    try:
        return ffmpeg.probe(file_path, select_streams="V")['streams'][0]
    except:
        raise Exception(f"Failed to analyze file at {file_path}")

def validate_video(file_path):
    try:
        if "video" in mimetypes.guess_type(file_path)[0]:
            fm = get_file_metadata(file_path)
            if fm is None or fm['codec_type'] != "video":
                raise Exception(f"File at {file_path} is not of type is not of video.")
        else:
            raise Exception(f"File at {file_path} is not of type is not of video.")
    except Exception as e:
        raise Exception(e)

def trigger_pipeline(file_path, session_db):
    try:
        validate_video(file_path)
        logging.info(f"Detected and validated video file at {file_path}")

        transcoder = Transcoder(file_path) # TODO MSA: refactor to consider continuation of class or method

        result = DataProcessor(file_path, session_db) # TODO MSA: refactor to consider continuation of class or method
    except Exception as e:
        logging.info(f"Pipeline error: {e}\n{traceback.format_exc()}")
