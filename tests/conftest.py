from typing import List

import pytest

from clio.schemas.facet import (
    CategoricalFacet,
    DateFacet,
    DateTimeFacet,
    FacetConfig,
    FreeTextFacet,
    NumericalFacet,
)


@pytest.fixture
def pipeline_config() -> List[FacetConfig]:
    return [
        FreeTextFacet(
            name="short_summary",
            description="Short summary of the document",
            required=True,
        ),
        NumericalFacet(name="message_count", description="Amount of messages"),
        CategoricalFacet(name="language", description="Language of the document"),
        DateFacet(name="date", description="Date of the document", required=False),
        DateTimeFacet(
            name="datetime",
            description="Datetime of the document",
            required=False,
        ),
    ]
