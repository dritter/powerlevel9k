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
my-namespace    kube-dns-fddsfs23h-gds32   0/3       Running   1          5m
another-namespace  kube-xxxx-nflnl34   2/3       Running   0          5m
my-namespace    kube-dns-lnklnknk-eerx33   2/4       Running   0          5m
my-namespace    kube-ignored1-lnnk-exxe56   2/4       Running   4          5m
my-namespace    kube-ignored2-lnnk-exxe58   2/4       Running   1          5m\"
" > "${FOLDER}/bin/kubectl"
  chmod +x "${FOLDER}/bin/kubectl"
}

function mockEmptyKubectl() {
    echo "#!/bin/sh\n\n
    echo \"NAMESPACE       NAME                       READY     STATUS    RESTARTS   AGE\"
" > "${FOLDER}/bin/kubectl"
  chmod +x "${FOLDER}/bin/kubectl"
}

# Hack: Mock an error script that throws an error to
# shadow potentially installed kubectl executable.
function mockKubectlNotInstalled() {
  echo "#!/bin/sh\n\n
    exit 1" > "${FOLDER}/bin/kubectl"
  chmod +x "${FOLDER}/bin/kubectl"
}

function testKubepodsShowsNothingIfKubectlIsNotInstalled() {
  mockKubectlNotInstalled
  local P9K_CUSTOM_WORLD='echo world'
  local -a P9K_LEFT_PROMPT_ELEMENTS
  P9K_LEFT_PROMPT_ELEMENTS=(kubepods custom_world)

  assertEquals "%K{015} %F{000}world %k%F{015}%f " "$(__p9k_build_left_prompt)"
}

function testKubepodsShowsNothingIfNoNamespacesAreRunning() {
  mockEmptyKubectl
  local P9K_CUSTOM_WORLD='echo world'
  local -a P9K_LEFT_PROMPT_ELEMENTS
  P9K_LEFT_PROMPT_ELEMENTS=(kubepods custom_world)

  assertEquals "%K{015} %F{000}world %k%F{015}%f " "$(__p9k_build_left_prompt)"
}

function testKubepodsSegmentWorks() {
  mockKubectl
  local -a P9K_LEFT_PROMPT_ELEMENTS
  P9K_LEFT_PROMPT_ELEMENTS=(kubepods)

  local P9K_KUBEPODS_NAMESPACES=(my-namespace kube-system xxx)

  assertEquals "%K{004} %F{015}⎈ %f%F{015}my-namespace: 6/15 kube-system: 3/3 xxx: 0/0 %k%F{004}%f " "$(__p9k_build_left_prompt)"
}

function testKubepodsSegmentShowsAllNamespacesIfNoNamespaceWasDefined() {
  mockKubectl
  local -a P9K_LEFT_PROMPT_ELEMENTS
  P9K_LEFT_PROMPT_ELEMENTS=(kubepods)

  assertEquals "%K{004} %F{015}⎈ %f%F{015}kube-system: 3/3 my-namespace: 6/15 another-namespace: 2/3 %k%F{004}%f " "$(__p9k_build_left_prompt)"
}

function testKubepodsSegmentIgnoresSpecifiedPods() {
  mockKubectl
  local -a P9K_LEFT_PROMPT_ELEMENTS
  P9K_LEFT_PROMPT_ELEMENTS=(kubepods)

  local P9K_KUBEPODS_NAMESPACES=(my-namespace)
  local P9K_KUBEPODS_IGNORE_PODS=(kube-ignored1 kube-ignored2)

  assertEquals "%K{004} %F{015}⎈ %f%F{015}my-namespace: 2/7 %k%F{004}%f " "$(__p9k_build_left_prompt)"
}

function testKubepodsSegmentCanChangeOutputIfAllPodsAreRunning() {
  mockKubectl
  local -a P9K_LEFT_PROMPT_ELEMENTS
  P9K_LEFT_PROMPT_ELEMENTS=(kubepods)

  local P9K_KUBEPODS_ALL_RUNNING_STRING="All Up!"
  local P9K_KUBEPODS_NAMESPACES=(kube-system)

  assertEquals "%K{004} %F{015}⎈ %f%F{015}All Up! %k%F{004}%f " "$(__p9k_build_left_prompt)"
}

function testKubepodsSegmentDoesNotChangeOutputIfNotAllPodsAreRunning() {
  mockKubectl
  local -a P9K_LEFT_PROMPT_ELEMENTS
  P9K_LEFT_PROMPT_ELEMENTS=(kubepods)

  local P9K_KUBEPODS_ALL_RUNNING_STRING="All Up!"
  local P9K_KUBEPODS_NAMESPACES=(another-namespace)

  assertEquals "%K{004} %F{015}⎈ %f%F{015}another-namespace: 2/3 %k%F{004}%f " "$(__p9k_build_left_prompt)"
}

function testKubepodsSegmentShowsRestarts() {
  mockKubectl
  local -a P9K_LEFT_PROMPT_ELEMENTS
  P9K_LEFT_PROMPT_ELEMENTS=(kubepods)

  local P9K_KUBEPODS_NAMESPACES=(my-namespace)
  local P9K_KUBEPODS_SHOW_RESTARTS="true"

  assertEquals "%K{004} %F{015}⎈ %f%F{015}my-namespace: 6/15/6 %k%F{004}%f " "$(__p9k_build_left_prompt)"
}

source shunit2/shunit2