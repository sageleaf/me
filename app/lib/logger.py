import logging
import os

here = os.path.dirname(os.path.abspath(__file__))
logger = logging.basicConfig(filename="../log/development.log" level=logging.INFO)