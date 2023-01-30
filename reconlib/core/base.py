import os
from abc import ABC, abstractmethod
from pathlib import Path
from urllib.request import Request, urlopen

from dotenv import load_dotenv

from reconlib.core.exceptions import APIKeyError
from reconlib.core.utils.user_agents import random_user_agent


class ExternalService(ABC):
    def __init__(self, target: str, user_agent: str, encoding: str):
        self.target = target
        self.user_agent = user_agent
        self.encoding = encoding

    @abstractmethod
    def get_query_url(self, *args, **kwargs) -> str:
        """
        Build an RFC 1808 compliant string defining the URL to be
        fetched based on user-supplied parameters

        :return: A string containing the URL formatted with the required
            path and query parameters
        """

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
        target: str,
        user_agent: str,
        encoding: str,
        api_key: [str, Path],
        api_key_env_name: str,
    ):
        super().__init__(target, user_agent, encoding)
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
                    f"attribute or set a '{self.api_key_env_name}' environment"
                    f"variable with the appropriate value."
                )
            self._api_key = api_key
