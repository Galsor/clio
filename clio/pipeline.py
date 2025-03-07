from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from clio.facets_extraction.agent import FacetExtractionTransformer
from clio.config import ClioConfig


def build_facet_extraction_transformer(config: ClioConfig) -> FacetExtractionTransformer:
    return FacetExtractionTransformer(config)

def build_mixed_encoder(config: ClioConfig) -> ColumnTransformer:
    """Dynamically build a pipeline from the given configuration."""
    return ColumnTransformer(
        [
            (facet_config.name, facet_config.encoder, [facet_config.name])
            for facet_config in config.facets
        ]
    )

def build_clio_pipeline(config:ClioConfig) -> Pipeline:
    return Pipeline(
        [
            ("facet_extraction", build_facet_extraction_transformer(config)),
            ("facet_encoding", build_mixed_encoder(config))
        ]
    )