#!/bin/bash

set -o errexit
set -o nounset

cd /app

exec watchfiles celery.__main__.main  --args '-A config.celery worker -l INFO'