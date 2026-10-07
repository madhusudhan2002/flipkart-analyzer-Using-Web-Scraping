import logging
import os

def setup_logger():
    log_dir = "logs"

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logging.basicConfig(
        filename="logs/scraper.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    return logging