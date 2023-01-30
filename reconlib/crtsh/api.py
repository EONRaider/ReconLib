import json
from collections import defaultdict

from reconlib.core.base import ExternalService


class CRTShAPI(ExternalService):
    def __init__(
        self,
        target: str,
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

        :param target: A domain name to search for in crt.sh
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
        super().__init__(target, user_agent, encoding)
        self.wildcard = wildcard
        self.include_expired = include_expired
        self.crtsh_url = crtsh_url
        self.subdomains = defaultdict(set)
        self.results = defaultdict(dict)

    def get_query_url(self) -> str:
        """
        A string defining the URL to be fetched based on user-supplied
        parameters

        :return: A string containing the URL formatted with the required
        path and query parameters
        """

        if "%" not in (domain := self.target) and self.wildcard is True:
            domain = f"%.{self.target}"

        url = f"{self.crtsh_url}/?q={domain}&output=json"

        if self.include_expired is False:
            url = f"{url}&exclude=expired"

        return url

    def fetch(self) -> list[dict]:
        """
        Fetch certificate information for a given domain from crt.sh

        :return A list of dictionaries in JSON format, each containing
        certificate information of a subdomain known by crt.sh to
        belong to the target domain
        """
        response = json.loads(self._query_service(url=self.get_query_url()))
        self.results[self.target] = response
        self.subdomains[self.target].update(host["common_name"] for host in response)
        return response
