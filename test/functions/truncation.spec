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

function testTruncateHomeWithChangedSubstituteWorks() {
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

function testTruncateMiddleWithChangedSubstituteWorks() {
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

function testTruncateRightWithChangedSubstituteWorks() {
    export HOME="/home/dritter"
    assertEquals "/home/dr**/test" "$(_p9k_truncateRight "/home/dritter/test" "2" "**")"
}

function testTruncateRightWithWhitespaceInPathWorks() {
    export HOME="/home/drit ter"
    assertEquals "/ho…/dr…/test" "$(_p9k_truncateRight "/home/drit ter/test" "2" "…")"
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

  assertEquals "My_Package/1/12/123/12…/12…/12…/12…/12…/123456789" "$(_p9k_truncatePackage "${FOLDER}" "2" "…")"

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

  assertEquals "My_Package/as…/qwerqwer" "$(_p9k_truncatePackage "${DEEP_LINKED_FOLDER}" "2" "…")"

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

  assertEquals "My_Package/.g…/re…/heads" "$(_p9k_truncatePackage "${LINKED_GIT_FOLDER}" "2" "…")"

  # Go back
  cd $p9kFolder
  rm -fr $BASEFOLDER
}

source shunit2/source/2.1/src/shunit2