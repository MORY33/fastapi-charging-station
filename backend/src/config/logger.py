import logging
from fastapi.logger import logger as fastapi_logger

def setup_logger():
    fastapi_logger = logging.getLogger('fastapi')

    log_format = '[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'

    logging.basicConfig(
        format=log_format,
        datefmt=date_format,
        level=logging.INFO,
        handlers=[logging.StreamHandler()]
    )
    fastapi_logger.setLevel(logging.INFO)
