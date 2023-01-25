from abc import ABC, abstractmethod


class ExternalService(ABC):
    def __init__(self, target: str):
        self.target = target

    def get_query_url(self, *args, **kwargs) -> str:
        """
        Build an RFC 1808 compliant string defining the URL to be
        fetched based on user-supplied parameters

        :return: A string containing the URL formatted with the required
            path and query parameters
        """

    @abstractmethod
    def _query_service(self, *args, **kwargs) -> str:
        """
        Send an HTTP GET request to an external service
        :return: A string containing the service's response
        """
        ...
