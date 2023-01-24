# ReconLib
A collection of modules and helpers for active and passive reconnaissance of remote hosts.

## Installation
```shell
pip install reconlib
```

## How to Use

### Unofficial crt.sh API
```python
from reconlib.crtsh import API

domain_info = API(domain="github.com")

domain_info.fetch()
# [{'issuer_ca_id': 185756, 'issuer_name': 'C=US, O=DigiCert Inc,
# CN=DigiCert TLS RSA SHA256 2020 CA1', 'common_name': 'skyline.github.com',
# 'name_value': 'skyline.github.com\nwww.skyline.github.com', 'id': 8383197569,
# 'entry_timestamp': '2023-01-10T23:48:41.932', ... }]

domain_info.num_results
# 737

domain_info.found_domains
# {'*.id.github.com', 'cla.github.com', 'graphql-stage.github.com', 'camo.github.com',
# 'www.github.com', 'vpn-ca.iad.github.com', '*.hq.github.com', ...}
```