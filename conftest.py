from pathlib import Path

import pytest


@pytest.fixture
def root_dir():
    return Path(__file__).parent.absolute()


@pytest.fixture
def crtsh_github_response():
    return '[{"issuer_ca_id":185756,"issuer_name":"C=US, O=DigiCert Inc, CN=DigiCert TLS RSA SHA256 2020 CA1","common_name":"skyline.github.com","name_value":"skyline.github.com\\nwww.skyline.github.com","id":8383197569,"entry_timestamp":"2023-01-10T23:48:41.932","not_before":"2023-01-10T00:00:00","not_after":"2024-01-24T23:59:59","serial_number":"071a522c3982234f64fdd14b8f4b9577"},{"issuer_ca_id":185756,"issuer_name":"C=US, O=DigiCert Inc, CN=DigiCert TLS RSA SHA256 2020 CA1","common_name":"*.proxima-review-lab.github.com","name_value":"*.proxima-review-lab.github.com\\nproxima-review-lab.github.com","id":8353864864,"entry_timestamp":"2023-01-05T17:04:06.714","not_before":"2023-01-05T00:00:00","not_after":"2024-01-04T23:59:59","serial_number":"04ddc3cb9e41c6f4d0f8331c59ef18a5"},{"issuer_ca_id":185756,"issuer_name":"C=US, O=DigiCert Inc, CN=DigiCert TLS RSA SHA256 2020 CA1","common_name":"*.registry.github.com","name_value":"*.registry.github.com\\nregistry.github.com","id":8299960444,"entry_timestamp":"2022-12-27T18:16:02.706","not_before":"2022-12-27T00:00:00","not_after":"2024-01-02T23:59:59","serial_number":"0e48119cceb96171a041a31752fc1adc"},{"issuer_ca_id":244621,"issuer_name":"C=BE, O=GlobalSign nv-sa, CN=GlobalSign Atlas R3 DV TLS CA 2022 Q4","common_name":"f.cloud.github.com","name_value":"f.cloud.github.com","id":7998084684,"entry_timestamp":"2022-11-17T19:45:02.684","not_before":"2022-11-17T19:45:02","not_after":"2023-12-19T19:45:01","serial_number":"01fdd231f5ad27a5acc8d6ffdcf8a4ab"},{"issuer_ca_id":185756,"issuer_name":"C=US, O=DigiCert Inc, CN=DigiCert TLS RSA SHA256 2020 CA1","common_name":"support.enterprise.github.com","name_value":"support.enterprise.github.com\\nwww.support.enterprise.github.com","id":7837200062,"entry_timestamp":"2022-10-26T08:58:44.768","not_before":"2022-10-26T00:00:00","not_after":"2023-10-26T23:59:59","serial_number":"0880a36e5ac215fe2720133414ebc005"},{"issuer_ca_id":185756,"issuer_name":"C=US, O=DigiCert Inc, CN=DigiCert TLS RSA SHA256 2020 CA1","common_name":"ws.support.github.com","name_value":"ws.support.github.com\\nwww.ws.support.github.com","id":7798962909,"entry_timestamp":"2022-10-21T07:39:27.613","not_before":"2022-10-21T00:00:00","not_after":"2023-10-21T23:59:59","serial_number":"01c4361712981217cb034f4eb66d2615"},{"issuer_ca_id":239799,"issuer_name":"C=US, O=\\"DigiCert, Inc.\\", CN=GeoTrust Global TLS RSA4096 SHA256 2022 CA1","common_name":"examregistration.github.com","name_value":"examregistration.github.com","id":7776339654,"entry_timestamp":"2022-10-17T17:06:07.728","not_before":"2022-10-17T00:00:00","not_after":"2023-04-17T23:59:59","serial_number":"092d02778b237968cd3f4a722c875884"},{"issuer_ca_id":185756,"issuer_name":"C=US, O=DigiCert Inc, CN=DigiCert TLS RSA SHA256 2020 CA1","common_name":"api.security.github.com","name_value":"api.security.github.com\\nwww.api.security.github.com","id":7687547527,"entry_timestamp":"2022-10-05T18:07:17.34","not_before":"2022-10-05T00:00:00","not_after":"2023-10-05T23:59:59","serial_number":"05ad0dd28e8ee76487f78dea11dc608d"},{"issuer_ca_id":185756,"issuer_name":"C=US, O=DigiCert Inc, CN=DigiCert TLS RSA SHA256 2020 CA1","common_name":"partnerportal.github.com","name_value":"partnerportal.github.com\\nwww.partnerportal.github.com","id":7681689500,"entry_timestamp":"2022-10-04T19:36:19.289","not_before":"2022-10-04T00:00:00","not_after":"2023-10-04T23:59:59","serial_number":"0bc3956f14f34e5a33dd8d98a4d759c8"},{"issuer_ca_id":185756,"issuer_name":"C=US, O=DigiCert Inc, CN=DigiCert TLS RSA SHA256 2020 CA1","common_name":"import2.github.com","name_value":"import2.github.com\\nimporter2.github.com\\nporter2.github.com","id":7486854481,"entry_timestamp":"2022-09-06T19:44:56.289","not_before":"2022-09-06T00:00:00","not_after":"2023-09-06T23:59:59","serial_number":"05eeef2f36260c7237439ebbd2af3e6a"},{"issuer_ca_id":185756,"issuer_name":"C=US, O=DigiCert Inc, CN=DigiCert TLS RSA SHA256 2020 CA1","common_name":"api.stars.github.com","name_value":"api.stars.github.com\\nwww.api.stars.github.com","id":7216594685,"entry_timestamp":"2022-07-28T10:11:51.965","not_before":"2022-07-28T00:00:00","not_after":"2023-07-28T23:59:59","serial_number":"039ce61a571eb9386009286a813e93f6"}]'


