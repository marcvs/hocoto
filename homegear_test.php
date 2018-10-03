#!/usr/bin/env php
<?php
//Wochenprogramm fuer Entkleide


$device=1;
//| ID | Name                      | Address | Serial     | Type | Type String |
//|----+---------------------------+---------+------------+------+-------------|
//| 1  | HM Entkleide OEQ1718409   | 63A25E  | OEQ1718409 | 0095 | HM-CC-RT-DN |
//| 2  | HM Wohnzimmer OEQ1711775  | 638586  | OEQ1711775 | 0095 | HM-CC-RT-DN |
//| 3  | HM Kueche vorn OEQ1711363 | 638718  | OEQ1711363 | 0095 | HM-CC-RT-DN |
//| 4  | HM Kueche hinten  OEQ1... | 63A260  | OEQ1718411 | 0095 | HM-CC-RT-DN |
//| 5  | HM Gaestezimmer OEQ171... | 63A278  | OEQ1718437 | 0095 | HM-CC-RT-DN |
//| 6  | HM Bad OEQ1718406         | 63A255  | OEQ1718406 | 0095 | HM-CC-RT-DN |
$t_low= 17.0;
$t_med= 20.0;
$t_hig= 21.0;
$t_hot= 22.0;


$hg = new \Homegear\Homegear();
//print_v($hg->listDevices());
//$x = $hg->setValue($device, 1, "ECO_TEMPERATURE", $t_low);
//print ($x);
//print_v($hg->getValue($device, 1, "ECO_TEMPERATURE"));
//print_v($hg->getValue($device, 1, "COMFORT_TEMPERATURE"));
//print_v($hg->getValue($device, 1, "DECALCIFICATION_TIME"));
//print_v($hg->getValue($device, 1, "DECALCIFICATION_WEEKDAY"));
//print_v($hg->getValue($device, 1, "MAX_TEMPERATURE"));

