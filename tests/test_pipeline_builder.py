from datetime import date, datetime
from typing import Optional


def test_build_mixed_encoder(pipeline_config):
    from sklearn.compose import ColumnTransformer

    from clio.facets_extraction.pipeline_builder import build_mixed_encoder

    encoder = build_mixed_encoder(pipeline_config)
    assert isinstance(encoder, ColumnTransformer)
    assert len(encoder.transformers) == 5
    assert all(
        [
            encoder.transformers[i][0] == value
            for i, value in enumerate(
                ["short_summary", "message_count", "language", "date", "datetime"]
            )
        ]
    )


def test_build_Facets_BaseModel(pipeline_config):
    from pydantic import BaseModel

    from clio.facets_extraction.pipeline_builder import build_Facets_BaseModel

    Facets = build_Facets_BaseModel(pipeline_config)
    print(Facets.model_fields)
    assert issubclass(Facets, BaseModel)
    assert len(Facets.model_fields) == 5
    assert all(
        [
            field_name in Facets.model_fields
            for field_name in [
                "short_summary",
                "message_count",
                "language",
                "date",
                "datetime",
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
    assert Facets.model_fields["datetime"].description == "Datetime of the document"
    assert Facets.model_fields["short_summary"].annotation is str
    assert Facets.model_fields["message_count"].annotation is float
    assert Facets.model_fields["language"].annotation is str
    assert Facets.model_fields["date"].annotation is Optional[date]
    assert Facets.model_fields["datetime"].annotation is Optional[datetime]
