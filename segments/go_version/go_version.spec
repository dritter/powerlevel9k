#!/usr/bin/env zsh
#vim:ft=zsh ts=2 sw=2 sts=2 et fenc=utf-8

# Required for shunit2 to run correctly
setopt shwordsplit
SHUNIT_PARENT=$0

function setUp() {
  export TERM="xterm-256color"
  local -a P9K_RIGHT_PROMPT_ELEMENTS
  P9K_RIGHT_PROMPT_ELEMENTS=()
  # Load Powerlevel9k
  source powerlevel9k.zsh-theme
  source segments/go_version/go_version.p9k
}

function mockGo() {
  case "$1" in
  'version')
    echo 'go version go1.5.3 darwin/amd64'
    ;;
  'env')
    echo "$HOME/go"
    ;;
  esac
}

function mockGoEmptyGopath() {
  case "$1" in
  'version')
    echo 'go version go1.5.3 darwin/amd64'
    ;;
  'env')
    echo ""
    ;;
  esac
}

function testGo() {
  alias go=mockGo
  P9K_GO_ICON=""
  local -a P9K_LEFT_PROMPT_ELEMENTS
  P9K_LEFT_PROMPT_ELEMENTS=(go_version)

  PWD="$HOME/go/src/github.com/bhilburn/powerlevel9k"

  __p9k_build_left_prompt
  assertEquals "%K{002} %F{255}Go %F{255}\${(Q)\${:-\"go1.5.3\"}} %k%F{002}%f " "${__P9K_RETVAL}"

  unset P9K_GO_ICON
  unset PWD
  unset P9K_LEFT_PROMPT_ELEMENTS
  unalias go
}

function testGoSegmentPrintsNothingIfEmptyGopath() {
  alias go=mockGoEmptyGopath
  P9K_CUSTOM_WORLD='echo world'
  local -a P9K_LEFT_PROMPT_ELEMENTS
  P9K_LEFT_PROMPT_ELEMENTS=(custom_world go_version)

  __p9k_build_left_prompt
  assertEquals "%K{015} %F{000}\${(Q)\${:-\"world\"}} %k%F{015}%f " "${__P9K_RETVAL}"

  unset P9K_LEFT_PROMPT_ELEMENTS
  unset P9K_CUSTOM_WORLD

}

function testGoSegmentPrintsNothingIfNotInGopath() {
  alias go=mockGo
  P9K_CUSTOM_WORLD='echo world'
  local -a P9K_LEFT_PROMPT_ELEMENTS
  P9K_LEFT_PROMPT_ELEMENTS=(custom_world go_version)

  __p9k_build_left_prompt
  assertEquals "%K{015} %F{000}\${(Q)\${:-\"world\"}} %k%F{015}%f " "${__P9K_RETVAL}"

  unset P9K_LEFT_PROMPT_ELEMENTS
  unset P9K_CUSTOM_WORLD
}

function testGoSegmentPrintsNothingIfGoIsNotAvailable() {
  alias go=noGo
  P9K_CUSTOM_WORLD='echo world'
  local -a P9K_LEFT_PROMPT_ELEMENTS
  P9K_LEFT_PROMPT_ELEMENTS=(custom_world go_version)

  __p9k_build_left_prompt
  assertEquals "%K{015} %F{000}\${(Q)\${:-\"world\"}} %k%F{015}%f " "${__P9K_RETVAL}"

  unset P9K_LEFT_PROMPT_ELEMENTS
  unset P9K_CUSTOM_WORLD
  unalias go
}

source shunit2/shunit2
