# ReconLib
A collection of modules and helpers for active and passive reconnaissance of remote hosts.

## Installation
```shell
pip install reconlib
```

## How to Use

### Unofficial crt.sh API

```python
from reconlib import crtsh

domain_info = crtsh.API(target="github.com")

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

### Unofficial HackerTarget API
```python
from reconlib import hackertarget

domain_info = hackertarget.API(target="github.com")

domain_info.hostsearch()
# {
#     IPv4Address("140.82.121.9"): "lb-140-82-121-9-fra.github.com",
#     IPv4Address("192.30.255.117"): "lb-192-30-255-117-sea.github.com",
#     IPv4Address("140.82.114.27"): "lb-140-82-114-27-iad.github.com",
#     ...
# }

domain_info.found_domains
# [ "lb-140-82-121-9-fra.github.com", "lb-192-30-255-117-sea.github.com",
# "lb-140-82-114-27-iad.github.com", "out-23.smtp.github.com", ...]

domain_info.found_ip_addrs
# [ IPv4Address("140.82.121.9"), IPv4Address("192.30.255.117"),
# IPv4Address("140.82.114.27"), IPv4Address("192.30.252.206"), ...]

domain_info.dnslookup()
# {
#     "A": ["140.82.113.4"],
#     "MX": [
#         "1 aspmx.l.google.com.",
#         "10 alt3.aspmx.l.google.com.",
#         "10 alt4.aspmx.l.google.com.",
#     ],
#     ...
# }
```