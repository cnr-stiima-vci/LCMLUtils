import os
import os.path
import sys
reload(sys)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.setdefaultencoding('utf-8')

PATH, _ = os.path.split(os.path.dirname(os.path.realpath(__file__)))
ROOT_PATH = os.path.abspath(os.path.join(PATH, os.pardir))
DATA_PATH = os.path.join(PATH, 'lcmlutils', 'data')
BFIS_SERVICE_PORT = '8080'
ANONYMOUS_USER_ID = -1
