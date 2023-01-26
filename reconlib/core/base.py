from abc import ABC, abstractmethod
from urllib.request import Request, urlopen

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

    def _query_service(self, url: str) -> str:
        """
        Send an HTTP GET request to an external service
        :return: A string containing the service's response
        """
        request = Request(
            url=url,
            data=None,
            headers={
                "User-Agent": self.user_agent
                if self.user_agent is not None
                else random_user_agent()
            },
        )
        with urlopen(request) as response:
            return response.read().decode(self.encoding)
