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
