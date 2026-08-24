import logging

logging.basicConfig(
    format="%(asctime)s %(name)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
    level=logging.INFO,
    filename="scraper.txt"
)

def get_logger(logger_name: str):
    return logging.getLogger(logger_name)
