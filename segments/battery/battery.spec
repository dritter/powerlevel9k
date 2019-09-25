#!/usr/bin/env zsh
#vim:ft=zsh ts=2 sw=2 sts=2 et fenc=utf-8

# Required for shunit2 to run correctly
setopt shwordsplit
SHUNIT_PARENT=$0

function setUp() {
  export TERM="xterm-256color"
  local -a P9K_RIGHT_PROMPT_ELEMENTS
  P9K_RIGHT_PROMPT_ELEMENTS=()
  # Load Powerlevel9k
  source powerlevel9k.zsh-theme
  source segments/battery/battery.p9k

  P9K_HOME=$(pwd)
  ### Test specific
  # Create default folder
  FOLDER=/tmp/powerlevel9k-test
  mkdir -p "${FOLDER}"
  cd $FOLDER

  # Prepare folder for pmset (OSX)
  PMSET_PATH=$FOLDER/usr/bin
  mkdir -p $PMSET_PATH
  # Prepare folder for ${BATTERY} (Linux)
  BATTERY_PATH=$FOLDER/sys/class/power_supply
  mkdir -p $BATTERY_PATH/BAT{0..2}
  # empty battery
  mkdir -p $BATTERY_PATH/BAT3
}

function tearDown() {
  # Go back to powerlevel9k folder
  cd "${P9K_HOME}"
  # Remove eventually created test-specific folder
  rm -fr "${FOLDER}" &>/dev/null
  # At least remove test folder completely
  rm -fr /tmp/powerlevel9k-test &>/dev/null
  unset PMSET_PATH
  unset BATTERY_PATH
  unset FOLDER
  unset P9K_HOME
}

# Mock Battery
# For mocking pmset on OSX this function takes one argument (the
# content that pmset should echo).
# For mocking the battery on Linux this function takes three
# arguments:
#   OSX:
#   - $1 The Battery String
#   Linux:
#   - $1 capacity in %
#   - $2 the battery status
#   - $3 charging speed in %
#   Windows:
#   - $1 capacity in %
#   - $2 Estimated Runtime
#   - $3 Battery Status
function makeBatterySay() {
  if [[ -z "${FOLDER}" ]]; then
    echo "Fake root path is not correctly set!"
    exit 1
  fi

  if [[ "${__P9K_OS}" == "OSX" ]]; then
    # OSX
    echo "#!/bin/sh" > $PMSET_PATH/pmset
    echo "echo \"$1\"" >> $PMSET_PATH/pmset
    chmod +x $PMSET_PATH/pmset
  fi

  if [[ "${__P9K_OS}" == "Linux" ]]; then
    # Linux
    local battery_status="$2"
    echo "$battery_status" > $BATTERY_PATH/BAT0/status
    echo "$battery_status" > $BATTERY_PATH/BAT1/status
    echo "$battery_status" > $BATTERY_PATH/BAT2/status

    local capacity="$1"
    if [[ $capacity =~ ^[0-9]*$ ]]; then
      echo "10000000" > $BATTERY_PATH/BAT0/energy_full
      echo  "5000000" > $BATTERY_PATH/BAT1/charge_full
      echo  "2500000" > $BATTERY_PATH/BAT2/energy_full
      echo  "$((10000000*$capacity/100))" > $BATTERY_PATH/BAT0/energy_now
      echo  "$(( 5000000*$capacity/100))" > $BATTERY_PATH/BAT1/energy_now
      echo  "$(( 2500000*$capacity/100))" > $BATTERY_PATH/BAT2/charge_now
    fi

    # charge or discharge
    local charging_speed="${3:-100}"
    if [[ $battery_status == (Charging|Discharging) ]]; then
      echo  "$((5000000*$charging_speed/100))" > $BATTERY_PATH/BAT0/current_now
      echo  "$((2500000*$charging_speed/100))" > $BATTERY_PATH/BAT1/power_now
      echo                                 "0" > $BATTERY_PATH/BAT2/power_now
    else
      echo        "0" > $BATTERY_PATH/BAT0/current_now
      echo        "0" > $BATTERY_PATH/BAT1/power_now
      echo        "0" > $BATTERY_PATH/BAT2/power_now
    fi
  fi

  if [[ "${__P9K_OS}" == "Windows" ]]; then
  # Windows
cat <<EOL > ${PMSET_PATH}/wmic
#!/bin/sh

cat <<FILEEND
Availability=3
BatteryRechargeTime=
BatteryStatus=${3}
Caption=Internal Battery
Chemistry=2
ConfigManagerErrorCode=
ConfigManagerUserConfig=
CreationClassName=Win32_Battery
Description=Internal Battery
DesignCapacity=
DesignVoltage=12261
DeviceID= 1156SMP01AV421
ErrorCleared=
ErrorDescription=
EstimatedChargeRemaining=${1}
EstimatedRunTime=${2}
ExpectedBatteryLife=
ExpectedLife=
FullChargeCapacity=
InstallDate=
LastErrorCode=
MaxRechargeTime=
Name=01AV421
PNPDeviceID=
PowerManagementCapabilities={1}
PowerManagementSupported=FALSE
SmartBatteryVersion=
Status=OK
StatusInfo=
SystemCreationClassName=Win32_ComputerSystem
SystemName=LAPTOP-B7L97D7T
TimeOnBattery=
TimeToFullCharge=
FILEEND
EOL
  chmod +x ${PMSET_PATH}/wmic

  fi
}

