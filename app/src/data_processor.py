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
    date_processed = Column(Date)

    def __repr__(self):
        return f'VideoLog(processed_id={self.processed_id}, imdb_id={self.imdb_id}, file_name={self.file_name}, file_type={self.file_type}, date_processed={self.date_processed})'

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
