from reconlib.crtsh import API


class TestCrtShAPI:
    def test_init_crtsh_api(self):
        crtsh = API(target="test.domain.abc")
        assert crtsh.wildcard is True
        assert crtsh.include_expired is True
        assert crtsh.encoding == "utf_8"

        assert crtsh.search_url == "https://crt.sh/?q=%.test.domain.abc&output=json"

        crtsh.wildcard = False
        assert crtsh.search_url == "https://crt.sh/?q=test.domain.abc&output=json"

        crtsh.include_expired = False
        assert (
            crtsh.search_url
            == "https://crt.sh/?q=test.domain.abc&output=json&exclude=expired"
        )

    def test_fetch_from_crtsh(
        self,
        mocker,
        mock_github_response,
        parsed_mock_github_response,
        mock_github_domains,
    ):
        # Mock API._query_service to prevent an HTTP request from being
        # made to crt.sh when calling API.fetch
        mocker.patch(
            "reconlib.crtsh.api.API._query_service", return_value=mock_github_response
        )

        domain_info = API(target="github.com")
        domain_info.fetch()

        assert domain_info.results == parsed_mock_github_response
        assert domain_info.num_results == len(mock_github_domains)
        assert domain_info.found_domains == mock_github_domains
