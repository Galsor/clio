from clio.facets_extraction.pipeline_builder import (
    build_Facets_BaseModel,
)
from clio.schemas.facet import CategoricalFacet, DateFacet, FreeTextFacet


def run_clio():
    print("Hello from Clio!")
    pipeline_config = [
        FreeTextFacet(
            name="short_summary", description="Short summary of the document"
        ),
        FreeTextFacet(name="description", description="Description of the document"),
        CategoricalFacet(name="language", description="Language of the document"),
        DateFacet(name="date", description="Date of the document"),
    ]
    # encoder = build_mixed_encoder(pipeline_config)
    Facets = build_Facets_BaseModel(pipeline_config)
    print(Facets.model_json_schema())


if __name__ == "__main__":
    run_clio()
