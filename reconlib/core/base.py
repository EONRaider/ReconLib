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

import os
from abc import ABC, abstractmethod
from pathlib import Path
from urllib.request import Request, urlopen

from dotenv import load_dotenv

from reconlib.core.exceptions import APIKeyError
from reconlib.core.utils.user_agents import random_user_agent


class ExternalService(ABC):
    def __init__(self, user_agent: str, encoding: str):
        self.user_agent = user_agent
        self.encoding = encoding

    def __repr__(self):
        attrs = (f"{attr}={value}" for attr, value in self.__dict__.items())
        return f"{self.__class__.__name__}({', '.join(attrs)})"

    @abstractmethod
    def get_query_url(self, *args, **kwargs) -> str:
        """
        Build an RFC 1808 compliant string defining the URL to be
        fetched based on user-supplied parameters

        :return: A string containing the URL formatted with the required
            path and query parameters
        """

    @abstractmethod
    def fetch_subdomains(self, target: str) -> set[str]:
        """
        Utility method that executes a request to the service's API,
        processes the response and returns a set of known subdomains for
        a given target

        :param target: A domain name to search for in the service's API
        """
        ...

    def _query_service(self, url: str, headers: dict = None) -> str:
        """
        Send an HTTP GET request to an external service
        :return: A string containing the service's response
        """
        # Build a User-Agent header from a user-supplied value or get a
        # random agent
        ua_header = {
            "User-Agent": self.user_agent
            if self.user_agent is not None
            else random_user_agent()
        }

        # Merge the User-Agent header with any supplied additional values
        headers = {**headers, **ua_header} if headers is not None else ua_header

        with urlopen(Request(url=url, data=None, headers=headers)) as response:
            return response.read().decode(self.encoding)


class AuthenticatedExternalService(ExternalService, ABC):
    def __init__(
        self,
        user_agent: str,
        encoding: str,
        api_key: [str, Path],
        api_key_env_name: str,
    ):
        super().__init__(user_agent, encoding)
        self.api_key_env_name = api_key_env_name
        self.api_key = api_key

    @property
    def api_key(self) -> str:
        """
        Get the API key value
        """
        return self._api_key

    @api_key.setter
    def api_key(self, value: [str, Path]) -> None:
        """
        Set the API key value from a user-supplied argument or by
        reading the "VIRUSTOTAL_API_KEY" environment variable
        :param value: A string containing an API key for use in
            requests to VirusTotal API or the absolute path to a file
            from which the value can be read
        """
        if value is not None:
            if (file_path := Path(value)).is_file():  # Read API key from file
                load_dotenv(file_path, override=True)
                self._api_key = os.environ.get(self.api_key_env_name)
            else:  # Read API key as an assigned string value
                self._api_key = value
        else:  # Read API key from environment variable
            if (api_key := os.environ.get(self.api_key_env_name)) is None:
                raise APIKeyError(
                    f"An API key is required when retrieving information from "
                    f"VirusTotal. Either initialize an API object with the 'api_key' "
                    f"attribute or set a '{self.api_key_env_name}' environment "
                    f"variable with the appropriate value."
                )
            self._api_key = api_key