function testBatterySegmentIfBatteryIsLowWhileDischargingOnOSX() {
  local __P9K_OS='OSX' # Fake OSX
  makeBatterySay "Now drawing from 'Battery Power'
 -InternalBattery-0 (id=1234567)	4%; discharging; 0:05 remaining present: true"

  prompt_battery "left" 1 false "${FOLDER}"
  assertEquals "%K{000} %F{001}🔋 %F{001}\${:-\"4%% (0:05)\"} " "${__P9K_RETVAL}"
}

function testBatterySegmentIfBatteryIsLowWhileChargingOnOSX() {
  local __P9K_OS='OSX' # Fake OSX
  makeBatterySay "Now drawing from 'Battery Power'
 -InternalBattery-0 (id=1234567)	4%; charging; 0:05 remaining present: true"

  prompt_battery "left" 1 false "${FOLDER}"
  assertEquals "%K{000} %F{003}🔋 %F{003}\${:-\"4%% (0:05)\"} " "${__P9K_RETVAL}"
}

function testBatterySegmentIfBatteryIsNormalWhileDischargingOnOSX() {
  local __P9K_OS='OSX' # Fake OSX
  makeBatterySay "Now drawing from 'Battery Power'
 -InternalBattery-0 (id=1234567)	98%; discharging; 3:57 remaining present: true"

  prompt_battery "left" 1 false "${FOLDER}"
  assertEquals "%K{000} %F{015}🔋 %F{015}\${:-\"98%% (3:57)\"} " "${__P9K_RETVAL}"
}

function testBatterySegmentIfBatteryIsNormalWhileChargingOnOSX() {
  local __P9K_OS='OSX' # Fake OSX
  makeBatterySay "Now drawing from 'Battery Power'
 -InternalBattery-0 (id=1234567)	98%; charging; 3:57 remaining present: true"

  prompt_battery "left" 1 false "${FOLDER}"
  assertEquals "%K{000} %F{003}🔋 %F{003}\${:-\"98%% (3:57)\"} " "${__P9K_RETVAL}"
}

function testBatterySegmentIfBatteryIsFullOnOSX() {
  local __P9K_OS='OSX' # Fake OSX
  makeBatterySay "Now drawing from 'AC Power'
 -InternalBattery-0 (id=1234567)	99%; charged; 0:00 remaining present: true"

  prompt_battery "left" 1 false "${FOLDER}"
  assertEquals "%K{000} %F{002}🔋 %F{002}\${:-\"99%%\"} " "${__P9K_RETVAL}"
}

function testBatterySegmentIfBatteryIsCalculatingOnOSX() {
  local __P9K_OS='OSX' # Fake OSX
  makeBatterySay "Now drawing from 'Battery Power'
 -InternalBattery-0 (id=1234567)	99%; discharging; (no estimate) present: true"

  prompt_battery "left" 1 false "${FOLDER}"
  assertEquals "%K{000} %F{015}🔋 %F{015}\${:-\"99%% (...)\"} " "${__P9K_RETVAL}"
}

function testBatterySegmentIfBatteryIsLowWhileDischargingOnLinux() {
  local __P9K_OS='Linux' # Fake Linux
  makeBatterySay "4" "Discharging"

  prompt_battery "left" 1 false "${FOLDER}"
  assertEquals "%K{000} %F{001}🔋 %F{001}\${:-\"4%% (0:05)\"} " "${__P9K_RETVAL}"
}

