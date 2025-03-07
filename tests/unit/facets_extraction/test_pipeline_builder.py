from datetime import date
from typing import Optional

from pydantic import BaseModel
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from skrub import DatetimeEncoder, GapEncoder, TextEncoder

from clio.config import build_Facets_BaseModel
from clio.clio.pipeline import (
    build_mixed_encoder,
)


def test_build_mixed_encoder(mock_ClioConfig):
    encoder = build_mixed_encoder(mock_ClioConfig)
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
    assert all(
        [
            isinstance(encoder.transformers[i][1], cls)
            for i, cls in enumerate(
                [TextEncoder, StandardScaler, GapEncoder, DatetimeEncoder]
            )
        ]
    )


def test_build_Facets_BaseModel(mock_ClioConfig):
    Facets = build_Facets_BaseModel(mock_ClioConfig)
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


def test_Facets_serialisability(mock_ClioConfig):
    Facets = build_Facets_BaseModel(mock_ClioConfig)
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
