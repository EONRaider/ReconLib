"""
ReconLib: A collection of modules and helpers for active and passive
reconnaissance of remote hosts.

Author: EONRaider
GitHub: https://github.com/EONRaider
Contact: https://www.twitter.com/eon_raider

    Copyright (C) 2023 EONRaider @ keybase.io/eonraider

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see
    <https://github.com/EONRaider/ReconLib/blob/master/LICENSE>.
"""

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
