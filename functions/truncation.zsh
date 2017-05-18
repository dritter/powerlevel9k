# vim:ft=zsh ts=2 sw=2 sts=2 et fenc=utf-8
################################################################
# truncation
# This file holds functions for truncate strings
# after certain rules for the powerlevel9k-ZSH-theme
# https://github.com/bhilburn/powerlevel9k
################################################################

function _p9k_truncateHome() {
    local subject="${1}"
    local substitute="${2}"

    # We just cut off the piece that gets truncated,
    # because we want to hand over the rest to the next
    # truncation strategy. So our truncatedPath is just
    # our substitute..
    local truncatedPath="${substitute}"
    local remainder="$(echo "${subject}" | sed -e "s,^$HOME,,")"
    [[ -n "${remainder}" ]] || remainder="false"
    # Check if $subject does not start with $HOME. If
    # so, we are outside of $HOME and need to reset
    # the truncatedPath and set $remainder to $subject.
    if [[ "${subject}" != "${HOME}"* ]]; then
        truncatedPath=""
        remainder="${subject}"
    fi

    # This is an encoded array! Delimiter is ";".
    echo "truncated;${truncatedPath};remainder;${remainder}"
}

# TODO: Make it work chained!
#
# This is a terminal truncation. After this one is
# applied, no other truncation strategy can be applied.
function _p9k_truncateDirectories() {
    local length="${1}"
    local substitute="${2}"

    local truncatedPath="$(print -P "%$((${1}+1))(c:${substitute}/:)%${length}c")"
    # This is an encoded array! Delimiter is ";".
    echo "truncated;${truncatedPath};remainder;false"
}

# This is a terminal truncation. After this one is
# applied, no other truncation strategy can be applied.
function _p9k_truncateMiddle() {
    local subject="${1}"
    local length="${2}"
    local substitute="${3}"

    local truncatedPath="$(echo "${subject}" | sed "${SED_EXTENDED_REGEX_PARAMETER}" "s/([^/]{$length})[^/]+([^/]{$length})\//\1$substitute\2\//g")"
    # This is an encoded array! Delimiter is ";".
    echo "truncated;${truncatedPath};remainder;false"
}

# Given a directory path, truncate it according to the
# settings for `truncate_from_right`
#
# This is a terminal truncation. After this one is
# applied, no other truncation strategy can be applied.
function _p9k_truncateRight() {
    local subject="${1}"
    local length="${2}"
    local substitute="${3}"
    local substituteLength="${#substitute}"

    local truncatedPath="$(echo "${subject}" | sed "${SED_EXTENDED_REGEX_PARAMETER}" "s@(([^/]{$((length))})([^/]{$substituteLength}))[^/]+/@\2$substitute/@g")"
    # This is an encoded array! Delimiter is ";".
    echo "truncated;${truncatedPath};remainder;false"
}


function _p9k_truncatePackage() {
    local subject="${1}"

    defined POWERLEVEL9K_DIR_PACKAGE_FILES || POWERLEVEL9K_DIR_PACKAGE_FILES=("package.json" "composer.json")
    for stopfile in ${POWERLEVEL9K_DIR_PACKAGE_FILES}; do
        for marked_folder in $(upsearch "${stopfile}"); do
            # Strip the path to the stopfile from the actual (deep),
            # path, so that we can prepend it with the package name.
            local pathSuffix="${subject:${#${(S%%)marked_folder//$~zero/}}}"

            local pkgFile="${marked_folder}/${stopfile}"
            local packageName=$(jq -r '.name' ${pkgFile} 2> /dev/null \
                    || node -e 'console.log(require(process.argv[1]).name);' ${pkgFile} 2>/dev/null \
                    || cat "${pkgFile}" 2> /dev/null | grep -m 1 "\"name\"" | awk -F ':' '{print $2}' | awk -F '"' '{print $2}' 2>/dev/null \
            )

            if [[ -n "${packageName}" ]]; then
                # set pathSuffix to false if empty
                if [[ -z "${pathSuffix}" ]]; then
                    pathSuffix="false"
                fi
                # This is an encoded array! Delimiter is ";".
                echo "truncated;${packageName};remainder;${pathSuffix}"

                # Exit early. We got our information.
                return 0
            fi
        done
    done

    # set subject to false if empty
    if [[ -z "${subject}" ]]; then
        subject="false"
    fi

    # Nothing truncated, just return
    # the whole string as remainder.
    # This is an encoded array! Delimiter is ";".
    echo "truncated;false;remainder;${subject}"
}

# Truncate via folder marker
function _p9k_truncateFoldermarker() {
    local subject="${1}"
    local substitute="${2}"
    local stopfile="${3}"

    local marked_folder="$(upsearchToParentFolder "${stopfile}")"
    if [[ -n "${marked_folder}" ]]; then
        # This is an encoded array! Delimiter is ";".
        echo "truncated;${substitute};remainder;${PWD#${marked_folder}}"

        return 0
    fi

    # Nothing truncated, just return
    # the whole string as remainder.
    # This is an encoded array! Delimiter is ";".
    echo "truncated;false;remainder;${subject}"
}
