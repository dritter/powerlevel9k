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
}

function testViInsertModeWorks() {
  local KEYMAP='viins'

  # Load Powerlevel9k
  source segments/vi_mode/vi_mode.p9k

  prompt_vi_mode left 1 false
  assertEquals "%K{000} %F{004}\${(Q)\${:-\"INSERT\"}} " "${__P9K_RETVAL}"
}

function testViInsertModeWorksWhenLabeledAsMain() {
  local KEYMAP='main'

  # Load Powerlevel9k
  source segments/vi_mode/vi_mode.p9k

  prompt_vi_mode left 1 false
  assertEquals "%K{000} %F{004}\${(Q)\${:-\"INSERT\"}} " "${__P9K_RETVAL}"
}

function testViCommandModeWorks() {
  local KEYMAP='vicmd'

  # Load Powerlevel9k
  source segments/vi_mode/vi_mode.p9k

  prompt_vi_mode left 1 false
  assertEquals "%K{000} %F{015}\${(Q)\${:-\"NORMAL\"}} " "${__P9K_RETVAL}"
}

function testViInsertModeStringIsCustomizable() {
  local KEYMAP='viins'

  # Load Powerlevel9k
  source segments/vi_mode/vi_mode.p9k

  prompt_vi_mode left 1 false
  assertEquals "%K{000} %F{004}\${(Q)\${:-\"INSERT\"}} " "${__P9K_RETVAL}"
}

source shunit2/shunit2
