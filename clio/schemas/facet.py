from typing import Optional, Type

from pydantic import BaseModel, ConfigDict, computed_field, field_validator

from clio.facets_extraction.facets import AVAILABLE_FACET_TYPES

class FacetConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    name: str
    description: str
    type: str
    pydantic_field_kwargs: dict = {}
    required: bool = True

    @field_validator("type", mode="before")
    @classmethod
    def validate_facet_type(cls, value):
        if value in AVAILABLE_FACET_TYPES:
            return value
        raise ValueError(
            f"Invalid facet type: {value}. Must be one of {list(AVAILABLE_FACET_TYPES.keys())}"
        )

    @field_validator("pydantic_field_kwargs", mode="before")
    @classmethod
    def validate_pydantic_field_kwargs(cls, value):
        if isinstance(value, dict):
            return value
        raise ValueError(
            f"Invalid pydantic_field_kwargs: {value}. Must be a dictionary not {type(value)}"
        )

    @computed_field
    @property
    def encoder(self) -> Type:
        return AVAILABLE_FACET_TYPES[self.type].encoder

    @computed_field
    @property
    def annotation_to_extract(self) -> Type:
        extracted_type = AVAILABLE_FACET_TYPES[self.type].extracted_type
        if not self.required:
            return Optional[extracted_type]
        return extracted_type