function testBatterySegmentIfBatteryIsLowWhileChargingOnLinux() {
  local __P9K_OS='Linux' # Fake Linux
  makeBatterySay "4" "Charging"

  prompt_battery "left" 1 false "${FOLDER}"
  assertEquals "%K{000} %F{003}🔋 %F{003}\${:-\"4%% (2:14)\"} " "${__P9K_RETVAL}"
}

function testBatterySegmentIfBatteryIsLowWhileUnknownOnLinux() {
  local __P9K_OS='Linux' # Fake Linux
  makeBatterySay "4" "Unknown"

  prompt_battery "left" 1 false "${FOLDER}"
  assertEquals "%K{000} %F{001}🔋 %F{001}\${:-\"4%%\"} " "${__P9K_RETVAL}"
}

function testBatterySegmentIfBatteryIsNormalWhileDischargingOnLinux() {
  local __P9K_OS='Linux' # Fake Linux
  makeBatterySay "98" "Discharging"

  prompt_battery "left" 1 false "${FOLDER}"
  assertEquals "%K{000} %F{015}🔋 %F{015}\${:-\"98%% (2:17)\"} " "${__P9K_RETVAL}"
}

function testBatterySegmentIfBatteryIsNormalWhileChargingOnLinux() {
  local __P9K_OS='Linux' # Fake Linux
  makeBatterySay "98" "Charging"

  prompt_battery "left" 1 false "${FOLDER}"
  assertEquals "%K{000} %F{003}🔋 %F{003}\${:-\"98%% (0:02)\"} " "${__P9K_RETVAL}"
}

function testBatterySegmentIfBatteryIsNormalWhileUnknownOnLinux() {
  local __P9K_OS='Linux' # Fake Linux
  makeBatterySay "98" "Unknown"

  prompt_battery "left" 1 false "${FOLDER}"
  assertEquals "%K{000} %F{015}🔋 %F{015}\${:-\"98%%\"} " "${__P9K_RETVAL}"
}

function testBatterySegmentIfBatteryIsFullOnLinux() {
  local __P9K_OS='Linux' # Fake Linux
  makeBatterySay "100" "Full"

  prompt_battery "left" 1 false "${FOLDER}"
  assertEquals "%K{000} %F{002}🔋 %F{002}\${:-\"100%%\"} " "${__P9K_RETVAL}"
}

function testBatterySegmentIfBatteryNearlyFullButNotChargingOnLinux() {
  local __P9K_OS='Linux' # Fake Linux
  makeBatterySay "98" "Unknown" "0"

  prompt_battery "left" 1 false "${FOLDER}"
  assertEquals "%K{000} %F{015}🔋 %F{015}\${:-\"98%%\"} " "${__P9K_RETVAL}"
}

function testBatterySegmentIfBatteryIsCalculatingOnLinux() {
  local __P9K_OS='Linux' # Fake Linux
  makeBatterySay "99" "Charging" "0"

  prompt_battery "left" 1 false "${FOLDER}"
  assertEquals "%K{000} %F{003}🔋 %F{003}\${:-\"99%% (...)\"} " "${__P9K_RETVAL}"
}

function testBatterySegmentIfBatteryIsLowWhileDischargingOnWindows() {
  local __P9K_OS='Windows' # Fake Windows
  makeBatterySay "4" "5" "4"

  prompt_battery "left" 1 false "${FOLDER}/usr/bin/"
  assertEquals "%K{000} %F{001}🔋 %F{001}\${:-\"4%% (0:05)\"} " "${__P9K_RETVAL}"
}

function testBatterySegmentIfBatteryIsLowWhileChargingOnWindows() {
  local __P9K_OS='Windows' # Fake Windows
  makeBatterySay "4" "5" "7"

  prompt_battery "left" 1 false "${FOLDER}/usr/bin/"
  assertEquals "%K{000} %F{003}🔋 %F{003}\${:-\"4%% (0:05)\"} " "${__P9K_RETVAL}"
}

function testBatterySegmentIfBatteryIsLowWhileUnknownOnWindows() {
  local __P9K_OS='Windows' # Fake Windows
  makeBatterySay "4" "Unknown" "5"

  prompt_battery "left" 1 false "${FOLDER}/usr/bin/"
  assertEquals "%K{000} %F{001}🔋 %F{001}\${:-\"4%% (...)\"} " "${__P9K_RETVAL}"
}

