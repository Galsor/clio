from tests.eval.eval_facets_extraction import (
    evaluate_facet_extraction_on_hyperdrive_solutions_inc_conversations_dataset,
)
import logging
from clio.utils import LOG_FORMAT, DATE_FORMAT

logging.basicConfig(
    level=logging.DEBUG,  # Capture DEBUG, INFO, WARNING, ERROR, CRITICAL
    format=LOG_FORMAT,
    datefmt=DATE_FORMAT
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    eval_results = (
        evaluate_facet_extraction_on_hyperdrive_solutions_inc_conversations_dataset()
    )
    eval_results.save_json()

    # Add additional evaluation steps here
    # ...
    logger.info("> Evaluation terminated successfully")
