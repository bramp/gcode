:::::::::::::::::::::::::::::::::::::::::: {.sc-3062e91e-0 .glZrnv role="main"}
::::::::: {.sc-87f52012-0 .kZqIwB}
This is a list of currently implemented G-Codes in [Prusa Buddy
firmware](https://github.com/prusa3d/Prusa-Firmware-Buddy) for
MINI/MINI+/XL/MK4/MK3.5 printers. The description is available only for
Prusa Research-specific G-codes or the ones having a specific
implementation.\
Since, Prusa Buddy firmware uses a fork of Marlin 2 firmware, the
generic G-codes should be Marlin-compatible and their description can be
found in [Marlin documentation](https://marlinfw.org/meta/gcode/) or on
[RepRap Wiki.](https://reprap.org/wiki/G-code)

::: {.sc-416e3c82-0 .hmjGvM .tip-callout type="tip-callout"}
![](data:image/svg+xml;base64,PHN2ZyBhcmlhLWhpZGRlbj0idHJ1ZSIgZm9jdXNhYmxlPSJmYWxzZSIgZGF0YS1wcmVmaXg9ImZhcyIgZGF0YS1pY29uPSJjaXJjbGUtaW5mbyIgY2xhc3M9InN2Zy1pbmxpbmUtLWZhIGZhLWNpcmNsZS1pbmZvIGZhLWxnICIgcm9sZT0iaW1nIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdib3g9IjAgMCA1MTIgNTEyIj48cGF0aCBmaWxsPSJjdXJyZW50Q29sb3IiIGQ9Ik0yNTYgNTEyQTI1NiAyNTYgMCAxIDAgMjU2IDBhMjU2IDI1NiAwIDEgMCAwIDUxMnpNMjE2IDMzNmwyNCAwIDAtNjQtMjQgMGMtMTMuMyAwLTI0LTEwLjctMjQtMjRzMTAuNy0yNCAyNC0yNGw0OCAwYzEzLjMgMCAyNCAxMC43IDI0IDI0bDAgODggOCAwYzEzLjMgMCAyNCAxMC43IDI0IDI0cy0xMC43IDI0LTI0IDI0bC04MCAwYy0xMy4zIDAtMjQtMTAuNy0yNC0yNHMxMC43LTI0IDI0LTI0em00MC0yMDhhMzIgMzIgMCAxIDEgMCA2NCAzMiAzMiAwIDEgMSAwLTY0eiIgLz48L3N2Zz4=){.svg-inline--fa
.fa-circle-info .fa-lg}For G-code documentation of Prusa firmware for i3
series printers (MK2.5/S, MK3/S/+ etc.), visit the [Prusa
firmware-specific G-code
commands](http://help.prusa3d.com/article/prusa-firmware-specific-g-code-commands_112173)
article.
:::

<div>

 

</div>

<div>

### G-codes

</div>

#### G0 - [G0 & G1: Move](https://reprap.org/wiki/G-code#G0_.26_G1:_Move)

#### G1 - [G0 & G1: Move](https://reprap.org/wiki/G-code#G0_.26_G1:_Move)

#### G2 - [G2 & G3: Controlled Arc Move](https://reprap.org/wiki/G-code#G2_.26_G3:_Controlled_Arc_Move)

#### G3 - [G2 & G3: Controlled Arc Move](https://reprap.org/wiki/G-code#G2_.26_G3:_Controlled_Arc_Move)

#### G4 - [G4: Dwell](https://reprap.org/wiki/G-code#G4:_Dwell)

#### G26 - [G26: Mesh Validation Pattern](https://reprap.org/wiki/G-code#G26:_Mesh_Validation_Pattern)

First layer calibration, must be run within selftest only.

#### G27 - [G27: Park toolhead](https://reprap.org/wiki/G-code#G27:_Park_toolhead)

See P0

#### G28 - [G28: Move to Origin (Home)](https://reprap.org/wiki/G-code#G28:_Move_to_Origin_.28Home.29)

Performs the precise homing. (with no MBL, even without the stadard W
parameter)

G28 issued without parameters homes the MMU3 as well. (invalidates the
homing flags of Selector and Idler. These will perform homing async once
it is considered safe, i.e. no filament in the selector)

**Parameters:**

- X, Y, Z: home the individual axes.
- C: home Z-axis only
- P: just invalidate the selector\'s homing validity flag
- I: just invalidate the idler\'s homing validity flag

#### G29 - [G29: Detailed Z-Probe](https://reprap.org/wiki/G-code#G29:_Detailed_Z-Probe)

Invalidates previous bed mesh measurements and starts the Mesh Bed
Leveling (MBL).

#### G30 - [G30: Single Z-Probe](https://reprap.org/wiki/G-code#G30:_Single_Z-Probe)

#### G54_59 - Select a new workspace 

(For iX printers only)\
A workspace is an XYZ offset to the machine native space. All workspaces
default to 0,0,0 at start, or with EEPROM support they may be restored
from a previous session.\
G92 is used to set the current workspace\'s offset.

#### G64 - Measure Z-Axis height

Measure the Z length and saves the max_z_pos into EEPROM. Then, it shows
the results on the serial line.

**Parameters:**

- D: Additional z offset

**Examples:**

G64 : Measure the Z length, save the measurement, show results on the
serial line.

G64 D0.2 : Execute the G64 command but add extra 0.2 to the measurement.

#### G65 - Advanced homing/part measurement

(For iX printers only)\
Homing to any endstop. Supports separate home positions in CNC
workspaces(G54-G59.3)(enabled by defining CNC_COORDINATE_SYSTEMS in
advanced config) Only supports homing of one axis at a time

Use: G65 \[AXIS\]\[ENDSTOP\] D\[DIRECTION\]\[DISTANCE\] \[AXIS\] Axis to
home(X, Y, Z, E) \[ENDSTOP\] Target endstop number. \[DIRECTION\]
Direction of homing \'+\' for positive or \'-\' for negative direction
\[DISTANCE\] Distance to travel. If endstop is not reached within this
distance, motion will stop and position will not be updated to endstop
position.

#### G75 - [G75: Print temperature interpolation](https://reprap.org/wiki/G-code#G75:_Print_temperature_interpolation)

#### G76 - [G76: PINDA probe temperature interpolation](https://reprap.org/wiki/G-code#G76:_PINDA_probe_temperature_calibration)

#### G80 - [G80: Mesh-based Z probe](https://reprap.org/wiki/G-code#G80:_Mesh-based_Z_probe)

For MK4 printer with MK3 G-code reverse compatibility.\
Performs the Mesh Bed Leveling as with the G29.

#### G90 - [G90: Set to Absolute Positioning](https://reprap.org/wiki/G-code#G90:_Set_to_Absolute_Positioning)

#### G91 - [G91: Set to Relative Positioning](https://reprap.org/wiki/G-code#G91:_Set_to_Relative_Positioning)

#### G92 - [G92: Set Position](https://reprap.org/wiki/G-code#G92:_Set_Position)

#### G162 - Calibrate Z

Z-axis leveling.

**Parameters:**

- Z: Calibrate Z.\
  With no parameters, no action is performed.

**Example:**

G162 Z : Level the Z-Axis.

#### G163 - Measure length of axis

**Parameters:**

- X, Y: Set an axis to measure the length on.
- S: Set sensitivity.
- P: Set measurement period.

#### G425 - [G425: Perform auto-calibration with calibration cube](https://reprap.org/wiki/G-code#G425:_Perform_auto-calibration_with_calibration_cube)

Automatic calibration with calibration object. Toolhead offset /
Backlash calibration

 

<div>

### M-codes

</div>

#### M0 - [M0: Stop or Unconditional stop](https://reprap.org/wiki/G-code#M0:_Stop_or_Unconditional_stop)

Pauses a print and waits for user interaction. 

#### M17 - [M17: Enable/Power all stepper motors](https://reprap.org/wiki/G-code#M17:_Enable.2FPower_all_stepper_motors)

#### M18 - [M18: Disable all stepper motors](https://reprap.org/wiki/G-code#M18:_Disable_all_stepper_motors)

#### M20 - [M20: List SD card](https://reprap.org/wiki/G-code#M20:_List_SD_card)

Lists the contents of the USB drive.

#### M23 - [M23: Select SD file](https://reprap.org/wiki/G-code#M23:_Select_SD_file)

Select a file from the USB drive.

#### M24 - [M24: Start/resume SD print](https://reprap.org/wiki/G-code#M24:_Start.2Fresume_SD_print)

Starts or resumes a print from USB drive.

#### M25 - [M25: Pause SD print](https://reprap.org/wiki/G-code#M25:_Pause_SD_print)

Pauses a print from the USB drive.

**Parameters:**

- U: Unload filament when paused

#### M27 - [M27: Report SD print status](https://reprap.org/wiki/G-code#M27:_Report_SD_print_status)

Reports a status of a print from USB drive.

#### M28 - [M28: Begin write to SD card](https://reprap.org/wiki/G-code#M28:_Begin_write_to_SD_card)

Related to USB drive instead.

#### M29 - [M29: Stop writing to SD card](https://reprap.org/wiki/G-code#M29:_Stop_writing_to_SD_card)

Related to USB drive instead.

#### M30 - [M30: Delete a file on the SD card ](https://reprap.org/wiki/G-code#M30:_Delete_a_file_on_the_SD_card)

Related to USB drive instead.

#### M31 - [M31: Output time since last M109 or SD card start to serial](https://reprap.org/wiki/G-code#M31:_Output_time_since_last_M109_or_SD_card_start_to_serial)

#### M32 - [M32: Select file and start SD print](https://reprap.org/wiki/G-code#M32:_Select_file_and_start_SD_print)

Related to USB drive instead.

#### M42 - [M42: Switch I/O pin](https://reprap.org/wiki/G-code#M42:_Switch_I.2FO_pin)

#### M46 - [M46: Show the assigned IP address](https://reprap.org/wiki/G-code#M46:_Show_the_assigned_IP_address)

#### M50 - Selftest

Enforce Selftest

**Parameters:**

- X: X axis test
- Y: Y axis test
- Z: Z axis test
- F: Fan test
- H: Heater test

#### M73 - [M73: Set/Get build percentage](https://reprap.org/wiki/G-code#M73:_Set.2FGet_build_percentage)

Tells the firmware the current build progress percentage to be
displayed.

**Parameters:**

- P: Percent finished
- R: Time remaining
- T: Time to pause

#### M74 - [M74: Set weight on print bed](https://reprap.org/wiki/G-code#M74:_Set_weight_on_print_bed)

Set mass. (Input shaper related)

**Parameters:**

- W: Set the total mass in grams of everything that is currently sitting
  on the bed.

#### M75 - [M75: Start print timer](https://reprap.org/wiki/G-code#M75:_Start_the_print_job_timer)

#### M76 - [M76: Pause print timer](https://reprap.org/wiki/G-code#M76:_Pause_the_print_job_timer)

#### M77 - [M77 Stop print job timer](https://reprap.org/wiki/G-code#M77:_Stop_the_print_job_timer)

#### M80 - [M80: ATX Power On](https://reprap.org/wiki/G-code#M80:_ATX_Power_On)

Turn on the Power Supply.

If you have a switch on suicide pin, this is useful if you want to start
another print with suicide feature after a print without a suicide\...

**Parameters:**

- S: Report the current state and exit

**Examples:**

- M80 : Turn on the Power Supply
- M80 S : Report the current state and exit

#### M81 - [M81: ATX Power Off](https://reprap.org/wiki/G-code#M81:_ATX_Power_Off)

Turn off Power, including Power Supply, if possible.

**Examples:**

M81: Turn off Power, including Power Supply, if there is one. This code
should ALWAYS be available for FULL SHUTDOWN!

#### M82 - [M82: Set extruder to absolute mode](https://reprap.org/wiki/G-code#M82:_Set_extruder_to_absolute_mode)

Set E axis normal mode (same as other axes).

#### M83 - [M83: Set extruder to relative mode](https://reprap.org/wiki/G-code#M83:_Set_extruder_to_relative_mode)

#### M84 - [M84: Stop idle hold](https://reprap.org/wiki/G-code#M84:_Stop_idle_hold)

Disable stepper motors / Set timeout.

**Parameters:**

- X, Y, Z, E:  Axis to disable stepper on

#### M85 - [M85: Set Inactivity Shutdown Timer](https://reprap.org/wiki/G-code#M85:_Set_Inactivity_Shutdown_Timer)

#### M86 - [M86: Set Safety Timeout](https://reprap.org/wiki/G-code#M86:_Set_Safety_Timeout)

#### M92 - [M92: Set axis_steps_per_unit](https://reprap.org/wiki/G-code#M92:_Set_axis_steps_per_unit)

#### M104 - [M104: Set Extruder Temperature](https://reprap.org/wiki/G-code#M104_in_Marlin_Firmware)

#### M105 - [M105: Get Extruder Temperature](https://reprap.org/wiki/G-code#M105:_Get_Extruder_Temperature)

#### M106 - [M106: Fan On](https://reprap.org/wiki/G-code#M106:_Fan_On)

#### M107 - [M107: Fan Off](https://reprap.org/wiki/G-code#M107:_Fan_Off)

#### M109 - [M109: Set Extruder Temperature and Wait](https://reprap.org/wiki/G-code#M109:_Set_Extruder_Temperature_and_Wait)

#### M110 - [M110: Set Current Line Number](https://reprap.org/wiki/G-code#M110:_Set_Current_Line_Number)

#### M111 - [M111: Set debug level](https://reprap.org/wiki/G-code#M111:_Set_Debug_Level)

#### M112 - [M112: Full (Emergency) Stop](https://reprap.org/wiki/G-code#M112:_Full_.28Emergency.29_Stop)

#### M113 - [M113: Host Keepalive](https://reprap.org/wiki/G-code#M113:_Host_Keepalive)

#### M114 - M114: Get Current Position

#### M115 - [M115: Get Firmware Version and Capabilities](https://reprap.org/wiki/G-code#M115:_Get_Firmware_Version_and_Capabilities)

#### M117 - [M117: Display Message](https://reprap.org/wiki/G-code#M117:_Display_Message)

Set LCD message text, if possible

#### M118 - [M118: Echo message on host ](https://reprap.org/wiki/G-code#M118:_Echo_message_on_host)

Display a message in the host console

#### M119 - [M119: Get Endstop Status](https://reprap.org/wiki/G-code#M119:_Get_Endstop_Status)

#### M120 - Enable endstops

#### M121 - Disable endstops

#### M122 - [M122: Debug Stepper drivers](https://reprap.org/wiki/G-code#M122:_Debug_Stepper_drivers_.28Marlin.29)

Report driver configuration and status.

#### M123 - [M123: Tachometer value](https://reprap.org/wiki/G-code#M123:_Tachometer_value_.28RepRap.2C_Prusa_.26_Marlin.29)

Print fan speed on serial port.

#### M125 - Store current position and move to parking position.

Called on pause (by M25) to prevent material leaking onto the object. On
resume (M24) the head will be moved back and the print will resume.\
 When not actively SD printing, M125 simply moves to the park position
and waits, resuming with a button click or M108. Without
PARK_HEAD_ON_PAUSE, the M125 command does nothing.

**Parameters:**

- L: override retract length
- X: override X
- Y: override Y
- Z: override Z raise

#### M140 - [M140: Set Bed Temperature (Fast)](https://reprap.org/wiki/G-code#M140:_Set_Bed_Temperature_.28Fast.29)

#### M142 - [M142: Set Cooler Temperature (Fast)](https://reprap.org/wiki/G-code#M142:_Set_Cooler_Temperature_.28Fast.29)

Set target heatbreak cooling temperature.

**Parameters:**

- S: Set heatbreak cooling temp in degree Celsius

#### M150 - [M150: Set LED color](https://reprap.org/wiki/G-code#M150:_Set_LED_color)

Set display LED color and animations. Color input supports RGB and HSV
format.\
LED strips on MK3.5, MK3.9, MK4, MINI, MINI+ and XL machines are not
user-configurable from a G-code!

**Parameters:**

RGB color space

- R: Red intensity from 0 to 255
- G: Green intensity from 0 to 255
- B: Blue intensity from 0 to 255

HSV color space

- H: Hue from 0 to 360
- S: Saturation from 0 to 100
- V: Saturation form 0 to 100

Effects

- A: animation type (SolidColor / Fading)
- S: printer state\
         - Idle,\
         - Printing,\
         - Pausing,\
         - Resuming,\
         - Aborting,\
         - Finishing,\
         - Warning,\
         - PowerPanic,\
         - PowerUp

#### M151 - LED control for Side LED lights

Basic settings are the same as for M150.

**Additional parameters:**

Effects

- D: duration in milliseconds, iX printer only: set to 0 for infinite
  duration
- T: transition in milliseconds (fade in / fade out)\
         - Fade in is counted toward duration, so if duration is greater
  than 0 and less than transition, the effect doesn\'t reach full color
  intensity.\
         - Fade out is not counted towards the duration.

#### M155 - [M155: Automatically send temperatures ](https://reprap.org/wiki/G-code#M155:_Automatically_send_temperatures)

Set temperature auto-report interval

#### M190 - [M190: Wait for bed temperature to reach target temp](https://reprap.org/wiki/G-code#M190:_Wait_for_bed_temperature_to_reach_target_temp)

#### M200 - [M200: Set filament diameter](https://reprap.org/wiki/G-code#M200:_Set_filament_diameter)

#### M201 - [M201: Set max acceleration](https://reprap.org/wiki/G-code#M202:_Set_max_travel_acceleration)

#### M203 - [M203: Set maximum feedrate](https://reprap.org/wiki/G-code#M203:_Set_maximum_feedrate)

#### M204 - [M204: Set default acceleration](https://reprap.org/wiki/G-code#M204:_Set_default_acceleration)

#### M205 - [M205: Advanced settings](https://reprap.org/wiki/G-code#M205:_Advanced_settings)

#### M206 - [M206: Offset axes](https://reprap.org/wiki/G-code#M206:_Offset_axes)

#### M211 - Enable, Disable, and/or Report software endstops

#### M217 - [M217: Toolchange Parameters](https://reprap.org/wiki/G-code#M217:_Toolchange_Parameters)

Set SINGLENOZZLE toolchange parameters. (MMU3)

**Parameters:**

- S\[linear\]:  Swap length (Requires TOOLCHANGE_FILAMENT_SWAP)
- E\[linear\]:   Purge length (Requires TOOLCHANGE_FILAMENT_SWAP)
- P\[linear/m\]: Prime speed (Requires TOOLCHANGE_FILAMENT_SWAP)
- R\[linear/m\]: Retract speed (Requires TOOLCHANGE_FILAMENT_SWAP)
- X\[linear\]:   Park X (Requires TOOLCHANGE_PARK)
- Y\[linear\]:   Park Y (Requires TOOLCHANGE_PARK)
- Z\[linear\]:   Z Raise

#### M218 - [M218: Set Hotend Offset](https://reprap.org/wiki/G-code#M218:_Set_Hotend_Offset)

For XL only.

#### M220 - [M220: Set speed factor override percentage](https://reprap.org/wiki/G-code#M220:_Set_speed_factor_override_percentage)

Set Feedrate Percentage.

**Parameters:**

- S: Feedrate Percentage

#### M221 - [M221: Set extrusion percentage](https://reprap.org/wiki/G-code#M221:_Set_extrude_factor_override_percentage)

**Parameters:**

- T: Tool number
- S: Extrusion rate Percentage

#### M226 - [M226: G-code Initiated Pause](https://reprap.org/wiki/G-code#M226:_G-code_Initiated_Pause)

Wait until a pin reaches a state

#### M290 - [M290: Babystepping](https://reprap.org/wiki/G-code#M290:_Babystepping)

#### M300 - [M300: Play beep sound](https://reprap.org/wiki/G-code#M300:_Play_beep_sound)

Beeep. Beep duration is limited to 0-5 seconds.\
 \
**Parameters:**

- S: Frequency in Hz
- P: Duration in ms
- V: Volume

#### M301 - [M301: Set PID parameters](https://reprap.org/wiki/G-code#M301:_Set_PID_parameters)

#### M302 - [M302: Allow cold extrudes](https://reprap.org/wiki/G-code#M302:_Allow_cold_extrudes)

Allow cold extrudes, or set the minimum extrude temperature

Parameters:  S sets the minimum extrude temperature\
  P enables (1) or disables (0) cold extrusion

**Examples:**

 M302         ; report current cold extrusion state\
 M302 P0      ; enable cold extrusion checking\
 M302 P1      ; disables cold extrusion checking\
 M302 S0      ; always allow extrusion (disables checking)\
 M302 S170    ; only allow extrusion above 170\
 M302 S170 P1 ; set min extrude temp to 170 but leave disabled

#### M303 - [M303: Run PID tuning](https://reprap.org/wiki/G-code#M303:_Run_PID_tuning)

PID relay autotune

**Parameters:**

- S: sets the target temperature. (default 150C / 70C)
- E: (-1 for the bed) (default 0)
- C: Minimum 3. Default 5.
- U: with a non-zero value will apply the result to current settings.

#### M304 - [M304: Set PID parameters - Bed](https://reprap.org/wiki/G-code#M304:_Set_PID_parameters_-_Bed)

#### M330 - Select handler

\*\*M330\*\*\` \` \-- Select \`handler\` for configuration (\`SYSLOG\`
is selected by default)

**Example:**

\`M330 SYSLOG\`

#### M331 - Enable metrics

\*\*M331\*\*\` \` \-- Enable \`metric\` for the currently selected
\`handler\`.

**Example:**

\`M331 pos_z\`

#### M332 - Disable metrics

\*\*M332\*\*\` \` \-- Disable \`metric\` for the currently selected
\`handler\`.

**Example:**

\`M332 pos_z\`

#### M333 - Print metrics and their settings for selected handler

List all metrics and whether they are enabled for the currently selected
\`handler\`.

#### M334 - Handler-specific configuration

Handler-specific configuration

**Example:**

\`M334 \`  - Configures the syslog handler to send all the enabled
metrics to the given IP address and port.

#### M335 - Logging

**Example:**

\`M335 \`

#### M340 - Syslog host and port configuration

#### M350 - [M350: Set microstepping mode](https://reprap.org/wiki/G-code#M350:_Set_microstepping_mode)

#### M400 - [M400: Wait for current moves to finish](https://reprap.org/wiki/G-code#M400:_Wait_for_current_moves_to_finish)

#### M401 - [M402: Deploy probe](https://reprap.org/wiki/G-code#M401:_Deploy_Z_Probe)

#### M402 - [M402: Stow probe](https://reprap.org/wiki/G-code#M402:_Stow_Z_Probe)

#### M403 - [M403: Set filament type (material) for particular extruder and notify the MMU](https://reprap.org/wiki/G-code#M403:_Set_filament_type_.28material.29_for_particular_extruder_and_notify_the_MMU)

#### M410 - [M410: Quick-Stop](https://reprap.org/wiki/G-code#M410:_Quick-Stop)

Abort all the planned moves.

#### M420 - Enable/Disable Bed Leveling

Enable/Disable Bed Leveling and/or set the Z fade height.

**Parameters:**

- S\[bool\]   Turns leveling on or off
- Z\[height\] Sets the Z fade height (0 or none to disable)
- V\[bool\]   Verbose - Print the leveling grid\
   \* With AUTO_BED_LEVELING_UBL only:
- L\[index\]  Load UBL mesh from index (0 is default)
- T\[map\]    0:Human-readable 1:CSV 2:\"LCD\" 4:Compact
-  C         Center mesh on the mean of the lowest and highest (With
  mesh-based leveling only)

#### M428 - Apply current_position to home_offset

Set home_offset based on the distance between the current_position and
the nearest \"reference point.\"\
 If an axis is past center its endstop position is the reference-point.
Otherwise it uses 0. This allows the Z offset to be set near the bed
when using a max endstop.\
M428 can\'t be used more than 2cm away from 0 or an endstop.\
Use M206 to set these values directly.

#### M486 - [M486: Cancel Object](https://reprap.org/wiki/G-code#M486:_Cancel_Object)

A simple interface to identify and cancel printing one of multiple
printed objects.

**Parameters:**

- T\[count\] : Reset objects and/or set the count
- S : Start an object with the given index
- P : Cancel the object with the given index
- U : Un-cancel object with the given index
- C        : Cancel the current object (the last index given by S)
- S-1      : Start a non-object like a brim or purge tower that should
  always print
- Aname    : Name the current object
- Nname    : Legacy, same as Aname
- A and N need to be alone in the G-code line, use \"M486 S1nM486
  AMyAwesomeObject\".\
   Spaces in name can get consumed by meatpack.

#### M500 - [M500: Store parameters in EEPROM](https://reprap.org/wiki/G-code#M500:_Store_parameters_in_non-volatile_storage)

#### M501 - [M501: Read parameters from EEPROM](https://reprap.org/wiki/G-code#M501:_Read_parameters_from_EEPROM)

#### M502 - [M502: Restore Default Settings](https://reprap.org/wiki/G-code#M502:_Restore_Default_Settings)

#### M503 - [M503: Report Current Settings](https://reprap.org/wiki/G-code#M503:_Report_Current_Settings)

Print settings currently in memory.

#### M509 - [M509: Force language selection](https://reprap.org/wiki/G-code#M509:_Force_language_selection)

#### M555 - Set print area

Set print area for detailed MBL.

**Parameters:**

- X: X coordinate of print area rectangle
- Y: Y coordinate of print area rectangle
- W: Width of print area rectangle
- H: Height of print area rectangle

**Example:**

M555 X112.5 Y88.5 W32 H29

#### M556 - Override modular bedlet active

XL only.

**Parameters:**

- X/Y: Set bedlet based on X, Y coordinates\
  (By default, all bedlets are set)
- I: set bedlet based on its index
- A: Activate bedlet
- D: Deactivate bedlet

#### M557 - Set modular bed gradient parameters

XL only.

**Parameters:**

- C: Set gradient cutoff
- E: Set gradient exponent
- S: Set expand to sides

#### M569 - Enable StealthChop

Used specifically to enable StealthChop on an axis.

**Parameters:**

- S\[1\|0\]: Enable or disable
- X\|Y\|Z\|E : target an axis
- No arguments reports the stealthChop status of all capable drivers.

**Example:**

M569 S0 E   - Set spreadcycle mode for extruder.

#### M572 [M572: Set or report extruder pressure advance](https://reprap.org/wiki/G-code#M572:_Set_or_report_extruder_pressure_advance)

Set parameters for pressure advance.

**Parameters:**

- D: Set the extruder number.
- S: Set the pressure advance value. If zero the pressure advance is
  disabled.
- W: Set a time range in seconds used for calculating the average
  extruder velocity for pressure advance. Default value is 0.04.

#### M591 - Configure Filament stuck monitoring

Enable/Disable Filament stuck monitoring.\
Prusa STM32 platform specific.

**Parameters:**

- S: 0 disable 1 enable\
  With no parameter, shows the state of EMotorStallDetector on the
  serial line.

#### M593 - Set parameters for input shapers.

Set parameters for input shapers.

**Parameters:**

- D: Set the input shaper damping ratio. If axes (X, Y, etc.) are not
  specified, set it for all axes. Default value is 0.1.
- F: Set the input shaper frequency. If axes (X, Y, etc.) are not
  specified, set it for all axes. Default value is 0Hz - It means that
  the input shaper is disabled.
- T\[map\]:  Set the input shaper type, 0:ZV, 1:ZVD, 2:MZV, 3:EI,
  4:2HUMP_EI, and 5:3HUMP_EI. Default value is 0:ZV.
- R: Set the input shaper vibration reduction. This parameter is used
  just for 3:EI, 4:2HUMP_EI, and 5:3HUMP_EI. Default value is 20.
- X\<1\>:         Set the input shaper parameters only for the X axis.
- Y\<1\>:        Set the input shaper parameters only for the Y axis.
- Z\<1\>:        Set the input shaper parameters only for the Z axis.
- A: Set the input shaper weight adjust frequency delta.
- M:     Set the input shaper weight adjust mass limit.
- W\<1\>:        Write current input shaper settings to EEPROM.

#### M600 - [M600: Filament change pause](https://reprap.org/wiki/G-code#M600:_Filament_change_pause)

**Parameters:**

- E\[distance\]: Retract the filament this far 
- Z\[distance\]: Move the Z axis by this distance
- X\[position\]: Move to this X position, with Y
- Y\[position\]: Move to this Y position, with X
- U\[distance\]: Retract distance for removal (manual reload)
- L\[distance\]: Extrude distance for insertion (manual reload)
- B\[count\]: Number of times to beep, -1 for indefinite (if equipped
  with a buzzer)
- T\[toolhead\]: Select extruder for filament change
- A: If automatic spool join is configured for this tool, do that
  instead, if not, do manual filament change\
   \*  Default values are used for omitted arguments.

#### M601 - [M601: Pause print](https://reprap.org/wiki/G-code#M601:_Pause_print)

#### M602 - [M602: Resume print](https://reprap.org/wiki/G-code#M602:_Resume_print)

#### M603 - [M603: Configure Filament Change](https://reprap.org/wiki/G-code#M603:_Configure_Filament_Change)

**Parameters:**

- T\[toolhead\]: Select extruder to configure, active extruder if not
  specified
- U\[distance\]: Retract distance for removal, for the specified
  extruder
- L\[distance\]: Extrude distance for insertion, for the specified
  extruder

#### M604 - Abort (serial) print

This is expected to be set as end-print command (\"After print job is
cancelled\") in Octoprint.

#### M701 - [M701: Load to nozzle](https://reprap.org/wiki/G-code#M701:_Load_filament)

M701 Pn

**Parameters:**

- T, L, Z (as defined in Marlin)
- Pn → n index of slot (zero based, so 0-4 like T0 and T4)

M701 also has a Tn parameter - that we understand like an extruder
index, not the MMU (having an XL with 5 MMU\'s connected   ) → M701 T4
P4

- T: Extruder number. Required for mixing extruder.\
   \*                For non-mixing, current extruder if omitted.
- Z: Move the Z axis by this distance
- L: Extrude distance for insertion (positive value) - 0 == PURGE
- S\"Filament\": save filament by name, for example S\"PLA\". RepRap
  compatible.
- W: Preheat\
  - W255: default without preheat\
  - W0: preheat no return no cool down\
  - W1: preheat with cool down option\
  - W2: preheat with return option\
  - W3: preheat with cool down and return options\
   Default values are used for omitted arguments.

#### M702 - [M702: Unload filament](https://reprap.org/wiki/G-code#M702:_Unload_filament)

M702 Pn

**Parameters:**

- T, U, Z (as defined in Marlin)
- W: preheat with options to show additional cooldown and return
  buttons\
  - W\'-1\': default without preheat\
  - W0: preheat no return no cool down\
  - W1: preheat with cool down option\
  - W2: preheat with return option\
  - W3: preheat with cool down and return options
- I: ask if the unload was successful

#### M704 - [M704: Preload to MMU](https://reprap.org/wiki/G-code#M704:_Preload_to_MMU)

M704 Pn

**Parameters:**

- Pn → n index of slot (zero based, so 0-4 like T0 and T4)

#### M705 - [M705: Eeject filament](https://reprap.org/wiki/G-code#M705:_Eject_filament)

M705 Pn

**Parameters:**

- Pn → n index of slot (zero based, so 0-4 like T0 and T4)

#### M706 - [M706: Cut filament](https://reprap.org/wiki/G-code#M706:_Cut_filament)

M706 Pn

**Parameters:**

- Pn → n index of slot (zero based, so 0-4 like T0 and T4)

#### M707 - [M707: Read from MMU register](https://reprap.org/wiki/G-code#M707:_Read_from_MMU_register)

M707 A

C\
Read a variable from MMU.

**Parameters:**

- A: Address of register in hexidecimal.
- C: How many bytes to read (Optional)

**Example:**

M707 A0X19 - Read a 8bit integer from register 0X19 (Idler_sg_thrs_R)
and prints the result onto the serial line.

Does nothing if the A parameter is not present or if MMU is not enabled.

#### M708 - [M708: Write to MMU register](https://reprap.org/wiki/G-code#M708:_Write_to_MMU_register)

M708 A

X C

Set a variable in the MMU

**Parameters:**

- A: Address of register in hexidecimal.
- X: Data to write (16-bit integer). Default value 0.

**Example:**

M708 A0x19 X07 - Write to register 0x19 (Idler_sg_thrs_R) the value 07.
Does nothing if A parameter is missing or if MMU is not enabled.

#### M709 - [M709: MMU power & Reset](https://reprap.org/wiki/G-code#M709:_MMU_power_.26_reset)

M709 Xn Sn Tn

**Parameters:**

- Xn: reset where n means:\
  0 - issue an X0 command via communication into the MMU (soft reset)\
  1 - toggle the MMU\'s reset pin\
  2 - power cycle the MMU (turn off and back on)
- Sn: power off/on\
  0 - turn off MMU\'s power supply\
  1 - power up the MMU after being turned off\
  S without any parameter returns 0 or 1 for current state
- T: index of MMU unit (in case there are multiple - same principle like
  M701 Tn)

#### M851 - [M851: Set Z Probe Z Offset](https://reprap.org/wiki/G-code#M851_in_Marlin_2.0.0)

#### M862 - [M862: Print checking](https://reprap.org/wiki/G-code#M862:_Print_checking)

Printer verifies if the G-code is compatible with the machine.

**Common parameters:**

- Q: get machine value.\
  - query is done during gcode execution (printing)
- P: check if supplied value matches machine value\
  - This check is done before starting the print from file. If an
  incompatible feature is found, the printer shows a corresponding
  message.\
  This parameter is ignored during print or if supplied via USB CDC

**Example:**

M862.3 P \"MINI\"

#### M862.1 - [M862.1: Check nozzle diameter](https://reprap.org/wiki/G-code#M862.1:_Check_nozzle_diameter)

**Parameters:**

- T: Specific tool, default to currently active nozzle.

#### M862.2 - [M862.2: Check model code](https://reprap.org/wiki/G-code#M862.2:_Check_model_code)

printer checks if the G-code is sliced for a compatible printer model.

#### M862.3 - [M862.3: Check model name](https://reprap.org/wiki/G-code#M862.3:_Model_name)

printer checks if the G-code is sliced for a compatible printer model.

#### M862.4 - [M862.4: Check Firmware version](https://reprap.org/wiki/G-code#M862.4:_Firmware_version)

#### M862.5 - [M862.5: Check G-code level](https://reprap.org/wiki/G-code#M862.5:_Gcode_level)

G-code levels refer to different versions or configurations of G-code.
The G-code level determines the set of commands and parameters that the
printer can understand and execute.\
The M862.5 command will compare the input value with the G-code level
supported by the printer. If the G-code level does not match the input
value, a warning or error message may be displayed.

**Parameters:**

- Pnnnn nnnn: Gcode level

- Q: Current Gcode level

  When run with P\<\> argument, the check is performed against the input
  value.\
  When run with Q argument, the current value is shown.

**Example messages:**

- G-code sliced for a different level. Continue?
- G-code sliced for a different level. Please re-slice the model again.
  Print cancelled.

#### M862.6 - [M862.6: Check Firmware features](https://reprap.org/wiki/G-code#M862.6:_Firmware_features)

The printer has a list of supported features. Using the M862.6
P\[feature\], it checks if the list of the required features in the
G-code matches the features available on the printer.\
If an incompatible feature is found, the printer shows a corresponding
message.

**Example:**

M862.6 P \"Input shaper\" 

**Example messages:**

- G-code isn\'t fully compatible. misssing requested features: Input
  shaper

#### M863 - Tool remapping

Allows to redefine which tools use for certain parts of the print. \
If a part of an object is sliced to be printed with filament 1 - but you
wish to print it with filament 2 instead, this G-code helps you achieve
so.

**Examples:**

M863 M P0 L1 : Instead of tool 0, use tool 1\
M863 E1/0 : Enable/disable tool remapping\
M863 R : Reset tool remapping\
M863 : Report current tool mapping

#### M864 - Spool join settings

Enables to configure Spool join function, defining which material to use
after the one used runs out.

**Examples:**

M864 J A1 B2 : When tool 1 runs out of filament, continue with tool 2\
M864 R : reset any settings\
M864 : Report current spool join settings

#### M900 - [M900: Set Linear advance K factor](https://reprap.org/wiki/G-code#M900_Set_Linear_Advance_Scaling_Factors)

#### M906 - [M906: Set motor current](https://reprap.org/wiki/G-code#M906:_Set_motor_currents)

In milliamps, using axis codes X, Y, Z, E.

**Parameters:**

- X\[current\]: Set mA current for X driver(s)
- Y\[current\]: Set mA current for Y driver(s)
- Z\[current\]: Set mA current for Z driver(s)
- E\[current\]: Set mA current for E driver(s)
- I\[index\]: Axis sub-index (Omit or 0 for X, Y, Z; 1 for X2, Y2, Z2; 2
  for Z3.)
- T\[index\]: Extruder index (Zero-based. Omit for E0 only.)\
   \* With no parameters, reports driver currents.

#### M910 - [M910: TMC2130 init](https://reprap.org/wiki/G-code#M910:_TMC2130_init)

#### M911 - Report stepper driver overtemperature pre-warn condition

Report TMC stepper driver overtemperature pre-warn flag.\
This flag is held by the library, persisting until cleared by M912.\
(Requires at least one \_DRIVER_TYPE defined as
TMC2130/2160/5130/5160/2208/2209/2660)

#### M912 - clear stepper driver overtemperature pre-warn condition flag

Clear TMC stepper driver overtemperature pre-warn flag held by the
library.\
(Requires at least one \_DRIVER_TYPE defined as
TMC2130/2160/5130/5160/2208/2209/2660)

**Parameters:**

- X, Y, Z, X1, Y1, Z1, X2, Y2, Z2, Z3 and E\[index\]: Specifies one or
  more axes to clear the flag on.
- If no axes are specified, clears all.

#### M914 - Set StallGuard sensitivity

**Parameters:**

- I: Index of a sensitivity value to set.
- X, Y, Z: Axis code
- \* With no parameters, reports the current StallGuard sensitivity.

**Examples:**

M914 I0 Z200: Set StallGuard sensitivity for the Z-axis to 200:

M914: Print the current StallGuard sensitivity values.

#### M919 - TMC Config Write

Writes a value to the TMC driver's register\
M919

**Example:**

M919 X I_HOLD_IRUN 1000

#### M920 - TMC Config Read

Reads a value from the TMC driver's register\
M920

**Example:**

M920 Z SG2

#### M930 - Set SPI prescaler for xLCD

Set up the prescaler of the LCD perifery SPI.\
This is used for manipulating communication frequency during HW
testing.\
If value was not set or was set 0, prescaler will set up 0 (frequency
will be divided by 1 = unchanged).

**Parameters:**

\[uint16\]       Prescaler value (0-7) is mapped internally on power of
2.

#### M931 - Set SPI prescaler for EXT_FLASH

Set up the prescaler of the EXT_FLASH perifery SPI.\
This is used for manipulating communication frequency during HW
testing.\
If value was not set or was set 0, prescaler will set up 0 (frequency
will be divided by 1 = unchanged).

**Parameters:**

\[uint16\]       Prescaler value (0-7) is mapped internally on power of
2.

#### M932 - Set SPI prescaler for TMC

Set up the prescaler of the TMC perifery SPI.\
This is used for manipulating communication frequency during HW
testing.\
If value was not set or was set 0, prescaler will set up 0 (frequency
will be divided by 1 = unchanged).

**Parameters:**

\[uint16\]       Prescaler value (0-7) is mapped internally on power of
2.

#### M958 - Excite harmonic vibration

#### M959 - Tune input shaper

#### M997 - Update firmware

Perform in-application firmware update. Prusa STM32 platform specific.

**Parameters:**

- O: Update older or same firmware on restart == force reflash == from
  menu
- S: Firmware module number(s), default 0\
   - 0 - main firmware.\
   - 1 - WiFi module firmware\
   - 2 - 4 - Reserved, check reprap wiki
- B: Expansion board address, default 0\
   - Currently unused, defined just to be reprap compatible
- /: Selected BBF SFN (short file name)

#### M999 - Reset MCU

Prusa STM32 platform specific.\
Restarts after being stopped. With R parameter, resets the MCU.

**Parameters:**

- R: reset MCU
- Z: Wait for finishing planned moves, save Z coordinate and restore it
  after reset.\
     - Must be combined with R parameter, doesn\'t work otherwise.\
     - Z is restored only if USB flash drive is present.\
       This strange requirement is due to coupling with power panic.

#### M1587 - Wi-Fi credentials

Open Wi-Fi credentials dialog.\
Similar to M587, but meant to be used internally.

**Parameters:**

- I: Generate ini file

#### M1600 - Change filament menu

Prusa STM32 platform specific.\
Non-print filament change.\
Not meant to be used during print.

**Parameters:**

- T: Extruder number. Required for mixing extruder.
- R: Preheat Return option
- U: Ask Unload type\
        - \`U0\` - return if filament unknown (default)\
        - \`U1\` - ask only if filament unknown\
        - \`U2\` - always ask
- S\"Filament\": change to filament by name, for example \`S\"PLA\"\`

#### M1601 - Filament stuck detection

Prusa STM32 platform specific

#### M1700 - Preheat

Prusa STM32 platform specific.

**Parameters:**

- T: Extruder number. Required for mixing extruder.\
          For non-mixing, current extruder if omitted.
- W: Preheat\
         - \`W0\`  - preheat no return no cool down\
         - \`W1\`  - preheat with cool down option\
         - \`W2\`  - preheat with return option\
         - \`W3\`  - preheat with cool down and return options - default
- S: Set filament
- E: Enforce target temperature

#### M1701 - Autoload

Prusa STM32 platform specific.\
 Not meant to be used during print.

**Parameters:**

- T: Extruder number. Required for mixing extruder.\
         For non-mixing, current extruder if omitted.
- Z: Move the Z axis by this distance
- L: Extrude distance for insertion (positive value) (manual reload)\
   \* Default values are used for omitted arguments.

#### M1704 - Load test

Triggers the MMU3 Loading test.

 

 

 

<div>

### T-codes

</div>

 

#### T Toolchange

Select extruder in case of multi extruder printer (XL). Select filament
position 1-5 (T0-T4) in case of MMU3.

**Parameters:**

- F\[units/min\]: Set the movement feedrate
- S1: Don\'t move the tool in XY after change
- M0/1: Use tool mapping or not (default is yes)
- Lx: Z Lift settings 0 =- no lift, 1 = lift by max MBL diff, 2 = full
  lift(default)
- Dx 0 = do not return in Z after lift, 1 = normal return

**Examples:**

T0 : Select filament position 1 on MMU3 / Select Tool 1 on XL.

T1 : Select filament position 2 / Tool 2.

#### Tx - Select filament

(MMU3) Printer asks user to select a filament position. Then loads the
filament from the MMU unit into the extruder wheels only.

#### Tc - Load to nozzle

(MMU3) Loads the filament tip from the extruder wheels into the nozzle.

 

 

<div>

### Special / Other commands

</div>

 

#### P0 - Tool park

Park extruder (tool) (XL only)\
Pn: n index of a tool (zero based, so 0-4 like T0 and T4 for tools 1 and
5)

**Parameters:**

- F\[units/min\]: Set the movement feedrate
- S1: Don\'t move the tool in XY after change
- M0/1: Use tool mapping or not (default is yes)
- Lx: Z Lift settings 0 =- no lift, 1 = lift by max MBL diff, 2 = full
  lift(default)
- Dx 0 = do not return in Z after lift, 1 = normal return

 

 
:::::::::

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
::::::::::::::::::::::::::::::::::::::::::
