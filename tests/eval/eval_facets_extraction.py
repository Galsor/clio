import json
from typing import List

from dotenv import load_dotenv

from clio.config import load_config
from clio.facets_extraction.agent import FacetExtractionTransformer
from tests.eval import EVAL_CONFIG_PATH, EVAL_DATA_PATH
from tests.eval.utils import EvalResults

load_dotenv()


def load_hyperdrive_solutions_inc_conversations_dataset() -> List[dict]:
    """
    Load the Hyperdrive Solutions Inc. Conversations dataset.
    """
    with open(EVAL_DATA_PATH / "hyperdrive_solutions_inc_conversations.json") as f:
        json_data = json.load(f)
    return [
        json.dumps(conv) for conv in json_data
    ]  # reformat conversation in string to prevent type conflict in agent processing


def setup_hyperdrive_solutions_inc_facet_extractor() -> FacetExtractionTransformer:
    config = load_config(EVAL_CONFIG_PATH / "hyperdrive_solutions_inc_config.yml")
    transformer = FacetExtractionTransformer(config)
    return transformer


def evaluate_facet_extraction_on_hyperdrive_solutions_inc_conversations_dataset() -> (
    EvalResults
):
    """
    Evaluate the facet extraction agent on the given dataset.
    """
    conversations = load_hyperdrive_solutions_inc_conversations_dataset()
    transformer = setup_hyperdrive_solutions_inc_facet_extractor()

    results = transformer.transform(conversations)
    return EvalResults(run_results=results)
