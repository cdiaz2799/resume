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
