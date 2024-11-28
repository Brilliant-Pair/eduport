#!/bin/bash

set -o errexit
set -o nounset

cd /app

exec watchfiles celery.__main__.main \
    --args "-A config.celery -b \"${CELERY_BROKER_URL}\" flower --basic-auth=\"${CELERY_FLOWER_USER}\":\"${CELERY_FLOWER_PASSWORD}\""