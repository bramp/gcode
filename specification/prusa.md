::::::::::::::::::::::::::::::::::::::::::::::::: {.sc-3062e91e-0 .glZrnv role="main"}
:::::::::::::::: {.sc-87f52012-0 .kZqIwB}
This is a list of currently implemented G-Codes in [Prusa
firmware](https://github.com/prusa3d/Prusa-Firmware) for i3 series
printers. The description is only for Prusa Research-specific G-codes.
The rest can be found on RepRap Wiki. With exception of M117, they are
all shown in order of appearance in the code. That is why some G Codes
aren\'t in numerical order.

::: {.sc-416e3c82-0 .hmjGvM .tip-callout type="tip-callout"}
![](data:image/svg+xml;base64,PHN2ZyBhcmlhLWhpZGRlbj0idHJ1ZSIgZm9jdXNhYmxlPSJmYWxzZSIgZGF0YS1wcmVmaXg9ImZhcyIgZGF0YS1pY29uPSJjaXJjbGUtaW5mbyIgY2xhc3M9InN2Zy1pbmxpbmUtLWZhIGZhLWNpcmNsZS1pbmZvIGZhLWxnICIgcm9sZT0iaW1nIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdib3g9IjAgMCA1MTIgNTEyIj48cGF0aCBmaWxsPSJjdXJyZW50Q29sb3IiIGQ9Ik0yNTYgNTEyQTI1NiAyNTYgMCAxIDAgMjU2IDBhMjU2IDI1NiAwIDEgMCAwIDUxMnpNMjE2IDMzNmwyNCAwIDAtNjQtMjQgMGMtMTMuMyAwLTI0LTEwLjctMjQtMjRzMTAuNy0yNCAyNC0yNGw0OCAwYzEzLjMgMCAyNCAxMC43IDI0IDI0bDAgODggOCAwYzEzLjMgMCAyNCAxMC43IDI0IDI0cy0xMC43IDI0LTI0IDI0bC04MCAwYy0xMy4zIDAtMjQtMTAuNy0yNC0yNHMxMC43LTI0IDI0LTI0em00MC0yMDhhMzIgMzIgMCAxIDEgMCA2NCAzMiAzMiAwIDEgMSAwLTY0eiIgLz48L3N2Zz4=){.svg-inline--fa
.fa-circle-info .fa-lg}For G-code documentation of Original Prusa Buddy
firmware (MINI/+/XL/MK4/MK3.9/MK3.5), visit the [Buddy firmware-specific
G-code commands
article.](http://help.prusa3d.com/article/buddy-firmware-specific-g-code-commands_633112)
:::

<div>

### Special internal commands

</div>

These are used by internal functions to process certain actions in the
right order. Some of these are also usable by the user. They are
processed early as the commands are complex (strings). These are only
available on the MK3(S) as these require TMC2130 drivers:

- CRASH DETECTED
- CRASH RECOVER
- CRASH_CANCEL
- TMC_SET_WAVE
- TMC_SET_STEP
- TMC_SET_CHOP

#### M0, M1 - Stop the printer [M0: Stop or Unconditional stop](https://reprap.org/wiki/G-code#M0:_Stop_or_Unconditional_stop)

#### Usage

M0 \[P\] \[string\] M1 \[P\] \[S\] \[string\]

#### Parameters

- `P` - Expire time, in milliseconds
- `S` - Expire time, in seconds
- `string` - Must for M1 and optional for M0 message to display on the
  LCD

------------------------------------------------------------------------

#### PRUSA - Internal command set [G98: Activate farm mode - Notes](https://reprap.org/wiki/G-code#G98:_Activate_farm_mode)

Set of internal PRUSA commands

#### Usage

PRUSA \[ Ping \| PRN \| FAN \| fn \| thx \| uvlo \| MMURES \| RESET \|
fv \| M28 \| SN \| Fir \| Rev \| Lang \| Lz \| Beat \| FR \]

#### Parameters

- `Ping`
- `PRN` - Prints revision of the printer
- `FAN` - Prints fan details
- `fn` - Prints farm no.
- `thx`
- `uvlo`
- `MMURES` - Reset MMU
- `RESET` - (Careful!)
- `fv` - ?
- `M28`
- `SN`
- `Fir` - Prints firmware version
- `Rev`- Prints filament size, elelectronics, nozzle type
- `Lang` - Reset the language
- `Lz`
- `Beat` - Kick farm link timer
- `FR` - Full factory reset
- `nozzle set ` - set nozzle diameter (farm mode only), e.g.
  `PRUSA nozzle set 0.4`
- `nozzle D` - check the nozzle diameter (farm mode only), works like
  M862.1 P, e.g. `PRUSA nozzle D0.4`
- `nozzle` - prints nozzle diameter (farm mode only), works like M862.1
  P, e.g. `PRUSA nozzle`

------------------------------------------------------------------------

<div>

### G Codes

</div>

#### G0, G1 - Coordinated movement X Y Z E [G0 & G1: Move](https://reprap.org/wiki/G-code#G0_.26_G1:_Move)

In Prusa Firmware G0 and G1 are the same.

#### Usage

``` fragment
G0 [ X | Y | Z | E | F | S ]
G1 [ X | Y | Z | E | F | S ]
```

#### Parameters

- `X` - The position to move to on the X-axis
- `Y` - The position to move to on the Y-axis
- `Z` - The position to move to on the Z-axis
- `E` - The amount to extrude between the starting point and ending
  point
- `F` - The feedrate per minute of the move between the starting point
  and ending point (if supplied)

#### G2, G3 - Controlled Arc Move [G2 & G3: Controlled Arc Move](https://reprap.org/wiki/G-code#G2_.26_G3:_Controlled_Arc_Move)

These commands don\'t propperly work with MBL enabled. The compensation
only happens at the end of the move, so avoid long arcs.

#### Usage

``` fragment
G2 [ X | Y | I | E | F ] (Clockwise Arc) 
G3 [ X | Y | I | E | F ] (Counter-Clockwise Arc)
```

#### Parameters

- `X` - The position to move to on the X-axis
- `Y` - The position to move to on the Y-axis
- `I` - The point in X space from the current X position to maintain a
  constant distance from
- `J` - The point in Y space from the current Y position to maintain a
  constant distance from
- `E` - The amount to extrude between the starting point and ending
  point
- `F` - The feedrate per minute of the move between the starting point
  and ending point (if supplied)

#### G4 - Dwell [G4: Dwell](https://reprap.org/wiki/G-code#G4:_Dwell)

Pause the machine for a period of time.

#### Usage

``` fragment
G4 [ P | S ]
```

#### Parameters

- `P` - Time to wait, in milliseconds
- `S` - Time to wait, in seconds

#### G10 - Retract [G10: Retract](https://reprap.org/wiki/G-code#G10:_Retract)

Retracts filament according to settings of `M207`

#### G11 - Retract recover [G11: Unretract](https://reprap.org/wiki/G-code#G11:_Unretract)

Unretracts/recovers filament according to settings of `M208`

#### G21 - Sets Units to Millimters [G21: Set Units to Millimeters](https://reprap.org/wiki/G-code#G21:_Set_Units_to_Millimeters)

Units are in millimeters. Prusa doesn\'t support inches.

#### G28 - Home all Axes one at a time [G28: Move to Origin (Home)](https://reprap.org/wiki/G-code#G28:_Move_to_Origin_.28Home.29)

Using `G28` without any parameters will perform homing of all axes AND
mesh bed leveling, while `G28 W` will just home all axes (no mesh bed
leveling).

#### Usage

``` fragment
 G28 [ X | Y | Z | W | C ]
```

#### Parameters

- `X` - Flag to go back to the X axis origin
- `Y` - Flag to go back to the Y axis origin
- `Z` - Flag to go back to the Z axis origin
- `W` - Suppress mesh bed leveling if `X`, `Y` or `Z` are not provided
- `C` - Calibrate X and Y origin (home) - Only on MK3/s

G28 issued without parameters homes the **MMU** as well (invalidates the
homing flags of Selector and Idler and these will perform homing async
once it is considered safe, i.e. no filament in the selector)

- P: just invalidate the selector\'s homing validity flag
- I: just invalidate the idler\'s homing validity flag

#### G29 - Detailed Z-Probe [G29: Detailed Z-Probe](https://reprap.org/wiki/G-code#G29:_Detailed_Z-Probe)

In Prusa i3 Firmware this G-code is deactivated by default, must be
turned on in the source code.

See `G81`

#### G30 - Single Z Probe [G30: Single Z-Probe](https://reprap.org/wiki/G-code#G30:_Single_Z-Probe)

In Prusa Firmware this G-code is deactivated by default, must be turned
on in the source code.

#### G31 - Dock the sled [G31: Dock Z Probe sled](https://reprap.org/wiki/G-code#G31:_Dock_Z_Probe_sled)

In Prusa Firmware this G-code is deactivated by default, must be turned
on in the source code.

#### G32 - Undock the sled [G32: Undock Z Probe sled](https://reprap.org/wiki/G-code#G32:_Undock_Z_Probe_sled)

In Prusa Firmware this G-code is deactivated by default, must be turned
on in the source code.

#### G30 - Single Z Probe [G30: Single Z-Probe](https://reprap.org/wiki/G-code#G30:_Single_Z-Probe)

The sensor must be over the bed. The maximum travel distance before an
error is triggered is 10mm.

#### G75 - Print temperature interpolation [G75: Print temperature interpolation](https://reprap.org/wiki/G-code#G75:_Print_temperature_interpolation)

Show/print PINDA temperature interpolating.

#### G76 - PINDA probe temperature calibration [G76: PINDA probe temperature calibration](https://reprap.org/wiki/G-code#G76:_PINDA_probe_temperature_calibration)

This G-code is used to calibrate the temperature drift of the PINDA
(inductive Sensor).

The PINDAv2 sensor has a built-in thermistor which has the advantage
that the calibration can be done once for all materials.

The Original i3 Prusa MK2/s uses PINDAv1 and this calibration improves
the temperature drift, but not as good as the PINDAv2.

SuperPINDA sensor has internal temperature compensation and no
thermistor output. There is no point of doing temperature calibration in
such case. If PINDA_THERMISTOR and SUPERPINDA_SUPPORT is defined during
compilation, calibration is skipped with serial message \"No PINDA
thermistor\". This can be caused also if PINDA thermistor connection is
broken or PINDA temperature is lower than PINDA_MINTEMP.

#### Example

::::::::: fragment
::: line
G76
:::

::: line
 
:::

::: line
echo PINDA probe calibration start
:::

::: line
echo start temperature: 35.0°
:::

::: line
echo \...
:::

::: line
echo PINDA temperature \-- Z shift (mm): 0.\-\--
:::
:::::::::

#### G80 - Mesh-based Z probe [G80: Mesh-based Z probe](https://reprap.org/wiki/G-code#G80:_Mesh-based_Z_probe)

Default 3x3 grid can be changed on MK2.5/s and MK3/s to 7x7 grid.

#### Usage

``` fragment
G80 [ N | C | O | M | L | R | F | B | X | Y | W | H ] 
```

#### Parameters

- N - Number of mesh points on x axis. Default is value stored in
  EEPROM. Valid values are 3 and 7.
- C - Probe retry counts. Default is value stored in EEPROM. Valid
  values are 1 to 10.
- O - Return to origin. Default is 1. Valid values are 0 (false) and 1
  (true).
- M - Use magnet compensation. Will only be used if number of mesh
  points is set to 7. Default is value stored in EEPROM. Valid values
  are 0 (false) and 1 (true).

#### Additional Parameters

Using the following parameters enables additional \"manual\" bed
leveling correction. Valid values are -100 microns to 100 microns.

- L - Left Bed Level correct value in um.
- R - Right Bed Level correct value in um.
- F - Front Bed Level correct value in um.
- B - Back Bed Level correct value in um.

The following parameters are used to define the area used by the print:

- X - area lower left point X coordinate
- Y - area lower left point Y coordinate
- W - area width (on X axis)
- H - area height (on Y axis)

#### G81 - Mesh bed leveling status [G81: Mesh bed leveling status](https://reprap.org/wiki/G-code#G81:_Mesh_bed_leveling_status)

Prints mesh bed leveling status and bed profile if activated.

#### G82: Single Z probe at current location - Not active [G82: Single Z probe at current location](https://reprap.org/wiki/G-code#G82:_Single_Z_probe_at_current_location)

WARNING! USE WITH CAUTION! If you\'ll try to probe where is no leveling
pad, nasty things can happen! In Prusa Firmware this G-code is
deactivated by default, must be turned on in the source code.

#### G83: Babystep in Z and store to EEPROM - Not active [G83: Babystep in Z and store to EEPROM](https://reprap.org/wiki/G-code#G83:_Babystep_in_Z_and_store_to_EEPROM)

In Prusa Firmware this G-code is deactivated by default, must be turned
on in the source code.

#### G84: UNDO Babystep Z (move Z axis back) - Not active [G84: UNDO Babystep Z (move Z axis back)](https://reprap.org/wiki/G-code#G84:_UNDO_Babystep_Z_.28move_Z_axis_back.29)

In Prusa Firmware this G-code is deactivated by default, must be turned
on in the source code.

#### G85: Pick best babystep - Not active [G85: Pick best babystep](https://reprap.org/wiki/G-code#G85:_Pick_best_babystep)

In Prusa Firmware this G-code is deactivated by default, must be turned
on in the source code.

#### G86 - Disable babystep correction after home [G86: Disable babystep correction after home](https://reprap.org/wiki/G-code#G86:_Disable_babystep_correction_after_home)

This G-code will be performed at the start of a calibration script.
(Prusa3D specific)

#### G87 - Enable babystep correction after home [G87: Enable babystep correction after home](https://reprap.org/wiki/G-code#G87:_Enable_babystep_correction_after_home)

This G-code will be performed at the end of a calibration script.
(Prusa3D specific)

#### G88 - Reserved [G88: Reserved](https://reprap.org/wiki/G-code#G88:_Reserved)

Currently has no effect.

#### G90 - Switch off relative mode [G90: Set to Absolute Positioning](https://reprap.org/wiki/G-code#G90:_Set_to_Absolute_Positioning)

All coordinates from now on are absolute relative to the origin of the
machine. E axis is left intact.

#### G91 - Switch on relative mode [G91: Set to Relative Positioning](https://reprap.org/wiki/G-code#G91:_Set_to_Relative_Positioning)

All coordinates from now on are relative to the last position. E axis is
left intact.

#### G92 - Set position [G92: Set Position](https://reprap.org/wiki/G-code#G92:_Set_Position)

It is used for setting the current position of each axis. The parameters
are always absolute to the origin. If a parameter is omitted, that axis
will not be affected. If `X`, `Y`, or `Z` axis are specified, the move
afterwards might stutter because of Mesh Bed Leveling. `E` axis is not
affected if the target position is 0 (`G92 E0`). A G92 without
coordinates will reset all axes to zero on some firmware. This is not
the case for Prusa-Firmware!

#### Usage

``` fragment
G92 [ X | Y | Z | E ]
```

#### Parameters

- `X` - new X axis position
- `Y` - new Y axis position
- `Z` - new Z axis position
- `E` - new extruder position

#### G98 - Activate farm mode [G98: Activate farm mode](https://reprap.org/wiki/G-code#G98:_Activate_farm_mode)

Enable Prusa-specific Farm functions and g-code. See Internal Prusa
commands.

#### G99 - Deactivate farm mode [G99: Deactivate farm mode](https://reprap.org/wiki/G-code#G99:_Deactivate_farm_mode)

Disables Prusa-specific Farm functions and g-code.

#### End of G-Codes

------------------------------------------------------------------------

<div>

### M Commands

</div>

#### M17 - Enable all axes [M17: Enable/Power all stepper motors](https://reprap.org/wiki/G-code#M17:_Enable.2FPower_all_stepper_motors)

#### M20 - SD Card file list [M20: List SD card](https://reprap.org/wiki/G-code#M20:_List_SD_card)

#### Usage

``` fragment
M20 [ L | T ]
```

#### Parameters

- `T` - Report timestamps as well. The value is one uint32_t encoded as
  hex. Requires host software parsing (Cap:EXTENDED_M20).
- `L` - Reports long filenames instead of just short filenames. Requires
  host software parsing (Cap:EXTENDED_M20).

#### M21 - Init SD card [M21: Initialize SD card](https://reprap.org/wiki/G-code#M21:_Initialize_SD_card)

#### M22 - Release SD card [M22: Release SD card](https://reprap.org/wiki/G-code#M22:_Release_SD_card)

#### M23 - Select file [M23: Select SD file](https://reprap.org/wiki/G-code#M23:_Select_SD_file)

#### Usage

``` fragment
M23 [filename]
```

#### M24 - Start SD print [M24: Start/resume SD print](https://reprap.org/wiki/G-code#M24:_Start.2Fresume_SD_print)

#### M26 - Set SD index [M26: Set SD position](https://reprap.org/wiki/G-code#M26:_Set_SD_position)

Set position in SD card file to index in bytes. This command is expected
to be called after M23 and before M24. Otherwise effect of this command
is undefined.

#### Usage

``` fragment
M26 [ S ]
```

#### Parameters

- `S` - Index in bytes

#### M27 - Get SD status [M27: Report SD print status](https://reprap.org/wiki/G-code#M27:_Report_SD_print_status)

#### Usage

``` fragment
M27 [ P ]
```

#### Parameters

- `P` - Show full SFN path instead of LFN only.

#### M28 - Start SD write [M28: Begin write to SD card](https://reprap.org/wiki/G-code#M28:_Begin_write_to_SD_card)

#### M29 - Stop SD write [M29: Stop writing to SD card](https://reprap.org/wiki/G-code#M29:_Stop_writing_to_SD_card)

Stops writing to the SD file signaling the end of the uploaded file. It
is processed very early and it\'s not written to the card.

#### M30 - Delete file [M30: Delete a file on the SD card](https://reprap.org/wiki/G-code#M30:_Delete_a_file_on_the_SD_card)

#### Usage

``` fragment
M30 [filename]
```

#### M32 - Select file and start SD print [M32: Select file and start SD print](https://reprap.org/wiki/G-code#M32:_Select_file_and_start_SD_print)

#### M928 - Start SD logging [M928: Start SD logging](https://reprap.org/wiki/G-code#M928:_Start_SD_logging)

#### Usage

``` fragment
M928 [filename]
```

#### M31 - Report current print time [M31: Output time since last M109 or SD card start to serial](https://reprap.org/wiki/G-code#M31:_Output_time_since_last_M109_or_SD_card_start_to_serial)

#### M42 - Set pin state [M42: Switch I/O pin](https://reprap.org/wiki/G-code#M42:_Switch_I.2FO_pin)

#### Usage

``` fragment
M42 [ P | S ]
```

#### Parameters

- `P` - Pin number.
- `S` - Pin value. If the pin is analog, values are from 0 to 255. If
  the pin is digital, values are from 0 to 1.

#### M44 - Reset the bed skew and offset calibration [M44: Reset the bed skew and offset calibration](https://reprap.org/wiki/G-code#M44:_Reset_the_bed_skew_and_offset_calibration)

#### M45 - Bed skew and offset with manual Z up [M45: Bed skew and offset with manual Z up](https://reprap.org/wiki/G-code#M45:_Bed_skew_and_offset_with_manual_Z_up)

#### Usage

``` fragment
M45 [ V ]
```

#### Parameters

- `V` - Verbosity level 1, 10 and 20 (low, mid, high). Only when
  SUPPORT_VERBOSITY is defined. Optional.
- `Z` - If it is provided, only Z calibration will run. Otherwise, full
  calibration is executed.

#### M46 - Show the assigned IP address [M46: Show the assigned IP address.](https://reprap.org/wiki/G-code#M46:_Show_the_assigned_IP_address)

#### M47 - Show end stops dialog on the display [M47: Show end stops dialog on the display](https://reprap.org/wiki/G-code#M47:_Show_end_stops_dialog_on_the_display)

#### M48 - Z-Probe repeatability measurement function [M48: Measure Z-Probe repeatability](https://reprap.org/wiki/G-code#M48:_Measure_Z-Probe_repeatability)

This function assumes the bed has been homed. Specifically, that a G28
command has been issued prior to invoking the M48 Z-Probe repeatability
measurement function. Any information generated by a prior G29 Bed
leveling command will be lost and needs to be regenerated.

The number of samples will default to 10 if not specified. You can use
upper or lower case letters for any of the options EXCEPT n. n must be
in lower case because Marlin uses a capital N for its communication
protocol and will get horribly confused if you send it a capital N.

**Usage**

``` fragment
M48 [ n | X | Y | V | L ]
```

#### Parameters

- `n` - Number of samples. Valid values 4-50
- `X` - X position for samples
- `Y` - Y position for samples
- `V` - Verbose level. Valid values 1-4
- `L` - Legs of movement prior to doing probe. Valid values 1-15

#### M72 - Set/get Printer State [M72: Set/get Printer State](https://reprap.org/wiki/G-code#M72:_Set.2FGet_Printer_State)

Without any parameter get printer state.

0 = NotReady Used by PrusaConnect\
1 = IsReady Used by PrusaConnect\
2 = Idle\
3 = SD printing finished\
4 = Host printing finished\
5 = SD printing\
6 = Host printing

#### Usage

    M72 [ S ]

#### Parameters

- Snnn - Set printer state 0 = not_ready, 1 = ready

#### M73 - Set/get print progress [M73: Set/Get build percentage](https://reprap.org/wiki/G-code#M73:_Set.2FGet_build_percentage)

#### Usage

``` fragment
M73 [ P | R | Q | S | C | D ]
```

#### Parameters

- `P` - Percent in normal mode
- `R` - Time remaining in normal mode
- `Q` - Percent in silent mode
- `S` - Time in silent mode
- `C` - Time to change/pause/user interaction in normal mode
- `D` - Time to change/pause/user interaction in silent mode

#### M75 - Start the print job timer [M75: Start the print job timer](https://reprap.org/wiki/G-code#M75:_Start_the_print_job_timer)

#### M76 - Pause the print job timer [M76: Pause the print job timer](https://reprap.org/wiki/G-code#M76:_Pause_the_print_job_timer)

#### M77 - Stop the print job timer M77: Stop the print job timer

#### M78 - Show statistical information about the print jobs [M78: Show statistical information about the print jobs](https://reprap.org/wiki/G-code#M78:_Show_statistical_information_about_the_print_jobs)

#### M79 - Start host timer [M79: Start host timer](https://reprap.org/wiki/G-code#M79:_Start_host_timer)

Start the printer-host enable keep-alive timer. While the timer has not
expired, the printer will enable host specific features.

#### Usage

    M79 [ S ]

#### Parameters

- S - Quoted string containing two characters e.g. \"PL\"

 

#### M104 - Set hotend temperature [M104: Set Extruder Temperature](https://reprap.org/wiki/G-code#M104:_Set_Extruder_Temperature)

#### Usage

``` fragment
M104 [ S ]
```

#### Parameters

- `S` - Target temperature

#### M112 - Emergency stop [M112: Full (Emergency) Stop](https://reprap.org/wiki/G-code#M112:_Full_.28Emergency.29_Stop)

It is processed much earlier as to bypass the cmdqueue.

#### M140 - Set bed temperature [M140: Set Bed Temperature (Fast)](https://reprap.org/wiki/G-code#M140:_Set_Bed_Temperature_.28Fast.29)

#### Usage

``` fragment
M140 [ S ]
```

#### Parameters

- `S` - Target temperature

#### M105 - Report temperatures [M105: Get Extruder Temperature](https://reprap.org/wiki/G-code#M105:_Get_Extruder_Temperature)

Prints temperatures:

- `T:` - Hotend (actual / target)
- `B:` - Bed (actual / target)
- `Tx:` - x Tool (actual / target)
- `@:` - Hotend power
- `B@:` - Bed power
- `P:` - PINDAv2 actual (only MK2.5/s and MK3/s)
- `A:` - Ambient actual (only MK3/s)

*Example:*

``` fragment
ok T:20.2 /0.0 B:19.1 /0.0 T0:20.2 /0.0 @:0 B@:0 P:19.8 A:26.4
```

#### M155 - Automatically send status [M155: Automatically send temperatures](https://reprap.org/wiki/G-code#M155:_Automatically_send_temperatures)

#### Usage

``` fragment
M155 [ S ] [ C ]
```

#### Parameters

- `S` - Set autoreporting interval in seconds. 0 to disable. Maximum:
  255

- `C` - Activate auto-report function (bit mask). Default is
  temperature.

  ``` fragment
  bit 0 = Auto-report temperatures bit 1 = Auto-report fans bit 2 = Auto-report position bit 3 = free bit 4 = free bit 5 = free bit 6 = free bit 7 = free
  ```

#### M109 - Wait for extruder temperature [M109: Set Extruder Temperature and Wait](https://reprap.org/wiki/G-code#M109:_Set_Extruder_Temperature_and_Wait)

#### Usage

``` fragment
M104 [ B | R | S ]
```

#### Parameters (not mandatory)

- `S` - Set extruder temperature
- `R` - Set extruder temperature
- `B` - Set max. extruder temperature, while `S` is min. temperature.
  Not active in default, only if AUTOTEMP is defined in source code.

Parameters S and R are treated identically. Command always waits for
both cool down and heat up. If no parameters are supplied waits for
previously set extruder temperature.

#### M190 - Wait for bed temperature [M190: Wait for bed temperature to reach target temp](https://reprap.org/wiki/G-code#M190:_Wait_for_bed_temperature_to_reach_target_temp)

#### Usage

``` fragment
M190 [ R | S ]
```

#### Parameters (not mandatory)

- `S` - Set extruder temperature and wait for heating
- `R` - Set extruder temperature and wait for heating or cooling

If no parameter is supplied, waits for heating or cooling to previously
set temperature.

#### M106 - Set fan speed [M106: Fan On](https://reprap.org/wiki/G-code#M106:_Fan_On)

#### Usage

M106 \[ S \]

#### Parameters

- `S` - Specifies the duty cycle of the print fan. Allowed values are
  0-255. If it\'s omitted, a value of 255 is used.

#### M107 - Fan off [M107: Fan Off](https://reprap.org/wiki/G-code#M107:_Fan_Off)

#### M80 - Turn on the Power Supply [M80: ATX Power On](https://reprap.org/wiki/G-code#M80:_ATX_Power_On)

Only works if the firmware is compiled with PS_ON_PIN defined.

#### M81 - Turn off Power Supply [M81: ATX Power Off](https://reprap.org/wiki/G-code#M81:_ATX_Power_Off)

Only works if the firmware is compiled with PS_ON_PIN defined.

#### M82 - Set E axis to absolute mode [M82: Set extruder to absolute mode](https://reprap.org/wiki/G-code#M82:_Set_extruder_to_absolute_mode)

Makes the extruder interpret extrusion as absolute positions.

#### M83 - Set E axis to relative mode [M83: Set extruder to relative mode](https://reprap.org/wiki/G-code#M83:_Set_extruder_to_relative_mode)

Makes the extruder interpret extrusion values as relative positions.

#### M84 - Disable steppers [M84: Stop idle hold](https://reprap.org/wiki/G-code#M84:_Stop_idle_hold)

This command can be used to set the stepper inactivity timeout (`S`) or
to disable steppers (`X`,`Y`,`Z`,`E`) This command can be used without
any additional parameters. In that case all steppers are disabled.

The file completeness check uses this parameter to detect an incomplete
file. It has to be present at the end of a file with no parameters.

``` fragment
M84 [ S | X | Y | Z | E ]
```

- `S` - Seconds
- `X` - X axis
- `Y` - Y axis
- `Z` - Z axis
- `E` - Exruder

#### M18 - Disable steppers [M18: Disable all stepper motors](https://reprap.org/wiki/G-code#M18:_Disable_all_stepper_motors)

Equal to M84 (compatibility)

#### M85 - Set max inactive time [M85: Set Inactivity Shutdown Timer](https://reprap.org/wiki/G-code#M85:_Set_Inactivity_Shutdown_Timer)

#### Usage

``` fragment
M85 [ S ]
```

#### Parameters

- `S` - specifies the time in seconds. If a value of 0 is specified, the
  timer is disabled.

#### M86 - Set safety timer expiration time [M86: Set Safety Timer expiration time](https://reprap.org/wiki/G-code#M86:_Set_Safety_Timer_expiration_time)

When safety timer expires, heatbed and nozzle target temperatures are
set to zero.

#### Usage

``` fragment
M86 [ S ]
```

#### Parameters

- `S` - specifies the time in seconds. If a value of 0 is specified, the
  timer is disabled.

#### M92 Set Axis steps-per-unit [M92: Set axis_steps_per_unit](https://reprap.org/wiki/G-code#M92:_Set_axis_steps_per_unit)

Allows programming of steps per unit (usually mm) for motor drives.
These values are reset to firmware defaults on power on, unless saved to
EEPROM if available (M500 in Marlin)

#### Usage

``` fragment
M92 [ X | Y | Z | E ]
```

#### Parameters

- `X` - Steps per unit for the X drive
- `Y` - Steps per unit for the Y drive
- `Z` - Steps per unit for the Z drive
- `E` - Steps per unit for the extruder drive

#### M110 - Set Line number [M110: Set Current Line Number](https://reprap.org/wiki/G-code#M110:_Set_Current_Line_Number)

Sets the line number in G-code

#### Usage

``` fragment
M110 [ N ]
```

#### Parameters

- `N` - Line number

#### M113 - Get or set host keep-alive interval [M113: Host Keepalive](https://reprap.org/wiki/G-code#M113:_Host_Keepalive)

During some lengthy processes, such as G29, Marlin may appear to the
host to have "gone away." The "host keepalive" feature will send
messages to the host when Marlin is busy or waiting for user response so
the host won't try to reconnect (or disconnect).

#### Usage

``` fragment
M113 [ S ]
```

#### Parameters

- `S` - Seconds. Default is 2 seconds between \"busy\" messages

#### M115 - Firmware info [M115: Get Firmware Version and Capabilities](https://reprap.org/wiki/G-code#M115:_Get_Firmware_Version_and_Capabilities)

Print the firmware info and capabilities Without any arguments, prints
Prusa firmware version number, machine type, extruder count and UUID.
`M115 U` Checks the firmware version provided. If the firmware version
provided by the U code is higher than the currently running firmware, it
will pause the print for 30s and ask the user to upgrade the firmware.

*Examples:*

`M115` results:

`FIRMWARE_NAME:Prusa-Firmware 3.8.1 based on Marlin FIRMWARE_URL:https://github.com/prusa3d/Prusa-Firmware PROTOCOL_VERSION:1.0 MACHINE_TYPE:Prusa i3 MK3S EXTRUDER_COUNT:1 UUID:00000000-0000-0000-0000-000000000000`

`M115 V` results:

`3.8.1`

`M115 U3.8.2-RC1` results on LCD display for 30s or user interaction:

`New firmware version available: 3.8.2-RC1 Please upgrade.`

#### Usage

``` fragment
M115 [ V | U ]
```

#### Parameters

- V - Report current installed firmware version
- U - Firmware version provided by G-code to be compared to current one.

#### M114 - Get current position [M114: Get Current Position](https://reprap.org/wiki/G-code#M114:_Get_Current_Position)

#### M117 - Display Message M117: Display Message

This causes the given message to be shown in the status line on an
attached LCD. It is processed early as to allow printing messages that
contain G, M, N, or T.

#### M118 - Serial print M118: Serial print

#### Usage

    M118 [ A1 | E1 ] [ String ]

#### Parameters

- A1 - Prepend // to denote a comment or action command. Hosts like
  OctoPrint can interpret such commands to perform special actions. See
  your host's documentation.
- E1 - Prepend echo: to the message. Some hosts will display echo
  messages differently when preceded by echo:.
- String - Message string. If omitted, a blank line will be sent.

#### M120 - Enable endstops [M120: Enable endstop detection](https://reprap.org/wiki/G-code#M120:_Enable_endstop_detection)

#### M121 - Disable endstops [M121: Disable endstop detection](https://reprap.org/wiki/G-code#M121:_Disable_endstop_detection)

#### M119 - Get endstop states [M119: Get Endstop Status](https://reprap.org/wiki/G-code#M119:_Get_Endstop_Status)

Returns the current state of the configured X, Y, Z endstops. Takes into
account any \'inverted endstop\' settings, so one can confirm that the
machine is interpreting the endstops correctly.

#### M123 - Tachometer value [M123: Tachometer value](https://www.reprap.org/wiki/G-code#M123:_Tachometer_value_.28RepRap_.26_Prusa.29)

This command is used to report fan speeds and fan pwm values.

#### Usage

``` fragment
M123
```

- E0: - Hotend fan speed in RPM
- PRN1: - Part cooling fans speed in RPM
- E0@: - Hotend fan PWM value
- PRN1@: -Part cooling fan PWM value

*Example:*

E0:3240 RPM PRN1:4560 RPM E0@:255 PRN1@:255

#### M150 - Set RGB(W) Color [M150: Set LED color](https://reprap.org/wiki/G-code#M150:_Set_LED_color)

In Prusa Firmware this G-code is deactivated by default, must be turned
on in the source code by defining BLINKM and its dependencies.

#### Usage

``` fragment
M150 [ R | U | B ]
```

#### Parameters

- `R` - Red color value
- `U` - Green color value. It is NOT `G`!
- `B` - Blue color value

#### M200 - Set filament diameter [M200: Set filament diameter](https://reprap.org/wiki/G-code#M200:_Set_filament_diameter)

#### Usage

``` fragment
M200 [ D | T ]
```

#### Parameters

- `D` - Diameter in mm
- `T` - Number of extruder (MMUs)

#### M201 - Set Print Max Acceleration [M201: Set max printing acceleration](https://reprap.org/wiki/G-code#M201:_Set_max_printing_acceleration)

For each axis individually.

#### M203 - Set Max Feedrate [M203: Set maximum feedrate](https://reprap.org/wiki/G-code#M203:_Set_maximum_feedrate)

For each axis individually.

#### M204 - Acceleration settings [M204: Set default acceleration](https://reprap.org/wiki/G-code#M204:_Set_default_acceleration)

#### Old format:

##### Usage

``` fragment
M204 [ S | T ]
```

##### Parameters

- `S` - normal moves
- `T` - filament only moves

#### New format:

##### Usage

``` fragment
M204 [ P | R | T ]
```

##### Parameters

- `P` - printing moves
- `R` - filament only moves
- `T` - travel moves (as of now T is ignored)

#### M205 - Set advanced settings [M205: Advanced settings](https://reprap.org/wiki/G-code#M205:_Advanced_settings)

Set some advanced settings related to movement.

#### Usage

``` fragment
M205 [ S | T | B | X | Y | Z | E ]
```

#### Parameters

- `S` - Minimum feedrate for print moves (unit/s)
- `T` - Minimum feedrate for travel moves (units/s)
- `B` - Minimum segment time (us)
- `X` - Maximum X jerk (units/s)
- `Y` - Maximum Y jerk (units/s)
- `Z` - Maximum Z jerk (units/s)
- `E` - Maximum E jerk (units/s)

#### M206 - Set additional homing offsets [M206: Offset axes](https://reprap.org/wiki/G-code#M206:_Offset_axes)

#### Usage

``` fragment
M206 [ X | Y | Z ]
```

#### Parameters

- `X` - X axis offset
- `Y` - Y axis offset
- `Z` - Z axis offset

#### M207 - Set firmware retraction [M207: Set retract length](https://reprap.org/wiki/G-code#M207:_Set_retract_length)

#### Usage

``` fragment
M207 [ S | F | Z ]
```

#### Parameters

- `S` - positive length to retract, in mm
- `F` - retraction feedrate, in mm/min
- `Z` - additional zlift/hop

#### M208 - Set retract recover length [M208: Set unretract length](https://reprap.org/wiki/G-code#M208:_Set_unretract_length)

#### Usage

``` fragment
M208 [ S | F ]
```

#### Parameters

- `S` - positive length surplus to the M207 Snnn, in mm
- `F` - feedrate, in mm/sec

#### M209 - Enable/disable automatict retract [M209: Enable automatic retract](https://reprap.org/wiki/G-code#M209:_Enable_automatic_retract)

This boolean value S 1=true or 0=false enables automatic retract detect
if the slicer did not support G10/G11: every normal extrude-only move
will be classified as retract depending on the direction.

#### Usage

``` fragment
M209 [ S ]
```

#### Parameters

- `S` - 1=true or 0=false

#### M214 - Set Arc configuration values (Use M500 to store in eeprom) [M214: Set Arc configuration value.](https://reprap.org/wiki/G-code#M214:_Set_Arc_configuration_values)

#### Usage

    M214 [P] [S] [N] [R] [F]

#### Parameters

- P - A float representing the max and default millimeters per arc
  segment. Must be greater than 0.
- S - A float representing the minimum allowable millimeters per arc
  segment. Set to 0 to disable
- N - An int representing the number of arcs to draw before correcting
  the small angle approximation. Set to 0 to disable.
- R - An int representing the minimum number of segments per arcs of any
  radius, except when the results in segment lengths greater than or
  less than the minimum and maximum segment length. Set to 0 to disable.
- F - An int representing the number of segments per second, unless this
  results in segment lengths greater than or less than the minimum and
  maximum segment length. Set to 0 to disable.

#### M218 - Set hotend offset [M218: Set Hotend Offset](https://reprap.org/wiki/G-code#M218:_Set_Hotend_Offset)

In Prusa Firmware this G-code is only active if `EXTRUDERS` is higher
then 1 in the source code. On Original i3 Prusa MK2/s MK2.5/s MK3/s it
is not active.

#### Usage

``` fragment
M218 [ X | Y ]
```

#### Parameters

- `X` - X offset
- `Y` - Y offset

#### M220 Set feedrate percentage [M220: Set speed factor override percentage](https://reprap.org/wiki/G-code#M220:_Set_speed_factor_override_percentage)

#### Usage

``` fragment
M220 [ B | S | R ]
```

#### Parameters

- `B` - Backup current speed factor
- `S` - Speed factor override percentage (0..100 or higher)
- `R` - Restore previous speed factor

#### M221 - Set extrude factor override percentage [M221: Set extrude factor override percentage](https://reprap.org/wiki/G-code#M221:_Set_extrude_factor_override_percentage)

#### Usage

``` fragment
M221 [ S | T ]
```

#### Parameters

- `S` - Extrude factor override percentage (0..100 or higher), default
  100%
- `T` - Extruder drive number (Prusa Firmware only), default 0 if not
  set.

#### M226 - Wait for Pin state [M226: Wait for pin state](https://reprap.org/wiki/G-code#M226:_Wait_for_pin_state)

Wait until the specified pin reaches the state required

#### Usage

``` fragment
M226 [ P | S ]
```

#### Parameters

- `P` - pin number
- `S` - pin state

#### M280 - Set/Get servo position [M280: Set servo position](https://reprap.org/wiki/G-code#M280:_Set_servo_position)

In Prusa Firmware this G-code is deactivated by default, must be turned
on in the source code.

#### Usage

``` fragment
M280 [ P | S ]
```

#### Parameters

- `P` -
  [Servo](https://helpdev.prusa3d.com/en/admin/article/classServo.html){.el}
  index (id)
- `S` - Target position

#### M300 - Play tone [M300: Play beep sound](https://reprap.org/wiki/G-code#M300:_Play_beep_sound)

In Prusa Firmware the defaults are `100Hz` and `1000ms`, so that `M300`
without parameters will beep for a second.

#### Usage

``` fragment
M300 [ S | P ]
```

#### Parameters

- `S` - frequency in Hz. Not all firmware versions support this
  parameter
- `P` - duration in milliseconds

#### M301 - Set hotend PID [M301: Set PID parameters](https://reprap.org/wiki/G-code#M301:_Set_PID_parameters)

Sets Proportional (P), Integral (I) and Derivative (D) values for hot
end. See also [PID Tuning.](https://reprap.org/wiki/PID_Tuning)

#### Usage

``` fragment
M301 [ P | I | D | C ]
```

#### Parameters

- `P` - proportional (Kp)
- `I` - integral (Ki)
- `D` - derivative (Kd)
- `C` - heating power=Kc\*(e_speed0)

#### M304 - Set bed PID [M304: Set PID parameters - Bed](https://reprap.org/wiki/G-code#M304:_Set_PID_parameters_-_Bed)

Sets Proportional (P), Integral (I) and Derivative (D) values for bed.
See also [PID Tuning.](https://reprap.org/wiki/PID_Tuning)

#### Usage

``` fragment
M304 [ P | I | D ]
```

#### Parameters

- `P` - proportional (Kp)
- `I` - integral (Ki)
- `D` - derivative (Kd)

#### M240 - Trigger camera [M240: Trigger camera](https://reprap.org/wiki/G-code#M240:_Trigger_camera)

In Prusa Firmware this G-code is deactivated by default, must be turned
on in the source code.

You need to (re)define and assign `CHDK` or `PHOTOGRAPH_PIN` the correct
pin number to be able to use the feature.

#### M302 - Allow cold extrude, or set minimum extrude temperature [M302: Allow cold extrudes](https://reprap.org/wiki/G-code#M302:_Allow_cold_extrudes)

This tells the printer to allow movement of the extruder motor above a
certain temperature, or if disabled, to allow extruder movement when the
hotend is below a safe printing temperature.

#### Usage

``` fragment
M302 [ S ]
```

#### Parameters

- `S` - Cold extrude minimum temperature

#### M303 - PID autotune [M303: Run PID tuning](https://reprap.org/wiki/G-code#M303:_Run_PID_tuning)

PID Tuning refers to a control algorithm used in some repraps to tune
heating behavior for hot ends and heated beds. This command generates
Proportional (Kp), Integral (Ki), and Derivative (Kd) values for the
hotend or bed. Send the appropriate code and wait for the output to
update the firmware values.

#### Usage

``` fragment
M303 [ E | S | C ]
```

#### Parameters

- `E` - Extruder, default `E0`. Use `E-1` to calibrate the bed PID
- `S` - Target temperature, default `210°C` for hotend, 70 for bed
- `C` - Cycles, default `5`

#### M310 - Thermal model settings [M310: Thermal model settings](https://reprap.org/wiki/G-code#M310:_Thermal_model_settings)

#### Usage

    M310                                           ; report values
    M310 [ A ] [ F ]                               ; autotune
    M310 [ S ]                                     ; set 0=disable 1=enable
    M310 [ I ] [ R ]                               ; set resistance at index
    M310 [ P | U | V | C ]                         ; set power, temperature coefficient, intercept, capacitance
    M310 [ D | L ]                                 ; set simulation filter, lag
    M310 [ B | E | W ]                             ; set beeper, warning and error threshold
    M310 [ T ]                                     ; set ambient temperature correction

#### Parameters

- I - resistance index position (0-15)
- R - resistance value at index (K/W; requires I)
- P - power (W)
- U - linear temperature coefficient (W/K/power)
- V - linear temperature intercept (W/power)
- C - capacitance (J/K)
- D - sim. 1st order IIR filter factor (f=100/27)
- L - sim. response lag (ms, 0-2160)
- S - set 0=disable 1=enable
- B - beep and warn when reaching warning threshold 0=disable 1=enable
  (default: 1)
- E - error threshold (K/s; default in variant)
- W - warning threshold (K/s; default in variant)
- T - ambient temperature correction (K; default in variant)
- A - autotune C+R values
- F - force model self-test state (0=off 1=on) during autotune using
  current values

#### M400 - Wait for all moves to finish [M400: Wait for current moves to finish](https://reprap.org/wiki/G-code#M400:_Wait_for_current_moves_to_finish)

Finishes all current moves and and thus clears the buffer. Equivalent to
`G4` with no parameters.

#### M403 - Set filament type (material) for particular extruder and notify the MMU [M403 - Set filament type (material) for particular extruder and notify the MMU](https://reprap.org/wiki/G-code#M403:_Set_filament_type_.28material.29_for_particular_extruder_and_notify_the_MMU.)

Currently three different materials are needed (default, flex and PVA).\
And storing this information for different load/unload profiles etc. in
the future firmware does not have to wait for \"ok\" from MMU.

#### Usage

``` fragment
M403 [ E | F ]
```

#### Parameters

- `E` - Extruder number. 0-indexed.
- `F` - Filament type

#### M405 - Filament Sensor on [M405: Filament Sensor on](https://reprap.org/wiki/G-code#M405:_Filament_Sensor_on)

Turn on Filament Sensor extrusion control.

#### Usage

    M405

#### M406 - Filament Sensor off [M406: Filament Sensor off](https://reprap.org/wiki/G-code#M406:_Filament_Sensor_off)

Turn off Filament Sensor extrusion control.

#### Usage

    M406

#### M420 - Mesh bed leveling status [M420: Mesh bed leveling status](https://reprap.org/wiki/G-code#M420:_Mesh_bed_leveling_status)

Prints mesh bed leveling status and bed profile if activated.

#### M500 - Store settings in EEPROM [M500: Store parameters in non-volatile storage](https://reprap.org/wiki/G-code#M500:_Store_parameters_in_non-volatile_storage)

Save current parameters to EEPROM.

#### M501 - Read settings from EEPROM [M501: Read parameters from EEPROM](https://reprap.org/wiki/G-code#M501:_Read_parameters_from_EEPROM)

Set the active parameters to those stored in the EEPROM. This is useful
to revert parameters after experimenting with them.

#### M502 - Revert all settings to factory default [M502: Restore Default Settings](https://reprap.org/wiki/G-code#M502:_Restore_Default_Settings)

This command resets all tunable parameters to their default values, as
set in the firmware\'s configuration files. This doesn\'t reset any
parameters stored in the EEPROM, so it must be followed by M500 to write
the default settings.

#### M503 - Repport all settings currently in memory [M503: Report Current Settings](https://reprap.org/wiki/G-code#M503:_Report_Current_Settings)

This command asks the firmware to reply with the current print settings
as set in memory. Settings will differ from EEPROM contents if changed
since the last load / save. The reply output includes the G-Code
commands to produce each setting. For example, Steps-Per-Unit values are
displayed as an M92 command.

#### M509 - Force language selection [M509: Force language selection](https://reprap.org/wiki/G-code#M509:_Force_language_selection)

Resets the language to English. Only on Original Prusa i3 MK2.5/s and
MK3/s with multiple languages.

#### M540 - Abort print on endstop hit (enable/disable) [M540 in Marlin: Enable/Disable \"Stop SD Print on Endstop Hit\"](https://reprap.org/wiki/G-code#M540_in_Marlin:_Enable.2FDisable_.22Stop_SD_Print_on_Endstop_Hit.22)

In Prusa Firmware this G-code is deactivated by default, must be turned
on in the source code. You must define
`ABORT_ON_ENDSTOP_HIT_FEATURE_ENABLED`.

#### Usage

``` fragment
M540 [ S ]
```

#### Parameters

- `S` - disabled=0, enabled=1

#### M851 - Set Z-Probe Offset [M851: Set Z-Probe Offset\"](https://reprap.org/wiki/G-code#M851:_Set_Z-Probe_Offset)

Sets the Z-probe Z offset. This offset is used to determine the actual Z
position of the nozzle when using a probe to home Z with G28. This value
may also be used by G81 (Prusa) / G29 (Marlin) to apply correction to
the Z position. This value represents the distance from nozzle to the
bed surface at the point where the probe is triggered. This value will
be negative for typical switch probes, inductive probes, and setups
where the nozzle makes a circuit with a raised metal contact. This
setting will be greater than zero on machines where the nozzle itself is
used as the probe, pressing down on the bed to press a switch. (This is
a common setup on delta machines.)

#### Usage

``` fragment
M851 [ Z ]
```

#### Parameters

- `Z` - Z offset probe to nozzle.

#### M552 - Set IP address [M552: Set IP address, enable/disable network interface\"](https://reprap.org/wiki/G-code#M552:_Set_IP_address.2C_enable.2Fdisable_network_interface)

Sets the printer IP address that is shown in the support menu. Designed
to be used with the help of host software. If P is not specified nothing
happens. If the structure of the IP address is invalid, 0.0.0.0 is
assumed and nothing is shown on the screen in the Support menu.

#### Usage

``` fragment
M552 [ P ]
```

#### Parameters

- `P` - The IP address in xxx.xxx.xxx.xxx format. Eg: P192.168.1.14

#### M600 - Initiate Filament change procedure [M600: Filament change pause](https://reprap.org/wiki/G-code#M600:_Filament_change_pause)

Initiates Filament change, it is also used during Filament Runout Sensor
process. If the `M600` is triggered under 25mm it will do a Z-lift of
25mm to prevent a filament blob.

#### Usage

``` fragment
M600 [ X | Y | Z | E | L | AUTO ]
```

- `X` - X position, default 211
- `Y` - Y position, default 0
- `Z` - relative lift Z, default 2.
- `E` - initial retract, default -2
- `L` - later retract distance for removal, default -80
- `AUTO` - Automatically (only with MMU)

#### M601 - Pause print [M601: Pause print](https://reprap.org/wiki/G-code#M601:_Pause_print)

Without any parameters it will park the extruder to default or last set
position. The default pause position will be set during power up and a
reset, the new pause positions aren\'t permanent.

#### Usage

     M601 [ X | Y | Z | S ]

#### Parameters

- X - X position to park at (default X_PAUSE_POS 50) these are saved
  until change or reset.
- Y - Y position to park at (default Y_PAUSE_POS 190) these are saved
  until change or reset.
- Z - Z raise before park (default Z_PAUSE_LIFT 20) these are saved
  until change or reset.
- S - Set values without pausing

#### M125 - Pause print [M125: Pause print](https://reprap.org/wiki/G-code#M125:_Pause_print)

Without any parameters it will park the extruder to default or last set
position. The default pause position will be set during power up and a
reset, the new pause positions aren\'t permanent.

#### Usage

     M125 [ X | Y | Z | S ]

#### Parameters

- X - X position to park at (default X_PAUSE_POS 50) these are saved
  until change or reset.
- Y - Y position to park at (default Y_PAUSE_POS 190) these are saved
  until change or reset.
- Z - Z raise before park (default Z_PAUSE_LIFT 20) these are saved
  until change or reset.
- S - Set values without pausing

#### M25 - Pause SD print [M25: Pause SD print](https://reprap.org/wiki/G-code#M25:_Pause_SD_print)

Without any parameters it will park the extruder to default or last set
position. The default pause position will be set during power up and a
reset, the new pause positions aren\'t permanent.

#### Usage

     M25 [ X | Y | Z | S ]

#### Parameters

- X - X position to park at (default X_PAUSE_POS 50) these are saved
  until change or reset.
- Y - Y position to park at (default Y_PAUSE_POS 190) these are saved
  until change or reset.
- Z - Z raise before park (default Z_PAUSE_LIFT 20) these are saved
  until change or reset.
- S - Set values without pausing

#### M602 - Resume print [M602: Resume print](https://reprap.org/wiki/G-code#M602:_Resume_print)

#### M603 - Stop print [M603: Stop print](https://reprap.org/wiki/G-code#M603:_Stop_print)

#### M850 - Set steel sheet parameters

Get and Set Sheet parameters.

#### Usage:

    M850 [ S | Z | L | B | P | A ]

#### Parameters

- S Sheet id \[0-7\]
- Z \[offset\]
- L - Label \[aA-zZ, 0-9 max 7 chars\]
- B \[Bed temp\]
- P \[PINDA temp\]
- A - Active \[0\|1\]

#### Notes

Z and L are optional, if one or both are missing the current values are
reported instead.\
If L and/or Z are specified, the sheet\'s values are updated.\
Z range is validated\
Sheet index is validated\
Requesting info (no L or Z) on an uncalibrated sheet reports as such.

Pronterface capitalizes anything sent. To use lowercase in your sheet
names you\'ll need to use a different terminal program.

#### M860 - Wait for extruder temperature (PINDA) [M860 Wait for Probe Temperature](https://reprap.org/wiki/G-code#M860_Wait_for_Probe_Temperature)

Wait for PINDA thermistor to reach target temperature

#### Usage

``` fragment
M860 [ S ]
```

#### Parameters

- `S` - Target temperature

#### M861 - Set/Get PINDA temperature compensation offsets [M861 Set Probe Thermal Compensation](https://reprap.org/wiki/G-code#M861_Set_Probe_Thermal_Compensation)

Set compensation ustep value `S` for compensation table index `I`.

#### Usage

``` fragment
M861 [ ? | ! | Z | S | I ]
```

#### Parameters

- `?` - Print current EEPROM offset values
- `!` - Set factory default values
- `Z` - Set all values to 0 (effectively disabling PINDA temperature
  compensation)
- `S` - Microsteps
- `I` - Table index

#### M862 - Print checking [M862: Print checking](https://reprap.org/wiki/G-code#M862:_Print_checking)

Checks the parameters of the printer and gcode and performs
compatibility check

- M862.1 { P \| Q } 0.25/0.40/0.60
- M862.2 { P \| Q }
- M862.3 { P\"\" \| Q }
- M862.4 { P \| Q }
- M862.5 { P \| Q }
- M862.6 Not used but reserved by 32-bit

When run with P\<\> argument, the check is performed against the input
value. When run with Q argument, the current value is shown.

M862.3 accepts text identifiers of printer types too. The syntax of
M862.3 is (note the quotes around the type):

``` fragment
M862.3 P "MK3S"
```

Accepted printer type identifiers and their numeric counterparts:

- MK1 (100)
- MK2 (200)
- MK2MM (201)
- MK2S (202)
- MK2SMM (203)
- MK2.5 (250)
- MK2.5MMU2 (20250)
- MK2.5S (252)
- MK2.5SMMU2S (20252)
- MK3 (300)
- MK3MMU2 (20300)
- MK3MMU3 (30300)
- MK3S (302)
- MK3SMMU2S (20302)
- MK3SMMU3 (30302)

#### M900 - Set Linear advance options [M900 Set Linear Advance Scaling Factors](https://reprap.org/wiki/G-code#M900_Set_Linear_Advance_Scaling_Factors)

Sets the advance extrusion factors for Linear Advance. If any of the R,
W, H, or D parameters are set to zero the ratio will be computed
dynamically during printing.

#### Usage

``` fragment
M900 [ K | R | W | H | D]
```

#### Parameters

- `K` - Advance K factor
- `R` - Set ratio directly (overrides WH/D)
- `W` - Width
- `H` - Height
- `D` - Diameter Set ratio from WH/D

#### M907 - Set digital trimpot motor current in mA using axis codes [M907: Set digital trimpot motor](https://reprap.org/wiki/G-code#M907:_Set_digital_trimpot_motor)

Set digital trimpot motor current using axis codes (X, Y, Z, E, B, S).
M907 has no effect when the experimental Extruder motor current scaling
mode is active (that applies to farm printing as well)

#### Usage

``` fragment
M907 [ X | Y | Z | E | B | S ]
```

#### Parameters

- `X` - X motor driver
- `Y` - Y motor driver
- `Z` - Z motor driver
- `E` - Extruder motor driver
- `B` - Second Extruder motor driver
- `S` - All motors

#### M908 - Control digital trimpot directly [M908: Control digital trimpot directly](https://reprap.org/wiki/G-code#M908:_Control_digital_trimpot_directly)

In Prusa Firmware this G-code is deactivated by default, must be turned
on in the source code. Not usable on Prusa printers.

#### Usage

``` fragment
M908 [ P | S ]
```

#### Parameters

- `P` - channel
- `S` - current

#### M910 - TMC2130 init [M910: TMC2130 init](https://reprap.org/wiki/G-code#M910:_TMC2130_init)

Not active in default, only if `TMC2130_SERVICE_CODES_M910_M918` is
defined in source code.

#### M911 - Set TMC2130 holding currents [M911: Set TMC2130 holding currents](https://reprap.org/wiki/G-code#M911:_Set_TMC2130_holding_currents)

Not active in default, only if `TMC2130_SERVICE_CODES_M910_M918` is
defined in source code.

#### Usage

``` fragment
M911 [ X | Y | Z | E ]
```

#### Parameters

- `X` - X stepper driver holding current value
- `Y` - Y stepper driver holding current value
- `Z` - Z stepper driver holding current value
- `E` - Extruder stepper driver holding current value

#### M912 - Set TMC2130 running currents [M912: Set TMC2130 running currents](https://reprap.org/wiki/G-code#M912:_Set_TMC2130_running_currents)

Not active in default, only if `TMC2130_SERVICE_CODES_M910_M918` is
defined in source code.

#### Usage

``` fragment
M912 [ X | Y | Z | E ]
```

#### Parameters

- `X` - X stepper driver running current value
- `Y` - Y stepper driver running current value
- `Z` - Z stepper driver running current value
- `E` - Extruder stepper driver running current value

#### M913 - Print TMC2130 currents [M913: Print TMC2130 currents](https://reprap.org/wiki/G-code#M913:_Print_TMC2130_currents)

Not active in default, only if `TMC2130_SERVICE_CODES_M910_M918` is
defined in source code. Shows TMC2130 currents.

#### M914 - Set TMC2130 normal mode [M914: Set TMC2130 normal mode](https://reprap.org/wiki/G-code#M914:_Set_TMC2130_normal_mode)

Updates EEPROM only if \"P\" is given, otherwise temporary (lasts until
reset or motor idle timeout)

#### Usage

    M914 [ P | R | Q ]

#### Parameters

- P - Make the mode change permanent (write to EEPROM)
- R - Revert to EEPROM value
- Q - Print effective silent/normal status. (Does not report override)

#### M915 - Set TMC2130 silent mode [M915: Set TMC2130 silent mode](https://reprap.org/wiki/G-code#M915:_Set_TMC2130_silent_mode)

Updates EEPROM only if \"P\" is given, otherwise temporary (lasts until
reset or motor idle timeout)

#### Usage

    M915 [ P | R | Q]

#### Parameters

- P - Make the mode change permanent (write to EEPROM)
- R - Revert to EEPROM value
- Q - Print effective silent/normal status. (Does not report override)

#### M916 - Set TMC2130 Stallguard sensitivity threshold [M916: Set TMC2130 Stallguard sensitivity threshold](https://reprap.org/wiki/G-code#M916:_Set_TMC2130_Stallguard_sensitivity_threshold)

Not active in default, only if `TMC2130_SERVICE_CODES_M910_M918` is
defined in source code.

#### Usage

``` fragment
M916 [ X | Y | Z | E ]
```

#### Parameters

- `X` - X stepper driver stallguard sensitivity threshold value
- `Y` - Y stepper driver stallguard sensitivity threshold value
- `Z` - Z stepper driver stallguard sensitivity threshold value
- `E` - Extruder stepper driver stallguard sensitivity threshold value

#### M917 - Set TMC2130 PWM amplitude offset (pwm_ampl) [M917: Set TMC2130 PWM amplitude offset (pwm_ampl)](https://reprap.org/wiki/G-code#M917:_Set_TMC2130_PWM_amplitude_offset_.28pwm_ampl.29)

Not active in default, only if `TMC2130_SERVICE_CODES_M910_M918` is
defined in source code.

#### Usage

``` fragment
M917 [ X | Y | Z | E ]
```

#### Parameters

- `X` - X stepper driver PWM amplitude offset value
- `Y` - Y stepper driver PWM amplitude offset value
- `Z` - Z stepper driver PWM amplitude offset value
- `E` - Extruder stepper driver PWM amplitude offset value

#### M918 - Set TMC2130 PWM amplitude gradient (pwm_grad) [M918: Set TMC2130 PWM amplitude gradient (pwm_grad)](https://reprap.org/wiki/G-code#M918:_Set_TMC2130_PWM_amplitude_gradient_.28pwm_grad.29)

Not active in default, only if `TMC2130_SERVICE_CODES_M910_M918` is
defined in source code.

#### Usage

``` fragment
M918 [ X | Y | Z | E ]
```

#### Parameters

- `X` - X stepper driver PWM amplitude gradient value
- `Y` - Y stepper driver PWM amplitude gradient value
- `Z` - Z stepper driver PWM amplitude gradient value
- `E` - Extruder stepper driver PWM amplitude gradient value

#### M350 - Set microstepping mode [M350: Set microstepping mode](https://reprap.org/wiki/G-code#M350:_Set_microstepping_mode)

Printers with TMC2130 drivers have `X`, `Y`, `Z` and `E` as options. The
steps-per-unit value is updated accordingly. Not all resolutions are
valid! Printers without TMC2130 drivers also have `B` and `S` options.
In this case, the steps-per-unit value in not changed!

#### Usage

``` fragment
M350 [ X | Y | Z | E | B | S ]
```

#### Parameters

- `X` - X new resolution
- `Y` - Y new resolution
- `Z` - Z new resolution
- `E` - E new resolution

Only valid for MK2.5(S) or printers without TMC2130 drivers

- `B` - Second extruder new resolution
- `S` - All axes new resolution

#### M351 - Toggle Microstep Pins [M351: Toggle MS1 MS2 pins directly](https://reprap.org/wiki/G-code#M351:_Toggle_MS1_MS2_pins_directly)

Toggle MS1 MS2 pins directly.

#### Usage

``` fragment
M351 [B<0|1>] [E<0|1>] S<1|2> [X<0|1>] [Y<0|1>] [Z<0|1>]
```

#### Parameters

- `X` - Update X axis
- `Y` - Update Y axis
- `Z` - Update Z axis
- `E` - Update E axis
- `S` - which MSx pin to toggle
- `B` - new pin value

#### M701 - Load filament to extruder [M701: Load filament](https://reprap.org/wiki/G-code#M701:_Load_filament)

Load filament into the active extruder.

#### Usage

    M701 [ P | T | L | Z ]

#### Parameters

- P - n index of MMU slot (zero based, so 0-4 like T0 and T4)
- T - Alias of P. Used for compatibility with Marlin
- L - Extrude distance for insertion (positive value)(manual reload)
- Z - Move the Z axis by this distance. Default value is 0 to maintain
  backwards compatibility with older gcodes.

 

#### G80 - Unload filament [M702: Unload filament](https://reprap.org/wiki/G-code#M702:_Unload_filament)

#### Usage

``` fragment
M702 [ U | Z ]
```

#### Parameters

- U - Retract distance for removal (manual reload). Default value is
  FILAMENTCHANGE_FINALRETRACT.
- Z - Move the Z axis by this distance. Default value is 0 to maintain
  backwards compatibility with older gcodes.

#### M704 - Preload to MMU [M704: Preload to MMU](https://reprap.org/wiki/G-code#M704:_Preload_to_MMU)

#### Usage

    M704 [ P ]

#### Parameters

- P - n index of slot (zero based, so 0-4 like T0 and T4)

#### M705 - Eject filament [M705: Eject filament](https://reprap.org/wiki/G-code#M705:_Eject_filament)

#### Usage

    M705 [ P ]

#### Parameters

- P - n index of slot (zero based, so 0-4 like T0 and T4)

#### M706 - Cut filament [M706: Cut filament](https://reprap.org/wiki/G-code#M706:_Cut_filament)

#### Usage

    M706 [ P ]

#### Parameters

- P - n index of slot (zero based, so 0-4 like T0 and T4)

#### M707 - Read value from [MMU3 register](http://help.prusa3d.com/article/registers-mmu-mmu3_511780), [M707: Read from MMU register](https://reprap.org/wiki/G-code#M707:_Read_from_MMU_register)

#### Usage

    M707 [ A ]

#### Parameters

- A - Address of register in hexidecimal.

#### Example

M707 A0X19 - Read a 8bit integer from register 0X19 (Idler_sg_thrs_R)
and prints the result onto the serial line.

Does nothing if the A parameter is not present or if MMU is not enabled.

#### M708 - Write value to [MMU3 register](http://help.prusa3d.com/article/registers-mmu-mmu3_511780), [M708: Write to MMU register](https://reprap.org/wiki/G-code#M708:_Write_to_MMU_register)

#### Usage

    M708 [ A | X ]

#### Parameters

- A - Address of register in hexidecimal.
- X - Data to write (16-bit integer). Default value 0.

#### Example

M708 A0x19 X07 - Write to register 0x19 (Idler_sg_thrs_R) the value 07.
Does nothing if A parameter is missing or if MMU is not enabled.

#### M709 - MMU reset M709: MMU reset

The MK3S cannot not power off the MMU, for that reason the functionality
is not supported.

#### Usage

    M709 [ S | X ]

#### Parameters

- X - Reset MMU (0:soft reset \| 1:hardware reset)

- S - En-/disable the MMU (0:off \| 1:on)

#### Example

M709 X0 - issue an X0 command via communication into the MMU (soft
reset)

M709 X1 - toggle the MMU\'s reset pin (hardware reset)

M709 X42 - erase MMU EEPROM

M709 S1 - enable MMU

M709 S0 - disable MMU

M709 - Serial message if en- or disabled

#### M999 - Restart after being stopped [M999: Restart after being stopped by error](https://reprap.org/wiki/G-code#M999:_Restart_after_being_stopped_by_error)

End of M-Commands

------------------------------------------------------------------------

<div>

### T Codes

</div>

**T** - Select extruder in case of multi extruder printer or MMU1.
Select filament position 1-5 (T0-T4) in case of MMU2/S or MMU3.

#### For MMU1:

**T? -** Printer asks user to select a filament position. Then loads the
desired filament from the multiplexer (Y-splitter) into the nozzle.

#### For MMU2/S / MMU3:

**T - **Selects the filament position. A Gcode to load a filament to the
nozzle must follow.

**Tx** - Printer asks user to select a filament position. Then loads the
filament from the MMU unit into the extruder wheels only. G-code to heat
up the nozzle follows.

**Tc** - Loads the filament tip from the extruder wheels into the
nozzle.

#### End of T-Codes

------------------------------------------------------------------------

<div>

### D codes

</div>

#### D-1 - Endless Loop [D-1: Endless Loop](https://reprap.org/wiki/G-code#D-1:_Endless_Loop)

#### D0 - Reset [D0: Reset](https://reprap.org/wiki/G-code#D0:_Reset)

#### Usage

``` fragment
D0 [ B ]
```

#### Parameters

- `B` - Bootloader

#### D1 - Clear EEPROM and RESET [D1: Clear EEPROM and RESET](https://reprap.org/wiki/G-code#D1:_Clear_EEPROM_and_RESET)

``` fragment
D1
```

#### D2 - Read/Write RAM [D3: Read/Write RAM](https://reprap.org/wiki/G-code#D2:_Read.2FWrite_RAM)

This command can be used without any additional parameters. It will read
the entire RAM.

#### Usage

``` fragment
D2 [ A | C | X ]
```

#### Parameters

- `A` - Address (x0000-x1fff)
- `C` - Count (1-8192)
- `X` - Data

#### Notes

- The hex address needs to be lowercase without the 0 before the x
- Count is decimal
- The hex data needs to be lowercase

#### D3 - Read/Write EEPROM [D3: Read/Write EEPROM](https://reprap.org/wiki/G-code#D3:_Read.2FWrite_EEPROM)

This command can be used without any additional parameters. It will read
the entire eeprom.

#### Usage

``` fragment
D3 [ A | C | X ]
```

#### Parameters

- `A` - Address (x0000-x0fff)
- `C` - Count (1-4096)
- `X` - Data (hex)

#### Notes

- The hex address needs to be lowercase without the 0 before the x
- Count is decimal
- The hex data needs to be lowercase

#### D4 - Read/Write PIN [D4: Read/Write PIN](https://reprap.org/wiki/G-code#D4:_Read.2FWrite_PIN)

To read the digital value of a pin you need only to define the pin
number.

#### Usage

``` fragment
D4 [ P | F | V ]
```

#### Parameters

- `P` - Pin (0-255)
- `F` - Function in/out (0/1)
- `V` - Value (0/1)

#### D5 - Read/Write FLASH [D5: Read/Write Flash](https://reprap.org/wiki/G-code#D5:_Read.2FWrite_FLASH)

This command can be used without any additional parameters. It will read
the 1kb FLASH.

#### Usage

``` fragment
D5 [ A | C | X | E ]
```

#### Parameters

- `A` - Address (x00000-x3ffff)
- `C` - Count (1-8192)
- `X` - Data (hex)
- `E` - Erase

#### Notes

- The hex address needs to be lowercase without the 0 before the x
- Count is decimal
- The hex data needs to be lowercase

#### D6 - Read/Write external FLASH [D6: Read/Write external Flash](https://reprap.org/wiki/G-code#D6:_Read.2FWrite_external_FLASH)

Reserved

#### D7 - Read/Write Bootloader [D7: Read/Write Bootloader](https://reprap.org/wiki/G-code#D7:_Read.2FWrite_Bootloader)

Reserved

#### D8 - Read/Write PINDA [D8: Read/Write PINDA](https://reprap.org/wiki/G-code#D8:_Read.2FWrite_PINDA)

#### Usage

``` fragment
D8 [ ? | ! | P | Z ]
```

#### Parameters

- `?` - Read PINDA temperature shift values
- `!` - Reset PINDA temperature shift values to default
- `P` - Pinda temperature \[C\]
- `Z` - Z Offset \[mm\]

#### D9 - Read ADC [D9: Read ADC](https://reprap.org/wiki/G-code#D9:_Read.2FWrite_ADC)

#### Usage

``` fragment
D9 [ I | V ]
```

#### Parameters

- `I` - ADC channel index
  - `0` - Heater 0 temperature
  - `1` - Heater 1 temperature
  - `2` - Bed temperature
  - `3` - PINDA temperature
  - `4` - PWR voltage
  - `5` - Ambient temperature
  - `6` - BED voltage
- `V` Value to be written as simulated

#### D10 - Set XYZ calibration = OK [D10: Set XYZ calibration = OK](https://reprap.org/wiki/G-code#D10:_Set_XYZ_calibration_.3D_OK)

#### D12 - Time [D12: Time](https://reprap.org/wiki/G-code#D12:_Time)

Writes the current time in the log file.

#### D20 - Generate an offline crash dump D20: [Generate an offline crash dump](https://reprap.org/wiki/G-code#D20:_Generate_an_offline_crash_dump)

Generate a crash dump for later retrival.

#### Usage

    D20 [E]

#### Parameters

- E - Perform an emergency crash dump (resets the printer).

#### Notes

- A crash dump can be later recovered with D21, or cleared with D22.
- An emergency crash dump includes register data, but will cause the
  printer to reset after the dump is completed.

#### D21 - Print crash dump to serial [D21: Print crash dump to serial](https://reprap.org/wiki/G-code#D21:_Print_crash_dump_to_serial)

Output the complete crash dump (if present) to the serial.

#### Usage

    D21

#### Notes

The starting address can vary between builds, but it\'s always at the
beginning of the data section.

#### D22 - Clear crash dump state [D22: Clear crash dump state](https://reprap.org/wiki/G-code#D22:_Clear_crash_dump_state)

Clear an existing internal crash dump.

#### Usage

    D22

#### D23 - Request emergency dump on serial [D23: Request emergency dump on serial](https://reprap.org/wiki/G-code#D23:_Request_emergency_dump_on_serial)

On boards without offline dump support, request online dumps to the
serial port on firmware faults. When online dumps are enabled, the FW
will dump memory on the serial before resetting.

#### Usage

    D23 [E] [R]

#### Parameters

- E - Perform an emergency crash dump (resets the printer).
- R - Disable online dumps.

#### D70 - Enable low-level thermal model logging for offline simulation

#### Usage

    D70 [ S ]

#### Parameters

- S - Enable 0-1 (default 0)

#### D80 - Bed check [D80: Bed check](https://reprap.org/wiki/G-code#D80:_Bed_check)

This command will log data to SD card file \"mesh.txt\".

#### Usage

``` fragment
D80 [ E | F | G | H | I | J ]
```

#### Parameters

- `E` - Dimension X (default 40)
- `F` - Dimention Y (default 40)
- `G` - Points X (default 40)
- `H` - Points Y (default 40)
- `I` - Offset X (default 74)
- `J` - Offset Y (default 34)

#### D81 - Bed analysis [D80: Bed analysis](https://reprap.org/wiki/G-code#D81:_Bed_analysis)

This command will log data to SD card file \"wldsd.txt\".

#### Usage

``` fragment
D81 [ E | F | G | H | I | J ]
```

#### Parameters

- `E` - Dimension X (default 40)
- `F` - Dimention Y (default 40)
- `G` - Points X (default 40)
- `H` - Points Y (default 40)
- `I` - Offset X (default 74)
- `J` - Offset Y (default 34)

#### D106 - Print measured fan speed for different pwm values [D106: Print measured fan speed for different pwm values](https://reprap.org/wiki/G-code#D106:_Print_measured_fan_speed_for_different_pwm_values)

#### D2130 - Trinamic stepper controller [D2130: Trinamic stepper controller](https://reprap.org/wiki/G-code#D2130:_Trinamic_stepper_controller)

#### Usage

``` fragment
D2130 [ Axis | Command | Subcommand | Value ]
```

#### Parameters

- Axis
  - `X` - X stepper driver
  - `Y` - Y stepper driver
  - `Z` - Z stepper driver
  - `E` - Extruder stepper driver
- Commands
  - `0` - Current off
  - `1` - Current on
  - `+` - Single step
  - `-` - Single step oposite direction
  - `NNN` - Value sereval steps
  - `?` - Read register
  - Subcommands for read register
    - `mres` - Micro step resolution. More information in datasheet
      \'5.5.2 CHOPCONF -- Chopper Configuration\'
    - `step` - Step
    - `mscnt` - Microstep counter. More information in datasheet \'5.5
      Motor Driver Registers\'
    - `mscuract` - Actual microstep current for motor. More information
      in datasheet \'5.5 Motor Driver Registers\'
    - `wave` - Microstep linearity compensation curve
  - `!` - Set register
  - Subcommands for set register
    - `mres` - Micro step resolution
    - `step` - Step
    - `wave` - Microstep linearity compensation curve
    - Values for set register
      - `0, 180 --> 250` - Off
      - `0.9 --> 1.25` - Valid values (recommended is 1.1)
  - `@` - Home calibrate axis

Examples:

``` fragment
D2130E?wave
```

Print extruder microstep linearity compensation curve

``` fragment
D2130E!wave0
```

Disable extruder linearity compensation curve, (sine curve is used)

``` fragment
D2130E!wave220
```

(sin(x))\^1.1 extruder microstep compensation curve used

Notes: For more information see
<https://www.trinamic.com/fileadmin/assets/Products/ICs_Documents/TMC2130_datasheet.pdf>

#### D9125 - PAT9125 filament sensor [D9125: PAT9125 filament sensor](https://reprap.org/wiki/G-code#D9:_Read.2FWrite_ADC)

#### Usage

``` fragment
D9125 [ ? | ! | R | X | Y | L ]
```

#### Parameters

- `?` - Print values
- `!` - Print values
- `R` - Resolution. Not active in code
- `X` - X values
- `Y` - Y values
- `L` - Activate filament sensor log

#### End of D-Codes
::::::::::::::::

::: {.sc-2e655ea2-0 .jwCGom}
 
:::

::::::::::::::::::::::::::::::::: {.lines style="vertical-align:top;align-items:start;justify-content:start;max-width:1280px;margin:2.5rem auto;gap:1.8rem"}
:::::::: {style="display:flex;gap:1rem;width:100%"}
::: {.thumb .pulse style="width:1.5rem;background-color:#e0e0e0;border-radius:0.5rem;flex-shrink:0;height:2rem"}
:::

:::::: {style="display:flex;flex-direction:column;gap:0.5rem;width:100%"}
::: {.line .pulse style="width:50%;background-color:#e0e0e0;border-radius:0.5rem;flex-shrink:0;height:2rem"}
:::

::: {.line .pulse style="width:100%;background-color:#e0e0e0;border-radius:0.5rem;flex-shrink:0"}
:::

::: {.line .pulse style="width:100%;background-color:#e0e0e0;border-radius:0.5rem;flex-shrink:0"}
:::
::::::
::::::::

:::::::: {style="display:flex;gap:1rem;width:100%"}
::: {.thumb .pulse style="width:1.5rem;background-color:#e0e0e0;border-radius:0.5rem;flex-shrink:0;height:2rem"}
:::

:::::: {style="display:flex;flex-direction:column;gap:0.5rem;width:100%"}
::: {.line .pulse style="width:50%;background-color:#e0e0e0;border-radius:0.5rem;flex-shrink:0;height:2rem"}
:::

::: {.line .pulse style="width:100%;background-color:#e0e0e0;border-radius:0.5rem;flex-shrink:0"}
:::

::: {.line .pulse style="width:100%;background-color:#e0e0e0;border-radius:0.5rem;flex-shrink:0"}
:::
::::::
::::::::

:::::::: {style="display:flex;gap:1rem;width:100%"}
::: {.thumb .pulse style="width:1.5rem;background-color:#e0e0e0;border-radius:0.5rem;flex-shrink:0;height:2rem"}
:::

:::::: {style="display:flex;flex-direction:column;gap:0.5rem;width:100%"}
::: {.line .pulse style="width:50%;background-color:#e0e0e0;border-radius:0.5rem;flex-shrink:0;height:2rem"}
:::

::: {.line .pulse style="width:100%;background-color:#e0e0e0;border-radius:0.5rem;flex-shrink:0"}
:::

::: {.line .pulse style="width:100%;background-color:#e0e0e0;border-radius:0.5rem;flex-shrink:0"}
:::
::::::
::::::::

:::::::: {style="display:flex;gap:1rem;width:100%"}
::: {.thumb .pulse style="width:1.5rem;background-color:#e0e0e0;border-radius:0.5rem;flex-shrink:0;height:2rem"}
:::

:::::: {style="display:flex;flex-direction:column;gap:0.5rem;width:100%"}
::: {.line .pulse style="width:50%;background-color:#e0e0e0;border-radius:0.5rem;flex-shrink:0;height:2rem"}
:::

::: {.line .pulse style="width:100%;background-color:#e0e0e0;border-radius:0.5rem;flex-shrink:0"}
:::

::: {.line .pulse style="width:100%;background-color:#e0e0e0;border-radius:0.5rem;flex-shrink:0"}
:::
::::::
::::::::

:::::::: {style="display:flex;gap:1rem;width:100%"}
::: {.thumb .pulse style="width:1.5rem;background-color:#e0e0e0;border-radius:0.5rem;flex-shrink:0;height:2rem"}
:::

:::::: {style="display:flex;flex-direction:column;gap:0.5rem;width:100%"}
::: {.line .pulse style="width:50%;background-color:#e0e0e0;border-radius:0.5rem;flex-shrink:0;height:2rem"}
:::

::: {.line .pulse style="width:100%;background-color:#e0e0e0;border-radius:0.5rem;flex-shrink:0"}
:::

::: {.line .pulse style="width:100%;background-color:#e0e0e0;border-radius:0.5rem;flex-shrink:0"}
:::
::::::
::::::::
:::::::::::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::::::::::::
