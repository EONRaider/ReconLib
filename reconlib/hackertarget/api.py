import urllib.parse
from enum import Enum
from ipaddress import ip_address, IPv4Address, IPv6Address
from urllib.request import Request, urlopen

from reconlib.core.base import ExternalService
from reconlib.utils.user_agents import random_user_agent


class HackerTarget(Enum):
    """Enumeration of API endpoints made available by HackerTarget"""

    HOSTSEARCH = "hostsearch"


class API(ExternalService):
    def __init__(
        self,
        target: str,
        *,
        user_agent: str = None,
        hackertarget_url: str = "https://api.hackertarget.com",
        encoding: str = "utf_8",
    ):
        super().__init__(target)
        self.user_agent = user_agent
        self.hackertarget_url = urllib.parse.urlparse(hackertarget_url)
        self.encoding = encoding
        self.found_domains: dict[str, list[str]] = dict()
        self.found_ip_addrs: dict[str:[IPv4Address, IPv6Address]] = dict()
        self.hostsearch_results: dict[[IPv4Address, IPv6Address]:str] = dict()

    def hostsearch(self) -> dict[[IPv4Address, IPv6Address], str]:
        """
        Send an HTTP request to HackerTarget's "hostsearch" API endpoint
        and fetch the results

        :return: A dictionary mapping each known IP address from the
            target to a given subdomain
        """
        query_url = self.get_query_url(
            endpoint=HackerTarget.HOSTSEARCH, params={"q": self.target}
        )
        response = self._query_service(url=query_url)
        for result in response.rstrip().split("\n"):
            domain, ip_addr = result.split(",")
            self.hostsearch_results.update({ip_address(ip_addr): domain})
        self.found_domains.update({self.target: [*self.hostsearch_results.values()]})
        self.found_ip_addrs.update({self.target: [*self.hostsearch_results.keys()]})
        return self.hostsearch_results

    def get_query_url(self, endpoint: HackerTarget, params: dict = None) -> str:
        return urllib.parse.urlunparse(
            (
                self.hackertarget_url.scheme,
                self.hackertarget_url.netloc,
                f"{endpoint.value}/",
                "",
                urllib.parse.urlencode(params) if params else "",
                "",
            )
        )

    def _query_service(self, url: str) -> str:
        """
        Send an HTTP GET request to HackerTarget endpoint

        :return A decoded string containing the response from HackerTarget
        """
        request = Request(
            url=url,
            data=None,
            headers={
                "User-Agent": self.user_agent
                if self.user_agent
                else random_user_agent()
            },
        )
        with urlopen(request) as response:
            return response.read().decode(self.encoding)
