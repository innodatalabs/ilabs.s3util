# ilabs.s3util
[![PyPI version](https://badge.fury.io/py/ilabs.s3util.svg)](https://badge.fury.io/py/ilabs.s3util)

Use Amazon S3 static website to distribute private pypi packages.

Inspired by https://github.com/novemberfiveco/s3pypi

ATTENTION! Not very secure method, as we use unencrypted HTTP connection and
no authentication. Protection is all in the "secret" bucket name.

## Requirements

* Python 3
* boto3

## How to configure S3 bucket as pypi host

1. Decide on unique and secret name of your S3 bucket. One simple way is to
   use https://www.uuidgenerator.net/ to generate globally unique identifier.
   Be creative! I will assume that bucket name is `<bucket_name>`

2. Go to [S3 AWS Management Console](https://console.aws.amazon.com/s3/home)
   and create bucket with this name.

3. Click on the bucket name and in the Properties tab click on
   `Static website hosting`, and enable radio button
   `Use this bucket to host a website`. Accept default values for
   `Index document` and `Error document`.

4. Make a note of website endpoint. It should look like this:

   ```
   http://<bucket_name>.s3-website-<region>.amazonaws.com
   ```
   Copy this name to the clipboard, as you will need it later

5. On your computer, open (or create) file `~/.config/pip/pip.conf` and
   add the following under `[global]` section:

   ```
   [global]
   extra-index-url=http://<bucket_name>.s3-website-<region>.amazonaws.com
   trusted-host=<bucket_name>.s3-website-<region>.amazonaws.com
   ```

Now your `pip install` command is ready to use your private PyPi (in addition
to the public one)

## Distributing private packages

To distribute packages you need in addition to the steps above do this:

### install this package
```
pip install ilabs.s3util
```

### configure AWS credentials
Open or create file
```
~/.aws/credentials
```
and add the following lines there:
```
[default]
aws_access_key_id=<YOUR_AWS_ACCESS_KEY_ID>
aws_secret_access_key=<YOUR_AWS_SECRET_ACCESS_KEY>
```
Finally, make sure that credentials are not readable by the general public:
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
   s3pypi dist/*
   ```

#### Use setup.py to upload packages to private pypi   
This is an alternative method to CLI, sometimes convenient in the automated
build environments like Jenkins.

1. Modify the contents of `setup.py` and add support for `ilabs.s3util` command:
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
s3upload dist/* s3://bucket/prefix --acl public-read --force
```

Uploadds all files found under `dist/*` to the bucket `s3://bucket/prefix`, setting
access as `public-read` and forcing overwrite if file already exist.

### setup.py
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
