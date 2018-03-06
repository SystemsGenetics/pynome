#!/usr/bin/env bash
set -e

_update_uid_gid() {
    # update UID
    if [[ ${UID_IRODS} != 998 ]]; then
        gosu root usermod -u ${UID_IRODS} irods
    fi
    # update GID
    if [[ ${GID_IRODS} != 998 ]]; then
        gosu root groupmod -g ${GID_IRODS} irods
    fi
    # update directories
    gosu root chown -R irods:irods /var/lib/irods
    gosu root chown -R irods:irods /pynome
}

_irods_environment_json() {
    gosu root mkdir -p /var/lib/irods/.irods
    local OUTFILE=/var/lib/irods/.irods/irods_environment.json
    gosu root jq -n \
        --arg h "${IRODS_HOST}" \
        --arg p "${IRODS_PORT}" \
        --arg z "${IRODS_ZONE_NAME}" \
        --arg n "${IRODS_USER_NAME}" \
        '{"irods_host": $h, "irods_port": $p | tonumber, "irods_zone_name": $z,
        "irods_user_name": $n}' > $OUTFILE
}

_irods_tgz() {
    if [ -z "$(ls -A /var/lib/irods)" ]; then
        gosu root cp /irods.tar.gz /var/lib/irods/irods.tar.gz
        cd /var/lib/irods/
        gosu root tar -zxf irods.tar.gz
        cd /
        gosu root rm -f /var/lib/irods/irods.tar.gz
    fi
}

_irods_tgz
_irods_environment_json
_update_uid_gid
gosu irods iinit ${IRODS_PASSWORD}
gosu irods "$@"

exit 0;
