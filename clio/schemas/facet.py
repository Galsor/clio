from datetime import date, datetime
from typing import Any, Optional, Type

from pydantic import BaseModel, ConfigDict, computed_field, field_validator
from sklearn.base import TransformerMixin
from sklearn.preprocessing import StandardScaler
from skrub import DatetimeEncoder, GapEncoder, TextEncoder


class FacetConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    name: str
    extracted_type: Type[Any]
    description: str
    vectorizer: TransformerMixin
    pydantic_field_kwargs: dict = {}
    required: bool = True

    @field_validator("extracted_type", mode="before")
    @classmethod
    def validate_type(cls, value):
        if isinstance(value, type) and value.__module__ == "builtins":
            return value
        if isinstance(value, type) and issubclass(value, BaseModel):
            return value
        raise ValueError(
            f"Invalid type: {value}. Must be a built-in type or a Pydantic BaseModel subclass."
        )

    @field_validator("vectorizer", mode="before")
    @classmethod
    def validate_vectorizer(cls, value):
        if not isinstance(value, TransformerMixin):
            raise ValueError(
                "Invalid vectorizer: {value}. Must be an instance of TransformerMixin"
            )
        return value

    @computed_field
    @property
    def annotation_to_extract(self) -> type:
        if not self.required:
            return Optional[self.extracted_type]
        return self.extracted_type


class FreeTextFacet(FacetConfig):
    extracted_type: Type[str] = str
    vectorizer: TransformerMixin = TextEncoder()


class CategoricalFacet(FacetConfig):
    extracted_type: Type[str] = str
    vectorizer: TransformerMixin = GapEncoder()


class NumericalFacet(FacetConfig):
    extracted_type: Type[float] = float
    vectorizer: TransformerMixin = StandardScaler()


class DateFacet(FacetConfig):
    extracted_type: Type[date] = date
    vectorizer: TransformerMixin = DatetimeEncoder(
        resolution="day", add_total_seconds=False, add_weekday=True
    )


class DateTimeFacet(FacetConfig):
    extracted_type: Type[datetime] = datetime
    vectorizer: TransformerMixin = DatetimeEncoder(
        resolution="second", add_total_seconds=False
    )
