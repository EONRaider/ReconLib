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

from reconlib import CRTShAPI


class TestCRTShAPI:
    def test_init_crtsh_api(self):
        """
        GIVEN an instance of type CRTShAPI
        WHEN no arguments are supplied to its initializer
        THEN this instance must return all default attributes without
            exceptions
        """
        crtsh = CRTShAPI()
        assert crtsh.wildcard is True
        assert crtsh.include_expired is True
        assert crtsh.encoding == "utf_8"

    def test_get_query_url(self):
        """
        GIVEN a correctly instantiated object of type CRTShAPI
        WHEN a string containing a correctly formatted domain is passed
            as an argument to its get_query_url method
        THEN a URL for the retrieval of results on crt.sh must be
            returned without exceptions
        """
        crtsh = CRTShAPI()
        assert (
            crtsh.get_query_url(target="test.domain.abc")
            == "https://crt.sh/?q=%.test.domain.abc&output=json"
        )

        crtsh.wildcard = False
        assert (
            crtsh.get_query_url(target="test.domain.abc")
            == "https://crt.sh/?q=test.domain.abc&output=json"
        )

        crtsh.include_expired = False
        assert (
            crtsh.get_query_url(target="test.domain.abc")
            == "https://crt.sh/?q=test.domain.abc&output=json&exclude=expired"
        )

    def test_fetch_certificates(
        self,
        mocker,
        crtsh_github_response,
        parsed_crtsh_github_response,
        crtsh_github_domains,
    ):
        """
        GIVEN a correctly instantiated object of type CRTShAPI
        WHEN a string containing a correctly formatted domain is passed
            as an argument to its fetch_certificates method
        THEN a string representing the service's response must be
            returned, parsed and processed into results
        """
        # Prevent execution of HTTP requests to external hosts. Present
        # a response equal to the one returned by the server.
        mocker.patch(
            "reconlib.crtsh.api.CRTShAPI._query_service",
            return_value=crtsh_github_response,
        )

        target = "github.com"
        (domain_info := CRTShAPI()).fetch_certificates(target=target)

        assert domain_info.results == parsed_crtsh_github_response
        assert domain_info.subdomains[target] == crtsh_github_domains

    def test_fetch_subdomains(
        self, mocker, crtsh_github_response, crtsh_github_domains
    ):
        """
        GIVEN a correctly instantiated object of type CRTShAPI
        WHEN a string containing a correctly formatted domain is passed
            as an argument to its fetch_subdomains method
        THEN a set of subdomains must be returned by the service without
            exceptions
        """
        # Prevent execution of HTTP requests to external hosts. Present
        # a response equal to the one returned by the server.
        mocker.patch(
            "reconlib.crtsh.api.CRTShAPI._query_service",
            return_value=crtsh_github_response,
        )

        assert CRTShAPI().fetch_subdomains(target="github.com") == crtsh_github_domains
