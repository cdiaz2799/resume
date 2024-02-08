"""
Module to retrieve Cloudflare IP ranges (IPv4 and IPv6) using the Cloudflare API.

This module provides a function `get_cloudflare_ips()` to fetch Cloudflare IP ranges in CIDR notation.
It sends a GET request to the Cloudflare API endpoint `/client/v4/ips` with the appropriate headers.
The function returns a list containing Cloudflare IP ranges.

Example:
    >>> from cloudflare_ips import get_cloudflare_ips
    >>> ips = get_cloudflare_ips()
    >>> print(ips)
    ['103.21.244.0/22', '103.22.200.0/22', ...]

Raises:
    Exception: If unable to retrieve Cloudflare IP ranges or encounter any other error during the process.
"""

import http.client
import json


def get_cloudflare_ips():
    """
    Retrieve Cloudflare IP ranges (IPv4 and IPv6) using Cloudflare API.

    Returns:
        list: A list containing Cloudflare IP ranges in CIDR notation.

    Raises:
        Exception: If unable to retrieve Cloudflare IP ranges.
    """
    conn = http.client.HTTPSConnection('api.cloudflare.com')
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer undefined',
    }

    conn.request('GET', '/client/v4/ips', headers=headers)

    res = conn.getresponse()
    data = res.read()
    ipv4_cidrs = json.loads(data.decode('utf-8'))['result']['ipv4_cidrs']
    ipv6_cidrs = json.loads(data.decode('utf-8'))['result']['ipv6_cidrs']
    cidrs = ipv4_cidrs + ipv6_cidrs
    return cidrs
