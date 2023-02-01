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

import re
from collections import defaultdict
from enum import Enum
from ipaddress import ip_address, IPv6Address, IPv4Address, IPv4Network
from typing import Any
from urllib.parse import urlencode, urlparse, urlunparse

from reconlib.core.base import ExternalService
from reconlib.core.utils.validation import validate_ip_address


class HackerTarget(Enum):
    """
    Enumeration of API endpoints made available by HackerTarget
    """

    URL = urlparse("https://api.hackertarget.com")
    HOSTSEARCH = "hostsearch"
    DNSLOOKUP = "dnslookup"
    REVERSEDNS = "reversedns"
    ASLOOKUP = "aslookup"


class HackerTargetAPI(ExternalService):
    def __init__(self, *, user_agent: str = None, encoding: str = "utf_8"):
        """
        Wrapper for HTTP requests to the API of HackerTarget

        :param user_agent: User-agent string to use when querying the
            HackerTarget API (defaults to None for a random user-agent
            string to be used at each new request)
        :param encoding: Encoding used on responses provided by the
            HackerTarget API
        """
        super().__init__(user_agent, encoding)
        self.ip_addresses = defaultdict(set)
        self.subdomains = defaultdict(set)
        self.results = defaultdict(dict)
        self.dns_records = defaultdict(dict)
        self.asn = defaultdict(dict)

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
                HackerTarget.URL.value[0],
                HackerTarget.URL.value[1],
                f"{endpoint.value}/",
                "",
                urlencode(params) if params else "",
                "",
            )
        )

    def hostsearch(self, target: str) -> defaultdict[str, dict]:
        """
        Send an HTTP request to HackerTarget's "hostsearch" API endpoint
        and fetch the results

        :param target: A domain name to search for in api.hackertarget.com

        :return: A dictionary mapping each known IP address from the
            target to a given subdomain
        """
        query_url = self.get_query_url(
            endpoint=HackerTarget.HOSTSEARCH, params={"q": target}
        )
        for result in self._query_service(url=query_url).rstrip().split("\n"):
            domain, ip_addr = result.split(",")
            ip_addr = ip_address(ip_addr)
            self.results[target].update({ip_addr: domain})
            self.subdomains[target].add(domain)
            self.ip_addresses[target].add(ip_addr)
        return self.results

    def fetch_subdomains(self, target: str) -> set[str]:
        """
        Utility method that executes a request to HackerTarget,
        processes the response and returns a set of known subdomains for
        a given target

        :param target: A domain name to search for in HackerTarget
        """
        self.hostsearch(target)
        return self.subdomains[target]

    def dnslookup(self, target: str) -> dict[str, dict]:
        """
        Send an HTTP request to HackerTarget's "dnslookup" API endpoint
        and fetch the results

        :param target: A domain name to search for in api.hackertarget.com

        :return: A dictionary mapping each known DNS registry entry to
            a list of known values.
        """
        query_url = self.get_query_url(
            endpoint=HackerTarget.DNSLOOKUP, params={"q": target}
        )
        self.dns_records.update({target: defaultdict(list)})
        for entry in self._query_service(url=query_url).rstrip().split("\n"):
            record, value = entry.split(" : ")
            self.dns_records[target][record].append(value)
        return self.dns_records

    def reverse_dns(self, target: str) -> dict[[IPv4Address, IPv6Address], str]:
        """
        Send an HTTP request to HackerTarget's "reverse_dns" API endpoint
        and fetch the results

        :param target: A domain name to search for in api.hackertarget.com

        :return: A dictionary mapping the supplied IP address to a
            resolved hostname
        :raise: InvalidTargetError if set to a target that cannot be
            cast into an IPv4/IPv6 address
        """
        query_url = self.get_query_url(
            endpoint=HackerTarget.REVERSEDNS,
            params={"q": validate_ip_address(target)},
        )
        ip_addr, domain = self._query_service(url=query_url).rstrip().split(" ")
        ip_addr = ip_address(ip_addr)
        self.subdomains[target].add(domain)
        self.ip_addresses[target].add(ip_addr)
        return {ip_addr: domain}

    def aslookup(self, target: str) -> dict[str, Any]:
        """
        Send an HTTP request to HackerTarget's "aslookup" API endpoint
        and fetch the results

        :param target: A domain name to search for in api.hackertarget.com

        :return: A dictionary mapping the lookup results (IP address,
            ASN, network address space and owner) to their respective
            values
        :raise: InvalidTargetError if set to a target that cannot be
            cast into an IPv4/IPv6 address
        """
        query_url = self.get_query_url(
            endpoint=HackerTarget.ASLOOKUP,
            params={"q": validate_ip_address(target)},
        )

        # Query the API and split the response into four pre-defined
        # groups: IP Address, ASN, IP Address Space (Network) and Owner
        # name
        response = re.match(
            r"^\"(?P<ip_addr>.+)\",\"(?P<asn>.+)\",\"(?P<network>.+)\","
            r"\"(?P<owner>.+)\"$",
            self._query_service(url=query_url).rstrip(),
        )

        self.asn[(asn := int(response.group("asn")))].update(
            {
                "NETWORK": IPv4Network(response.group("network")),
                "OWNER": response.group("owner"),
            }
        )

        return {
            "IP_ADDRESS": ip_address(response.group("ip_addr")),
            "ASN": asn,
            **self.asn[asn],
        }
