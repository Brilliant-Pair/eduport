#!/usr/bin/env bash

set -o errexit
set -o nounset

working_dir="$(dirname "${0}")"

source "${working_dir}/utils/constant.sh"
source "${working_dir}/utils/messages.sh"

message_info "These are the backups:"

ls -lht "${BACKUP_DIR_PATH}"