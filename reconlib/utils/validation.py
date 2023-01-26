from ipaddress import ip_address, IPv6Address, IPv4Address
from typing import Any

from reconlib.core.exceptions import InvalidTargetError


def validate_ip_address(ip_addr: Any) -> [IPv4Address, IPv6Address]:
    try:
        return ip_address(ip_addr)
    except ValueError as e:
        raise InvalidTargetError(str(e))
