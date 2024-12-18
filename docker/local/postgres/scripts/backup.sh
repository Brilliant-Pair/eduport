#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail

working_dir="$(dirname "${0}")"

source "${working_dir}/utils/constant.sh"
source "${working_dir}/utils/messages.sh"

message_welcome "Backing up the ${POSTGRES_DB} database..."

export PGDATABASE="${POSTGRES_DB}"
export PGUSER="${POSTGRES_USER}"
export PGPASSWORD="${POSTGRES_PASSWORD}"
export PGHOST="${POSTGRES_HOST}"
export PGPORT="${POSTGRES_PORT}"

backup_filename="${BACKUP_FILE_PREFIX}_$(date +'%Y_%m_%dT%H_%M_%S').sql.gz"

pg_dump | gzip > "${BACKUP_DIR_PATH}/${backup_filename}"

message_success "${POSTGRES_DB} database backup ${backup_filename} has been created successfully and placed in ${BACKUP_DIR_PATH}."