@pytest.fixture
def crtsh_github_domains():
    return {
        "skyline.github.com",
        "*.proxima-review-lab.github.com",
        "*.registry.github.com",
        "f.cloud.github.com",
        "support.enterprise.github.com",
        "ws.support.github.com",
        "examregistration.github.com",
        "api.security.github.com",
        "partnerportal.github.com",
        "import2.github.com",
        "api.stars.github.com",
    }


@pytest.fixture
def parsed_crtsh_github_response():
    return [
        {
            "common_name": "skyline.github.com",
            "entry_timestamp": "2023-01-10T23:48:41.932",
            "id": 8383197569,
            "issuer_ca_id": 185756,
            "issuer_name": "C=US, O=DigiCert Inc, CN=DigiCert TLS RSA SHA256 2020 CA1",
            "name_value": "skyline.github.com\nwww.skyline.github.com",
            "not_after": "2024-01-24T23:59:59",
            "not_before": "2023-01-10T00:00:00",
            "serial_number": "071a522c3982234f64fdd14b8f4b9577",
        },
        {
            "common_name": "*.proxima-review-lab.github.com",
            "entry_timestamp": "2023-01-05T17:04:06.714",
            "id": 8353864864,
            "issuer_ca_id": 185756,
            "issuer_name": "C=US, O=DigiCert Inc, CN=DigiCert TLS RSA SHA256 2020 CA1",
            "name_value": "*.proxima-review-lab.github.com\n"
            "proxima-review-lab.github.com",
            "not_after": "2024-01-04T23:59:59",
            "not_before": "2023-01-05T00:00:00",
            "serial_number": "04ddc3cb9e41c6f4d0f8331c59ef18a5",
        },
        {
            "common_name": "*.registry.github.com",
            "entry_timestamp": "2022-12-27T18:16:02.706",
            "id": 8299960444,
            "issuer_ca_id": 185756,
            "issuer_name": "C=US, O=DigiCert Inc, CN=DigiCert TLS RSA SHA256 2020 CA1",
            "name_value": "*.registry.github.com\nregistry.github.com",
            "not_after": "2024-01-02T23:59:59",
            "not_before": "2022-12-27T00:00:00",
            "serial_number": "0e48119cceb96171a041a31752fc1adc",
        },
        {
            "common_name": "f.cloud.github.com",
            "entry_timestamp": "2022-11-17T19:45:02.684",
            "id": 7998084684,
            "issuer_ca_id": 244621,
            "issuer_name": "C=BE, O=GlobalSign nv-sa, CN=GlobalSign Atlas R3 DV TLS CA "
            "2022 Q4",
            "name_value": "f.cloud.github.com",
            "not_after": "2023-12-19T19:45:01",
            "not_before": "2022-11-17T19:45:02",
            "serial_number": "01fdd231f5ad27a5acc8d6ffdcf8a4ab",
        },
        {
            "common_name": "support.enterprise.github.com",
            "entry_timestamp": "2022-10-26T08:58:44.768",
            "id": 7837200062,
            "issuer_ca_id": 185756,
            "issuer_name": "C=US, O=DigiCert Inc, CN=DigiCert TLS RSA SHA256 2020 CA1",
            "name_value": "support.enterprise.github.com\n"
            "www.support.enterprise.github.com",
            "not_after": "2023-10-26T23:59:59",
            "not_before": "2022-10-26T00:00:00",
            "serial_number": "0880a36e5ac215fe2720133414ebc005",
        },
        {
            "common_name": "ws.support.github.com",
            "entry_timestamp": "2022-10-21T07:39:27.613",
            "id": 7798962909,
            "issuer_ca_id": 185756,
            "issuer_name": "C=US, O=DigiCert Inc, CN=DigiCert TLS RSA SHA256 2020 CA1",
            "name_value": "ws.support.github.com\nwww.ws.support.github.com",
            "not_after": "2023-10-21T23:59:59",
            "not_before": "2022-10-21T00:00:00",
            "serial_number": "01c4361712981217cb034f4eb66d2615",
        },
        {
            "common_name": "examregistration.github.com",
            "entry_timestamp": "2022-10-17T17:06:07.728",
            "id": 7776339654,
            "issuer_ca_id": 239799,
            "issuer_name": 'C=US, O="DigiCert, Inc.", CN=GeoTrust Global TLS RSA4096 '
            "SHA256 2022 CA1",
            "name_value": "examregistration.github.com",
            "not_after": "2023-04-17T23:59:59",
            "not_before": "2022-10-17T00:00:00",
            "serial_number": "092d02778b237968cd3f4a722c875884",
        },
        {
            "common_name": "api.security.github.com",
            "entry_timestamp": "2022-10-05T18:07:17.34",
            "id": 7687547527,
            "issuer_ca_id": 185756,
            "issuer_name": "C=US, O=DigiCert Inc, CN=DigiCert TLS RSA SHA256 2020 CA1",
            "name_value": "api.security.github.com\nwww.api.security.github.com",
            "not_after": "2023-10-05T23:59:59",
            "not_before": "2022-10-05T00:00:00",
            "serial_number": "05ad0dd28e8ee76487f78dea11dc608d",
        },
        {
            "common_name": "partnerportal.github.com",
            "entry_timestamp": "2022-10-04T19:36:19.289",
            "id": 7681689500,
            "issuer_ca_id": 185756,
            "issuer_name": "C=US, O=DigiCert Inc, CN=DigiCert TLS RSA SHA256 2020 CA1",
            "name_value": "partnerportal.github.com\nwww.partnerportal.github.com",
            "not_after": "2023-10-04T23:59:59",
            "not_before": "2022-10-04T00:00:00",
            "serial_number": "0bc3956f14f34e5a33dd8d98a4d759c8",
        },
        {
            "common_name": "import2.github.com",
            "entry_timestamp": "2022-09-06T19:44:56.289",
            "id": 7486854481,
            "issuer_ca_id": 185756,
            "issuer_name": "C=US, O=DigiCert Inc, CN=DigiCert TLS RSA SHA256 2020 CA1",
            "name_value": "import2.github.com\nimporter2.github.com\nporter2.github.com",
            "not_after": "2023-09-06T23:59:59",
            "not_before": "2022-09-06T00:00:00",
            "serial_number": "05eeef2f36260c7237439ebbd2af3e6a",
        },
        {
            "common_name": "api.stars.github.com",
            "entry_timestamp": "2022-07-28T10:11:51.965",
            "id": 7216594685,
            "issuer_ca_id": 185756,
            "issuer_name": "C=US, O=DigiCert Inc, CN=DigiCert TLS RSA SHA256 2020 CA1",
            "name_value": "api.stars.github.com\nwww.api.stars.github.com",
            "not_after": "2023-07-28T23:59:59",
            "not_before": "2022-07-28T00:00:00",
            "serial_number": "039ce61a571eb9386009286a813e93f6",
        },
    ]
