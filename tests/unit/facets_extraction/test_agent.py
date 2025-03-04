import datetime

import pytest
from pydantic_ai import capture_run_messages, models
from pydantic_ai.messages import (
    ModelRequest,
    ModelResponse,
    SystemPromptPart,
    ToolCallPart,
    UserPromptPart,
    ToolReturnPart,
)
from pydantic_ai.models.test import TestModel
from dirty_equals import IsNow


from clio.facets_extraction.agent import (
    FacetExtractionTransformer,
    setup_facet_extraction_agent,
)

pytestmark = pytest.mark.anyio
models.ALLOW_MODEL_REQUESTS = False


def test_setup_facet_extraction_agent(mock_ClioConfig):
    agent = setup_facet_extraction_agent(mock_ClioConfig)
    assert isinstance(agent.model, TestModel)


@pytest.fixture
def mock_FacetExtractionTransformer(mock_ClioConfig):
    mock_transformer = FacetExtractionTransformer(mock_ClioConfig)
    return mock_transformer


def test_FacetExtractionTransformer_transform(mock_FacetExtractionTransformer):
    with capture_run_messages() as messages:
        results = mock_FacetExtractionTransformer.transform(["doc1", "doc2"])

    assert len(results) == 2
    assert messages == [
        ModelRequest(
            parts=[
                SystemPromptPart(
                    content="You are an AI assistant specializing in extracting key information from provided files containing various types of content, such as conversations, news articles, and corporate documents. Your primary goal is to summarize the most relevant and accurate details concisely while preserving critical context.\n\nGuidelines for Extraction:\n\t1.\tConciseness & Clarity: Extract only the essential information while ensuring clarity and coherence. Avoid redundant or verbose explanations.\n\t2.\tAccuracy & Fidelity: Ensure the extracted information reflects the original meaning without distortion or misinterpretation.\n\t3.\tContext Awareness: Recognize the type of document (conversation, news, corporate, etc.) and adapt the extraction to maintain its intended meaning.\n\t4.\tRelevance Filtering: Prioritize key facts, events, decisions, insights, and actions over minor details.\n\t5.\tNeutrality & Objectivity: Avoid adding opinions, speculations, or biases—strictly focus on the given content.",
                    dynamic_ref=None,
                    part_kind="system-prompt",
                ),
                UserPromptPart(
                    content="doc1",
                    timestamp=IsNow(tz=datetime.timezone.utc),
                    part_kind="user-prompt",
                ),
            ],
            kind="request",
        ),
        ModelResponse(
            parts=[
                ToolCallPart(
                    tool_name="final_result",
                    args={
                        "short_summary": "a",
                        "message_count": 0.0,
                        "language": "a",
                        "date": "2024-01-01",
                    },
                    tool_call_id=None,
                    part_kind="tool-call",
                )
            ],
            model_name="test",
            timestamp=IsNow(tz=datetime.timezone.utc),
            kind="response",
        ),
        ModelRequest(
            parts=[
                ToolReturnPart(
                    tool_name="final_result",
                    content="Final result processed.",
                    tool_call_id=None,
                    timestamp=IsNow(tz=datetime.timezone.utc),
                    part_kind="tool-return",
                )
            ],
            kind="request",
        ),
    ]
