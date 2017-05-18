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

    typeset -Ah truncationResult
    truncationResult=("${(@s.;.)$(_p9k_truncateHome "/home/dritter/test" "~")}")

    assertEquals "~/test" "${truncationResult[truncated]}${truncationResult[remainder]}"
}

function testTruncateHomeWithChangedSubstituteWorks() {
    export HOME="/home/dritter"

    typeset -Ah truncationResult
    truncationResult=("${(@s.;.)$(_p9k_truncateHome "/home/dritter/test" "*")}")

    assertEquals "*/test" "${truncationResult[truncated]}${truncationResult[remainder]}"
}

function testTruncateHomeWithWhitespaceInPathWorks() {
    export HOME="/home/drit ter"

    typeset -Ah truncationResult
    truncationResult=("${(@s.;.)$(_p9k_truncateHome "/home/drit ter/test" "~")}")

    assertEquals "~/test" "${truncationResult[truncated]}${truncationResult[remainder]}"
}

function testTruncateMiddleWorks() {
    export HOME="/home/dritter"

    typeset -Ah truncationResult
    truncationResult=("${(@s.;.)$(_p9k_truncateMiddle "/home/dritter/test" "2" "…")}")

    assertEquals "/home/dr…er/test" "${truncationResult[truncated]}"
    assertFalse "${truncationResult[remainder]}"
}

function testTruncateMiddleWithChangedSubstituteWorks() {
    export HOME="/home/dritter"

    typeset -Ah truncationResult
    truncationResult=("${(@s.;.)$(_p9k_truncateMiddle "/home/dritter/test" "2" "**")}")

    assertEquals "/home/dr**er/test" "${truncationResult[truncated]}"
    assertFalse "${truncationResult[remainder]}"
}

function testTruncateMiddleWithWhitespaceInPathWorks() {
    export HOME="/home/drit ter"

    typeset -Ah truncationResult
    truncationResult=("${(@s.;.)$(_p9k_truncateMiddle "/home/drit ter/test" "2" "…")}")

    assertEquals "/home/dr…er/test" "${truncationResult[truncated]}"
    assertFalse "${truncationResult[remainder]}"
}

function testTruncateRightWorks() {
    export HOME="/home/dritter"

    typeset -Ah truncationResult
    truncationResult=("${(@s.;.)$(_p9k_truncateRight "/home/dritter/test" "2" "…")}")

    assertEquals "/ho…/dr…/test" "${truncationResult[truncated]}"
    assertFalse "${truncationResult[remainder]}"
}

function testTruncateRightWithChangedSubstituteWorks() {
    export HOME="/home/dritter"

    typeset -Ah truncationResult
    truncationResult=("${(@s.;.)$(_p9k_truncateRight "/home/dritter/test" "2" "**")}")

    assertEquals "/home/dr**/test" "${truncationResult[truncated]}"
    assertFalse "${truncationResult[remainder]}"
}

function testTruncateRightWithWhitespaceInPathWorks() {
    export HOME="/home/drit ter"

    typeset -Ah truncationResult
    truncationResult=("${(@s.;.)$(_p9k_truncateRight "/home/drit ter/test" "2" "…")}")

    assertEquals "/ho…/dr…/test" "${truncationResult[truncated]}"
    assertFalse "${truncationResult[remainder]}"
}

function testTruncateWithPackageNameWorks() {
  local p9kFolder=$(pwd)
  local BASEFOLDER=/tmp/powerlevel9k-test
  local FOLDER=$BASEFOLDER/1/12/123/1234/12345/123456/1234567/12345678/123456789
  mkdir -p $FOLDER

  cd /tmp/powerlevel9k-test
  echo '
{
  "name": "My_Package"
}
' > package.json
  # Unfortunately: The main folder must be a git repo..
  git init &>/dev/null

  # Go back to deeper folder
  cd "${FOLDER}"

  typeset -Ah truncationResult
  truncationResult=("${(@s.;.)$(_p9k_truncatePackage "${FOLDER}" "2" "…")}")

  assertEquals "My_Package" "${truncationResult[truncated]}"
  assertEquals "/1/12/123/1234/12345/123456/1234567/12345678/123456789" "${truncationResult[remainder]}"

  # Go back
  cd $p9kFolder
  rm -fr $BASEFOLDER
}

function testTruncateWithPackageNameIfRepoIsSymlinkedInsideDeepFolder() {
  local p9kFolder=$(pwd)
  local BASEFOLDER=/tmp/powerlevel9k-test
  local FOLDER=$BASEFOLDER/1/12/123/1234/12345/123456/1234567/12345678/123456789
  mkdir -p $FOLDER
  cd "${FOLDER}"

  # Unfortunately: The main folder must be a git repo..
  git init &>/dev/null

  echo '
{
  "name": "My_Package"
}
' > package.json

  # Create a subdir inside the repo
  mkdir -p asdfasdf/qwerqwer

  cd $BASEFOLDER
  ln -s ${FOLDER} linked-repo

  # Go to deep folder inside linked repo
  local DEEP_LINKED_FOLDER="${BASEFOLDER}/linked-repo/asdfasdf/qwerqwer"
  cd "${DEEP_LINKED_FOLDER}"

  typeset -Ah truncationResult
  truncationResult=("${(@s.;.)$(_p9k_truncatePackage "${DEEP_LINKED_FOLDER}" "2" "…")}")

  assertEquals "My_Package" "${truncationResult[truncated]}"
  assertEquals "/asdfasdf/qwerqwer" "${truncationResult[remainder]}"

  # Go back
  cd $p9kFolder
  rm -fr $BASEFOLDER
}

function testTruncateWithPackageNameIfRepoIsSymlinkedInsideGitDir() {
  local p9kFolder=$(pwd)
  local BASEFOLDER=/tmp/powerlevel9k-test
  local FOLDER=$BASEFOLDER/1/12/123/1234/12345/123456/1234567/12345678/123456789
  mkdir -p $FOLDER
  cd $FOLDER

  # Unfortunately: The main folder must be a git repo..
  git init &>/dev/null

  echo '
{
  "name": "My_Package"
}
' > package.json

  cd "${BASEFOLDER}"
  ln -s ${FOLDER} linked-repo

  local LINKED_GIT_FOLDER="${BASEFOLDER}/linked-repo/.git/refs/heads"
  cd "${LINKED_GIT_FOLDER}"

  typeset -Ah truncationResult
  truncationResult=("${(@s.;.)$(_p9k_truncatePackage "${LINKED_GIT_FOLDER}" "2" "…")}")

  assertEquals "My_Package" "${truncationResult[truncated]}"
  assertEquals "/.git/refs/heads" "${truncationResult[remainder]}"

  # Go back
  cd $p9kFolder
  rm -fr $BASEFOLDER
}

source shunit2/source/2.1/src/shunit2