function testBatterySegmentIfBatteryIsNormalWhileDischargingOnWindows() {
  local __P9K_OS='Windows' # Fake Windows
  makeBatterySay "98" "215" "1"

  prompt_battery "left" 1 false "${FOLDER}/usr/bin/"
  assertEquals "%K{000} %F{015}🔋 %F{015}\${:-\"98%% (3:35)\"} " "${__P9K_RETVAL}"
}

function testBatterySegmentIfBatteryIsNormalWhileChargingOnWindows() {
  local __P9K_OS='Windows' # Fake Windows
  makeBatterySay "98" "298" "2"

  prompt_battery "left" 1 false "${FOLDER}/usr/bin/"
  assertEquals "%K{000} %F{003}🔋 %F{003}\${:-\"98%% (4:58)\"} " "${__P9K_RETVAL}"
}

function testBatterySegmentIfBatteryIsFullOnWindows() {
  local __P9K_OS='Windows' # Fake Windows
  makeBatterySay "100" "181" "1"

  prompt_battery "left" 1 false "${FOLDER}/usr/bin/"
  assertEquals "%K{000} %F{015}🔋 %F{015}\${:-\"100%% (3:01)\"} " "${__P9K_RETVAL}"
}

function testBatterySegmentIfBatteryIsCalculatingOnWindows() {
  local __P9K_OS='Windows' # Fake Windows
  makeBatterySay "99" "" "2"

  prompt_battery "left" 1 false "${FOLDER}/usr/bin/"
  assertEquals "%K{000} %F{003}🔋 %F{003}\${:-\"99%% (...)\"} " "${__P9K_RETVAL}"
}

function testBatteryStagesString() {
  # as long as the percentages is ok (other tests),
  # the P9K_BATTERY_STAGES tests should be independent of OS type
  local __P9K_OS='Linux'
  P9K_BATTERY_STAGES="abcde"

  makeBatterySay "1" "Charging"
  prompt_battery "left" 1 false "${FOLDER}"
  assertEquals "%K{000} %F{003}a %F{003}\${:-\"1%% (2:18)\"} " "${__P9K_RETVAL}"

  makeBatterySay "26" "Charging"
  prompt_battery "left" 1 false "${FOLDER}"
  assertEquals "%K{000} %F{003}b %F{003}\${:-\"26%% (1:43)\"} " "${__P9K_RETVAL}"

  makeBatterySay "52" "Charging"
  prompt_battery "left" 1 false "${FOLDER}"
  assertEquals "%K{000} %F{003}c %F{003}\${:-\"52%% (1:07)\"} " "${__P9K_RETVAL}"

  makeBatterySay "99" "Charging"
  prompt_battery "left" 1 false "${FOLDER}"
  assertEquals "%K{000} %F{003}d %F{003}\${:-\"99%% (0:01)\"} " "${__P9K_RETVAL}"

  makeBatterySay "100" "Full"
  prompt_battery "left" 1 false "${FOLDER}"
  assertEquals "%K{000} %F{002}e %F{002}\${:-\"100%%\"} " "${__P9K_RETVAL}"
}

function testBatteryStagesArray() {
  local __P9K_OS='Linux'
  P9K_BATTERY_STAGES=("charge!" "low" "med" "high" "full")

  makeBatterySay "1" "Charging"
  prompt_battery "left" 1 false "${FOLDER}"
  assertEquals "%K{000} %F{003}charge! %F{003}\${:-\"1%% (2:18)\"} " "${__P9K_RETVAL}"

  makeBatterySay "26" "Charging"
  prompt_battery "left" 1 false "${FOLDER}"
  assertEquals "%K{000} %F{003}low %F{003}\${:-\"26%% (1:43)\"} " "${__P9K_RETVAL}"

  makeBatterySay "52" "Charging"
  prompt_battery "left" 1 false "${FOLDER}"
  assertEquals "%K{000} %F{003}med %F{003}\${:-\"52%% (1:07)\"} " "${__P9K_RETVAL}"

  makeBatterySay "99" "Charging"
  prompt_battery "left" 1 false "${FOLDER}"
  assertEquals "%K{000} %F{003}high %F{003}\${:-\"99%% (0:01)\"} " "${__P9K_RETVAL}"

  makeBatterySay "100" "Full"
  prompt_battery "left" 1 false "${FOLDER}"
  assertEquals "%K{000} %F{002}full %F{002}\${:-\"100%%\"} " "${__P9K_RETVAL}"
}

source shunit2/shunit2
