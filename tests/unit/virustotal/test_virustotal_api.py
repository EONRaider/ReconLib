import os
import re

import pytest

from reconlib.core.exceptions import APIKeyError
from reconlib import VirusTotalAPI
from reconlib.virustotal.api import VirusTotal


class TestVirusTotalAPI:
    def test_set_api_key_from_env(self, api_key, root_dir):
        # Set API key value directly from environment variable
        env_api_key = f"{api_key}_from_env"
        os.environ["VIRUSTOTAL_API_KEY"] = env_api_key
        domain_info = VirusTotalAPI(target="nmap.org")
        assert domain_info.api_key == env_api_key
        os.environ.pop("VIRUSTOTAL_API_KEY", None)  # Cleanup environment

    def test_set_api_key_from_init(self, api_key, root_dir):
        # Set API key at instantiation
        inst_api_key = f"{api_key}_from_instance"
        domain_info = VirusTotalAPI(target="nmap.org", api_key=inst_api_key)
        assert domain_info.api_key == inst_api_key
        os.environ.pop("VIRUSTOTAL_API_KEY", None)

    def test_set_api_key_from_file(self, api_key, root_dir):
        # Set API key from a file
        api_key_file_path = root_dir.joinpath("tests/unit/virustotal/.test_env")
        with open(api_key_file_path) as file:
            file_api_key = re.search(r"\"(.*)\"", file.read()).group(1)
        domain_info = VirusTotalAPI(target="nmap.org", api_key=api_key_file_path)
        assert domain_info.api_key == file_api_key
        os.environ.pop("VIRUSTOTAL_API_KEY", None)

    def test_undefined_api_key(self):
        with pytest.raises(APIKeyError):
            # API key not defined neither as an environment variable nor
            # an instance attribute
            VirusTotalAPI(target="nmap.org")

    def test_headers(self, api_key):
        domain_info = VirusTotalAPI(target="nmap.org", api_key=api_key)
        assert domain_info.headers == {
            "accept": "application/json",
            "x-apikey": api_key,
        }

    def test_get_query_url(self, api_key):
        target = "nmap.org"
        limit = 1000
        domain_info = VirusTotalAPI(target, api_key=api_key)

        assert (
            domain_info.get_query_url(
                endpoint=VirusTotal.SUBDOMAINS, params={"limit": limit}
            )
            == f"https://www.virustotal.com/api/v3/domains/{target}/subdomains?"
            f"limit={limit}"
        )

    def test_subdomains(
        self,
        mocker,
        api_key,
        virustotal_subdomains_nmap_response,
        virustotal_nmap_subdomains,
    ):
        # Mock API._query_service to prevent an HTTP request from being
        # made to VirusTotal API
        mocker.patch(
            "reconlib.virustotal.api.VirusTotalAPI._query_service",
            return_value=virustotal_subdomains_nmap_response,
        )
        domain_info = VirusTotalAPI(target="nmap.org", api_key=api_key)
        assert domain_info.get_subdomains() == virustotal_nmap_subdomains
        assert domain_info.subdomains == {
            domain_info.target: virustotal_nmap_subdomains
        }
