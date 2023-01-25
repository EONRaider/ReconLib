from ipaddress import IPv4Address

from reconlib.hackertarget import API
from reconlib.hackertarget.api import HackerTarget


class TestHackerTargetAPI:
    def test_get_query_url(self):
        domain_info = API(target="github.com")
        assert (
            domain_info.get_query_url(endpoint=HackerTarget.HOSTSEARCH)
            == "https://api.hackertarget.com/hostsearch/"
        )
        assert (
            domain_info.get_query_url(
                endpoint=HackerTarget.HOSTSEARCH,
                params={"q": domain_info.target, "apikey": "SOMEAPIKEY"},
            )
            == "https://api.hackertarget.com/hostsearch/?q=github.com&apikey=SOMEAPIKEY"
        )

    def test_hostsearch(self, mocker, hackertarget_hostsearch_github_response):
        # Mock API._query_service to prevent an HTTP request from being
        # made to api.hackertarget.com
        mocker.patch(
            "reconlib.hackertarget.api.API._query_service",
            return_value=hackertarget_hostsearch_github_response,
        )

        domain_info = API(target="github.com")
        assert domain_info.hostsearch() == {
            IPv4Address("140.82.121.9"): "lb-140-82-121-9-fra.github.com",
            IPv4Address("192.30.255.117"): "lb-192-30-255-117-sea.github.com",
            IPv4Address("140.82.114.27"): "lb-140-82-114-27-iad.github.com",
            IPv4Address("192.30.252.206"): "out-23.smtp.github.com",
            IPv4Address("192.254.114.176"): "o1.sgmail.github.com",
        }
        assert domain_info.found_domains == {
            "github.com": [
                "lb-140-82-121-9-fra.github.com",
                "lb-192-30-255-117-sea.github.com",
                "lb-140-82-114-27-iad.github.com",
                "out-23.smtp.github.com",
                "o1.sgmail.github.com",
            ]
        }
        assert domain_info.found_ip_addrs == {
            "github.com": [
                IPv4Address("140.82.121.9"),
                IPv4Address("192.30.255.117"),
                IPv4Address("140.82.114.27"),
                IPv4Address("192.30.252.206"),
                IPv4Address("192.254.114.176"),
            ]
        }
