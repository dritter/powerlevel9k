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

function _p9k_truncateMiddle() {
    local subject="${1}"
    local length="${2}"
    local delimiter="${3}"
    
    echo "${subject}" | sed "${SED_EXTENDED_REGEX_PARAMETER}" "s/([^/]{$length})[^/]+([^/]{$length})\//\1$delimiter\2\//g"
}

# Given a directory path, truncate it according to the
# settings for `truncate_from_right`
function _p9k_truncateFromRight() {
    local subject="${1}"
    local length="${2}"
    local delimiter="${3}"
    local delimiterLength="${#delimiter}"

    echo "${subject}" | sed "${SED_EXTENDED_REGEX_PARAMETER}" "s@(([^/]{$((length))})([^/]{$delimiterLength}))[^/]+/@\2$delimiter/@g"
}

