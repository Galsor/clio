import asyncio
import logging
import time
from typing import List

from pydantic_ai import Agent
from sklearn.base import TransformerMixin

from clio.config import ClioConfig, build_Facets_BaseModel
from clio.utils import generate_short_id

logger = logging.getLogger(__name__)


def setup_facet_extraction_agent(config: ClioConfig) -> Agent:
    agent_config = config.facets_extraction_agent
    facets_model = build_Facets_BaseModel(config)
    agent = Agent(
        agent_config.model_name,
        system_prompt=agent_config.system_prompt,
        result_type=facets_model,
    )
    return agent


class FacetExtractionTransformer(TransformerMixin):
    def __init__(self, config: ClioConfig):
        logger.debug("> Loading agent based on config: %s", config)
        self.agent = setup_facet_extraction_agent(config)
        logger.debug("> Loaded Agent: %s", self.agent)
        self.max_concurrent_requests = (
            config.facets_extraction_agent.max_concurrent_requests
        )

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        if isinstance(X, str):
            X = [X]
        return asyncio.run(self.batch_query(X, self.max_concurrent_requests))

    async def query_agent(self, document: str):
        """Send a single request using the client's run_async method and return the response."""
        # FIXME Shall be replace by a proper id generation and tracking at pipeline level
        tmp_id = generate_short_id(document)
        logger.debug("Querying agent with document [%s]: %s", tmp_id, document)
        try:
            response = await self.agent.run(document)
        except Exception as e:
            logger.error("Error querying agent with document %s", tmp_id)
            response = {"error": str(e)}
        logger.debug("Response: %s for document %s", response, tmp_id)
        return response

    async def batch_query(
        self, documents: List[str], max_concurrent_requests: int = 10
    ):
        """Send multiple requests with a limit on concurrent requests."""
        start_time = time.time()
        logger.debug(
            "Starting batching %s queries with max_concurrent_requests: %s ",
            len(documents),
            max_concurrent_requests,
        )
        semaphore = asyncio.Semaphore(max_concurrent_requests)  # Limit concurrency

        async def bounded_request(doc: str):
            async with semaphore:
                return await self.query_agent(doc)

        tasks = [bounded_request(doc) for doc in documents]
        results = await asyncio.gather(*tasks)
        logger.debug(
            "Finished batching %s queries in %s seconds",
            len(documents),
            time.time() - start_time,
        )
        print(">>> RESULTS: ", results)
        return results
