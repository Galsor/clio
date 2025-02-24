from typing import List

from pydantic import BaseModel, Field, create_model
from sklearn.compose import ColumnTransformer

from clio.schemas.facet import FacetConfig


def build_Facets_BaseModel(config: List[FacetConfig]) -> BaseModel:
    return create_model(
        "Facets",
        **{
            facet_config.name: (
                facet_config.annotation_to_extract,
                Field(
                    description=facet_config.description,
                    **facet_config.pydantic_field_kwargs,
                ),
            )
            for facet_config in config
        },
    )


def build_mixed_encoder(config: List[FacetConfig]) -> ColumnTransformer:
    """Dynamically build a pipeline from the given configuration."""
    return ColumnTransformer(
        [
            (facet_config.name, facet_config.vectorizer, [facet_config.name])
            for facet_config in config
        ]
    )
