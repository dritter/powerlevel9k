#!/usr/bin/env zsh
#vim:ft=zsh ts=2 sw=2 sts=2 et fenc=utf-8

# Required for shunit2 to run correctly
setopt shwordsplit
SHUNIT_PARENT=$0

function setUp() {
  export TERM="xterm-256color"
  __P9K_HOME="${PWD}"
  source powerlevel9k.zsh-theme
  source segments/kubepods.p9k

  # Test specific
  TEST_BASE_FOLDER=/tmp/powerlevel9k-test
  FOLDER=${TEST_BASE_FOLDER}/vagrant-test
  mkdir -p "${FOLDER}/bin"
  OLD_PATH=$PATH
  PATH=${FOLDER}/bin:$PATH
  cd $FOLDER
}

function tearDown() {
  cd "${__P9K_HOME}"
  rm -fr "${TEST_BASE_FOLDER}"
  PATH="${OLD_PATH}"
  unset OLD_PATH
  unset __P9K_HOME
}

function mockKubectl() {
    echo "#!/bin/sh\n\n
    echo \"NAMESPACE       NAME                       READY     STATUS    RESTARTS   AGE
kube-system     kube-dns-ffd85c78c-6frzd   3/3       Running   0          5m
my-namespace    kube-dns-fddsfs23h-gds32   0/3       Running   0          5m
another-namespace  kube-xxxx-nflnl34   3/3       Running   0          5m
my-namespace    kube-dns-lnklnknk-eerx33   2/4       Running   0          5m\"
" > "${FOLDER}/bin/kubectl"
chmod +x "${FOLDER}/bin/kubectl"
}

function testKubepodsSegmentWorks() {
  mockKubectl
  local -a P9K_LEFT_PROMPT_ELEMENTS
  P9K_LEFT_PROMPT_ELEMENTS=(kubepods)

  local P9K_KUBEPODS_NAMESPACES=(my-namespace kube-system xxx)

  assertEquals " my-namespace: 2/7 kube-system: 3/3 xxx: 0/0 %k%f " "$(__p9k_build_left_prompt)"
}

source shunit2/shunit2