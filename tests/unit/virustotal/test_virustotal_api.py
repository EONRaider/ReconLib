from reconlib.virustotal import API
from reconlib.virustotal.api import VirusTotal


class TestVirusTotalAPI:
    def test_headers(self, api_key):
        domain_info = API(target="nmap.org", api_key=api_key)
        assert domain_info.headers == {
            "accept": "application/json",
            "x-apikey": api_key,
        }

    def test_get_query_url(self, api_key):
        domain_info = API(target="nmap.org", api_key=api_key)
        assert (
            domain_info.get_query_url(
                endpoint=VirusTotal.SUBDOMAINS, params={"limit": 1000}
            )
            == "https://www.virustotal.com/api/v3/domains/nmap.org/subdomains?"
            "limit=1000"
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
            "reconlib.virustotal.api.API._query_service",
            return_value=virustotal_subdomains_nmap_response,
        )
        domain_info = API(target="nmap.org", api_key=api_key)
        assert domain_info.get_subdomains() == virustotal_nmap_subdomains
        assert domain_info.subdomains == {
            domain_info.target: virustotal_nmap_subdomains
        }
