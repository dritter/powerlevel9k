#!/usr/bin/env zsh
#vim:ft=zsh ts=2 sw=2 sts=2 et fenc=utf-8

# Required for shunit2 to run correctly
setopt shwordsplit
SHUNIT_PARENT=$0

function setUp() {
  # Load Powerlevel9k
  source functions/icons.zsh
  source functions/utilities.zsh
}

function testDefinedFindsDefinedVariable() {
  my_var='X'

  assertTrue "defined 'my_var'"
  unset my_var
}

function testDefinedDoesNotFindUndefinedVariable() {
  assertFalse "defined 'my_var'"
}

function testSetDefaultSetsVariable() {
  set_default 'my_var' 'x'

  assertEquals 'x' "$my_var"
  unset my_var
}

function testPrintSizeHumanReadableWithBigNumber() {
  # Interesting: Currently we can't support numbers bigger than that.
  assertEquals '0.87E' "$(printSizeHumanReadable 1000000000000000000)"
}

function testPrintSizeHumanReadableWithExabytesAsBase() {
  assertEquals '9.77Z' "$(printSizeHumanReadable 10000 'E')"
}

function testGetRelevantItem() {
  typeset -a list
  list=(a b c)
  local callback='[[ "$item" == "b" ]] && echo "found"'

  local result=$(getRelevantItem "$list" "$callback")
  assertEquals 'found' "$result"

  unset list
}

function testGetRelevantItemDoesNotReturnNotFoundItems() {
  typeset -a list
  list=(a b c)
  local callback='[[ "$item" == "d" ]] && echo "found"'

  local result=$(getRelevantItem "$list" "$callback")
  assertEquals '' ''

  unset list
}

function testSegmentShouldBeJoinedIfDirectPredecessingSegmentIsJoined() {
  typeset -a segments
  segments=(a b_joined c_joined)
  # Look at the third segment
  local current_index=3
  local last_element_index=2

  local joined
  segmentShouldBeJoined $current_index $last_element_index "$segments" && joined=true || joined=false
  assertTrue "$joined"

  unset segments
}

function testSegmentShouldBeJoinedIfPredecessingSegmentIsJoinedTransitivley() {
  typeset -a segments
  segments=(a b_joined c_joined)
  # Look at the third segment
  local current_index=3
  # The last printed segment was the first one,
  # the second segmend was conditional.
  local last_element_index=1

  local joined
  segmentShouldBeJoined $current_index $last_element_index "$segments" && joined=true || joined=false
  assertTrue "$joined"

  unset segments
}

function testSegmentShouldNotBeJoinedIfPredecessingSegmentIsNotJoinedButConditional() {
  typeset -a segments
  segments=(a b_joined c d_joined)
  # Look at the fourth segment
  local current_index=4
  # The last printed segment was the first one,
  # the second segmend was conditional.
  local last_element_index=1

  local joined
  segmentShouldBeJoined $current_index $last_element_index "$segments" && joined=true || joined=false
  assertFalse "$joined"

  unset segments
}

function testUpsearchFindsFileInCurrentFolder() {
  local OLD_PWD="${PWD}"
  local BASEFOLDER="/tmp/powerlevel9k-test"
  local PARENTFOLDER="${BASEFOLDER}/1/12/123"
  local FOLDER="${PARENTFOLDER}/1234"
  mkdir -p "${FOLDER}"
  cd "${FOLDER}"

  local STOPFILE=".p9k_test_stopfile"
  touch "${FOLDER}/${STOPFILE}"

  assertEquals "${FOLDER}" "$(upsearch "${STOPFILE}")"

  cd "${OLD_PWD}"
  rm -fr "${BASEFOLDER}"
  PWD="${OLD_PWD}"
}

function testUpsearchFindsFileInParentFolder() {
  local OLD_PWD="${PWD}"
  local BASEFOLDER="/tmp/powerlevel9k-test"
  local GRANDPARENTFOLDER="${BASEFOLDER}/1/12"
  local PARENTFOLDER="${GRANDPARENTFOLDER}/123"
  local FOLDER="${PARENTFOLDER}/1234"
  mkdir -p "${FOLDER}"
  cd "${FOLDER}"

  local STOPFILE=".p9k_test_stopfile"
  touch "${PARENTFOLDER}/${STOPFILE}"

  assertEquals "${PARENTFOLDER}" "$(upsearch "${STOPFILE}")"

  cd "${OLD_PWD}"
  rm -fr "${BASEFOLDER}"
  PWD="${OLD_PWD}"
}

# This test originally should test if it is possible to
# find a file in the root folder. Unfortunately it is
# not possible for normal users to create a file in the
# root folder. So we just test if upsearch finds a file
# far up the directory tree..
function testUpsearchFindsFileInTmpFolder() {
  local OLD_PWD="${PWD}"
  local BASEFOLDER="/tmp/powerlevel9k-test"
  local FOLDER="${BASEFOLDER}/1/12/123/1234"
  mkdir -p "${FOLDER}"
  cd "${FOLDER}"

  local STOPFILE=".p9k_test_stopfile"
  local STOPFILE_PATH="/tmp"
  touch "${STOPFILE_PATH}/${STOPFILE}"

  assertEquals "/tmp" "$(upsearch "${STOPFILE}")"

  cd "${OLD_PWD}"
  rm -fr "${BASEFOLDER}"
  rm -f "${STOPFILE_PATH}/${STOPFILE}"
  PWD="${OLD_PWD}"
}

function testUpsearchFindsFileInHomeFolder() {
  local OLD_PWD="${PWD}"
  local BASEFOLDER="${HOME}/.powerlevel9k-test"
  local FOLDER="${BASEFOLDER}/1/12/123/1234"
  mkdir -p "${FOLDER}"
  cd "${FOLDER}"

  local STOPFILE=".p9k_test_stopfile"
  local STOPFILE_PATH="${BASEFOLDER}"
  touch "${STOPFILE_PATH}/${STOPFILE}"

  assertEquals "${BASEFOLDER}" "$(upsearch "${STOPFILE}")"

  cd "${OLD_PWD}"
  rm -fr "${BASEFOLDER}"
  rm -f "${STOPFILE_PATH}/${STOPFILE}"
  PWD="${OLD_PWD}"
}

source shunit2/source/2.1/src/shunit2
