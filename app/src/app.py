from utils import *
from ingestion import Pipeline
from data_processor import *


if __name__ == "__main__":

    logging.info("Transcoder pipeline is ready...")
    Session = init_db()

    # TODO MSA: reconsider if this needs to be a class or a function
    pipeline_status = Pipeline(session_db=Session())
