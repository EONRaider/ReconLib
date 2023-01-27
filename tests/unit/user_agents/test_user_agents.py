import pytest

from reconlib.core.utils.user_agents import random_user_agent


class TestUserAgents:
    def test_random_user_agent(self):
        user_agent = random_user_agent()
        assert isinstance(user_agent, str)
        assert len(user_agent)

    def test_open_invalid_file(self):
        with pytest.raises(FileNotFoundError):
            random_user_agent(file_path="invalid")
