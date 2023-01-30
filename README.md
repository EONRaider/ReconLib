# ReconLib
A collection of modules and helpers for active and passive reconnaissance of remote hosts.
ReconLib can be used as a standalone library on Python code or as an engine for tools
such as subdomain enumerators and others.

## Installation
```shell
pip install reconlib
```

## How to Use
Click on a section to expand a code snippet that illustrates how to use each API and its
available methods.

### Unofficial crt.sh API
<details>
<summary>Fetch Certificate Information</summary>

```python
from reconlib import CRTShAPI

certificates = CRTShAPI().fetch_certificates(target="github.com")

print(certificates)

# [{'issuer_ca_id': 185756, 'issuer_name': 'C=US, O=DigiCert Inc,
# CN=DigiCert TLS RSA SHA256 2020 CA1', 'common_name': 'skyline.github.com',
# 'name_value': 'skyline.github.com\nwww.skyline.github.com', 'id': 8383197569,
# 'entry_timestamp': '2023-01-10T23:48:41.932', ... }]
```
</details>

<details>
<summary>Fetch All Subdomains of a given target</summary>

```python
from reconlib import CRTShAPI

subdomains = CRTShAPI().fetch_subdomains(target="github.com")

print(subdomains)

# {
#     'import2.github.com', 'api.security.github.com', 'examregistration.github.com',
#     '*.registry.github.com', 'api.stars.github.com', ...
# }
```
</details>

### Unofficial HackerTarget API

<details>
<summary>Perform a request to HackerTarget's API "hostsearch" endpoint</summary>

```python
from reconlib import HackerTargetAPI

hackertarget = HackerTargetAPI()

print(hackertarget.hostsearch(target="github.com"))
# {
#     IPv4Address("140.82.121.9"): "lb-140-82-121-9-fra.github.com",
#     IPv4Address("192.30.255.117"): "lb-192-30-255-117-sea.github.com",
#     IPv4Address("140.82.114.27"): "lb-140-82-114-27-iad.github.com",
#     ...
# }

print(hackertarget.ip_addresses)
# {
#     "github.com": {
#         IPv4Address("140.82.121.9"),
#         IPv4Address("192.30.255.117"),
#         IPv4Address("140.82.114.27"),
#         ...
#     }
# }

print(hackertarget.subdomains)
# {
#     "lb-140-82-121-9-fra.github.com",
#     "lb-192-30-255-117-sea.github.com",
#     "lb-140-82-114-27-iad.github.com",
#     ...
# }
```
</details>

<details>
<summary>Perform a request to HackerTarget's API "dnslookup" endpoint</summary>

```python
from reconlib import HackerTargetAPI

dnslookup = HackerTargetAPI().dnslookup(target="github.com")

print(dnslookup)

# {
#     "github.com": {
#         "A": ["140.82.113.4"],
#         "MX": [
#             "1 aspmx.l.google.com.",
#             "10 alt3.aspmx.l.google.com.",
#             "10 alt4.aspmx.l.google.com.",
#         ],
#         "NS": ["dns1.p08.nsone.net.", "dns2.p08.nsone.net."],
#         ...
#     }
# }
```
</details>

<details>
<summary>Perform a request to HackerTarget's API "reversedns" endpoint</summary>

```python
from reconlib import HackerTargetAPI

reverse_dns = HackerTargetAPI().reverse_dns(target="140.82.121.9")

print(reverse_dns)

# {IPv4Address("140.82.121.9"): "lb-140-82-121-9-fra.github.com"}
```
</details>

<details>
<summary>Perform a request to HackerTarget's API "aslookup" endpoint</summary>

```python
from reconlib import HackerTargetAPI

aslookup = HackerTargetAPI().aslookup(target="140.82.121.9")

print(aslookup)

# {
#     "ASN": 36459,
#     "IP_ADDRESS": IPv4Address("140.82.121.9"),
#     "NETWORK": IPv4Network("140.82.121.0/24"),
#     "OWNER": "GITHUB, US",
# }
```
</details>

<details>
<summary>Fetch All Subdomains of a given target</summary>

```python
from reconlib import HackerTargetAPI

subdomains = HackerTargetAPI().fetch_subdomains(target="github.com")

print(subdomains)

# {
#     "lb-140-82-121-9-fra.github.com",
#     "lb-192-30-255-117-sea.github.com",
#     "lb-140-82-114-27-iad.github.com",
#     ...
# }
```
</details>

### VirusTotal API
A `VirusTotalAPI` object can be instantiated with the "api_key" attribute
set to a pre-defined value, but setting it with the "VIRUSTOTAL_API_KEY"
environment variable is the recommended way to do it before proceeding. Setting it up
like this guarantees hardcoded secrets to be completely avoided. ReconLib will detect
environment variables set directly through a shell or a file.

```shell
EXPORT VIRUSTOTAL_API_KEY="YOUR-VT-API-KEY"
```

<details>
<summary>Fetch All Subdomains of a given target</summary>

```python
from reconlib import VirusTotalAPI

'''An instance of VirusTotalAPI will read the API key value from
the environment by default. Passing it as an argument in code is
possible, but not required.'''
subdomains = VirusTotalAPI().fetch_subdomains(target="scanme.nmap.org")

print(subdomains)
# {
#     "ckeepingthechristmasspiritalive365.nmap.org",
#     "dgbridgedgbridgedgbridge.nmap.org",
#     "echoriseaboveyourlimits.nmap.org",
#     "wwwtradingdeportivo-domingodearmas.nmap.org",
#     ...
# }
```
</details>