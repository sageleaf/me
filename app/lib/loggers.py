import logging
import sys 

logger = logging.getLogger('APPLICATION')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s]: %(message)s', "%Y-%m-%d %H:%M:%S")

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)