//Wochenprogramm einspielen
//$hg->putParamset($device, 0, "MASTER", array(
//     "TEMPERATURE_MONDAY_1"     => $t_low, "ENDTIME_MONDAY_1"     => 60*5  + 30,
//     "TEMPERATURE_MONDAY_2"     => $t_hig, "ENDTIME_MONDAY_2"     => 60*7  + 0,
//     "TEMPERATURE_MONDAY_3"     => $t_low, "ENDTIME_MONDAY_3"     => 60*16 + 0,
//     "TEMPERATURE_MONDAY_4"     => $t_med, "ENDTIME_MONDAY_4"     => 60*21 + 0,
//     "TEMPERATURE_MONDAY_5"     => $t_low, "ENDTIME_MONDAY_5"     => 60*23 + 0,
//     "TEMPERATURE_MONDAY_6"     => $t_low, "ENDTIME_MONDAY_6"     => 60*24 + 0,
//     "TEMPERATURE_MONDAY_7"     => $t_low, "ENDTIME_MONDAY_7"     => 60*24 + 0,
//     "TEMPERATURE_MONDAY_8"     => $t_low, "ENDTIME_MONDAY_8"     => 60*24 + 0,
//     "TEMPERATURE_MONDAY_9"     => $t_low, "ENDTIME_MONDAY_9"     => 60*24 + 0,
//     "TEMPERATURE_MONDAY_10"    => $t_low, "ENDTIME_MONDAY_10"    => 60*24 + 0,
//     "TEMPERATURE_MONDAY_11"    => $t_low, "ENDTIME_MONDAY_11"    => 60*24 + 0,
//     "TEMPERATURE_MONDAY_12"    => $t_low, "ENDTIME_MONDAY_12"    => 60*24 + 0,
//     "TEMPERATURE_MONDAY_13"    => $t_low, "ENDTIME_MONDAY_13"    => 60*24 + 0,
//
//     "TEMPERATURE_TUESDAY_1"    => $t_low, "ENDTIME_TUESDAY_1"    => 60*5  + 30,
//     "TEMPERATURE_TUESDAY_2"    => $t_hig, "ENDTIME_TUESDAY_2"    => 60*7  + 0,
//     "TEMPERATURE_TUESDAY_3"    => $t_low, "ENDTIME_TUESDAY_3"    => 60*16 + 0,
//     "TEMPERATURE_TUESDAY_4"    => $t_med, "ENDTIME_TUESDAY_4"    => 60*21 + 0,
//     "TEMPERATURE_TUESDAY_5"    => $t_low, "ENDTIME_TUESDAY_5"    => 60*23 + 0,
//     "TEMPERATURE_TUESDAY_6"    => $t_low, "ENDTIME_TUESDAY_6"    => 60*24 + 0,
//     "TEMPERATURE_TUESDAY_7"    => $t_low, "ENDTIME_TUESDAY_7"    => 60*24 + 0,
//     "TEMPERATURE_TUESDAY_8"    => $t_low, "ENDTIME_TUESDAY_8"    => 60*24 + 0,
//     "TEMPERATURE_TUESDAY_9"    => $t_low, "ENDTIME_TUESDAY_9"    => 60*24 + 0,
//     "TEMPERATURE_TUESDAY_10"   => $t_low, "ENDTIME_TUESDAY_10"   => 60*24 + 0,
//     "TEMPERATURE_TUESDAY_11"   => $t_low, "ENDTIME_TUESDAY_11"   => 60*24 + 0,
//     "TEMPERATURE_TUESDAY_12"   => $t_low, "ENDTIME_TUESDAY_12"   => 60*24 + 0,
//     "TEMPERATURE_TUESDAY_13"   => $t_low, "ENDTIME_TUESDAY_13"   => 60*24 + 0,
//
//     "TEMPERATURE_WEDNESDAY_1"  => $t_low, "ENDTIME_WEDNESDAY_1"  => 60*5  + 30,
//     "TEMPERATURE_WEDNESDAY_2"  => $t_hig, "ENDTIME_WEDNESDAY_2"  => 60*7  + 0,
//     "TEMPERATURE_WEDNESDAY_3"  => $t_low, "ENDTIME_WEDNESDAY_3"  => 60*16 + 0,
//     "TEMPERATURE_WEDNESDAY_4"  => $t_med, "ENDTIME_WEDNESDAY_4"  => 60*21 + 0,
//     "TEMPERATURE_WEDNESDAY_5"  => $t_low, "ENDTIME_WEDNESDAY_5"  => 60*23 + 0,
//     "TEMPERATURE_WEDNESDAY_6"  => $t_low, "ENDTIME_WEDNESDAY_6"  => 60*24 + 0,
//     "TEMPERATURE_WEDNESDAY_7"  => $t_low, "ENDTIME_WEDNESDAY_7"  => 60*24 + 0,
//     "TEMPERATURE_WEDNESDAY_8"  => $t_low, "ENDTIME_WEDNESDAY_8"  => 60*24 + 0,
//     "TEMPERATURE_WEDNESDAY_9"  => $t_low, "ENDTIME_WEDNESDAY_9"  => 60*24 + 0,
//     "TEMPERATURE_WEDNESDAY_10" => $t_low, "ENDTIME_WEDNESDAY_10" => 60*24 + 0,
//     "TEMPERATURE_WEDNESDAY_11" => $t_low, "ENDTIME_WEDNESDAY_11" => 60*24 + 0,
//     "TEMPERATURE_WEDNESDAY_12" => $t_low, "ENDTIME_WEDNESDAY_12" => 60*24 + 0,
//     "TEMPERATURE_WEDNESDAY_13" => $t_low, "ENDTIME_WEDNESDAY_13" => 60*24 + 0,
//
//     "TEMPERATURE_THURSDAY_1"   => $t_low, "ENDTIME_THURSDAY_1"   => 60*5  + 30,
//     "TEMPERATURE_THURSDAY_2"   => $t_hig, "ENDTIME_THURSDAY_2"   => 60*7  + 0,
//     "TEMPERATURE_THURSDAY_3"   => $t_low, "ENDTIME_THURSDAY_3"   => 60*16 + 0,
//     "TEMPERATURE_THURSDAY_4"   => $t_med, "ENDTIME_THURSDAY_4"   => 60*21 + 0,
//     "TEMPERATURE_THURSDAY_5"   => $t_low, "ENDTIME_THURSDAY_5"   => 60*23 + 0,
//     "TEMPERATURE_THURSDAY_6"   => $t_low, "ENDTIME_THURSDAY_6"   => 60*24 + 0,
//     "TEMPERATURE_THURSDAY_7"   => $t_low, "ENDTIME_THURSDAY_7"   => 60*24 + 0,
//     "TEMPERATURE_THURSDAY_8"   => $t_low, "ENDTIME_THURSDAY_8"   => 60*24 + 0,
//     "TEMPERATURE_THURSDAY_9"   => $t_low, "ENDTIME_THURSDAY_9"   => 60*24 + 0,
//     "TEMPERATURE_THURSDAY_10"  => $t_low, "ENDTIME_THURSDAY_10"  => 60*24 + 0,
//     "TEMPERATURE_THURSDAY_11"  => $t_low, "ENDTIME_THURSDAY_11"  => 60*24 + 0,
//     "TEMPERATURE_THURSDAY_12"  => $t_low, "ENDTIME_THURSDAY_12"  => 60*24 + 0,
//     "TEMPERATURE_THURSDAY_13"  => $t_low, "ENDTIME_THURSDAY_13"  => 60*24 + 0,
//
//     "TEMPERATURE_FRIDAY_1"     => $t_low, "ENDTIME_FRIDAY_1"     => 60*5  + 30,
//     "TEMPERATURE_FRIDAY_2"     => $t_hig, "ENDTIME_FRIDAY_2"     => 60*7  + 0,
//     "TEMPERATURE_FRIDAY_3"     => $t_low, "ENDTIME_FRIDAY_3"     => 60*16 + 0,
//     "TEMPERATURE_FRIDAY_4"     => $t_med, "ENDTIME_FRIDAY_4"     => 60*21 + 0,
//     "TEMPERATURE_FRIDAY_5"     => $t_low, "ENDTIME_FRIDAY_5"     => 60*23 + 0,
//     "TEMPERATURE_FRIDAY_6"     => $t_low, "ENDTIME_FRIDAY_6"     => 60*24 + 0,
//     "TEMPERATURE_FRIDAY_7"     => $t_low, "ENDTIME_FRIDAY_7"     => 60*24 + 0,
//     "TEMPERATURE_FRIDAY_8"     => $t_low, "ENDTIME_FRIDAY_8"     => 60*24 + 0,
//     "TEMPERATURE_FRIDAY_9"     => $t_low, "ENDTIME_FRIDAY_9"     => 60*24 + 0,
//     "TEMPERATURE_FRIDAY_10"    => $t_low, "ENDTIME_FRIDAY_10"    => 60*24 + 0,
//     "TEMPERATURE_FRIDAY_11"    => $t_low, "ENDTIME_FRIDAY_11"    => 60*24 + 0,
//     "TEMPERATURE_FRIDAY_12"    => $t_low, "ENDTIME_FRIDAY_12"    => 60*24 + 0,
//     "TEMPERATURE_FRIDAY_13"    => $t_low, "ENDTIME_FRIDAY_13"    => 60*24 + 0,
//
//     "TEMPERATURE_SATURDAY_1"   => $t_low, "ENDTIME_SATURDAY_1"   => 60*5  + 30,
//     "TEMPERATURE_SATURDAY_2"   => $t_hig, "ENDTIME_SATURDAY_2"   => 60*7  + 0,
//     "TEMPERATURE_SATURDAY_3"   => $t_low, "ENDTIME_SATURDAY_3"   => 60*16 + 0,
//     "TEMPERATURE_SATURDAY_4"   => $t_med, "ENDTIME_SATURDAY_4"   => 60*21 + 0,
//     "TEMPERATURE_SATURDAY_5"   => $t_low, "ENDTIME_SATURDAY_5"   => 60*23 + 0,
//     "TEMPERATURE_SATURDAY_6"   => $t_low, "ENDTIME_SATURDAY_6"   => 60*24 + 0,
//     "TEMPERATURE_SATURDAY_7"   => $t_low, "ENDTIME_SATURDAY_7"   => 60*24 + 0,
//     "TEMPERATURE_SATURDAY_8"   => $t_low, "ENDTIME_SATURDAY_8"   => 60*24 + 0,
//     "TEMPERATURE_SATURDAY_9"   => $t_low, "ENDTIME_SATURDAY_9"   => 60*24 + 0,
//     "TEMPERATURE_SATURDAY_10"  => $t_low, "ENDTIME_SATURDAY_10"  => 60*24 + 0,
//     "TEMPERATURE_SATURDAY_11"  => $t_low, "ENDTIME_SATURDAY_11"  => 60*24 + 0,
//     "TEMPERATURE_SATURDAY_12"  => $t_low, "ENDTIME_SATURDAY_12"  => 60*24 + 0,
//     "TEMPERATURE_SATURDAY_13"  => $t_low, "ENDTIME_SATURDAY_13"  => 60*24 + 0,
//
//     "TEMPERATURE_SUNDAY_1"     => $t_low, "ENDTIME_SUNDAY_1"     => 60*5  + 30,
//     "TEMPERATURE_SUNDAY_2"     => $t_hig, "ENDTIME_SUNDAY_2"     => 60*7  + 0,
//     "TEMPERATURE_SUNDAY_3"     => $t_low, "ENDTIME_SUNDAY_3"     => 60*16 + 0,
//     "TEMPERATURE_SUNDAY_4"     => $t_med, "ENDTIME_SUNDAY_4"     => 60*21 + 0,
//     "TEMPERATURE_SUNDAY_5"     => $t_low, "ENDTIME_SUNDAY_5"     => 60*23 + 0,
//     "TEMPERATURE_SUNDAY_6"     => $t_low, "ENDTIME_SUNDAY_6"     => 60*24 + 0,
//     "TEMPERATURE_SUNDAY_7"     => $t_low, "ENDTIME_SUNDAY_7"     => 60*24 + 0,
//     "TEMPERATURE_SUNDAY_8"     => $t_low, "ENDTIME_SUNDAY_8"     => 60*24 + 0,
//     "TEMPERATURE_SUNDAY_9"     => $t_low, "ENDTIME_SUNDAY_9"     => 60*24 + 0,
//     "TEMPERATURE_SUNDAY_10"    => $t_low, "ENDTIME_SUNDAY_10"    => 60*24 + 0,
//     "TEMPERATURE_SUNDAY_11"    => $t_low, "ENDTIME_SUNDAY_11"    => 60*24 + 0,
//     "TEMPERATURE_SUNDAY_12"    => $t_low, "ENDTIME_SUNDAY_12"    => 60*24 + 0,
//     "TEMPERATURE_SUNDAY_13"    => $t_low, "ENDTIME_SUNDAY_13"    => 60*24 + 0
//     ));

print_v($hg->getParamset($device, 0, "MASTER"));
