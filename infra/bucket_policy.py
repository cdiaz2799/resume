"""
This module creates an AWS S3 Bucket Policy to allow access only from Cloudflare IP addresses.

The policy grants read-only permission (`s3:GetObject`) for any object in the bucket
to requests originating from IP addresses that belong to Cloudflare. This is to ensure
that the bucket content is only served through the Cloudflare CDN and not directly accessible.

Functions:
- get_cloudflare_ips: External function that retrieves a list of Cloudflare IP addresses.

Resources:
- cloudflare_ips: A list of IP addresses fetched from the Cloudflare service.
- bucket_policy: The AWS S3 Bucket Policy that sets the permission to allow read access from Cloudflare IPs.
"""
import pulumi
import pulumi_aws_native as aws

from buckets import primary_bucket
from cloudflare_ips import get_cloudflare_ips

# Allow Cloudflare Access
cloudflare_ips = get_cloudflare_ips()


bucket_policy = aws.s3.BucketPolicy(
    'cloudflare-bucket-policy',
    bucket=primary_bucket.bucket_name,
    policy_document=pulumi.Output.all(
        bucket_arn=primary_bucket.arn, ips=cloudflare_ips
    ).apply(
        lambda args: {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Sid': 'AllowCloudflareIPsGetObject',
                    'Effect': 'Allow',
                    'Principal': '*',
                    'Action': ['s3:GetObject'],
                    'Resource': [
                        args['bucket_arn'],
                        f"{args['bucket_arn']}/*",
                    ],
                    'Condition': {'IpAddress': {'aws:SourceIp': args['ips']}},
                },
            ],
        }
    ),
    opts=pulumi.ResourceOptions(parent=primary_bucket),
)
