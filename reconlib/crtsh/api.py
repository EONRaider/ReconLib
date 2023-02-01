"""
ReconLib: A collection of modules and helpers for active and passive
reconnaissance of remote hosts.

Author: EONRaider
GitHub: https://github.com/EONRaider
Contact: https://www.twitter.com/eon_raider

    Copyright (C) 2023 EONRaider @ keybase.io/eonraider

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see
    <https://github.com/EONRaider/ReconLib/blob/master/LICENSE>.
"""

import json
from collections import defaultdict
from enum import Enum

from reconlib.core.base import ExternalService


class CRTSh(Enum):
    """
    Enumeration of API endpoints made available by CRTSh
    """

    URL = "https://crt.sh"


class CRTShAPI(ExternalService):
    def __init__(
        self,
        *,
        user_agent: str = None,
        wildcard: bool = True,
        include_expired: bool = True,
        encoding: str = "utf_8",
    ):
        """
        Wrapper for HTTP requests for domain information to the crt.sh
        service

        :param user_agent: User-agent string to use when querying the
            crt.sh service (defaults to None for a random user-agent
            string to be used at each new request)
        :param wildcard: Prepend a wildcard to the domain when querying
            the crt.sh service (defaults to True)
        :param include_expired: Include expired certificates in search
            results (defaults to True)
        :param encoding: Encoding used on responses provided by crt.sh
        """
        super().__init__(user_agent, encoding)
        self.wildcard = wildcard
        self.include_expired = include_expired
        self.subdomains = defaultdict(set)
        self.results = defaultdict(dict)

    def get_query_url(self, target: str) -> str:
        """
        A string defining the URL to be fetched based on user-supplied
        parameters

        :param target: A domain name to search for in crt.sh

        :return: A string containing the URL formatted with the required
        path and query parameters
        """

        target = (
            f"%.{target}" if "%" not in target and self.wildcard is True else target
        )

        url = f"{CRTSh.URL.value}/?q={target}&output=json"

        if self.include_expired is False:
            url = f"{url}&exclude=expired"

        return url

    def fetch_certificates(self, target: str) -> list[dict]:
        """
        Fetch certificate information for a given domain from crt.sh

        :param target: A domain name to search for in crt.sh

        :return A list of dictionaries in JSON format, each containing
        certificate information of a subdomain known by crt.sh to
        belong to the target domain
        """
        response = json.loads(self._query_service(url=self.get_query_url(target)))
        self.results[target] = response
        self.subdomains[target].update(host["common_name"] for host in response)
        return response

    def fetch_subdomains(self, target: str) -> set[str]:
        """
        Utility method that executes a request to crt.sh, processes the
        response and returns a set of known subdomains for a given target

        :param target: A domain name to search for in crt.sh
        """
        self.fetch_certificates(target)
        return self.subdomains[target]
