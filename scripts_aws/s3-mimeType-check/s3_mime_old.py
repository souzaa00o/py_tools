'''
usage:
    Limit mode:
        python3 s3_mime_type_check.py -b <nome_bucket> -f <pasta_bucket> -p <local_path> -l <limite_objetos>
    Production mode:
        python3 s3_mime_type_check.py -b <nome_bucket> -f <pasta_bucket> -p <local_path>

        python3 s3_mime_type_check.py -b noverde-documents-549971784374 -f documents/ -p /home/s0uz4/Downloads/ImageTst/ -l 5
'''

import boto3 
import filetype
import argparse
import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s [%(asctime)s]: %(message)s',
    handlers=[
        logging.FileHandler("s3_check.log", mode='w'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
logging.getLogger("botocore").setLevel(logging.WARNING)

s3_resource = boto3.resource('s3')
s3_client = boto3.client('s3')

file_prefix = 'object'

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--bucket', type=str, help='Bucket Name')
parser.add_argument('-f', '--folder', type=str, help='Folder in bucket')
parser.add_argument('-p', '--path', type=str, help='Path to download files')
parser.add_argument('-l', '--limit', type=int, default=None, help='Limit object')
args = parser.parse_args()


def main():
    count = 0
    objects = s3_client.list_objects_v2(Bucket=args.bucket, Prefix=args.folder)
    object_count = save_obj(objects, count)
    count += object_count
    
    if args.limit and count == args.limit:
        sys.exit()

    objects = list_more(objects['NextContinuationToken'])
    
    while 'NextContinuationToken' in objects:
        object_count = save_obj(objects, count)
        count += object_count
        
        if args.limit and count == args.limit:
            break

        objects = list_more(objects['NextContinuationToken'])


def save_obj(objects, count):    
    for object_count, obj in enumerate(objects['Contents'], start=1):
        local_name = download(obj['Key'], object_count)
        kind = mime_check(local_name)

        if kind is None:
            save_log(obj['Key'], "None", "None")

        else:
            save_log(obj['Key'], kind.extension, kind.mime)

        count += 1

        if args.limit and count == args.limit:
            break

    return object_count


def download(key_name, i):
    file_name = str(file_prefix+str(i))
    s3_resource.Object(args.bucket, key_name).download_file(args.path+file_name)
    return file_name


def mime_check(file_name):
    return filetype.guess(args.path+file_name)


def save_log(key_name, ext, mime_type):
    line = f"{key_name};{ext};{mime_type};"
    logger.info(line)


def list_more(nxToken):
    return s3_client.list_objects_v2(Bucket=args.bucket, Prefix=args.folder, ContinuationToken=nxToken)
    

if __name__ == '__main__':
    main()
