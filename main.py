import logging

from clio.utils import DATE_FORMAT, LOG_FORMAT

logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    datefmt=DATE_FORMAT,
)
logger = logging.getLogger(__name__)


def run_clio():
    logger.info("No Clio pipeline define. Please implement one in main.py")


if __name__ == "__main__":
    run_clio()
