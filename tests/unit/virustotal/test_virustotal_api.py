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

import os
import re

import pytest

from reconlib.core.exceptions import APIKeyError
from reconlib import VirusTotalAPI
from reconlib.virustotal.api import VirusTotal


class TestVirusTotalAPI:
    def test_set_api_key_from_env(self, api_key, root_dir, setup_virustotal_api_key):
        """
        GIVEN a correctly instantiated object of type VirusTotalAPI
        WHEN an API key is set as an environment variable with the name
            "VIRUSTOTAL_API_KEY"
        THEN this API key must be set as the "api_key" attribute of the
            VirusTotal instance without exceptions
        """
        assert VirusTotalAPI().api_key == api_key

    def test_set_api_key_from_init(self, api_key, root_dir):
        """
        GIVEN a correctly instantiated object of type VirusTotalAPI
        WHEN an API key is set as an argument to the object's constructor
        THEN this API key must be set as the "api_key" attribute of the
            VirusTotal instance without exceptions
        """
        inst_api_key = f"{api_key}_from_instance"
        assert VirusTotalAPI(api_key=inst_api_key).api_key == inst_api_key

    def test_set_api_key_from_file(self, api_key, root_dir):
        """
        GIVEN a correctly instantiated object of type VirusTotalAPI
        WHEN an API key is set as an environment variable with the name
            "VIRUSTOTAL_API_KEY" through a correctly formatted text file
        THEN this API key must be set as the "api_key" attribute of the
            VirusTotal instance without exceptions
        """
        api_key_file_path = root_dir.joinpath("tests/unit/virustotal/.test_env")
        with open(api_key_file_path) as file:
            file_api_key = re.search(r"\"(.*)\"", file.read()).group(1)
        assert VirusTotalAPI(api_key=api_key_file_path).api_key == file_api_key
        os.environ.pop("VIRUSTOTAL_API_KEY", None)  # Cleanup environment

    def test_undefined_api_key(self):
        """
        GIVEN a correctly instantiated object of type VirusTotalAPI
        WHEN no API key is set neither as an environment variable nor as
            an argument passed to the object's constructor
        THEN an exception of type APIKeyError must be raised
        """
        with pytest.raises(APIKeyError):
            VirusTotalAPI()

    def test_headers(self, api_key):
        """
        GIVEN a correctly instantiated object of type VirusTotalAPI
        WHEN an API key has been correctly set as an argument to the
            object's constructor
        THEN an "x-apikey" HTTP header containing the API key as a value
            must be made available for access through the "headers"
            attribute
        """
        domain_info = VirusTotalAPI(api_key=api_key)
        assert domain_info.headers == {
            "accept": "application/json",
            "x-apikey": api_key,
        }

    def test_get_query_url(self, api_key):
        """
        GIVEN a correctly instantiated object of type VirusTotalAPI
        WHEN a string containing a correctly formatted domain is passed
            as an argument to its get_query_url method
        THEN a URL for the retrieval of results on VirusTotal must be
            returned without exceptions
        """
        target = "nmap.org"
        limit = 1000
        domain_info = VirusTotalAPI(api_key=api_key)

        assert (
            domain_info.get_query_url(
                target=target, endpoint=VirusTotal.SUBDOMAINS, params={"limit": limit}
            )
            == f"https://www.virustotal.com/api/v3/domains/{target}/subdomains?"
            f"limit={limit}"
        )

    def test_fetch_subdomains(
        self,
        mocker,
        api_key,
        virustotal_subdomains_nmap_response,
        virustotal_nmap_subdomains,
    ):
        """
        GIVEN a correctly instantiated object of type VirusTotalAPI
        WHEN a string containing a correctly formatted domain is passed
            as an argument to its fetch_subdomains method
        THEN a set of subdomains must be returned by the service without
            exceptions
        """
        # Prevent execution of HTTP requests to external hosts. Present
        # a response equal to the one returned by the server.
        mocker.patch(
            "reconlib.virustotal.api.VirusTotalAPI._query_service",
            return_value=virustotal_subdomains_nmap_response,
        )
        assert (
            VirusTotalAPI(api_key=api_key).fetch_subdomains(target="nmap.org")
            == virustotal_nmap_subdomains
        )
