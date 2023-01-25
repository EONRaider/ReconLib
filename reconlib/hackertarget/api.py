from collections import defaultdict
from enum import Enum
from ipaddress import ip_address
from urllib.parse import urlencode, urlparse, urlunparse
from urllib.request import Request, urlopen

from reconlib.core.base import ExternalService
from reconlib.utils.user_agents import random_user_agent


class HackerTarget(Enum):
    """Enumeration of API endpoints made available by HackerTarget"""

    HOSTSEARCH = "hostsearch"
    DNSLOOKUP = "dnslookup"


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
        self.hackertarget_url = urlparse(hackertarget_url)
        self.encoding = encoding
        self.found_ip_addrs = defaultdict(list)
        self.found_domains = defaultdict(list)
        self.hostsearch_results = defaultdict(dict)
        self.dns_records: dict[str:defaultdict] = dict()

    def get_query_url(self, endpoint: HackerTarget, params: dict = None) -> str:
        """
        Build an RFC 1808 compliant string defining the URL to be
        fetched based on user-supplied parameters

        :param endpoint: An enumerated endpoint value of type HackerTarget
        :param params: A dictionary mapping query string parameters to
            their respective values
        :return: The URL formatted as a string
        """
        return urlunparse(
            (
                self.hackertarget_url.scheme,
                self.hackertarget_url.netloc,
                f"{endpoint.value}/",
                "",
                urlencode(params) if params else "",
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

    def hostsearch(self) -> defaultdict[str, dict]:
        """
        Send an HTTP request to HackerTarget's "hostsearch" API endpoint
        and fetch the results

        :return: A dictionary mapping each known IP address from the
            target to a given subdomain
        """
        query_url = self.get_query_url(
            endpoint=HackerTarget.HOSTSEARCH, params={"q": self.target}
        )
        for result in self._query_service(url=query_url).rstrip().split("\n"):
            domain, ip_addr = result.split(",")
            ip_addr = ip_address(ip_addr)
            self.hostsearch_results[self.target].update({ip_addr: domain})
            self.found_domains[self.target].append(domain)
            self.found_ip_addrs[self.target].append(ip_addr)
        return self.hostsearch_results

    def dnslookup(self) -> dict[str, list[str]]:
        """
        Send an HTTP request to HackerTarget's "dnslookup" API endpoint
        and fetch the results

        :return: A dictionary mapping each known DNS registry entry to
            a list of known values.
        """
        query_url = self.get_query_url(
            endpoint=HackerTarget.DNSLOOKUP, params={"q": self.target}
        )
        response = self._query_service(url=query_url)
        self.dns_records.update({self.target: defaultdict(list)})
        for entry in response.rstrip().split("\n"):
            record, value = entry.split(" : ")
            self.dns_records[self.target][record].append(value)
        return self.dns_records
