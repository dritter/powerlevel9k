#!/usr/bin/env zsh
#vim:ft=zsh ts=2 sw=2 sts=2 et fenc=utf-8

# Required for shunit2 to run correctly
setopt shwordsplit
SHUNIT_PARENT=$0

function setUp() {
  # Load Powerlevel9k
  source functions/colors.zsh
}

function testGetColorCodeWithAnsiForegroundColor() {
  __p9k_get_color_code 'green'
  assertEquals '002' "${__P9K_RETVAL}"
}

function testGetColorCodeWithAnsiBackgroundColor() {
  __p9k_get_color_code 'bg-green'
  assertEquals '002' "${__P9K_RETVAL}"
}

function testGetColorCodeWithNumericalColor() {
  __p9k_get_color_code '002'
  assertEquals '002' "${__P9K_RETVAL}"
}

function testIsSameColorComparesAnsiForegroundAndNumericalColorCorrectly() {
  assertTrue "p9k::is_same_color 'green' '002'"
}

function testIsSameColorComparesAnsiBackgroundAndNumericalColorCorrectly() {
  assertTrue "p9k::is_same_color 'bg-green' '002'"
}

function testIsSameColorComparesShortCodesCorrectly() {
  assertTrue "p9k::is_same_color '002' '2'"}

function testIsSameColorDoesNotYieldNotEqualColorsTruthy() {
  assertFalse "p9k::is_same_color 'green' '003'"
}

function testGetColorCodeWithTrueColor() {
  __p9k_get_color '#fff8e7'
  assertEquals '#fff8e7' "${__P9K_RETVAL}"  # truecolor (hex)
  __p9k_get_color '137'
  assertEquals '137' "${__P9K_RETVAL}"          # number (dec)
  __p9k_get_color 'yellow4'
  assertEquals '100' "${__P9K_RETVAL}"      # named
}

function testBrightColorsWork() {
  # We had some code in the past that equalized bright colors
  # with normal ones. This code is now gone, and this test should
  # ensure that all input channels for bright colors are handled
  # correctly.
  assertTrue "p9k::is_same_color 'lightcyan' '014'"
  __p9k_get_color_code 'lightcyan'
  assertEquals '014' "${__P9K_RETVAL}"
  __p9k_get_color 'lightcyan'
  assertEquals '014' "${__P9K_RETVAL}"
}

source shunit2/shunit2
