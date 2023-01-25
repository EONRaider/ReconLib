from collections import defaultdict
from enum import Enum
from ipaddress import ip_address, IPv6Address, IPv4Address
from urllib.parse import urlencode, urlparse, urlunparse
from urllib.request import Request, urlopen

from reconlib.core.base import ExternalService
from reconlib.core.exceptions import InvalidTargetError
from reconlib.utils.user_agents import random_user_agent


class HackerTarget(Enum):
    """Enumeration of API endpoints made available by HackerTarget"""

    URL = urlparse("https://api.hackertarget.com")
    HOSTSEARCH = "hostsearch"
    DNSLOOKUP = "dnslookup"
    REVERSEDNS = "reversedns"


class API(ExternalService):
    def __init__(
        self,
        target: str,
        *,
        user_agent: str = None,
        encoding: str = "utf_8",
    ):
        """
        Wrapper for HTTP requests to the API of HackerTarget

        :param target: A domain name to search for in api.hackertarget.com
        :param user_agent: User-agent string to use when querying the
            HackerTarget API (defaults to None for a random user-agent
            string to be used at each new request)
        :param encoding: Encoding used on responses provided by the
            HackerTarget API
        """
        super().__init__(target)
        self.user_agent = user_agent
        self.encoding = encoding
        self.found_ip_addrs = defaultdict(set)
        self.found_domains = defaultdict(set)
        self.hosts = defaultdict(dict)
        self.dns_records = defaultdict(dict)

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
                HackerTarget.URL.value.scheme,
                HackerTarget.URL.value.netloc,
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
            self.hosts[self.target].update({ip_addr: domain})
            self.found_domains[self.target].add(domain)
            self.found_ip_addrs[self.target].add(ip_addr)
        return self.hosts

    def dnslookup(self) -> dict[str, dict]:
        """
        Send an HTTP request to HackerTarget's "dnslookup" API endpoint
        and fetch the results

        :return: A dictionary mapping each known DNS registry entry to
            a list of known values.
        """
        query_url = self.get_query_url(
            endpoint=HackerTarget.DNSLOOKUP, params={"q": self.target}
        )
        self.dns_records.update({self.target: defaultdict(list)})
        for entry in self._query_service(url=query_url).rstrip().split("\n"):
            record, value = entry.split(" : ")
            self.dns_records[self.target][record].append(value)
        return self.dns_records

    def reverse_dns(self) -> dict[[IPv4Address, IPv6Address], str]:
        """
        Send an HTTP request to HackerTarget's "reverse_dns" API endpoint
        and fetch the results

        :return: A dictionary mapping the supplied IP address to a
            resolved hostname
        """
        try:
            target_addr = ip_address(self.target)
        except ValueError as e:
            raise InvalidTargetError(str(e))

        query_url = self.get_query_url(
            endpoint=HackerTarget.REVERSEDNS, params={"q": target_addr}
        )
        ip_addr, domain = self._query_service(url=query_url).rstrip().split(" ")
        ip_addr = ip_address(ip_addr)
        self.found_domains[self.target].add(domain)
        self.found_ip_addrs[self.target].add(ip_addr)
        return {ip_addr: domain}
