import pytest


@pytest.fixture(scope="session")
def mock_system_prompt() -> str:
    with open(
        "tests/configs/prompts/mock_system_prompt.txt", "r", encoding="utf-8"
    ) as f:
        prompt = f.read()
    return prompt


def test_load_config(mock_system_prompt):
    from clio.config import load_config

    config = load_config("tests/configs/hyperdrive_solutions_inc_config.yml")
    assert config.facets_extraction_agent.model_name == "gpt-4o-mini"
    assert config.facets_extraction_agent.system_prompt == mock_system_prompt
    assert len(config.facets) == 4
