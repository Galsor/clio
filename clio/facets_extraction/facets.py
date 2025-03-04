from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Type

from sklearn.base import TransformerMixin
from sklearn.preprocessing import StandardScaler
from skrub import DatetimeEncoder, GapEncoder, TextEncoder

# Facet types registry
AVAILABLE_FACET_TYPES = {}


@dataclass
class FacetType:
    name: str
    description: str
    encoder: TransformerMixin
    extracted_type: Type[Any]

    def __post_init__(self):
        AVAILABLE_FACET_TYPES[self.name] = self


CategoricalFacet = FacetType(
    name="default_categorical",
    description="A categorical facet",
    encoder=GapEncoder(),
    extracted_type=str,
)
FreeTextFacet = FacetType(
    name="default_free_text",
    description="A free text facet",
    encoder=TextEncoder(),
    extracted_type=str,
)
NumericalFacet = FacetType(
    name="default_numerical",
    description="A numerical facet",
    encoder=StandardScaler(),
    extracted_type=float,
)
DateFacet = FacetType(
    name="default_date",
    description="A date facet",
    encoder=DatetimeEncoder(
        resolution="day", add_total_seconds=False, add_weekday=True
    ),
    extracted_type=date,
)
DateTimeFacet = FacetType(
    name="default_datetime",
    description="A datetime facet",
    encoder=DatetimeEncoder(
        resolution="second", add_total_seconds=True, add_weekday=True
    ),
    extracted_type=datetime,
)
