#!/usr/bin/env zsh
#vim:ft=zsh ts=2 sw=2 sts=2 et fenc=utf-8

# Required for shunit2 to run correctly
setopt shwordsplit
SHUNIT_PARENT=$0

function setUp() {
  export TERM="xterm-256color"
  source powerlevel9k.zsh-theme
}

function testAnacondaSegmentPrintsNothingIfNoAnacondaPathIsSet() {
  local P9K_CUSTOM_WORLD='echo world'
  local -a P9K_LEFT_PROMPT_ELEMENTS
  P9K_LEFT_PROMPT_ELEMENTS=(anaconda custom_world)
  local -a P9K_RIGHT_PROMPT_ELEMENTS
  P9K_RIGHT_PROMPT_ELEMENTS=()

  # Load Powerlevel9k
  source segments/anaconda/anaconda.p9k

  # Unset anacona variables
  unset CONDA_ENV_PATH
  unset CONDA_PREFIX

  __p9k_build_left_prompt
  assertEquals "%K{015} %F{000}\${(Q)\${:-\"world\"}} %k%F{015}%f " "${__P9K_RETVAL}"
}

function testAnacondaSegmentWorksIfOnlyAnacondaPathIsSet() {
  local -a P9K_LEFT_PROMPT_ELEMENTS
  P9K_LEFT_PROMPT_ELEMENTS=(anaconda)
  local P9K_ANACONDA_ICON="icon-here"

  # Load Powerlevel9k
  source segments/anaconda/anaconda.p9k

  CONDA_ENV_PATH=/tmp
  unset CONDA_PREFIX

  __p9k_build_left_prompt
  assertEquals "%K{004} %F{000}icon-here %F{000}\${(Q)\${:-\"(tmp)\"}} %k%F{004}%f " "${__P9K_RETVAL}"
}

function testAnacondaSegmentWorksIfOnlyAnacondaPrefixIsSet() {
  local -a P9K_LEFT_PROMPT_ELEMENTS
  P9K_LEFT_PROMPT_ELEMENTS=(anaconda)
  local P9K_ANACONDA_ICON="icon-here"

  # Load Powerlevel9k
  source segments/anaconda/anaconda.p9k

  unset CONDA_ENV_PATH
  local CONDA_PREFIX="test"

  __p9k_build_left_prompt
  assertEquals "%K{004} %F{000}icon-here %F{000}\${(Q)\${:-\"(test)\"}} %k%F{004}%f " "${__P9K_RETVAL}"
}

function testAnacondaSegmentWorks() {
  local -a P9K_LEFT_PROMPT_ELEMENTS
  P9K_LEFT_PROMPT_ELEMENTS=(anaconda)
  local P9K_ANACONDA_ICON="icon-here"

  # Load Powerlevel9k
  source segments/anaconda/anaconda.p9k

  local CONDA_ENV_PATH=/tmp
  local CONDA_PREFIX="test"

  __p9k_build_left_prompt
  assertEquals "%K{004} %F{000}icon-here %F{000}\${(Q)\${:-\"(tmptest)\"}} %k%F{004}%f " "${__P9K_RETVAL}"
}

function testAnacondaDoesNotLeadTermcapChars() {
  local -a P9K_LEFT_PROMPT_ELEMENTS
  P9K_LEFT_PROMPT_ELEMENTS=(anaconda)
  local P9K_ANACONDA_ICON="icon-here"

  # Load Powerlevel9k
  source segments/anaconda/anaconda.p9k

  local CONDA_ENV_PATH=/tmp
  local CONDA_PREFIX="\r\n%K{blue}leaking%F{red}string"

  __p9k_build_left_prompt
  assertEquals "%K{004} %F{000}icon-here %F{000}\${(Q)\${:-\"(tmp\\\r\\\n%%K{blue}leaking%%F{red}string)\"}} %k%F{004}%f " "${__P9K_RETVAL}"
}

source shunit2/shunit2
