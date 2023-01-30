from reconlib import CRTShAPI


class TestCRTShAPI:
    def test_init_crtsh_api(self):
        crtsh = CRTShAPI()
        assert crtsh.wildcard is True
        assert crtsh.include_expired is True
        assert crtsh.encoding == "utf_8"

    def test_get_query_url(self):
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
        # Mock API._query_service to prevent an HTTP request from being
        # made to crt.sh when calling API.fetch
        mocker.patch(
            "reconlib.crtsh.api.CRTShAPI._query_service",
            return_value=crtsh_github_response,
        )

        target = "github.com"
        (domain_info := CRTShAPI()).fetch_certificates(target=target)

        assert domain_info.results == parsed_crtsh_github_response
        assert domain_info.subdomains[target] == crtsh_github_domains
