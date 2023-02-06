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
                (url := VirusTotal.URL.value)[0],
                url[1],
                f"{url[2]}/{endpoint.value.format(target)}",
                "",
                urlencode(params) if params else "",
                "",
            )
        )

    def fetch_subdomains(self, target: str, limit: int = 1000) -> set[str]:
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
