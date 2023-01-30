from pathlib import Path

import pytest

from reconlib.core.utils.user_agents import random_user_agent


@pytest.fixture
def user_agents_file(root_dir) -> Path:
    return root_dir.joinpath("reconlib/core/utils/user_agents_list.txt")


@pytest.fixture
def user_agents(user_agents_file) -> set[str]:
    with open(user_agents_file, encoding="utf_8") as file:
        return {user_agent.rstrip() for user_agent in file.readlines()}


class TestUserAgents:
    def test_random_user_agent(self, user_agents):
        assert random_user_agent() in user_agents

    def test_open_invalid_file(self):
        with pytest.raises(FileNotFoundError):
            random_user_agent(file_path="invalid")
