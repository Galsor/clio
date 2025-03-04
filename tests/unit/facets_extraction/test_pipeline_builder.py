from datetime import date
from typing import Optional

from pydantic import BaseModel
from sklearn.compose import ColumnTransformer

from clio.facets_extraction.pipeline_builder import (
    build_Facets_BaseModel,
    build_mixed_encoder,
)


def test_build_mixed_encoder(facets_config):
    encoder = build_mixed_encoder(facets_config)
    assert isinstance(encoder, ColumnTransformer)
    assert len(encoder.transformers) == 4
    assert all(
        [
            encoder.transformers[i][0] == value
            for i, value in enumerate(
                ["short_summary", "message_count", "language", "date"]
            )
        ]
    )


def test_build_Facets_BaseModel(facets_config):
    Facets = build_Facets_BaseModel(facets_config)
    assert issubclass(Facets, BaseModel)
    assert len(Facets.model_fields) == 4
    assert all(
        [
            field_name in Facets.model_fields
            for field_name in [
                "short_summary",
                "message_count",
                "language",
                "date",
            ]
        ]
    )
    assert (
        Facets.model_fields["short_summary"].description
        == "Short summary of the document"
    )
    assert Facets.model_fields["message_count"].description == "Amount of messages"
    assert Facets.model_fields["language"].description == "Language of the document"
    assert Facets.model_fields["date"].description == "Date of the document"
    assert Facets.model_fields["short_summary"].annotation is str
    assert Facets.model_fields["message_count"].annotation is float
    assert Facets.model_fields["language"].annotation is str
    assert Facets.model_fields["date"].annotation is Optional[date]


def test_Facets_serialisability(facets_config):
    Facets = build_Facets_BaseModel(facets_config)
    today = date.today()
    facets = Facets(
        short_summary="A short summary",
        message_count=4,
        language="en",
        date=today,
    )
    assert (
        facets.model_dump_json()
        == f"""{{"short_summary":"A short summary","message_count":4.0,"language":"en","date":"{today}"}}"""
    )
