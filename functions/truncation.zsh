# vim:ft=zsh ts=2 sw=2 sts=2 et fenc=utf-8
################################################################
# truncation
# This file holds functions for truncate strings
# after certain rules for the powerlevel9k-ZSH-theme
# https://github.com/bhilburn/powerlevel9k
################################################################

function _p9k_truncateHome() {
    local subject="${1}"
    local delimiter="${2}"

    echo "${subject}" | sed -e "s,^$HOME,${delimiter},"
}

# TODO: Make it work chained!
function _p9k_truncateDirectories() {
    local length="${1}"
    local delimiter="${2}"

    print -P "%$((${1}+1))(c:${delimiter}/:)%${length}c"
}

function _p9k_truncateMiddle() {
    local subject="${1}"
    local length="${2}"
    local delimiter="${3}"
    
    echo "${subject}" | sed "${SED_EXTENDED_REGEX_PARAMETER}" "s/([^/]{$length})[^/]+([^/]{$length})\//\1$delimiter\2\//g"
}

# Given a directory path, truncate it according to the
# settings for `truncate_from_right`
function _p9k_truncateRight() {
    local subject="${1}"
    local length="${2}"
    local delimiter="${3}"
    local delimiterLength="${#delimiter}"

    echo "${subject}" | sed "${SED_EXTENDED_REGEX_PARAMETER}" "s@(([^/]{$((length))})([^/]{$delimiterLength}))[^/]+/@\2$delimiter/@g"
}

function _p9k_truncatePackage() {
    local subject="${1}"
    local length="${2}"
    local delimiter="${3}"
    local name repo_path package_path current_dir zero

    # Get the path of the Git repo, which should have the package.json file
    if [[ $(git rev-parse --is-inside-work-tree 2> /dev/null) == "true" ]]; then
        # Get path from the root of the git repository to the current dir
        local gitPath=$(git rev-parse --show-prefix)
        # Remove trailing slash from git path, so that we can
        # remove that git path from the pwd.
        gitPath=${gitPath%/}
        package_path=${${subject}%%$gitPath}
        # Remove trailing slash
        package_path=${package_path%/}
    elif [[ $(git rev-parse --is-inside-git-dir 2> /dev/null) == "true" ]]; then
        package_path=${${subject}%%/.git*}
    fi

    # Replace the shortest possible match of the marked folder from
    # the current path. Remove the amount of characters up to the
    # folder marker from the left. Count only the visible characters
    # in the path (this is done by the "zero" pattern; see
    # http://stackoverflow.com/a/40855342/5586433).
    local zero='%([BSUbfksu]|([FB]|){*})'
    current_dir=$(pwd)
    # Then, find the length of the package_path string, and save the
    # subdirectory path as a substring of the current directory's path from 0
    # to the length of the package path's string
    subdirectory_path=$(_p9k_truncateRight "${current_dir:${#${(S%%)package_path//$~zero/}}}" "${POWERLEVEL9K_SHORTEN_DIR_LENGTH}" "${POWERLEVEL9K_SHORTEN_DELIMITER}")
    # Parse the 'name' from the package.json; if there are any problems, just
    # print the file path
    defined POWERLEVEL9K_DIR_PACKAGE_FILES || POWERLEVEL9K_DIR_PACKAGE_FILES=(package.json composer.json)

    local pkgFile="unknown"
    for file in "${POWERLEVEL9K_DIR_PACKAGE_FILES[@]}"; do
        if [[ -f "${package_path}/${file}" ]]; then
        pkgFile="${package_path}/${file}"
        break;
        fi
    done

    local packageName=$(jq -r '.name' ${pkgFile} 2> /dev/null \
        || node -e 'console.log(require(process.argv[1]).name);' ${pkgFile} 2>/dev/null \
        || cat "${pkgFile}" 2> /dev/null | grep -m 1 "\"name\"" | awk -F ':' '{print $2}' | awk -F '"' '{print $2}' 2>/dev/null \
        )
    if [[ -n "${packageName}" ]]; then
        # Instead of printing out the full path, print out the name of the package
        # from the package.json and append the current subdirectory


        # TODO: This won't work chained, as we either get a already truncated path,
        # or we hand over our path with the (maybe long) package name to the next
        # truncation function, which will truncate the package name as well...

        echo "${packageName}${subdirectory_path}"
    fi
}
