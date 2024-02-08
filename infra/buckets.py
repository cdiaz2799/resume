"""
This Pulumi program sets up S3 buckets to host a static website with an optional apex domain.
It uses AWS native provider to create S3 buckets with website configuration and ownership controls,
and disables blocking of public ACLs to allow public access. Additionally, it configures DNS
records using a Cloudflare utility to point to the created S3 buckets. Outputs include the bucket names
and URLs for the primary bucket and its regional domain.

Configurations:
- `subdomain`: Required. The subdomain for the primary S3 bucket.
- `apexDomain`: Optional. If provided, an additional apex S3 bucket is created to redirect to the subdomain.

Resources:
- `primary_bucket`: An S3 bucket configured for static website hosting.
- `apex_bucket`: An additional apex S3 bucket that redirects all requests to the subdomain, if `apexDomain` is provided.
- DNS records: Uses the `create_bucket_record` function from the `cloudflare` module to map the buckets to DNS records.
"""
import pulumi
import pulumi_aws_native as aws

from cloudflare import create_bucket_record

# Setup Config
config = pulumi.Config()
subdomain = config.require('subdomain')
apex = config.get('apexDomain') or None


# Create Empty List
bucket_list = []
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
bucket_list.append(primary_bucket)


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
    bucket_list.append(apex_bucket)

# Create DNS for Bucket
create_bucket_record(primary_bucket.bucket_name, primary_bucket.website_url)

# Setup Outputs
pulumi.export('bucket_name', primary_bucket.bucket_name)
pulumi.export('bucket_website_url', primary_bucket.website_url)
pulumi.export('bucket_regional_domain', primary_bucket.regional_domain_name)
