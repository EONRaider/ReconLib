import json
import os
import urllib.error
from collections import defaultdict
from enum import Enum
from urllib.parse import urlunparse, urlencode, urlparse

from dotenv import load_dotenv

from reconlib.core.base import ExternalService
from reconlib.core.exceptions import APIKeyError


class VirusTotal(Enum):
    """Enumeration of API endpoints made available by VirusTotal"""

    URL = urlparse("https://www.virustotal.com/api/v3")
    SUBDOMAINS = "domains/{}/subdomains"


class API(ExternalService):
    def __init__(
        self,
        target: str,
        *,
        user_agent: str = None,
        encoding: str = "utf_8",
        api_key: str = None,
    ):
        """
        Wrapper for HTTP requests to the API of VirusTotal

        :param target: A domain name to search for in VirusTotal API
        :param user_agent: User-agent string to use when querying the
            VirusTotal API (defaults to None for a random user-agent
            string to be used at each new request)
        :param encoding: Encoding used on responses provided by the
            VirusTotal API
        :param api_key: An API key for use in requests to VirusTotal API
        """
        super().__init__(target, user_agent, encoding)
        self.api_key = api_key
        self.results: dict[str, dict] = defaultdict(dict)
        self.subdomains: dict[str, set] = dict()

    @property
    def api_key(self) -> str:
        """
        Get the API key value
        """
        return self._api_key

    @api_key.setter
    def api_key(self, value: str) -> None:
        """
        Set the API key value from a user-supplied argument or by
        reading the "VIRUSTOTAL_API_KEY" environment variable
        :param value: A string containing an API key
        """
        if value is not None:
            self._api_key = value
        else:
            load_dotenv()
            if (api_key := os.environ.get("VIRUSTOTAL_API_KEY")) is None:
                raise APIKeyError(
                    "An API key is required when retrieving information from "
                    "VirusTotal. Either initialize an API object with the 'api_key' "
                    "attribute or set a 'VIRUSTOTAL_API_KEY' environment variable "
                    "with the appropriate value."
                )
            self._api_key = api_key

    @property
    def headers(self) -> dict:
        """
        A dictionary containing the headers required by VirusTotal API
        """
        return {"accept": "application/json", "x-apikey": self.api_key}

    def get_query_url(self, endpoint: VirusTotal, params: dict = None) -> str:
        """
        Build an RFC 1808 compliant string defining the URL to be
        fetched based on user-supplied parameters

        :param endpoint: An enumerated endpoint value of type VirusTotal
        :param params: A dictionary mapping query string parameters to
            their respective values
        :return: The URL formatted as a string
        """
        return urlunparse(
            (
                (url := VirusTotal.URL.value).scheme,
                url.netloc,
                f"{url.path}/{endpoint.value.format(self.target)}",
                "",
                urlencode(params) if params else "",
                "",
            )
        )

    def get_subdomains(self, limit: int = 1000) -> set[str]:
        """
        Send an HTTP request to VirusTotal's "domains" API endpoint
        and fetch the results from is "subdomains" relationship

        :param limit: Maximum number of subdomains to retrieve per
            request

        :return: A set of strings containing each known subdomain
        """
        query_url = self.get_query_url(
            endpoint=VirusTotal.SUBDOMAINS, params={"limit": limit}
        )

        try:
            response = self._query_service(url=query_url, headers=self.headers)
        except urllib.error.HTTPError:
            raise APIKeyError("Unauthorized. Check the API key settings and try again.")

        self.results[self.target].update(json.loads(response))
        self.subdomains[self.target] = {
            host["id"] for host in self.results[self.target]["data"]
        }

        return self.subdomains[self.target]