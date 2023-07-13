from utils import *
import os
import datetime as d
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer, String, Date, JSON
from sqlalchemy.orm import declarative_base, sessionmaker
import requests
import tmdbsimple as tmdb

Base = declarative_base()

class TmdbMetadata(Base):
    __tablename__ = "tmdb_metadata"
    id = Column(String, primary_key=True)
    title_metadata = Column(JSON)

    def __repr__(self):
        return f'TmdbMetadata(id={self.id}, title_metadata={self.metadata}'

class VideoLog(Base):
    __tablename__ = "video_log"
    processed_id = Column(Integer, primary_key=True)
    imdb_id = Column(String, ForeignKey('tmdb_metadata.id'))
    file_name = Column(String)
    date_processed = Column(Date)

    def __repr__(self):
        return f'VideoLog(processed_id={self.processed_id}, imdb_id={self.imdb_id}, file_name={self.file_name}, date_processed={self.date_processed})'

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

class DataProcessor:

    def __init__(self, file_path, session):
        
        self.database_session = session
        self.file_path = file_path

        self.insert_tmdb_metadata(self.fetch_tmdb_metadata())
        self.log_video()

    def build_video_log_query(self, file_path):
        return VideoLog(imdb_id=os.path.splitext(os.path.basename(self.file_path))[0], file_name=os.path.basename(self.file_path), date_processed=d.datetime.now().strftime("%Y-%m-%d  %H:%M:%S"))
    
    def log_video(self):
        logging.info("Putting video info into DB...")

        movie_metadata = self.build_video_log_query(self.file_path)
        self.database_session.add(movie_metadata)
        self.database_session.commit()
        logging.info(f'Added transcoded video info to video_log table.')
    
    def insert_tmdb_metadata(self, metadata):
        switch_command = self.database_session.query(TmdbMetadata).\
        filter(TmdbMetadata.id == os.path.splitext(os.path.basename(self.file_path))[0]).first()

        if not switch_command:
            tmdb_metadata = TmdbMetadata(id=os.path.splitext(os.path.basename(self.file_path))[0], title_metadata=metadata)
            self.database_session.add(tmdb_metadata)
            self.database_session.commit()
            logging.info(f'Added TMDB info to tmdb_metadata table.')
    
    def fetch_tmdb_metadata(self):
        logging.info("Fetching info from TMDB...")

        tmdb.API_KEY = os.environ.get('TMDB_API_KEY')
        tmdb.REQUESTS_TIMEOUT = 5
        tmdb.REQUESTS_SESSION = requests.Session()
        movie = tmdb.Movies(os.path.splitext(os.path.basename(self.file_path))[0])
        return(movie.info())


