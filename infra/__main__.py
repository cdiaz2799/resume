"""An AWS Python Pulumi program"""

import json
import pulumi
import pulumi_aws_native as aws
import pulumi_synced_folder as synced_folder
from cloudflare_ips import get_cloudflare_ips
from sync_bucket import sync_bucket

# Setup Vars
config = pulumi.Config()
website_path = config.require('websitePath')
subdomain = config.require('subdomain')
apex = config.get('apexDomain') or None


# Create Empty Bucket List
buckets = []

# Setup Primary Bucket
primary_bucket = aws.s3.Bucket(
    'bucket',
    bucket_name=subdomain,
    ## Define Website Configuration
    website_configuration=aws.s3.BucketWebsiteConfigurationArgs(
        index_document='index.html',
        error_document='404.html',
    ),
    ## Define Ownership Controls
    ownership_controls=aws.s3.BucketOwnershipControlsArgs(
        rules=[
            aws.s3.BucketOwnershipControlsRuleArgs(
                object_ownership=aws.s3.BucketOwnershipControlsRuleObjectOwnership(
                    'ObjectWriter'
                )
            )
        ]
    ),
    ## Don't Block Public Access
    public_access_block_configuration=aws.s3.BucketPublicAccessBlockConfigurationArgs(
        block_public_acls=False,
    ),
)
buckets.append(primary_bucket)

if apex:
    apex_bucket = aws.s3.Bucket(
        'apex-bucket',
        bucket_name=apex,
        website_configuration=aws.s3.BucketWebsiteConfigurationArgs(
            redirect_all_requests_to=aws.s3.BucketRedirectAllRequestsToArgs(
                host_name=subdomain
            ),
        ),
    )
    buckets.append(apex_bucket)

# Allow Cloudflare Access
cloudflare_ips = get_cloudflare_ips()
ip_conditions = [{'IpAddress': {'aws:SourceIp': ip}} for ip in cloudflare_ips]

bucket_policy = aws.s3.BucketPolicy(
    'cloudflare-bucket-policy',
    bucket=primary_bucket.bucket_name,
    policy_document=pulumi.Output.all(
        bucket_arn=primary_bucket.arn,
        ips=ip_conditions,
    ).apply(
        lambda args: {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Sid': 'AllowCloudflareIPsGetObject',
                    'Effect': 'Allow',
                    'Principal': '*',
                    'Action': ['s3:GetObject'],
                    'Resource': args['bucket_arn'],
                    'Condition': {'IpAddress': args['ips']},
                },
            ],
        }
    ),
    opts=pulumi.ResourceOptions(parent=primary_bucket),
)

## Sync Jekyll Output to S3
sync_bucket(folder=website_path, bucket=primary_bucket)

# Setup Outputs
pulumi.export('bucket_name', primary_bucket.bucket_name)
pulumi.export('bucket_website_url', primary_bucket.website_url)
pulumi.export('bucket_regional_domain', primary_bucket.regional_domain_name)
