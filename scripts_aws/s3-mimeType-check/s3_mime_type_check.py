"""
usage:
    Limit mode:
        python3 s3_mime_type_check.py -b <nome_bucket> -f <pasta_bucket> -p <local_path> -l <limite_objetos>
    Production mode:
        python3 s3_mime_type_check.py -b <nome_bucket> -f <pasta_bucket> -p <local_path>

"""

import boto3
import filetype
import argparse
import logging
import botocore
from concurrent.futures import ThreadPoolExecutor


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s [%(asctime)s]: %(message)s",
    handlers=[logging.FileHandler("s3_check.log", mode="w"), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)
logging.getLogger("botocore").setLevel(logging.WARNING)


def main(args, executor):
    count = 0

    client_config = botocore.config.Config(
        max_pool_connections=args.thread,
    )
    s3_client = boto3.client("s3", config=client_config)

    objects = s3_client.list_objects_v2(Bucket=args.bucket, Prefix=args.folder)
    object_count = save_obj(executor, s3_client, objects, count, args.limit)
    count += object_count

    if args.limit and count == args.limit:
        return

    if "NextContinuationToken" not in objects:
        return

    objects = s3_client.list_objects_v2(
        Bucket=args.bucket, Prefix=args.folder, ContinuationToken=objects["NextContinuationToken"]
    )

    while "NextContinuationToken" in objects:
        object_count = save_obj(executor, s3_client, objects, count, args.limit)

        count += object_count

        if args.limit and count == args.limit:
            break

        objects = s3_client.list_objects_v2(
            Bucket=args.bucket,
            Prefix=args.folder,
            ContinuationToken=objects["NextContinuationToken"],
        )


def check_type(obj, s3_client):
    resp = s3_client.get_object(
        Bucket=args.bucket,
        Key=obj["Key"],
    )
    kind = filetype.guess(resp["Body"].read())

    if kind is None:
        save_log(obj["Key"])

    else:
        save_log(obj["Key"], kind.extension, kind.mime)


def save_obj(executor, s3_client, objects, count, limit):
    for object_count, obj in enumerate(objects["Contents"], start=1):
        executor.submit(check_type, obj, s3_client)
        count += 1

        if limit and count == limit:
            break

    return object_count


def save_log(key_name, ext=None, mime_type=None):
    line = f"{key_name};{ext};{mime_type};"
    logger.info(line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--bucket", type=str, help="Bucket Name")
    parser.add_argument("-f", "--folder", type=str, help="Folder in bucket")
    parser.add_argument("-l", "--limit", type=int, default=None, help="Limit object")
    parser.add_argument("-t", "--thread", type=int, default=8, help="Number of threads")
    args = parser.parse_args()

    with ThreadPoolExecutor(args.thread) as executor:
        main(args, executor)
