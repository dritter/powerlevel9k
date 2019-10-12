#!/usr/bin/env zsh
#vim:ft=zsh ts=2 sw=2 sts=2 et fenc=utf-8

# Required for shunit2 to run correctly
setopt shwordsplit
SHUNIT_PARENT=$0

function setUp() {
  emulate -L zsh
  export TERM="xterm-256color"
  local -a P9K_RIGHT_PROMPT_ELEMENTS
  P9K_RIGHT_PROMPT_ELEMENTS=()
  # Load Powerlevel9k
  source powerlevel9k.zsh-theme
}

function tearDown() {
  # __P9K-vars (e.g. __P9K_DATA) have to be unset manually since they are set globally
  # and leak to other tests
  unset -m '__P9K_*' || true
}

# Regular Segment
function testNoBoldOnregularSegment(){
  local P9K_LEFT_PROMPT_ELEMENTS=(date)
  local P9K_RIGHT_PROMPT_ELEMENTS=(date)
  local P9K_DATE_ICON="date-icon"
  source segments/date/date.p9k
  
  __p9k_build_left_prompt
  assertEquals "%K{015} %F{000}date-icon %F{000}\${(Q)\${:-\"%D{%d.%m.%y}\"}} %k%F{015}%f " "${__P9K_RETVAL}"
  __p9k_build_right_prompt
  assertEquals "%F{015}%K{015}%F{000} \${(Q)\${:-\"%D{%d.%m.%y}\"}} %F{000}date-icon%f %E%f%k%b" "${__P9K_RETVAL}"
}

function testBoldOnRegularSegments() {
  local P9K_LEFT_PROMPT_ELEMENTS=(date)
  local P9K_RIGHT_PROMPT_ELEMENTS=(date)
  local P9K_DATE_ICON="date-icon"
  local P9K_DATE_BOLD=true
  source segments/date/date.p9k

  __p9k_build_left_prompt
  assertEquals "%K{015} %F{000}date-icon %F{000}\${(Q)\${:-\"%B%D{%d.%m.%y}%b\"}} %k%F{015}%f " "${__P9K_RETVAL}"
  __p9k_build_right_prompt
  assertEquals "%F{015}%K{015}%F{000} \${(Q)\${:-\"%B%D{%d.%m.%y}%b\"}} %F{000}date-icon%f %E%f%k%b" "${__P9K_RETVAL}"
}

function testBoldOnRegularSegmentVisualIdentifiers() {
  local P9K_LEFT_PROMPT_ELEMENTS=(date)
  local P9K_RIGHT_PROMPT_ELEMENTS=(date)
  local P9K_DATE_ICON="date-icon"
  local P9K_DATE_ICON_BOLD=true
  source segments/date/date.p9k

  __p9k_build_left_prompt
  assertEquals "%K{015} %F{000}%Bdate-icon%b %F{000}\${(Q)\${:-\"%D{%d.%m.%y}\"}} %k%F{015}%f " "${__P9K_RETVAL}"
  __p9k_build_right_prompt
  assertEquals "%F{015}%K{015}%F{000} \${(Q)\${:-\"%D{%d.%m.%y}\"}} %F{000}%Bdate-icon%b%f %E%f%k%b" "${__P9K_RETVAL}"
}

# Stateful Segment
function testNotBoldOnStatefulSegment() {
  local P9K_LEFT_PROMPT_ELEMENTS=(host)
  local P9K_RIGHT_PROMPT_ELEMENTS=(host)
  local P9K_HOST_REMOTE_ICON="ssh-icon"
  # Provoke state
  local SSH_CLIENT="x"
  source segments/host/host.p9k

  __p9k_build_left_prompt
  assertEquals "%K{003} %F{000}ssh-icon %F{000}\${(Q)\${:-\"%m\"}} %k%F{003}%f " "${__P9K_RETVAL}"
  __p9k_build_right_prompt
  assertEquals "%F{003}%K{003}%F{000} \${(Q)\${:-\"%m\"}} %F{000}ssh-icon%f %E%f%k%b" "${__P9K_RETVAL}"
}

