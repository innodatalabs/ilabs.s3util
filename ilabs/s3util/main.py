import argparse
from ilabs.s3util.util import cli_pypi, cli_upload


def main_pypi():
    parser = argparse.ArgumentParser(description='Uploads packages to private PyPI server hosted on Amazon S3')
    parser.add_argument('file_mask', help='File name or file name mask to upload. Typically "dist/*"')
    parser.add_argument('--target', '-t', default=None, help='Name of the target S3 url, in the form s3://bucket/prefix. If not set, will try to infer this from pip.conf')
    parser.add_argument('--force', '-f', action='store_true', default=False, help='Force overwrite of existing key')
    parser.add_argument('--aws_access_key_id', default=None, help='AWS access key id. If not set, will use AWS credentials configuration, if available')
    parser.add_argument('--aws_secret_access_key', default=None, help='AWS secret access key. If not set, will use AWS credentials configuration, if available')

    args = parser.parse_args()
    print(args)

    parser.exit(cli_pypi(args))


def main_upload():
    parser = argparse.ArgumentParser(description='Uploads files to Amazon S3 bucket')
    parser.add_argument('file_mask', help='File name or file name mask to upload. Typically "dist/*"')
    parser.add_argument('target', help='Name of the target S3 url, in the form s3://bucket/prefix')
    parser.add_argument('--acl', '-a', default='private', help='Canned access control value. Use "public-read" to make uploaded files readable by all. Default is "private"')
    parser.add_argument('--force', '-f', action='store_true', default=False, help='Force overwrite of existing key')
    parser.add_argument('--aws_access_key_id', default=None, help='AWS access key id. If not set, will use AWS credentials configuration, if available')
    parser.add_argument('--aws_secret_access_key', default=None, help='AWS secret access key. If not set, will use AWS credentials configuration, if available')

    args = parser.parse_args()
    print(args)

    parser.exit(cli_upload(args))
