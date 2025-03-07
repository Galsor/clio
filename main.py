import logging
from dotenv import load_dotenv
from clio.utils import DATE_FORMAT, LOG_FORMAT
from clio.config import load_config
from clio.pipeline import build_clio_pipeline

logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    datefmt=DATE_FORMAT,
)
logger = logging.getLogger(__name__)


def run_clio():
    load_dotenv()
    config = load_config()
    pipeline = build_clio_pipeline(config)
    logger.info("succesfully loaded %s", pipeline)


if __name__ == "__main__":
    run_clio()
