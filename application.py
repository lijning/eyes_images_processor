from flask_cors import CORS
from flask import Flask
import logging

app = Flask(__name__)

cors = CORS(app)

logger = logging.getLogger('my_pipeline')

_console_handler = logging.StreamHandler()
_console_handler.setLevel(logging.DEBUG)
_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(message)s')
_console_handler.setFormatter(_formatter)

logger.setLevel(logging.DEBUG)
logger.addHandler(_console_handler)