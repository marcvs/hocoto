#!/bin/bash

PROFILE_MANAGER=hocoto
PROFILE_DIR=./

$PROFILE_MANAGER --todev 1 -r $PROFILE_DIR/entkleide.profile     
$PROFILE_MANAGER --todev 2 -r $PROFILE_DIR/wohnzimmer.profile    
$PROFILE_MANAGER --todev 4 -r $PROFILE_DIR/kueche.profile        
$PROFILE_MANAGER --todev 7 -r $PROFILE_DIR/kueche.profile        
$PROFILE_MANAGER --todev 5 -r $PROFILE_DIR/gaestezimmer.profile  
$PROFILE_MANAGER --todev 6 -r $PROFILE_DIR/bad.profile           


# 1  | Entkleide
# 2  | Wohnzimmer
# 4  | Kueche hinten
# 5  | Gaestezimmer
# 6  | Bad
# 7  | Kueche vorn neu
