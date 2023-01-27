from ipaddress import IPv4Address, IPv4Network

import pytest

from reconlib.core.exceptions import InvalidTargetError
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
            "github.com": {
                IPv4Address("140.82.114.27"): "lb-140-82-114-27-iad.github.com",
                IPv4Address("140.82.121.9"): "lb-140-82-121-9-fra.github.com",
                IPv4Address("192.30.252.206"): "out-23.smtp.github.com",
                IPv4Address("192.30.255.117"): "lb-192-30-255-117-sea.github.com",
                IPv4Address("192.254.114.176"): "o1.sgmail.github.com",
            }
        }
        assert domain_info.subdomains == {
            "github.com": {
                "lb-140-82-121-9-fra.github.com",
                "lb-192-30-255-117-sea.github.com",
                "lb-140-82-114-27-iad.github.com",
                "out-23.smtp.github.com",
                "o1.sgmail.github.com",
            }
        }
        assert domain_info.ip_addresses == {
            "github.com": {
                IPv4Address("140.82.121.9"),
                IPv4Address("192.30.255.117"),
                IPv4Address("140.82.114.27"),
                IPv4Address("192.30.252.206"),
                IPv4Address("192.254.114.176"),
            }
        }

    def test_dns_lookup(self, mocker, hackertarget_dnslookup_github_response):
        # Mock API._query_service to prevent an HTTP request from being
        # made to api.hackertarget.com
        mocker.patch(
            "reconlib.hackertarget.api.API._query_service",
            return_value=hackertarget_dnslookup_github_response,
        )
        domain_info = API(target="github.com")
        assert domain_info.dnslookup() == {
            "github.com": {
                "A": ["140.82.113.4"],
                "MX": [
                    "1 aspmx.l.google.com.",
                    "10 alt3.aspmx.l.google.com.",
                    "10 alt4.aspmx.l.google.com.",
                ],
                "NS": ["dns1.p08.nsone.net.", "dns2.p08.nsone.net."],
                "TXT": [
                    '"MS=6BF03E6AF5CB689E315FB6199603BABF2C88D805"',
                    '"MS=ms44452932"',
                ],
                "SOA": [
                    "dns1.p08.nsone.net. hostmaster.nsone.net. 1656468023 43200 7200 "
                    "1209600 3600"
                ],
            }
        }

    def test_reverse_dns(self, mocker, hackertarget_reversedns_github_response):
        # Mock API._query_service to prevent an HTTP request from being
        # made to api.hackertarget.com
        mocker.patch(
            "reconlib.hackertarget.api.API._query_service",
            return_value=hackertarget_reversedns_github_response,
        )
        domain_info = API(target="140.82.121.9")
        assert domain_info.reverse_dns() == {
            IPv4Address("140.82.121.9"): "lb-140-82-121-9-fra.github.com"
        }

    def test_invalid_reverse_dns(self):
        invalid_target = "github.com"
        with pytest.raises(InvalidTargetError) as e:
            API(target=invalid_target).reverse_dns()
        assert (
            str(e.value.message) == f"InvalidTargetError: '{invalid_target}' does not "
            f"appear to be an IPv4 or IPv6 address"
        )
        assert e.value.code == 1

    def test_aslookup(self, mocker, hackertarget_aslookup_github_response):
        # Mock API._query_service to prevent an HTTP request from being
        # made to api.hackertarget.com
        mocker.patch(
            "reconlib.hackertarget.api.API._query_service",
            return_value=hackertarget_aslookup_github_response,
        )
        domain_info = API(target="140.82.121.9")
        assert domain_info.aslookup() == {
            "ASN": 36459,
            "IP_ADDRESS": IPv4Address("140.82.114.27"),
            "NETWORK": IPv4Network("140.82.114.0/24"),
            "OWNER": "GITHUB, US",
        }
        assert domain_info.asn == {
            36459: {
                "NETWORK": IPv4Network("140.82.114.0/24"),
                "OWNER": "GITHUB, US",
            }
        }

    def test_invalid_aslookup(self):
        invalid_target = "github.com"
        with pytest.raises(InvalidTargetError) as e:
            API(target=invalid_target).aslookup()
        assert (
            str(e.value.message) == f"InvalidTargetError: '{invalid_target}' does not "
            f"appear to be an IPv4 or IPv6 address"
        )
        assert e.value.code == 1
