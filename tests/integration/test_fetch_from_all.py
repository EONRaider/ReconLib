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

import pytest

from reconlib import CRTShAPI, HackerTargetAPI, VirusTotalAPI


@pytest.mark.external_fetch
class TestFetchFromAll:
    def test_fetch_all(self, root_dir):
        """
        GIVEN the execution of this test takes place with the
            "--external-fetch" flag enabled
        WHEN connectivity to external hosts is guaranteed
        THEN the results of all available APIs on ReconLib must be
            retrieved without errors
        """
        """
        Execute a live fetch from all available APIs on ReconLib. This
        test is single-threaded, possibly consumes API usage quotas,
        will perform external HTTP requests and takes several seconds
        to complete.
        """
        # A file named .env located at the project root and defining
        # an API key for VirusTotal is required for this test
        virus_total_api_key = root_dir.joinpath(".env")

        all_apis = (
            CRTShAPI(),
            HackerTargetAPI(),
            VirusTotalAPI(api_key=virus_total_api_key),
        )

        subdomains = set().union(
            *(api.fetch_subdomains(target="nmap.com") for api in all_apis)
        )

        assert subdomains  # <-- Add breakpoint here to inspect results
