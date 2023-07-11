from utils import *
from ingestion import Ingestor
from data_processor import DataProcessor

if __name__ == "__main__":

    logging.info("Transcoder pipeline is ready...")

    ingestor = Ingestor() # TODO MSA: reconsider if this needs to be a class or a function
