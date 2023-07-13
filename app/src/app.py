from utils import *
from ingestion import Pipeline
from data_processor import *


if __name__ == "__main__":

    logging.info("Transcoder pipeline is ready...")
    Session = init_db()

    pipeline = Pipeline(session_db=Session())
    pipeline.start_ingestion()
