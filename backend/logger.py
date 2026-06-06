import time
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from config import settings

logs_dir = Path(settings.logs_dir)
logs_dir.mkdir(exist_ok=True, parents=True)
log_file = logs_dir / 'app.log'

logging.Formatter.converter = time.localtime

formatter = logging.Formatter(
    fmt="[%(asctime)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

file_hnd = RotatingFileHandler(
    filename=log_file, 
    maxBytes= 10*1024*1024,
    backupCount=5,
    encoding='utf-8')
file_hnd.setFormatter(formatter)

std_hnd = logging.StreamHandler()
std_hnd.setFormatter(formatter)


logging.basicConfig(
    level=logging.INFO,
    handlers=[file_hnd, std_hnd],
    force=True
)

logger = logging.getLogger(__name__)
