import os
from pathlib import Path
from typing import List

import yaml
from pydantic import BaseModel, FilePath, computed_field, Field, create_model


from clio.schemas.facet import FacetConfig


class AgentConfig(BaseModel):
    model_name: str
    system_prompt_path: FilePath
    max_concurrent_requests: int = 10

    @computed_field
    @property
    def system_prompt(self) -> str:
        with open(self.system_prompt_path, "r", encoding="utf-8") as f:
            return f.read()


class ClioConfig(BaseModel):
    facets_extraction_agent: AgentConfig
    facets: List[FacetConfig]

def build_Facets_BaseModel(config: ClioConfig) -> BaseModel:
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
            for facet_config in config.facets
        },
    )

def load_config(config_dir: os.PathLike = "configs/config.yml") -> ClioConfig:
    """Open all yaml files in the config directory and return a dictionary with the contents."""
    config_path = Path(config_dir)
    with open(config_path, "r", encoding="utf-8") as f:
        configs = yaml.safe_load(f)

    return ClioConfig(**configs)
