#!/bin/bash

SET_PROFILE=$1
SET_DAY=$2

PROFILE_MANAGER=hocoto_manager
PROFILE_DIR=./

$PROFILE_MANAGER --todev 1 -r $PROFILE_DIR/entkleide.profile     --fromday $SET_PROFILE --today $SET_DAY
$PROFILE_MANAGER --todev 2 -r $PROFILE_DIR/wohnzimmer.profile    --fromday $SET_PROFILE --today $SET_DAY
$PROFILE_MANAGER --todev 4 -r $PROFILE_DIR/kueche.profile        --fromday $SET_PROFILE --today $SET_DAY
$PROFILE_MANAGER --todev 7 -r $PROFILE_DIR/kueche.profile        --fromday $SET_PROFILE --today $SET_DAY
$PROFILE_MANAGER --todev 5 -r $PROFILE_DIR/gaestezimmer.profile  --fromday $SET_PROFILE --today $SET_DAY
$PROFILE_MANAGER --todev 6 -r $PROFILE_DIR/bad.profile           --fromday $SET_PROFILE --today $SET_DAY


# 1  | Entkleide
# 2  | Wohnzimmer
# 4  | Kueche hinten
# 5  | Gaestezimmer
# 6  | Bad
# 7  | Kueche vorn neu