function testBoldOnStatefulSegment() {
  local P9K_LEFT_PROMPT_ELEMENTS=(host)
  local P9K_RIGHT_PROMPT_ELEMENTS=(host)
  local P9K_HOST_REMOTE_ICON="ssh-icon"
  local P9K_HOST_REMOTE_BOLD=true
  # Provoke state
  local SSH_CLIENT="x"
  source segments/host/host.p9k

  __p9k_build_left_prompt
  assertEquals "%K{003} %F{000}ssh-icon %F{000}\${(Q)\${:-\"%B%m%b\"}} %k%F{003}%f " "${__P9K_RETVAL}"
  __p9k_build_right_prompt
  assertEquals "%F{003}%K{003}%F{000} \${(Q)\${:-\"%B%m%b\"}} %F{000}ssh-icon%f %E%f%k%b" "${__P9K_RETVAL}"
}

function testBoldOnStatefulVisualIdentifiers() {
  local P9K_LEFT_PROMPT_ELEMENTS=(host)
  local P9K_RIGHT_PROMPT_ELEMENTS=(host)
  local P9K_HOST_REMOTE_ICON="ssh-icon"
  local P9K_HOST_REMOTE_ICON_BOLD=true
  # Provoke state
  local SSH_CLIENT="x"
  source segments/host/host.p9k

  __p9k_build_left_prompt
  assertEquals "%K{003} %F{000}%Bssh-icon%b %F{000}\${(Q)\${:-\"%m\"}} %k%F{003}%f " "${__P9K_RETVAL}"
  __p9k_build_right_prompt
  assertEquals "%F{003}%K{003}%F{000} \${(Q)\${:-\"%m\"}} %F{000}%Bssh-icon%b%f %E%f%k%b" "${__P9K_RETVAL}"
}

# Custom Segment
function testNotBoldOnCustomSegment() {
  local P9K_LEFT_PROMPT_ELEMENTS=(custom_world)
  local P9K_RIGHT_PROMPT_ELEMENTS=(custom_world)
  local P9K_CUSTOM_WORLD='echo world'
  local P9K_CUSTOM_WORLD_ICON='CW'

  __p9k_build_left_prompt
  assertEquals "%K{015} %F{000}CW %F{000}\${(Q)\${:-\"world\"}} %k%F{015}%f " "${__P9K_RETVAL}"
  __p9k_build_right_prompt
  assertEquals "%F{015}%K{015}%F{000} \${(Q)\${:-\"world\"}} %F{000}CW%f %E%f%k%b" "${__P9K_RETVAL}"
}

function testBoldOnCustomSegment() {
  local P9K_LEFT_PROMPT_ELEMENTS=(custom_world)
  local P9K_RIGHT_PROMPT_ELEMENTS=(custom_world)
  local P9K_CUSTOM_WORLD='echo world'
  local P9K_CUSTOM_WORLD_ICON='CW'
  local P9K_CUSTOM_WORLD_BOLD=true

  __p9k_build_left_prompt
  assertEquals "%K{015} %F{000}CW %F{000}\${(Q)\${:-\"%Bworld%b\"}} %k%F{015}%f " "${__P9K_RETVAL}"
  __p9k_build_right_prompt
  assertEquals "%F{015}%K{015}%F{000} \${(Q)\${:-\"%Bworld%b\"}} %F{000}CW%f %E%f%k%b" "${__P9K_RETVAL}"
}

function testBoldOnCustomSegmentVisualIdentifiers() {
  local P9K_LEFT_PROMPT_ELEMENTS=(custom_world)
  local P9K_RIGHT_PROMPT_ELEMENTS=(custom_world)
  local P9K_CUSTOM_WORLD='echo world'
  local P9K_CUSTOM_WORLD_ICON='CW'
  local P9K_CUSTOM_WORLD_ICON_BOLD=true

  __p9k_build_left_prompt
  assertEquals "%K{015} %F{000}%BCW%b %F{000}\${(Q)\${:-\"world\"}} %k%F{015}%f " "${__P9K_RETVAL}"
  __p9k_build_right_prompt
  assertEquals "%F{015}%K{015}%F{000} \${(Q)\${:-\"world\"}} %F{000}%BCW%b%f %E%f%k%b" "${__P9K_RETVAL}"
}

source shunit2/shunit2
