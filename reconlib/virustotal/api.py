import json
import urllib.error
from collections import defaultdict
from enum import Enum
from pathlib import Path
from urllib.parse import urlunparse, urlencode, urlparse

from reconlib.core.base import AuthenticatedExternalService
from reconlib.core.exceptions import APIKeyError


class VirusTotal(Enum):
    """
    Enumeration of API endpoints made available by VirusTotal
    """

    URL = urlparse("https://www.virustotal.com/api/v3")
    SUBDOMAINS = "domains/{}/subdomains"


class VirusTotalAPI(AuthenticatedExternalService):
    def __init__(
        self,
        *,
        user_agent: str = None,
        encoding: str = "utf_8",
        api_key: [str, Path] = None,
        api_key_env_name: str = "VIRUSTOTAL_API_KEY",
    ):
        """
        Wrapper for HTTP requests to the API of VirusTotal

        :param user_agent: User-agent string to use when querying the
            VirusTotal API (defaults to None for a random user-agent
            string to be used at each new request)
        :param encoding: Encoding used on responses provided by the
            VirusTotal API
        :param api_key: A string containing an API key for use in
            requests to VirusTotal API or the absolute path to a file
            in which the value can be found
        :param api_key_env_name: String representing the expected name
            of the environment variable from which the API key value
            will be read. Defaults to VIRUSTOTAL_API_KEY.
        """
        super().__init__(user_agent, encoding, api_key, api_key_env_name)
        self.results = defaultdict(dict)
        self.subdomains = defaultdict(set)

    @property
    def headers(self) -> dict:
        """
        A dictionary containing the headers required by VirusTotal API
        """
        return {"accept": "application/json", "x-apikey": self.api_key}

    def get_query_url(
        self, target: str, endpoint: VirusTotal, params: dict = None
    ) -> str:
        """
        Build an RFC 1808 compliant string defining the URL to be
        fetched based on user-supplied parameters

        :param target: A domain name to search for in VirusTotal API
        :param endpoint: An enumerated endpoint value of type VirusTotal
        :param params: A dictionary mapping query string parameters to
            their respective values
        :return: The URL formatted as a string
        """
        return urlunparse(
            (
                (url := VirusTotal.URL.value).scheme,
                url.netloc,
                f"{url.path}/{endpoint.value.format(target)}",
                "",
                urlencode(params) if params else "",
                "",
            )
        )

    def get_subdomains(self, target: str, limit: int = 1000) -> set[str]:
        """
        Send an HTTP request to VirusTotal's "domains" API endpoint
        and fetch the results from is "subdomains" relationship

        :param target: A domain name to search for in VirusTotal API
        :param limit: Maximum number of subdomains to retrieve per
            request

        :return: A set of strings containing each known subdomain
        """
        query_url = self.get_query_url(
            target=target, endpoint=VirusTotal.SUBDOMAINS, params={"limit": limit}
        )

        try:
            response = self._query_service(url=query_url, headers=self.headers)
            parsed_response = json.loads(response)
        except urllib.error.HTTPError:
            raise APIKeyError("Unauthorized. Check the API key settings and try again.")

        self.results[target].update(parsed_response)
        subdomains = {host["id"] for host in parsed_response["data"]}
        self.subdomains[target] = subdomains

        return subdomains
