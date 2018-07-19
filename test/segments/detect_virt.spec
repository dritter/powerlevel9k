#!/usr/bin/env zsh
#vim:ft=zsh ts=2 sw=2 sts=2 et fenc=utf-8

# Required for shunit2 to run correctly
setopt shwordsplit
SHUNIT_PARENT=$0

function setUp() {
  export TERM="xterm-256color"
  # Load Powerlevel9k
  source powerlevel9k.zsh-theme
}

function testDetectVirtSegmentPrintsNothingIfSystemdIsNotAvailable() {
    alias systemd-detect-virt="novirt"

    local POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(detect_virt custom_world)
    local POWERLEVEL9K_CUSTOM_WORLD='echo world'

    assertEquals "%K{white} %F{black}world %k%F{white}%f " "$(build_left_prompt)"

    unalias systemd-detect-virt
}

function testDetectVirtSegmentIfSystemdReturnsPlainName() {
    local POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(detect_virt)
    alias systemd-detect-virt="echo 'xxx'"

    assertEquals "%K{black} %F{yellow}xxx %k%F{black}%f " "$(build_left_prompt)"

    unalias systemd-detect-virt
}

function testDetectVirtSegmentIfRootFsIsOnExpectedInode() {
    local POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(detect_virt)
    # Well. This is a weak test, as it fixates the implementation,
    # but it is necessary, as the implementation relys on the root
    # directory having the inode number "2"..
    alias systemd-detect-virt="echo 'none'"

    # The original command in the implementation is "ls -di / | grep -o 2",
    # which translates to: Show the inode number of "/" and test if it is "2".
    alias ls="echo '2'"

    assertEquals "%K{black} %F{yellow}none %k%F{black}%f " "$(build_left_prompt)"

    unalias ls
    unalias systemd-detect-virt
}

function testDetectVirtSegmentIfRootFsIsNotOnExpectedInode() {
    local POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(detect_virt)
    # Well. This is a weak test, as it fixates the implementation,
    # but it is necessary, as the implementation relys on the root
    # directory having the inode number "2"..
    alias systemd-detect-virt="echo 'none'"

    # The original command in the implementation is "ls -di / | grep -o 2",
    # which translates to: Show the inode number of "/" and test if it is "2".
    alias ls="echo '3'"

    assertEquals "%K{black} %F{yellow}chroot %k%F{black}%f " "$(build_left_prompt)"

    unalias ls
    unalias systemd-detect-virt
}

source shunit2/source/2.1/src/shunit2