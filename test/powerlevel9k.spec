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
  source functions/*
  source segments/dir/dir.p9k

  # Unset mode, so that user settings
  # do not interfere with tests
}

function oneTimeSetUp() {
  function stripEsc() {
    local clean_string="" escape_found=false
    for (( i = 1; i <= ${#1}; i++ )); do
      case ${1[i]}; in
        "")  clean_string+="<Esc>"; escape_found=true ;; # escape character
        "[")  if [[ ${escape_found} == true ]]; then
              escape_found=false
            else
              clean_string+="${1[i]}"
            fi
            ;;
        *)    clean_string+="${1[i]}" ;;
      esac
    done
    echo "${clean_string}"
  }
}

function oneTimeTearDown() {
  unfunction stripEsc
}

function testUsingUnsetVariables() {
  local P9K_CUSTOM_WORLD='echo world'
  local -a P9K_LEFT_PROMPT_ELEMENTS
  local P9K_LEFT_PROMPT_ELEMENTS=(custom_world)
  local -a P9K_RIGHT_PROMPT_ELEMENTS
  local P9K_RIGHT_PROMPT_ELEMENTS=()

  setopt local_options
  set -u
  local result="$(__p9k_prepare_prompts 2>&1)"

  assertEquals "" "${result}"
}

function testJoinedSegments() {
  local -a P9K_LEFT_PROMPT_ELEMENTS
  local P9K_LEFT_PROMPT_ELEMENTS=(dir dir_joined)
  cd /tmp

  __p9k_build_left_prompt
  assertEquals "%K{004} %F{000}\${:-\"/tmp\"} %F{000}\${:-\"/tmp\"} %k%F{004}%f " "${__P9K_RETVAL}"

  cd -
}

function testTransitiveJoinedSegments() {
  local -a P9K_LEFT_PROMPT_ELEMENTS
  local P9K_LEFT_PROMPT_ELEMENTS=(dir root_indicator_joined dir_joined)
  source segments/root_indicator/root_indicator.p9k
  cd /tmp

  __p9k_build_left_prompt
  assertEquals "%K{004} %F{000}\${:-\"/tmp\"} %F{000}\${:-\"/tmp\"} %k%F{004}%f " "${__P9K_RETVAL}"

  cd -
}

function testJoiningWithConditionalSegment() {
  local -a P9K_LEFT_PROMPT_ELEMENTS
  local P9K_LEFT_PROMPT_ELEMENTS=(dir background_jobs dir_joined)
  source segments/background_jobs/background_jobs.p9k
  local jobs_running=0
  local jobs_suspended=0

  cd /tmp

  __p9k_build_left_prompt
  assertEquals "%K{004} %F{000}\${:-\"/tmp\"}  %F{000}\${:-\"/tmp\"} %k%F{004}%f " "${__P9K_RETVAL}"

  cd -
}

function testDynamicColoringOfSegmentsWork() {
  local -a P9K_LEFT_PROMPT_ELEMENTS
  local P9K_LEFT_PROMPT_ELEMENTS=(dir)
  local P9K_DIR_DEFAULT_BACKGROUND='red'
  source segments/dir/dir.p9k

  cd /tmp

  __p9k_build_left_prompt
  assertEquals "%K{001} %F{000}\${:-\"/tmp\"} %k%F{001}%f " "${__P9K_RETVAL}"

  cd -
}

function testDynamicColoringOfVisualIdentifiersWork() {
  local -a P9K_LEFT_PROMPT_ELEMENTS
  local P9K_LEFT_PROMPT_ELEMENTS=(dir)
  local P9K_DIR_DEFAULT_ICON_COLOR='green'
  local P9K_DIR_DEFAULT_ICON="icon-here"
  source segments/dir/dir.p9k

  cd /tmp

  __p9k_build_left_prompt
  assertEquals "%K{004} %F{002}icon-here %F{000}\${:-\"/tmp\"} %k%F{004}%f " "${__P9K_RETVAL}"

  cd -
}

function testColoringOfVisualIdentifiersDoesNotOverwriteColoringOfSegment() {
  local -a P9K_LEFT_PROMPT_ELEMENTS
  local P9K_LEFT_PROMPT_ELEMENTS=(dir)
  local P9K_DIR_DEFAULT_ICON_COLOR='green'
  local P9K_DIR_DEFAULT_FOREGROUND='red'
  local P9K_DIR_DEFAULT_BACKGROUND='yellow'
  local P9K_DIR_DEFAULT_ICON="icon-here"
  source segments/dir/dir.p9k

  # Re-Source the icons, as the P9K_MODE is directly
  # evaluated there.
  source functions/icons.zsh

  cd /tmp

  __p9k_build_left_prompt
  assertEquals "%K{003} %F{002}icon-here %F{001}\${:-\"/tmp\"} %k%F{003}%f " "${__P9K_RETVAL}"

  cd -
}

function testOverwritingIconsWork() {
  local -a P9K_LEFT_PROMPT_ELEMENTS
  local P9K_LEFT_PROMPT_ELEMENTS=(dir)
  local P9K_DIR_DEFAULT_ICON='icon-here'
  source segments/dir/dir.p9k
  #local testFolder=$(mktemp -d -p p9k)
  # Move testFolder under home folder
  #mv testFolder ~
  # Go into testFolder
  #cd ~/$testFolder

  cd /tmp
    __p9k_build_left_prompt
  assertEquals "%K{004} %F{000}icon-here %F{000}\${:-\"/tmp\"} %k%F{004}%f " "${__P9K_RETVAL}"

  cd -
  # rm -fr ~/$testFolder
}

function testNewlineOnRpromptCanBeDisabled() {
  # Fake environment
  local COLUMNS=100

  local P9K_PROMPT_ON_NEWLINE=true
  local P9K_RPROMPT_ON_NEWLINE=false
  local P9K_CUSTOM_WORLD='echo world'
  local P9K_CUSTOM_RWORLD='echo rworld'
  local -a P9K_LEFT_PROMPT_ELEMENTS
  local P9K_LEFT_PROMPT_ELEMENTS=(custom_world)
  local -a P9K_RIGHT_PROMPT_ELEMENTS
  local P9K_RIGHT_PROMPT_ELEMENTS=(custom_rworld)

  __p9k_prepare_prompts

  local nl=$'\n'
  local expected='%f%b%k╭─%K{015} %F{000}${:-"world"} %k%F{015}%f ${(pl.79.. .)}${__P9K_RPROMPT}
╰─ %f%b%k'
  local _real=$(stripEsc "${PROMPT}${RPROMPT}")

  # use this to debug output with special escape sequences
  # new lines for escape codes that move output one line above
  # set -vx;
  # echo "\n__1__\n"
  # echo "\n__${expected}__\n"
  # echo "\n__2__\n"
  # echo "\n__${_real}__\n"
  # echo "\n__3__\n"
  # set +vx;

  assertEquals "${expected}" "${_real}"
}

source shunit2/shunit2
