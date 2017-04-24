# ilabs.s3util
[![PyPI version](https://badge.fury.io/py/ilabs.s3util.svg)](https://badge.fury.io/py/ilabs.s3util)

Use Amazon S3 static website to distribute private pypi packages.

Inspired by https://github.com/novemberfiveco/s3pypi

ATTENTION! Not very secure method, as we use no authentication. All protection is in
the "secret" bucket key prefix.

## Requirements

* Python 3
* boto3

## How to configure S3 bucket as pypi host

1. Decide on unique and secret key prefix for your S3 bucket. One simple way is to
   use https://www.uuidgenerator.net/ to generate globally unique identifier.
   Be creative! I will assume that prefix name is `<secret_prefix>`

2. Go to [S3 AWS Management Console](https://console.aws.amazon.com/s3/home)
   and create a new bucket (choose whatever reasonable name you want,
   for example `pypi.yourcompany.com`). I will assume that bucket name is `<bucket_name>`.

3. Click on the bucket name and in the Properties tab click on
   `Static website hosting`, and enable radio button
   `Use this bucket to host a website`. Make sure that value for
   `Index document` is set to `index.html`.

4. Make a note of website endpoint. It should look like this:

   ```
   http://<bucket_name>.s3-website-<region>.amazonaws.com
   ```
   Copy this name to the clipboard, as you will need it later

5. Go to [AWS CloudFront](https://console.aws.amazon.com/cloudfront/home) and create
   new distribution. We need CloudFront because pip refuses to locally cache packages
   from unsecured PyPI sources. We will use CloudFront to wrap S3 bucket website into HTTPS.
   
   Use your S3 website endpoint as "Origin Domain Name", and accept all defaults.

6. Wait till your CloudFront distribution activates. Make note of the domain name for the
   created service. It looks something like this:
   
   '''
   bz456hgfyth38dj.cloudfront.net
   '''
   
   I will call it `<cloudfront_host>.cloudfron.net`.

6. On your computer, open (or create) file `~/.config/pip/pip.conf` (on Windows file name is `~/AppData/Rouming/pip/pip.ini`) and
   add the following entries (create sections as needed):

   ```
   [global]
   extra-index-url=https://<cloudfron_host>.cloudfront.net/<secret_prefix>
   
   [ilabs.s3util]
   target=s3://<bucket_name>/<secret_prefix>
   ```

Now your `pip install` command is ready to use your private PyPi (in addition
to the public one).

Distribute `pip.conf` to all users that need to be able to install packages from private PyPI. They will not be
able to upload packages to the PyPI. Typically only admin and build machines would have upload configured.

## Distributing private packages

To distribute (upload) packages you need in addition to the steps above do this:

### install this package
```
pip install ilabs.s3util
```

### configure AWS credentials
Open or create file  `~/.aws/credentials` and add the following lines there:
```
[default]
aws_access_key_id=<YOUR_AWS_ACCESS_KEY_ID>
aws_secret_access_key=<YOUR_AWS_SECRET_ACCESS_KEY>
```
Finally, make sure that credentials are not readable by the general public (skip this step if you are on Windows):
```
chmod 0600 ~/.aws/credentials
```

### Use CLI to upload packages, or use setup.py to do the same

Which upload method to use, depends on your preferences.

#### Upload packages using CLI

1. Build your awesome project, as usual:
   ```
   python setup.py sdist bdist_wheel
   ```
2. Run CLI command to upload artifacts to the private pypi:
   ```
   s3pypi dist/*
   ```
   Command will parse `pip.conf` content to find the name of the
   S3 bucket.

   Alternatively, you can explicitly specify where to upload:
   ```
   s3pypi dist/* --target s3://<bucket_name>/<prefix_name>
   ```

   By the default, CLI will not override the package if the same version already
   exists in private pypi. To force overwrite use `'--force/-f` option:
   ```
   s3pypi dist/* --force
   ```

#### Use setup.py to upload packages to private pypi   
This is an alternative method to CLI, sometimes convenient in the automated
build environments like Jenkins.

1. Modify the contents of `setup.py` and add support for `s3pypi` command:
```
...
from ilabs.s3util.command import PyPICommand

...
setup(
  name=<your_awesome_name>,
  ...
  cmdclass={
    's3pypi': PyPICommand
  },
  options={
    's3pypi': {
      'force': True
    }
  }
)
```

Now you can build and upload using `setup.py`:

```
python setup.py sdist bdist_wheel s3pypi
```

### Other useful tools
Generic CLI and `setup.py` tool for file upload to S3:

#### CLI
```
s3upload dist/* --target s3://bucket/prefix --acl public-read --force
```

Uploadds all files found under `dist/*` to the bucket `s3://bucket/prefix`, setting
access as `public-read` and forcing overwrite if file already exist.

### setup.py
You can use `UploadCommand` to upload files to S3 during `setup.py` processing, like this:
```
...
from ilabs.s3util.command import UploadCommand

...
setup(
  name=<your_awesome_name>,
  ...
  cmdclass={
      's3upload': UploadCommand
  },
  options={
    's3upload': {
      'file_mask': 'dist/*',
      'target': 's3://<bucket_name>/<prefix>',
      'force': False,
      'acl': 'public-read'
    }
  }
)
```
