Homematic Commandline Tools (HoCoTo)

Control Homematic Thermostats from the commandline.

# Features:
- Visualisation: Output device status as a graph or table
- Save device status into an easily reasable table
- Read from tables and write to devices
- Specify multiple profiles in a table
- Assign profiles per day (templating)
- Duplicaton detection
- Copy profiles between devices
- Offline capability

# Examples:

## Plotting
```
$ ./hocoto -in dev:test -p --day mon
 testing
=========
MONDAY
22.0 +----+---+----+---+----+---+----+---+
21.5 | · ·|· ·|· · | · | · ·|· ·|· · | · |
21.0 | · ·|· ·***· | · | · ·|· ·|· · | · |
20.5 | · ·|· ·|· · | · | · ·|********* · |
20.0 +----+---+----+---+----+---+----+---+
19.5 | · ·|· ·|· · | · | · ·|· ·|· · | · |
19.0 | · ·|· ·|· · | · | · ·|· ·|· · | · |
18.5 | · ·|· ·|· · | · | · ·|· ·|· · | · |
18.0 +----+---+----+---+----+---+----+---+
17.5 | · ·|· ·|· · | · | · ·|· ·|· · | · |
17.0 |*********·************** ·|· · ****|
16.5 | · ·|· ·|· · | · | · ·|· ·|· · | · |
16.0 +----+---+----+---+----+---+----+---+
          3   6    9  12   15  18   21  24
```

## Tables
```

$ ./hocoto -in dev:test --table --day mon
 testing
=========
MONDAY         | TUESDAY        | WEDNESDAY      | THURSDAY       | FRIDAY         | SATURDAY       | SUNDAY         | 
 5:30 - 17°C   | Same as MONDAY | Same as MONDAY | Same as MONDAY | Same as MONDAY | Same as MONDAY | Same as MONDAY | 
 7:00 - 21°C   |                |                |                |                |                |                | 
16:00 - 17°C   |                |                |                |                |                |                | 
21:00 - 20.5°C |                |                |                |                |                |                | 
23:00 - 17°C   |                |                |                |                |                |                | 
24:00 - 17°C   |                |                |                |                |                |                | 
```

## File ouptput:
```
$ ./hocoto -in dev:test --out file:delme
 testing
=========

$ cat delme 
MONDAY
 5:30 - 17°C
 7:00 - 21°C
16:00 - 17°C
21:00 - 20.5°C
23:00 - 17°C
24:00 - 17°C
TUESDAY
Same as MONDAY 
WEDNESDAY
Same as MONDAY 
THURSDAY
Same as MONDAY 
FRIDAY
Same as MONDAY 
SATURDAY
Same as MONDAY 
SUNDAY
Same as MONDAY 
```

## Apply profile for whole week:
```
$ ./hocoto -in file:delme -o dev:test
 Input from file "delme"
=========================
Copying from Input from file "delme" to Testing-Target
All days
```
## Use profiles:
```
$ cat profiles
Workday
 5:30 - 17°C
 7:00 - 21°C
16:00 - 17°C
21:00 - 20.5°C
23:00 - 17°C

Weekend
 5:30 - 17°C
23:00 - 20.5°C
24:00 - 17°C

Homeoffice
 5:30 - 17°C
23:00 - 20.5°C
24:00 - 17°C

MONDAY
= workday

TUESDAY
Same as MONDAY 

WEDNESDAY
= homeoffice 

THURSDAY
Same as MONDAY 

FRIDAY
Same as homeoffice

SATURDAY
= weekend

SUNDAY
Same as  saturday

./hocoto -in file:delme -o dev:test
```

## Use profiles for specific dasy:

```
./hocoto -in file:delme -out dev:test -p --fromday weekend --today MON
```


# Background:

HoCoTo is written in python3 using the homegear Python interface.

The intention was to be as useful as possible. The use case I needed to
cover was "Bring the house into homeoffice state next tuesday" or "I am
sick today, so bring the house into weekend state".

# Future work:

I want to add a tool that monitors a calendar (e.g. ics) file, so that I
can set profiles for longer periods of time, and based on whether anybody
is at home at a given day or not.

