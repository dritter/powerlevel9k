#!/usr/bin/env zsh
#vim:ft=zsh ts=2 sw=2 sts=2 et fenc=utf-8

# Required for shunit2 to run correctly
setopt shwordsplit
SHUNIT_PARENT=$0

function setUp() {
  # Load Powerlevel9k
  source functions/icons.zsh
  source functions/utilities.zsh
  source functions/truncation.zsh

  OLDHOME=$HOME
}

function tearDown() {
    # Reset home folder
    HOME=$OLDHOME
}

function testTruncateHomeWorks() {
    export HOME="/home/dritter"
    assertEquals "~/test" "$(_p9k_truncateHome "/home/dritter/test" "~")"
}

function testTruncateHomeWithChangedDelimiterWorks() {
    export HOME="/home/dritter"
    assertEquals "*/test" "$(_p9k_truncateHome "/home/dritter/test" "*")"
}

function testTruncateHomeWithWhitespaceInPathWorks() {
    export HOME="/home/drit ter"
    assertEquals "~/test" "$(_p9k_truncateHome "/home/drit ter/test" "~")"
}

function testTruncateMiddleWorks() {
    export HOME="/home/dritter"
    assertEquals "/home/dr…er/test" "$(_p9k_truncateMiddle "/home/dritter/test" "2" "…")"
}

function testTruncateMiddleWithChangedDelimiterWorks() {
    export HOME="/home/dritter"
    assertEquals "/home/dr**er/test" "$(_p9k_truncateMiddle "/home/dritter/test" "2" "**")"
}

function testTruncateMiddleWithWhitespaceInPathWorks() {
    export HOME="/home/drit ter"
    assertEquals "/home/dr…er/test" "$(_p9k_truncateMiddle "/home/drit ter/test" "2" "…")"
}

function testTruncateRightWorks() {
    export HOME="/home/dritter"
    assertEquals "/ho…/dr…/test" "$(_p9k_truncateRight "/home/dritter/test" "2" "…")"
}

function testTruncateRightWithChangedDelimiterWorks() {
    export HOME="/home/dritter"
    assertEquals "/home/dr**/test" "$(_p9k_truncateRight "/home/dritter/test" "2" "**")"
}

function testTruncateRightWithWhitespaceInPathWorks() {
    export HOME="/home/drit ter"
    assertEquals "/ho…/dr…/test" "$(_p9k_truncateRight "/home/drit ter/test" "2" "…")"
}

source shunit2/source/2.1/src/shunit2