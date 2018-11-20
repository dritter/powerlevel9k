#!/usr/bin/env zsh
#vim:ft=zsh ts=2 sw=2 sts=2 et fenc=utf-8

# Required for shunit2 to run correctly
setopt shwordsplit
SHUNIT_PARENT=$0

function setUp() {
  export TERM="xterm-256color"
  source powerlevel9k.zsh-theme
}

function mockKubectl() {
    echo "NAMESPACE       NAME                       READY     STATUS    RESTARTS   AGE
kube-system     kube-dns-ffd85c78c-6frzd   3/3       Running   0          5m
my-namespace    kube-dns-fddsfs23h-gds32   0/3       Running   0          5m"
}

function testKubepodsSegmentWorks() {
  alias kubectl=mockKubectl
  local -a P9K_LEFT_PROMPT_ELEMENTS
  P9K_LEFT_PROMPT_ELEMENTS=(kubepods)

  local P9K_KUBEPODS_NAMESPACES=(my-namespace kube-system)

  # Load Powerlevel9k
  source segments/kubepods.p9k

  assertEquals "my-namespace: 0/3" "$(__p9k_build_left_prompt)"
  unalias kubectl
}

source shunit2/shunit2