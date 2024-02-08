"""An AWS Python Pulumi program"""


import pulumi

import bucket_policy
import buckets
from sync_bucket import sync_bucket

# Setup Vars
config = pulumi.Config()
website_path = config.require('websitePath')

## Sync Jekyll Output to S3
sync_bucket(folder=website_path, bucket=buckets.primary_bucket)
