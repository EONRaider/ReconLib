import json
from urllib.request import Request, urlopen

from reconlib.utils.user_agents import random_user_agent


class API:
    def __init__(
        self,
        domain: str,
        *,
        user_agent: str = None,
        wildcard: bool = True,
        include_expired: bool = True,
        crtsh_url: str = "https://crt.sh",
        encoding: str = "utf_8",
    ):
        """
        Wrapper for HTTP requests for domain information to the crt.sh
        service

        :param domain: A domain name to search for in crt.sh
        :param user_agent: User-agent string to use when querying the
            crt.sh service (defaults to None for a random user-agent
            string to be used at each new request)
        :param wildcard: Prepend a wildcard to the domain when querying
            the crt.sh service (defaults to True)
        :param include_expired: Include expired certificates in search
            results (defaults to True)
        :param crtsh_url: URL assigned to the crt.sh service
        :param encoding: Encoding used on responses provided by crt.sh
        """
        self.domain = domain
        self.user_agent = user_agent
        self.wildcard = wildcard
        self.include_expired = include_expired
        self.crtsh_url = crtsh_url
        self.encoding = encoding
        self.results: list[dict] = []

    @property
    def search_url(self) -> str:
        """
        A string defining the URL to be fetched based on user-supplied
        parameters

        :return A string containing the URL formatted with the required
        path and query parameters
        """
        if "%" not in (domain := self.domain) and self.wildcard is True:
            domain = f"%.{self.domain}"

        url = f"{self.crtsh_url}/?q={domain}&output=json"

        if self.include_expired is False:
            url = f"{url}&exclude=expired"

        return url

    @property
    def num_results(self) -> int:
        """
        Number of results returned successfully from a query to crt.sh
        """
        return len(self.results)

    @property
    def found_domains(self) -> set[str]:
        """
        Set containing strings defining each domain returned by a
        query to crt.sh
        """
        return {result["common_name"] for result in self.results}

    def _query_service(self) -> str:
        """
        Send an HTTP GET request to crt.sh in a fetch operation

        :return A decoded string containing the response from crt.sh
        """
        request = Request(
            url=self.search_url,
            data=None,
            headers={
                "User-Agent": self.user_agent
                if self.user_agent is not None
                else random_user_agent()
            },
        )
        with urlopen(request) as response:
            return response.read().decode(self.encoding)

    def fetch(self) -> list[dict]:
        """
        Fetch certificate information for a given domain from crt.sh

        :return A list of dictionaries, each containing certificate
        information of a subdomain known by crt.sh to belong to the
        target domain
        """
        self.results = json.loads(self._query_service())
        return self.results
