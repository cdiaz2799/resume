"""
Module for synchronizing a local folder with an S3 bucket.

This module provides functionality to synchronize a local folder with an S3 bucket in Pulumi.

Usage:
    To synchronize a local folder with an S3 bucket, use the `sync_bucket` function.

Example:
    ```python
    import pulumi
    import pulumi_synced_folder as synced_folder

    # Create an S3 bucket
    bucket = pulumi.aws.s3.Bucket('my-bucket')

    # Synchronize a local folder with the S3 bucket
    synced_folder = sync_bucket('local-folder', bucket)

    pulumi.export('synchronized_folder_id', synced_folder.id)
    ```

Functions:
    sync_bucket(folder: str, bucket: pulumi.Resource) -> synced_folder.S3BucketFolder:
        Synchronizes a local folder with an S3 bucket.

Args:
    folder (str): The local folder path to be synchronized with the S3 bucket.
    bucket (pulumi.Resource): The S3 bucket resource where the folder contents will be synced.

Returns:
    synced_folder.S3BucketFolder: A Pulumi resource representing the synchronized bucket folder.
"""

import pulumi
import pulumi_synced_folder as synced_folder


def sync_bucket(folder, bucket):
    """
    Synchronizes a local folder with an S3 bucket.

    Args:
        folder (str): The local folder path to be synchronized with the S3 bucket.
        bucket (pulumi.Resource): The S3 bucket resource where the folder contents will be synced.

    Returns:
        synced_folder.S3BucketFolder: A Pulumi resource representing the synchronized bucket folder.

    """
    bucket_sync = synced_folder.S3BucketFolder(
        'bucket-folder',
        acl='public-read',
        bucket_name=bucket.bucket_name,
        path=folder,
        opts=pulumi.ResourceOptions(parent=bucket),
    )
    return bucket_sync
