"""
A Pulumi program to manage Cloudflare DNS records.

This module contains a configuration setup for defining the apex domain and website path,
a function to create DNS CNAME records, and it utilizes Cloudflare's DNS service to
map subdomains to specified endpoints.


Example:
    create_bucket_record('www', pulumi.Output.from_input('https://example.com'))
"""
import pulumi
import pulumi_cloudflare as cloudflare

# Setup Config
config = pulumi.Config()
domain_apex = config.require('apexDomain')
website_path = config.require('websitePath')
apex = config.get('apexDomain') or None
org = pulumi.get_organization()
project = pulumi.get_project()
stack = pulumi.get_stack()

# Retrieve Zone
zone = cloudflare.get_zone(name=domain_apex)

# Create Primary Bucket Record
def create_bucket_record(subdomain, endpoint):
    """
    Creates a DNS CNAME record for a given subdomain pointing to the specified endpoint.

    This function takes the endpoint URL, removes the 'http://' or 'https://'
    protocol from it, and creates a CNAME record under the given subdomain using
    Cloudflare's DNS service.

    Args:
    subdomain (str): The subdomain for which to create the CNAME record.
    endpoint (pulumi.Output): The endpoint URL to which the subdomain will point, as a Pulumi Output.

    Returns:
    pulumi_cloudflare.Record: A Pulumi Cloudflare Record resource.
    """
    trimmed_endpoint = endpoint.apply(
        lambda url: url.replace('http://', '').replace('https://', '')
    )
    hostname = subdomain.apply(
        lambda hostname: hostname.replace(f'.{domain_apex}', '')
    )
    record = cloudflare.Record(
        'record',
        args=cloudflare.RecordArgs(
            zone_id=zone.id,
            name=hostname,
            type='CNAME',
            value=trimmed_endpoint,
            proxied=True,
            comment=f'Managed by Pulumi: {org}/{project}/{stack}',
        ),
    )
    return record
