import os
import logging
import mimetypes
import ffmpeg
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine

"""Global logging"""
logger = logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

"""Utility functions relating to database"""
Base = declarative_base()


def create_database_engine():
    db = os.environ.get('POSTGRES_DB')
    user = os.environ.get('POSTGRES_USER')
    password = os.environ.get('POSTGRES_PASSWORD')
    return create_engine(f'postgresql://{user}:{password}@db:5432/{db}', echo=True)


def init_db():
    db_engine = create_database_engine()
    db_engine.echo = False
    Base.metadata.create_all(db_engine)
    return sessionmaker(bind=db_engine)


"""Utility functions relating to ffmpeg"""


def get_file_metadata(file_path):
    try:
        return ffmpeg.probe(file_path, select_streams="V")['streams'][0]
    except:
        raise Exception(f"Failed to analyze file at {file_path}")


"""Utility functions relating to validation"""


def validate_video(file_path):
    try:
        if "video" in mimetypes.guess_type(file_path)[0]:
            fm = get_file_metadata(file_path)
            if fm is None or fm['codec_type'] != "video":
                raise Exception(
                    f"File at {file_path} is not of type is not of video.")
        else:
            raise Exception(
                f"File at {file_path} is not of type is not of video.")
    except Exception as e:
        raise Exception(e)


"""
If yes then add function or logic to check if its a valid imdbid file name
    (IMDb's identifiers always take the form of two letters, which signify the type of entity being identified, 
        followed by a sequence of at least seven numbers that uniquely identify a specific entity of that type.
            https://developer.imdb.com/documentation/key-concepts
            https://stackoverflow.com/questions/57746487/how-to-run-the-regexmatchingeventhandler-of-watchdog-correctly)
"""


def is_tmdb_id():
    return
