```{=mediawiki}
{{Languages|G-code}}
```

------------------------------------------------------------------------

This page tries to describe the flavour of **G-codes** that the RepRap
firmwares use and how they work. The main target is additive fabrication
using [FFF](FFF "FFF"){.wikilink} processes. Codes for print head
movements follow the [NIST RS274NGC G-code
standard](http://www.nist.gov/manuscript-publication-search.cfm?pub_id=823374),
so RepRap firmwares are quite usable for CNC milling and similar
applications as well. See also on [Wikipedia\'s G-code
article](https://en.wikipedia.org/wiki/G-code).

There are a few different ways to prepare G-code for a printer. One
method would be to use a slicing program such as
[Slic3r](Slic3r "Slic3r"){.wikilink},
[Skeinforge](Skeinforge "Skeinforge"){.wikilink} or
[Cura](Cura "Cura"){.wikilink}. These programs import a CAD model, slice
it into layers, and output the G-code required to print each layer.
Slicers are the easiest way to go from a 3D model to a printed part,
however the user sacrifices some flexibility when using them. Another
option for G-code generation is to use a lower level library like
[mecode](mecode "mecode"){.wikilink}. Libraries like mecode give you
precise control over the tool path, and thus are useful if you have a
complex print that is not suitable for naive slicing. The final option
is to just write the G-code yourself. This may be the best choice if you
just need to run a few test lines while calibrating your printer.

As many different firmwares exist and their developers tend to implement
new features without discussing strategies or looking what others did
before them, a lot of different sub-flavours for the 3D-Printer specific
codes developed over the years. This particular page is the master page
for RepRap. Nowhere in here should the same code be used for two
different things; there are always more numbers to use\... The rule is:
**add your new code here, then implement it**.

Unfortunately human nature being what it is, the best procedures aren\'t
always followed, so some multiple uses of the same code exist. The rule
which should be followed is that later appearances of a code on this
page (later than the original use of a code), are deprecated and should
be changed, unless there is a good technical reason (like the general
G-Code standard) why a later instance should be preferred. Note that the
key date is appearance here, not date of implementation.

## Introduction

A typical piece of G-code as sent to a RepRap machine might look like
this:

`N3 T0*57`\
`N4 G92 E0*67`\
`N5 G28*22`\
`N6 G1 F1500.0*82`\
`N7 G1 X2.0 Y2.0 F3000.0*85`\
`N8 G1 X3.0 Y3.0*33`

G-code can also be stored in files on SD cards. A file containing RepRap
G-code usually has the extension `.g`, `.gco` or `.gcode`. Files for
BFB/RapMan have the extension `.bfb`. G-code stored in file or produced
by a slicer might look like this:

`G92 E0`\
`G28`\
`G1 F1500`\
`G1 X2.0 Y2.0 F3000`\
`G1 X3.0 Y3.0`

The meaning of all those symbols and numbers (and more) is explained
below.

Slicers will (optionally?) add G-code scripts to the beginning and end
of their output file to perform specified actions before and/or after a
print such as z-probing the build-area, heating/cooling the bed and
hotend, performing ooze free \"nozzle wipe\" startup routine, switching
system power on/off, and even \"ejecting\" parts. More info on the
[Start GCode
routines](Start_GCode_routines "Start GCode routines"){.wikilink} and
[End GCode routines](End_GCode_routines "End GCode routines"){.wikilink}
pages.

To find out which specific G-code(s) are implemented in any given
firmware, there are little tables attached to the command descriptions,
like this one:
`{{Firmware Support | fived={{yes}} | teacup={{automatic}} | sprinter={{no}} | marlin={{partial}} | repetier={{experimental}} | smoothie={{???}}`{=mediawiki}
\| redeem=`{{yes}}`{=mediawiki} \| mk4duo=`{{partial}}`{=mediawiki} \|
yaskawa=`{{yes}}`{=mediawiki} }}

Here means:

  -------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  ???            Unknown if the firmware supports this G-code. You may want to test this yourself before using it in production.
  Yes            The G-code is fully supported by the firmware.
  1.23+          The G-code is supported by version 1.23 and above.
  No             The firmware does not support the G-code at all.
  Partial        There is only partial support for the full G-code specification. It may be required to rebuild the source code with extra options or flip configuration switches on the mainboard.
  Experimental   The G-code is experimental and may change or be removed.
  Automatic      The firmware handles this G-code automatically, so there\'s no need to send the command. An example is power supply on/off G-code (`M80`/`M81`) in the Teacup firmware.
  -------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

For the technically-minded, G-code line endings are Unix Line Endings
(`\n`), but will accept Windows Line Endings (`\r\n`), so you should not
need to worry about converting between the two, but it is best practice
to use Unix Line Endings where possible.

## Fields

A RepRap G-code is a list of fields that are separated by white spaces
or line breaks. A field can be interpreted as a command, parameter, or
for any other special purpose. It consists of one letter directly
followed by a number, or can be only a stand-alone letter (Flag). The
letter gives information about the meaning of the field (see the list
below in this section). Numbers can be *integers* (128) or *fractional*
numbers (12.42), depending on context. For example, an X coordinate can
take integers (`X175`) or fractionals (`X17.62`), but selecting extruder
number 2.76 would make no sense. In this description, the numbers in the
fields are represented by `nnn` as a placeholder.

In RepRapFirmware, some parameters can be followed by more than one
number, with colon used to separate them. Typically this is used to
specify extruder parameters, with one value provided per extruder. If
only one value is provided where a value is needed for each extruder,
then that value is applied to all extruders.

  Letter   Meaning
  -------- ----------------------------------------------------------------------------------------------------------------------
  Gnnn     Standard G-code command, such as move to a point
  Mnnn     RepRap-defined command, such as turn on a cooling fan
  Tnnn     Select tool nnn. In RepRap, a tool is typically associated with a nozzle, which may be fed by one or more extruders.
  Snnn     Command parameter, such as time in seconds; temperatures; voltage to send to a motor
  Pnnn     Command parameter, such as time in milliseconds; proportional (Kp) in PID Tuning
  Xnnn     A X coordinate, usually to move to. This can be an Integer or Fractional number.
  Ynnn     A Y coordinate, usually to move to. This can be an Integer or Fractional number.
  Znnn     A Z coordinate, usually to move to. This can be an Integer or Fractional number.
  U,V,W    Additional axis coordinates (RepRapFirmware)
  Innn     Parameter - X-offset in arc move; integral (Ki) in PID Tuning
  Jnnn     Parameter - Y-offset in arc move
  Dnnn     Parameter - used for diameter; derivative (Kd) in PID Tuning
  Hnnn     Parameter - used for heater number in PID Tuning
  Fnnn     Feedrate in mm per minute. (Speed of print head movement)
  Rnnn     Parameter - used for temperatures
  Qnnn     Parameter - not currently used
  Ennn     Length of extrudate. This is exactly like X, Y and Z, but for the length of filament to consume.
  Nnnn     Line number. Used to request repeat transmission in the case of communications errors.
  \*nnn    Checksum. Used to check for communications errors.
           

## Case sensitivity {#case_sensitivity}

The original NIST G-code standard requires gcode interpreters to be
case-insensitive, except for characters in comments. However, not all 3D
printer firmwares conform to this and some recognise uppercase command
letters and parameters only.

Firmwares that are known to be case-insensitive:
:   RepRapFirmware version 1.19 and later (except within quoted strings)
:   Druid Firmware version 1.00 by default is case-insensitive: ( M544
    S0 = case-sensitive / M544 S1 = case-insensitive )

<!-- -->

Firmwares that are known to be case-sensitive:
:   RepRapFirmware version 1.18 and earlier
:   Druid Firmware version 1.00 for case-sensitive: M544 S0 =
    case-sensitive

## Quoted strings {#quoted_strings}

In RepRapFirmware, some commands support quoted strings when providing
file names and other string parameters. This allows file names, WiFi
passwords etc. to contain spaces, semicolons and other characters that
would otherwise not be permitted. Double-quote characters are used to
delimit the string, and any double-quote character within the string
must be repeated.

Unfortunately, some gcode sender programs convert all characters to
uppercase and don\'t provide any means to disable this feature.
Therefore, within a quoted-string, the single-quote character is used as
a flag to force the following character to lowercase. If you want to
include a single quote character in the string, use two single quote
characters to represent one single quote character.

Example: to add SSID MYROUTER with password `ABCxyz;" 123` to the WiFi
network list, use command:

`M587 S"MYROUTER" P"ABCxyz;"" 123"`

or if you can\'t send lowercase characters:

`M587 S"MYROUTER" P"ABC'X'Y'Z;"" 123"`

## Using expressions in parameters {#using_expressions_in_parameters}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | druid={{no}} | reprapfirmware={{yes}} | grbl={{???}}
```
\| redeem=`{{no}}`{=mediawiki} \| mk4duo=`{{no}}`{=mediawiki} \|
yaskawa=`{{no}}`{=mediawiki} }}

RepRapFirmware 3.1 and later allow parameter values to be computed from
an expression enclosed in { }. Such an expression may include constants,
values from the machine object model, operators and functions. Example:

`G1 X{move.axes[0].max-5} Y{move.axes[1].min+5} F6000 ; move to 5mm short of the X and Y axis limits`

See
<https://docs.duet3d.com/en/User_manual/Reference/Gcode_meta_commands>
for more details.

## Comments

G-code comments begin at a semicolon, and end at the end of the line:

    N3 T0*57 ; This is a comment
    N4 G92 E0*67
    ; So is this
    N5 G28*22

Some firmwares also obey the CNC G-code standard, which is to enclose
comments in round brackets. Comments of this form must start and end on
the same line:

    (Home some axes)
    G28 (here come the axes to be homed) X Y

Comments and white space will be ignored by your RepRap Printer. It\'s
better to strip these out on the host computer before sending the G-code
to your printer, as this saves bandwidth.

## Special fields {#special_fields}

#### N: Line number {#n_line_number}

```{=mediawiki}
{{Firmware Support | fived={{yes}} | teacup={{yes}} | sprinter={{yes}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | repetier={{yes}} | druid={{yes}} | reprapfirmware={{yes}} | machinekit={{yes}} | grbl={{???}}
```
\| redeem=`{{yes}}`{=mediawiki} \| mk4duo=`{{yes}}`{=mediawiki} \|
yaskawa=`{{yes}}`{=mediawiki} \| klipper=`{{yes}}`{=mediawiki} }}

Example

`N123`

If present, the line number should be the first field in a line. For
G-code stored in files on SD cards the line number is usually omitted.

If checking is supported, the RepRap firmware expects line numbers to
increase by 1 each line, and if that doesn\'t happen it is flagged as an
error. But you can reset the count using `M110` (see below).

Although supported, usage of N in Machinekit is discouraged as it serves
no purpose.

#### \*: Checksum

```{=mediawiki}
{{Firmware Support | fived={{yes}} | teacup={{yes}} | sprinter={{yes}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | repetier={{yes}} | druid={{no}} | reprapfirmware={{yes}} | grbl={{???}}
```
\| redeem=`{{no}}`{=mediawiki} \| mk4duo=`{{yes}}`{=mediawiki} \|
yaskawa=`{{no}}`{=mediawiki} }}

Example: `*71`

If present, the checksum should be the last field in a line, but before
a comment. For G-code stored in files on SD cards the checksum is
usually omitted.

The firmware compares the checksum against a locally-computed value. If
they differ, it requests a repeat transmission of the line.

#### \*: CRC

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | druid={{no}} | reprapfirmware={{yes}} | grbl={{???}}
```
\| redeem=`{{no}}`{=mediawiki} \| mk4duo=`{{no}}`{=mediawiki} \|
yaskawa=`{{no}}`{=mediawiki} }}

Example: `*37428`

The 8-bit checksum provides insufficient protection against noise on the
received data connection in some situations, for example where the cable
from a display device runs close to an extruder cable. Therefore
RepRapFirmware allows a CRC to be used in place of a checksum. If
present, the CRC should be the last field in a line, but before the
semicolon and comment if present. RepRapFirmware assumes that \*
followed by 5 digits is a CRC, whereas \* followed by 1, 2 or 3 digits
is a checksum. The polynomial used is 0x1021 as for CCITT CRC16.

## Checking

```{=mediawiki}
{{Firmware Support | fived={{yes}} | teacup={{yes}} | sprinter={{yes}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | repetier={{yes}} | reprapfirmware={{yes}} | grbl={{???}}
```
\| redeem=`{{no}}`{=mediawiki} \| mk4duo=`{{yes}}`{=mediawiki} \|
yaskawa=`{{no}}`{=mediawiki} }}

Example

`N123 [...G Code in here...] *71`

The RepRap firmware checks the line number and the checksum (or CRC if
supported). You can leave both of these out - RepRap will still work,
but it won\'t do checking. You have to have both or neither though. If
only one appears, it produces an error.

The checksum \"cs\" for a G-code string \"cmd\" (including its line
number) is computed by exor-ing the bytes in the string up to and not
including the \* character as follows:

`int cs = 0;`\
`for(i = 0; cmd[i] != '*' && cmd[i] != NULL; i++)`\
`   cs = cs ^ cmd[i];`\
`cs &= 0xff;  // Defensive programming...`

and the value is appended as a decimal integer to the command after the
\* character.

## Conditional Execution and Loops {#conditional_execution_and_loops}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{yes}} | grbl={{???}}
```
\| redeem=`{{no}}`{=mediawiki} \| mk4duo=`{{no}}`{=mediawiki} \|
yaskawa=`{{no}}`{=mediawiki} }}

RepRapFirmware 3.01 and later supports conditions and loops in GCode.
Properties from the firmware object model (e.g. current position,
current tool) can be included in controlling expressions. See
<https://docs.duet3d.com/en/User_manual/Reference/Gcode_meta_commands>
for details.

## Buffering

```{=mediawiki}
{{Firmware Support | fived={{yes}} | marlin={{yes}} | teacup={{yes}} | reprapfirmware={{yes}} | grbl={{yes}} | redeem={{yes}} | mk4duo={{yes}} | yaskawa={{yes}} }}
```
If buffering is supported, the RepRap firmware stores some commands in a
ring buffer internally for execution. This means that there is no
(appreciable) delay while a command is acknowledged and the next
transmitted. In turn, this means that sequences of line segments can be
plotted without a dwell between one and the next. As soon as one of
these buffered commands is received it is acknowledged and stored
locally. If the local buffer is full, then the acknowledgment is delayed
until space for storage in the buffer is available. This is how flow
control is achieved.

Typically, the following moving commands are buffered: `G0`-`G3` and
`G28`-`G32`. The [Teacup
Firmware](Teacup_Firmware "Teacup Firmware"){.wikilink} buffers also
some setting commands: `G20`, `G21`, `G90` and `G91`. All other `G`, `M`
or `T` commands are not buffered.

[RepRapFirmware](RepRapFirmware "RepRapFirmware"){.wikilink} also
implements an internal queue to ensure that certain codes (like
[M106](G-code#M106:_Fan_On "M106"){.wikilink}) are executed in the right
order and not when the last move has been added to the look-ahead queue.

When an unbuffered command is received it is stored, but it is not
acknowledged to the host until the buffer is exhausted and then the
command has been executed. Thus the host will pause at one of these
commands until it has been done. Short pauses between these commands and
any that might follow them do not affect the performance of the machine.

## G-commands {#g_commands}

#### G0 & G1: Move {#g0_g1_move}

```{=mediawiki}
{{Firmware Support | fived={{yes}} | teacup={{yes}} | sprinter={{yes}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | repetier={{yes}} | druid={{yes}} | smoothie={{yes}} | reprapfirmware={{yes}} | klipper={{yes}} | bfb={{yes}} | machinekit={{yes}} | makerbot={{yes}} | grbl={{yes}} | redeem={{yes}} | mk4duo={{yes}} | yaskawa={{yes}}  }}
```
- `G0` : Rapid Move
- `G1` : Linear Move

Usage
:   `G0 Xnnn Ynnn Znnn Ennn Fnnn Snnn`
:   `G1 Xnnn Ynnn Znnn Ennn Fnnn Snnn`

Parameters
:   *Not all parameters need to be used, but at least **one** has to be
    used*
:   `Xnnn` The position to move to on the X axis
:   `Ynnn` The position to move to on the Y axis
:   `Znnn` The position to move to on the Z axis
:   `Ennn` The amount to extrude between the starting point and ending
    point
:   `Fnnn` The feedrate per minute of the move between the starting
    point and ending point (if supplied)
:   `Hnnn` (RepRapFirmware) Flag to check if an endstop was hit *(`H1`
    to check, `H0` to ignore, other `Hnnn` see note, default is
    `H0`)*^1^
:   `Rnnn` (RepRapFirmware) Restore point number ^4^
:   `Snnn` Laser cutter/engraver power. In RepRapFirmware, when not in
    laser mode S in interpreted the same as H.

Examples

`G0 X12               ; move to 12mm on the X axis`\
`G0 F1500             ; Set the feedrate to 1500mm/min`\
`G1 X90.6 Y13.8 E22.4 ; Move to 90.6mm on the X axis and 13.8mm on the Y axis while extruding 22.4mm of material`

The RepRap firmware spec treats `G0` and `G1` as the same command, since
it\'s just as efficient as not doing so.^2^

Most RepRap firmwares do subtle things with feedrates.

`G1 F1500           ; Set feedrate to 1500mm/min`\
`G1 X50 Y25.3 E22.4 ; Move and extrude`

In the above example, we first set the feedrate to 1500mm/min, then move
to 50mm on X and 25.3mm on Y while extruding 22.4mm of filament between
the two points.

`G1 F1500                 ; Feedrate 1500mm/min`\
`G1 X50 Y25.3 E22.4 F3000 ; Accelerate to 3000mm/min`

However, in the above example, we set a feedrate of 1500 mm/min, then do
the same move, but accelerating to 3000 mm/min. Everything stays
synchronized, so extrusion accelerates right along with X and Y
movement.

The RepRap spec treats the feedrate as simply another variable (like X,
Y, Z, and E) to be linearly interpolated. This gives complete control
over the acceleration and deceleration of the printer head in a way that
ensures everything moves smoothly together and the right volume of
material is extruded at all points.^3^

To reverse the extruder by a given amount (for example to reduce its
internal pressure while it does an in-air movement so that it doesn\'t
dribble) simply use `G0` or `G1` to send an `E` value that is less than
the currently extruded length.

Notes

^1^Some firmwares allow for the RepRap to enable or disable the
\"sensing\" of endstops during a move. Please check with whatever
firmware you are using to see if they support the `H` parameter in this
way, as damage may occur if you assume incorrectly. In RepRapFirmware,
using the `H1` or `H2` parameter on a delta printer causes the `XYZ`
parameters to refer to the individual tower motor positions instead of
the head position, and to enable endstop detection as well if the
parameter is H1. H3 may be used to measure axis lengths and H4 can be
used to stop when an endstop is hit while updating the position only (H4
is supported in 3.2-b4 and later).

^2^In the RS274NGC Spec, `G0` is *Rapid Move*, which was used to move
between the current point in space and the new point as quickly and
efficiently as possible, and `G1` is *Controlled Move*, which was used
to move between the current point in space and the new point as precise
as possible. In RepRapFirmware, G1 is always a linear move but G0 may
not be linear (e.g. on a SCARA machine); however a G0 move will never go
below the lower of the initial and final Z height of the move.

^3^Some firmwares may not support setting the feedrate inline with a
move.

^4^RepRapFirmware provides an additional \'R\' parameter to tell the
machine to add the coordinates of the specified restore point to all
axis coordinates mentioned in the G0 or G1 command. Axes that are not
mentioned in the G0 or G1 command are not moved. When a print is paused,
the coordinates are saved in restore point #1. When a tool change is
commenced, the coordinates are saved in restore point #2. Coordinates
can also be saved in restore points explicity using the G60 command.

Some older machines, CNC or otherwise, used to move faster if they did
not move in a straight line. This is also true for some non-Cartesian
printers, like delta or polar printers, which move easier and faster in
a curve.

#### G2 & G3: Controlled Arc Move {#g2_g3_controlled_arc_move}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{yes}} | marlin={{yes}}<sup>1</sup> | prusa={{yes}}<sup>2</sup> | buddy={{yes}} | repetier={{yes}} | druid={{yes}} | smoothie={{yes}} | reprapfirmware={{yes}} | klipper={{yes}}<sup>3</sup> | bfb={{no}} | machinekit={{yes}} | grbl={{yes}} | makerbot={{no}} | redeem={{experimental}} | mk4duo={{yes}} | yaskawa={{yes}} }}
```

Usage:
:   `G2 Xnnn Ynnn Innn Jnnn Ennn Fnnn` *(Clockwise Arc)*
:   `G3 Xnnn Ynnn Innn Jnnn Ennn Fnnn` *(Counter-Clockwise Arc)*

Parameters
:   `Xnnn` The position to move to on the X axis
:   `Ynnn` The position to move to on the Y axis
:   `Znnn` The position to move to on the Z axis (optional, may not be
    supported in some firmwares)
:   `Innn` The point in X space from the current X position to maintain
    a constant distance from
:   `Jnnn` The point in Y space from the current Y position to maintain
    a constant distance from
:   `Ennn` The amount to extrude between the starting point and ending
    point
:   `Fnnn` The feedrate per minute of the move between the starting
    point and ending point (if supplied)
:   `Knnn` The point in Z space from the current Z position to maintain
    a constant distance from (used only when the current plane is YZ or
    ZX - see G18 and G19)
:   `Rnnn` The radius of the arc (can be used in place of I and J, may
    not be supported in some firmwares)

Examples

`G2 X90.6 Y13.8 I5 J10 E22.4`

(Move in a Clockwise arc from the current point to point
(X=90.6,Y=13.8), with a center point at (X=current_X+5, Y=current_Y+10),
extruding 22.4mm of material between starting and stopping)

`G3 X90.6 Y13.8 I5 J10 E22.4`

(Move in a Counter-Clockwise arc from the current point to point
(X=90.6,Y=13.8), with a center point at (X=current_X+5, Y=current_Y+10),
extruding 22.4mm of material between starting and stopping)

Notes

^1^In Marlin Firmware not implemented for **DELTA** printers.

^2^Prusa Firmware implements arcs only in Cartesian XY.

^3^On Klipper, a `gcode_arcs` section must be enabled in the
configuration file.

#### G4: Dwell {#g4_dwell}

```{=mediawiki}
{{Firmware Support | fived={{yes}} | teacup={{yes}} | sprinter={{yes}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | repetier={{yes}} | druid={{yes}} | smoothie={{yes}} | klipper={{yes}} | reprapfirmware={{yes}} | bfb={{yes}} | machinekit={{yes}} | makerbot={{yes}} | grbl={{yes}} | redeem={{yes}} | mk4duo={{yes}} | yaskawa={{yes}} }}
```
Pause the machine for a period of time.

Parameters
:   `Pnnn` Time to wait, in milliseconds (In Teacup, P0, wait until all
    previous moves are finished)
:   `Snnn` Time to wait, in seconds (Only on Repetier, Marlin, Prusa,
    Smoothieware, and RepRapFirmware 1.16 and later)

Example

`G4 P200`

In this case sit still doing nothing for 200 milliseconds. During delays
the state of the machine (for example the temperatures of its extruders)
will still be preserved and controlled.

On Marlin, Smoothie and RepRapFirmware, the \"S\" parameter will wait
for seconds, while the \"P\" parameter will wait for milliseconds. \"G4
S2\" and \"G4 P2000\" are equivalent.

#### G6: External Motion Control (Marlin) {#g6_external_motion_control_marlin}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|2.1.2}} | prusa={{no}} | buddy={{no}} | klipper={{no}} | repetier={{no}} | druid={{no}} | smoothie={{no}} | reprapfirmware={{no}} | bfb={{no}} | machinekit={{no}} | makerbot={{no}} | grbl={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
With `DIRECT_STEPPING` enabled Marlin can receive low-level stepper
movement commands from a host device (e.g., OctoPrint with a plugin) in
a compact binary format, so all acceleration and other motion tuning can
be done on the host side.

The commands are routed directly to page storage on the printer by a
\"page manager\" system on the host side. The page manager operates in
parallel with the usual G-code commands over the USB serial connection.
The host is thus able to load data onto the machine quickly alongside
regular G-code processing.

The **G6** command triggers the movements stored in the pages by
referencing the corresponding page. Depending on the format, direction
arguments may also be needed in the **G6** command.

Requires [Step Daemon](https://github.com/colinrgodsey/step-daemon) by
[\@ColinRGodsey](https://github.com/colinrgodsey). See the [Direct
Stepping](Direct_Stepping "Direct Stepping"){.wikilink} article for more
information.

Parameters
:   `I(index)` Set page index
:   `R(rate)` Step rate per second. Last value is cached for future
    invocations.
:   `S(rate)` Number of steps to take. Defaults to max steps.
:   `X(direction)` 1 for positive, 0 for negative. Last value is cached
    for future invocations. Not used for directional formats.
:   `Y(direction)` 1 for positive, 0 for negative. Last value is cached
    for future invocations. Not used for directional formats.
:   `Z(direction)` 1 for positive, 0 for negative. Last value is cached
    for future invocations. Not used for directional formats.
:   `E(direction)` 1 for positive, 0 for negative. Last value is cached
    for future invocations. Not used for directional formats.

#### G6: Direct Stepper Move (Druid) {#g6_direct_stepper_move_druid}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | klipper={{no}} | repetier={{no}} | druid={{yes}} | smoothie={{no}} | reprapfirmware={{partial|Use G1 S2 or G1 H2 instead}} | bfb={{no}} | machinekit={{no}} | makerbot={{no}} | grbl={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
Perform a direct, uninterpolated, and non-kinematic synchronized move of
one or more steppers directly. Units may be linear (e.g., mm or inches
on `DELTA`) or specified in degrees (SCARA). This command is useful for
initialization, diagnostics, and calibration, and should be disabled on
production equipment. This type of move can be potentially dangerous,
especially for deltabots, so implementations should do their best to
limit movement to prevent twerking and damaging the carriage assembly.

Parameters
:   `Annn` Stepper A position or angle
:   `Bnnn` Stepper B position or angle
:   `Cnnn` Stepper C position or angle
:   `R` Relative move flag

SCARA Examples

`G6 A45     ; Move SCARA A stepper to the 45° position`\
`G6 B20 R   ; Move SCARA B stepper 20° counter-clockwise`

DELTA Example

`G6 C10 R   ; Move DELTA C carriage up by 10mm`

#### G10: Set tool Offset and/or workplace coordinates and/or tool temperatures {#g10_set_tool_offset_andor_workplace_coordinates_andor_tool_temperatures}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | druid={{no}} | smoothie={{yes}} | reprapfirmware={{yes}} | bfb={{no}} | machinekit={{yes}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{yes}} | klipper={{no}} }}
```

Usage
:   `G10 Lnnn Pnnn Xnnn Ynnn Znnn Rnnn Snnn`^1^

Parameters
:   `Pnnn` Tool number
:   `Lnnn` Offset mode ^5^
:   `Xnnn` X offset
:   `Ynnn` Y offset
:   `Znnn` Z offset^2^
:   `U,V,W,A,B,Cnnn` other axis offsets^4^
:   `Rnnn` Standby temperature(s) (RepRapFirmware)
:   `Snnn` Active temperature(s) (RepRapFirmware)

Examples

`G10 L1 P2 X17.8 Y-19.3 Z0.0`

(sets the offset for tool 2 to the X, Y, and Z values specified)

`G10 P1 R140 S205`

(RepRapFirmware only - set standby and active temperatures^3^ for tool
1)

Remember that any parameter that you don\'t specify will automatically
be set to the last value for that parameter. That usually means that you
want explicitly to set Z0.0. RepRapFirmware will report the tool
parameters if only the tool number is specified.

The precise meaning of the X, Y (and other offset) values is: *with no
offset this tool is at this position relative to where a tool with
offset (0, 0, 0) would be*. So if the tool is 10mm to the left of a
zero-offset tool the X value would be -10, and so on.

The `R` value is the standby temperature in ^o^C that will be used for
the tool, and the `S` value is its operating temperature. If you don\'t
want the tool to be at a different temperature when not in use, set both
values the same. See the [ T code (select
tool)](G-code#T:_Select_Tool " T code (select tool)"){.wikilink} below.
In tools with multiple heaters the temperatures for them all are
specified thus: R100.0:90.0:20.0 S185.0:200.0:150.0 .

See also `M585`.

Notes

^1^Marlin uses
[G10](G-code#G10:_Retract "G10"){.wikilink}/[G11](G-code#G11:_Unretract "G11"){.wikilink}
for executing a retraction/unretraction move. Smoothie uses `G10` for
retract and `G10 Ln` for setting workspace coordinates. RepRapFirmware
interprets a G10 command with no P or L parameter as a retraction
command.

^2^It\'s usually a bad idea to put a non-zero `Z` value in as well
unless the tools are loaded and unloaded by some sort of tool changer or
are on indepedent carriages. When all the tools are in the machine at
once they should all be set to the same Z height.

^3^If the absolute zero temperature (-273.15) is passed as active and
standby temperatures, RepRapFirmware will only switch off the tool
heater(s) without changing their preset active or standby temperatures.
RepRapFirmware-dc42 does not support this setting.

^4^Tool offsets are applied after any X axis mapping has been performed.
Therefore if for example you map X to U in your `M563` command to create
the tool, you should specify a U offset not an X offset. If you map X to
both X and U, you can specify both offsets. (Not supported on all
firmwares).

^5^L1 sets the offsets of the specified tool relative to the head
reference point to the specified values. L2 sets the current workplace
coordinate offsets to the specified values. L20 adjusts the current
workplace coordinate offsets so that the current tool head position has
the specified coordinates. NOTE on some firmwares L is required (and is
required by NIST standard). P is also required to specify either the
tool to update or the WCS to update.

#### G10: Retract {#g10_retract}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | repetier={{yes|0.92}} | druid={{yes}} | smoothie={{yes}} | klipper={{yes}} | reprapfirmware={{yes}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   `Snnn` retract length (S1 = long retract, S0 = short retract =
    default) (Repetier only)

Example

`G10`

Retracts filament according to settings of `M207` (Marlin,
RepRapFirmware) or according to the `S` value (Repetier).

RepRapFirmware recognizes `G10` as a command to set tool offsets and/or
temperatures if the `P` parameter is present, and as a retraction
command if it is absent.

#### G11: Unretract {#g11_unretract}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | repetier={{yes|0.92}} | druid={{yes}} | smoothie={{yes}} | klipper={{yes}} | reprapfirmware={{yes}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   `Snnn` retract length (S1 = long retract, S0 = short retract =
    default) (Repetier only)

Example

`G11`

Unretracts/recovers filament according to settings of `M208` (Marlin,
RepRapFirmware) or according to the `S` value (Repetier).

#### G12: Clean Tool {#g12_clean_tool}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|1.1.0}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | druid={{no}} | smoothie={{no}} | reprapfirmware={{partial|Use a macro instead}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | makerbot={{no}} | mk4duo={{yes}} | yaskawa={{no}} | klipper={{no}} }}
```

Usage

`[P<0|1>] [S``<count>`{=html}`] [T``<count>`{=html}`]`

:   `G12 Pnnn Snnn Tnnn`

Parameters
:   `Pnnn`^1^ Pattern style selection
:   `Snnn` Number of strokes (i.e. back-and-forth movements)
:   `Tnnn` Number of repetitions
:   `Ennn` 0=Never 1=Always apply software endstops (Marlin 2.0.6+)

Examples

G12 ; stroke pattern (default)

To generate a three triangle zig-zag pattern which will be stroked three
times time use the following command. G12 P1 S3 T2 ; zig-zag pattern
with 2 triangles

Notes

^1^In Marlin firmware and Derivatives Mk4duo this is implemented by
hard-coded firmware behaviours As defined for variables
NOZZLE_CLEAN_STROKES, NOZZLE_CLEAN_START_POINT, NOZZLE_CLEAN_END_POINT
and NOZZLE_CLEAN_PARK.

With NOZZLE_CLEAN_PARK enabled, the nozzle will automatically return to
the XYZ position after G12 is run.

More on this behaviour is documented inside of the code base.

The use of G12 for tool cleaning clashes with the established use of G12
for circular pocket milling on CNC machines. For this reason,
RepRapFirmware does not support G12.

#### G17..19: Plane Selection (CNC specific) {#g17..19_plane_selection_cnc_specific}

```{=mediawiki}
{{Firmware Support | marlin={{yes|1.1.4}} | prusa={{no}} | buddy={{no}} | reprapfirmware={{yes|G18 and G19 need RRF 3.3 or later}} | grbl={{yes}} | druid={{no}} | machinekit={{yes}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{yes}} }}
```
These codes set the current plane as follows:

- `G17` : XY (default)
- `G18` : ZX
- `G19` : YZ

This mode applies to `G2`/`G3` arc moves. Normal arc moves are in the XY
plane, and for most applications that\'s all you need. For CNC routing
it can be useful to do small \"digging\" moves while making cuts, so to
keep the G-code compact it uses `G2`/`G3` arcs involving the Z plane.

These commands are supported in Marlin 1.1.4 and later with
`ARC_SUPPORT` and `CNC_WORKSPACE_PLANES` enabled.

#### G20: Set Units to Inches {#g20_set_units_to_inches}

```{=mediawiki}
{{Firmware Support | fived={{yes}} | teacup={{yes}} | sprinter={{yes}} | marlin={{yes}} | prusa={{no}} | buddy={{no}} | repetier={{yes}} | druid={{yes}} | smoothie={{yes}} | reprapfirmware={{yes}} | bfb={{no}} | machinekit={{yes}} | grbl={{yes}} | redeem={{no}} | makerbot={{no}} | mk4duo={{yes}} | yaskawa={{yes}} | klipper={{no}} }}
```

Example

`G20`

Units from now on are in inches. In RepRapFirmware, the inches/mm
setting applies to regular printing and travel moves (G0, G1, G2 etc.)
but not to configuration commands. Therefore configuration should be
done in mm.

When executing a macro file, RepRapFirmware remembers the initial
inches/mm setting and restores it after execution of the macro has
completed.

#### G21: Set Units to Millimeters {#g21_set_units_to_millimeters}

```{=mediawiki}
{{Firmware Support | fived={{yes}} | teacup={{yes}} | sprinter={{yes}} | marlin={{yes}} | prusa={{no}} | buddy={{no}} | repetier={{yes}} | druid={{yes}} | smoothie={{yes}} | reprapfirmware={{yes}} | bfb={{yes}} | machinekit={{yes}} | grbl={{yes}} | redeem={{yes}} | makerbot{{yes}} | mk4duo={{yes}} | yaskawa={{yes}} | klipper={{yes}} }}
```

Example

`G21`

Units from now on are in millimeters. (This is the RepRap default.)

In RepRapFirmware, the inches/mm setting applies to regular printing and
travel moves (G0, G1, G2 etc.) but not to configuration commands.
Therefore configuration should be done in mm.

When executing a macro file, RepRapFirmware remembers the initial
inches/mm setting and restores it after execution of the macro has
completed. So a macro file such as pause.g (executed when a pause
command is received) can safely use G21 at the start to switch the units
to mm without affecting the job after the macro completes, regardless of
whether the job was using inches or mm.

#### G22: Firmware Retract {#g22_firmware_retract}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no|G10}} | prusa={{no}} | buddy={{no|G10}} | repetier={{no}} | druid={{no}} | reprapfirmware={{partial|Use G10}} | smoothie={{no}} | bfb={{no}} | grbl={{no}} | machinekit={{yes}} | makerbot={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Usage
:   `G22 ; Do a retract move`

Use this command (along with `G23`) to have the firmware to do
retraction moves (in contrast to generating an E axis `G1` move). The
retract length and speed are set in the firmware.

#### G23: Firmware Recover {#g23_firmware_recover}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no|G11}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | druid={{no}} | reprapfirmware={{partial|Use G11}} | smoothie={{no}} | bfb={{no}} | grbl={{no}} | machinekit={{yes}} | makerbot={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Usage
:   `G23 ; Do a recover move`

Use this command (along with `G22`) to have the firmware to do a recover
move. The recover length and speed are set in the firmware.

#### G26: Mesh Validation Pattern {#g26_mesh_validation_pattern}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|1.1.0}} | prusa={{no}} | buddy={{yes}} | repetier={{no}} | druid={{no}} | reprapfirmware={{no}} | smoothie={{no}} | klipper={{no}} | bfb={{no}} | machinekit={{no}} |  makerbot={{no}} | grbl={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Usage

`G26 C P O2.25 ; Do a typical test sequence`

The `G26` Mesh Validation Pattern is designed to be used in conjunction
with various Mesh Bed Leveling systems -- those that adjust for an
uneven ---rather than just tilted--- bed. The `G26` command prints a
single layer pattern over the entire print bed, giving a clear
indication of how accurately every mesh point is defined. `G26` can be
used to determine which areas of the mesh are less-than-perfect and how
much to adjust each mesh point.

`G26` has large feature list, including a built-in test that extrudes
material onto the bed. By default this is configured for PLA
temperatures and a nozzle size of 0.4mm. (This will be adjustable in an
upcoming version of Marlin.)

See the [`G26_Mesh_Validation_Tool.cpp`
file](https://raw.githubusercontent.com/MarlinFirmware/Marlin/1.1.x/Marlin/G26_Mesh_Validation_Tool.cpp)
in the Marlin source code for full documentation of the `G26` parameter
list.

#### G27: Park toolhead {#g27_park_toolhead}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|1.1.0}} | prusa={{no}} | buddy={{yes}}<sup>1</sup> | repetier={{no}} | druid={{yes}} | reprapfirmware={{no}} | smoothie={{no}} | klipper={{no}} | bfb={{no}} | machinekit={{no}} |  makerbot={{no}} | grbl={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```
Park the toolhead (i.e., nozzle) at a predefined XY position, with a Z
raise value that applies over 0 or over the current position depending
on the `P` parameter.

In Marlin this G-code is enabled by `NOZZLE_PARK_FEATURE` and the park
position is defined by `NOZZLE_PARK_POINT`. See [G27 Park
Toolhead](https://marlinfw.org/docs/gcode/G027.html) for details.

Usage
:   `G27 Xnnn Ynnn Znnn Pn`

<!-- -->

Parameters
:   *Not all parameters need to be used, but at least **one** has to be
    used*
:   `Xnnn` X park position ^1^
:   `Ynnn` Y park position ^1^
:   `Znnn` Z park position ^1^
:   `Pn` \[value\] Z action

    :   `0` (Default) Relative raise by NOZZLE_PARK_Z_RAISE_MIN before
        XY parking
    :   `1` (Default) Absolute move to NOZZLE_PARK_POINT.z before XY
        parking. This may move the nozzle down, so use with caution!
    :   `2` Relative raise by NOZZLE_PARK_POINT.z before XY parking.

<!-- -->

Examples

`G27 P0 ; Park, raising Z by NOZZLE_PARK_Z_RAISE_MIN, using NOZZLE_PARK_POINT.z as a safe height over 0`\
`G27 P1 ; Park, raising Z to at least NOZZLE_PARK_POINT.z over 0`\
`G27 P2 ; Park, raising Z by NOZZLE_PARK_POINT.z over the current Z`

#### G28: Move to Origin (Home) {#g28_move_to_origin_home}

```{=mediawiki}
{{Firmware Support | fived={{yes}} | teacup={{yes}} | sprinter={{yes}} | marlin={{yes}} | prusa={{yes}}<sup>2</sup> | buddy={{yes}}<sup>3</sup> | repetier={{yes}} | druid={{yes}} | smoothie={{yes}} | reprapfirmware={{yes}} | klipper={{yes}} | bfb={{yes}} | machinekit={{yes}} | makerbot={{yes}} | grbl={{yes}} | redeem={{yes}} | mk4duo={{yes}} | yaskawa={{yes}}<sup>1</sup> }}
```

Usage

`G28 Xnnn Ynnn Znnn I N O P Rnnn S W C`

Parameters
:   *This command can be used without any additional parameters.*
:   `X` Flag to go back to the X axis origin
:   `Y` Flag to go back to the Y axis origin
:   `Z` Flag to go back to the Z axis origin
:   `I` imprecise: do not perform precise refinement ^3^
:   `L` Force leveling state ON (if possible) or OFF after homing
    (Requires RESTORE_LEVELING_AFTER_G28 or ENABLE_LEVELING_AFTER_G28)
    ^3^
:   `N` No-change mode (do not change any motion setting such as
    feedrate) ^3^
:   `O` Home only if the position is not known and trusted ^3^
:   `P` Do not check print sheet presence ^3^
:   `R` `<linear>`{=html} Raise by n mm/inches before homing ^3^
:   `S` Simulated homing only in MARLIN_DEV_MODE ^3^
:   `W` Suppress mesh bed leveling if \`X\`, \`Y\` or \`Z\` are not
    provided ^2^
:   `C` Calibrate X and Y origin (home) - Only on MK3/s ^2^

<!-- -->

Examples

`G28     ; Home all axes (On Prusa i3 MK2/s,MK2.5/s,MK3/s it will also perform mesh bed leveling)`^`2`^\
`G28 X Z ; Home the X and Z axes`

When the firmware receives this command, it quickly moves the specified
axes (or all axes if none are given) to the endstops, backs away from
each endstop by a short distance, and slowly bumps the endstop again to
increase positional accuracy. This process, known as \"*Homing*\", is
required to determine the position of the print carriage(s). Some
firmware may even forbid movement away from endstops and other
operations until the axes have been homed.

The `X`, `Y`, and `Z` parameters act only as flags. Any coordinates
given are ignored. For example, `G28 Z10` results in the same behavior
as `G28 Z`. Delta printers cannot home individual axes, but must always
home all three towers, so the `X Y Z` parameters are simply ignored on
these machines.

Marlin firmware (version 1.1.0 and later) provides an option called
`Z_SAFE_HOMING` for printers that use a Z probe to home Z instead of an
endstop. With this option, the XY axes are homed first, then the
carriage moves to a position --usually the middle of the bed-- where it
can safely probe downward to home Z.

RepRapFirmware uses macro files to home either all axes or individual
axes. If all axes are homed, the file `homeall.g` is processed. For
individual axes the `homex.g`, `homey.g`, or `homez.g` file will be
used. On Delta printers, `G28` command will always home all three towers
by processing the `homedelta.g` file, regardless of any `X` `Y` `Z`
parameters.

Because the behavior of `G28` is unspecified, it is recommended **not**
to automatically include `G28` in your ending G-code. On a Cartesian
this will result in damaging the printed object. If you need to move the
carriage at the completion of a print, use `G0` or `G1`.

Notes

^1^ MK4duo has a `B` parameter that tells the printer to return to the
coordinates it was at before homing.\
^2^ Original Prusa i3 MK2/s, MK2.5/s, MK3/s supports a `W` parameter to
suppress mesh bed leveling. If `W` is omitted, G28 will home only and
NOT perform mesh bed leveling. Original Prusa i3 MK3/s (TMC2130 drivers)
supports a `C` parameter to calibrate the X and Y home position.

:   `W` Suppress mesh bed leveling (Prusa MK2/s, MK2.5/s and MK3/s
    only)^2^
:   `C` Calibrate X and Y home position (Prusa MK3/s only)^2^

#### G29: Detailed Z-Probe {#g29_detailed_z_probe}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{yes|G81}}<sup>1</sup> | buddy={{yes}} | repetier={{yes|0.91.7}} | druid={{no}} | smoothie={{no}}: see G32 | reprapfirmware={{yes|1.17+}} | bfb={{no}} | grbl={{no}} | machinekit={{yes}} | redeem={{yes}} | mk4duo={{yes}} | yaskawa={{no}} }}
```
This command uses a probe to measure the bed height at 3 or more points
to determine its tilt and overall flatness. It then enables compensation
so that the nozzle will remain parallel to the bed. The printer must be
homed with `G28` before using this command.

Each firmware behaves differently and depends on the type of bed
leveling that\'s been configured. For example, Marlin 1.0.2 provides 3
different types of automatic bed leveling (probe required) and a manual
bed leveling option. See your firmware\'s documentation for the specific
options available.

Usage
:   `G29`
:   `G29 Snnn`

Parameters
:   `Snnn` Firmware-dependent behavior
:   `Pfile.csv` Optional file name for bed height map file
    (RepRapFirmware only)

Examples

`G29    ; Probe the bed and enable compensation`\
`G29 S2 ; Special operation - see below`\
`G29 P1 ; UBL automated probe - see below`

##### G29 Auto Bed Leveling (Marlin - MK4duo) {#g29_auto_bed_leveling_marlin___mk4duo}

Marlin 1.0.2 and earlier provides three options for automatic bed
leveling:

- The 3-point method probes the bed at three points to produce a matrix,
  adjusting for a flat but tilted bed.
- The planar grid method (non-Delta) probes a grid pattern to produce a
  matrix by the \"least-squares\" method, adjusting for a flat but
  tilted bed.
- The bilinear grid method (Delta only) probes a grid pattern to produce
  a mesh, using bilinear interpolation to adjust for an uneven bed.

Marlin 1.1.0 and later allows the bilinear grid (i.e., \"mesh\") method
to be used on all types of machines, not just deltas. ***This is the
recommended leveling method going forward.***

Also in Marlin 1.1.0 and later, the `PROBE_MANUALLY` option allows all
forms of Auto Bed Leveling to be used without a probe. The procedure is
similar to that of `MESH_BED_LEVELING` (see below). Begin the process
with `G29` to move the nozzle to the first point. Adjust the Z axis
using `G1` or your host software. Send `G29` again to move to the next
point and repeat until all points have been sampled.

Parameters
:   `P` Set the size of the grid that will be probed (P x P points). Not
    supported by non-linear delta printer bed leveling. Example:
    `G29 P4`
:   `S` Set the XY travel speed between probe points (in units/min)
:   `D` Dry-Run mode. Just evaluate the bed Topology - Don\'t apply or
    clean the rotation Matrix. Useful to check the topology after a
    first run of G29.
:   `V` Set the verbose level (0-4). Example: `G29 V3`
:   `T` Generate a Bed Topology Report. Example: `G29 P5 T` for a
    detailed report. This is useful for manual bed leveling and finding
    flaws in the bed (to assist with part placement). Not supported by
    non-linear delta printer bed leveling.
:   `F` Set the Front limit of the probing grid
:   `B` Set the Back limit of the probing grid
:   `L` Set the Left limit of the probing grid
:   `R` Set the Right limit of the probing grid

<!-- -->

Global Parameters:
:   `E` By default `G29` will engage the Z probe, test the bed, then
    disengage. Include `E` or `E1` to engage/disengage the Z probe for
    each sample. (This has no effect for fixed probes.)

##### G29 Unified Bed Leveling (Marlin - MK4duo) {#g29_unified_bed_leveling_marlin___mk4duo}

Marlin firmware (version 1.1.0 and later) includes the
`AUTO_BED_LEVELING_UBL` option for Unified Bed Leveling. UBL combines
mesh leveling, tilted plane adjustment, 3-point leveling, and manual
editing tools all together in a single package. To accomplish so much,
UBL overloads \`G29\` with several new parameters and provides an
additional `G26` Mesh Tuning feature.

See the MarlinFW website for a dedicated [Unified Bed Leveling
page](http://marlinfw.org/docs/features/unified_bed_leveling.html) and
complete documentation on [\`G29\` for
UBL](http://marlinfw.org/docs/gcode/G029-ubl.html) and [\`G26\` Mesh
Validation](http://marlinfw.org/docs/gcode/G026.html).

G29 UBL Parameters (synopsis):

<!-- -->

    A     Activate   Activate the Unified Bed Leveling system. (i.e., M420 S1)
    D     Disable    Disable the Unified Bed Leveling system. (i.e., M420 S0)

    B#    Business   Do Manual Probing in 'Business Card' mode.
    H#    Height     Height to raise the nozzle after each Manual Probe of the bed.

    C     Continue   Continue, Constant, or Current Location, depending on Phase.
    E     Every      Stow the probe after every sampled point.
    F#    Fade       Fade leveling compensation gradually, until it ceases at the given height.
    I#    Invalidate Invalidate a specified number of Mesh Points (X and Y).
    J#    Grid       Do a grid (planar) leveling of the current Mesh using a grid with n points on a side.
    K#    Kompare    Compare (diff) current Mesh with stored Mesh #, replacing current Mesh with the result.

    L     Load       Load Mesh from the previously activated location in the EEPROM.
    L#    Load       Load Mesh from the specified location in the EEPROM.
    S     Store      Store the current Mesh in the Activated area of the EEPROM. Also save all settings.
    S #   Store      Store the current Mesh at the specified area in EEPROM, set as the Activated area.
    S -1  Store      Store the current Mesh as a print-out suitable to be fed back into the system.

    O     Map        Display the Mesh Map Topology.

    P0    Phase 0    Zero Mesh Data and turn off the Mesh Compensation System.
    P1    Phase 1    Invalidate the Mesh and do Automatic Probing to generate new Mesh data.
    P2    Phase 2    Probe unpopulated areas of the Mesh (those that couldn't be auto-probed).
    P3    Phase 3    Fill unpopulated Mesh points with a fixed value. No 'C' for "smart fill" extrapolation.
    P4    Phase 4    Fine tune the Mesh. ** Delta Mesh Compensation requires an LCD panel. **
    P5    Phase 5    Find Mean Mesh Height and Standard Deviation.
    P6    Phase 6    Shift Mesh height. All Mesh points are adjusted by the amount specified with 'C'.

    Q     Test       Load specified Test Pattern to help check system operation.

    R #   Repeat     Repeat the command the specified number of times. Default: grid points X * Y.

    T     3-Point    Perform a 3-Point Bed Leveling on the current Mesh.

    U     Unlevel    Perform a probe of the outer perimeter to assist in physically leveling the bed.

    W     What?      Print a report of Unified Bed Leveling stored data.

    X #              The X location for the command
    Y #              The Y location for the command

    Z     Zero       Do a single probe to set the Z Height of the nozzle.
    Z #   Zero       Raise/lower the entire Mesh to conform with the specified difference (plus zprobe_zoffset).

##### G29 Manual Bed Leveling (Marlin - MK4duo) {#g29_manual_bed_leveling_marlin___mk4duo}

Marlin firmware (version 1.0.2 and later) also provides a
`MESH_BED_LEVELING` feature that can be used to perform bed leveling on
machines lacking a probe. This form of bed leveling compensates for
uneven Z height across the surface of the bed using a mesh and bilinear
interpolation.

Manual Bed Leveling Usage

`G29 S1 ; Move to the first point and wait for a measurement`\
`G29 S2 ; Store the current Z, move to the next point`\
`G29 S3 Xn Yn Zn.nn ; Modify the Z height of a single point`

Options for the `S` parameter
:   `S0` Produces a mesh report
:   `S1` Start probing mesh points
:   `S2` Probe the next mesh point
:   `S3 Xn Yn Zn.nn` Manually modify a single point
:   `S4 Zn.nn` Set z offset. Positive away from bed, negative closer to
    bed.

##### G29 Auto Bed Leveling (Repetier-Firmware) {#g29_auto_bed_leveling_repetier_firmware}

Repetier firmware since v0.91 supports `G29` with the optional Snnn
parameter as described below. Useful to simply detect the Z bed angle so
you can manually readjust your bed and get it as close to in plane as
possible. If you wish to apply automatic software Z plane compensation
on Repetier, use `G32` instead with firmware 0.92.8 and above.

:   `S0` Default value. Z bed heights are calculated at the measured
    points, relative to current Z position before issuing `G29`.
:   `S1` Same as `S0`, except printer immediately moves to Z maximum
    position (Z max endstop required!), and calculates new Z maximum
    height. You must first issue `G28 Z` to home to Z maximum position
    before issuing `G29 Snnn` for this to work correctly, or the printer
    height will be invalid.
:   `S2` Same as `S1`, except new calculated Z height is also stored to
    EEPROM.

##### G29 Mesh Bed Compensation (RepRapFirmware) {#g29_mesh_bed_compensation_reprapfirmware}

RepRapFirmware:

:   `S0` (default if no `S` parameter) Probe the bed, save the height
    map in a file on the SD card, and activate the height map. The
    default folder for the height map file is `/sys` and the default
    file name is `heightmap.csv`.
:   `S1` Load the height map from file and activate bed compensation.
    The default folder and filename as for `S0`.
:   `S2` Clear the currently-loaded bed height map

To define the grid, see
[M557](G-code#M557:_Set_Z_probe_point_or_define_probing_grid "M557"){.wikilink}.

In RepRapFirmware 3.2 and later, G29 runs macro file mesh.g if it
exists, otherwise it behaves like G29 S0. The mesh.g file can perform
other actions (e.g. homing or tool selection) and then use G29 S0 to do
the probing.

Notes

In Prusa Firmware `G29` is not active by default, instead
[G81](G-code#G81:_Mesh_bed_leveling_status "G81"){.wikilink} is used.^1^

#### G29.1: Set Z probe head offset {#g29.1_set_z_probe_head_offset}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no|M851}} | prusa={{no|M851}} | buddy={{no|M851}} || repetier={{no}} | druid={{no}} | smoothie={{no}} | reprapfirmware={{no}} | bfb={{no}} | grbl={{no}} | machinekit={{yes}} | makerbot={{no}} | redeem={{no}} | mk4duo={{no|M851}} | yaskawa={{no}} }}
```

Example

`G29.1 X30 Y20 Z0.5`

Set the offset of the Z probe head. The offset will be subtracted from
all probe moves.

#### G29.2: Set Z probe head offset calculated from toolhead position {#g29.2_set_z_probe_head_offset_calculated_from_toolhead_position}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | druid={{no}} | smoothie={{no}} | reprapfirmware={{no}} | klipper={{no}} | bfb={{no}} | grbl={{no}} | machinekit={{yes}} | makerbot={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Example

`G29.2 Z0.0`

Set the offset of the Z probe head. The offset will be subtracted from
all probe moves. The calculated value is derived from the distance of
the toolhead from the current axis zero point.

The user would typically place the toolhead at the zero point of the
axis and issue the `G29.2` command.

#### G30: Single Z-Probe {#g30_single_z_probe}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no|G28,G92}} | sprinter={{no}} | marlin={{yes}} | prusa={{no}}<sup>2</sup> | buddy={{yes}} | repetier={{yes}} | druid={{no}} | smoothie={{yes}} | reprapfirmware={{yes}} | bfb={{no}} | grbl={{no}} | machinekit={{yes}} | makerbot={{no}} | redeem={{yes}} | mk4duo={{yes}} | yaskawa={{no}}<sup>1</sup> }}
```

Usage
:   `G30 Pnnn Xnnn Ynnn Znnn Hnnn Snnn`

Parameters
:   `Pnnn` Probe point number
:   `Xnnn` X coordinate
:   `Ynnn` Y coordinate
:   `Znnn` Z coordinate
:   `Hnnn` Height correction
:   `Snnn` Set parameter

Example

`G30`

Examples (RepRapFirmware)

`G30                          ; Probe the bed at the current XY position. When the probe is triggered, set the Z coordinate to the probe trigger height.`\
`G30 S-1                      ; Probe the bed at the current XY position. When the probe is triggered, do not adjust the Z coordinate.`\
`G30 P0 X20 Y50 Z-99999       ; Probe the bed at X20 Y50 and save the XY coordinates and the height error as point 0`\
`G30 P3 X180 Y180 Z-99999 S4  ; Probe the bed at X180 Y180, save the XY coordinates and the height error as point 3 and calculate 4-point compensation or calibration`\
`G30 P3 X180 Y180 Z-99999 S-1 ; As previous example but just report the height errors`

In its simplest form probes bed at current XY location.

RepRapFirmware supports additional behaviour: if a `Pn` field is
specified the probed `X`, `Y`, and `Z` values are saved as point n on
the bed for calculating the offset plane or for performing delta printer
calibration. If `X`, `Y`, or `Z` values are specified (e.g.
`G30 P1 X20 Y50 Z0.3`) then those values are used instead of the
machine\'s current coordinates. A silly `Z` value (less than -9999.0)
causes the machine to probe at the current point to get Z, rather than
using the given value. If an S field is specified (e.g. `G30 P1 Z0.3 S`)
the bed plane is computed for compensation and stored. The combination
of these options allows for the machine to be moved to points using `G1`
commands, and then probe the bed, or for the user to position the nozzle
interactively and use those coordinates. The user can also record those
values and place them in a setup G-code file for automatic execution.

RepRapFirmware uses the value of the `S` parameter to specify what
computation to perform. If the value is -1 then the Z offsets of all the
points probed are printed, but no calibration is done. If the value is
zero or not present, then this specifies that the number of factors to
be calibrated is the same as the number of points probed. Otherwise, the
value indicates the number of factors to be calibrated, which must be no
greater than the number of points probed. In version 1.09, the number of
factors may be 3, 4 or 5 when doing auto bed compensation on a Cartesian
or CoreXY printer, and 3, 4, 6 or 7 when doing auto calibration of a
Delta printer.

RepRapFirmware supports an optional `H` parameter, which is a height
correction for that probe point. It allows for the Z probe having a
trigger height that varies with XY position. The nominal trigger height
of the Z probe (e.g. at bed centre) is declared in the `Z` parameter of
the `G31` command in the config.g file. When you probe using `G30` and
the probe triggers, the firmware will assume that the nozzle is at the
nominal trigger height plus the value you have in the `H` parameter.

^1^MK4duo Firmware support an optional parameter for Delta.

Usage
:   `G30 Xnnn Ynnn S Z P`

Parameters
:   `Xnnn` X coordinate
:   `Ynnn` Y coordinate
:   `Sn` Stows the probe if 1 (default=1)
:   `Zn` `<bool>`{=html} with a non-zero value will apply the result to
    current delta_height
:   `Pn` `<bool>`{=html} with a non-zero value will apply the result to
    current zprobe_zoffset

<!-- -->

Notes

In Prusa Firmware this G-code is deactivated by default, must be turned
on in the source code.^2^

#### G31: Set or Report Current Probe status {#g31_set_or_report_current_probe_status}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{yes|0.91.7}} | druid={{no}} | smoothie={{yes}} | reprapfirmware={{yes}} | bfb={{no}} | grbl={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Usage
:   `G31 Pnnn Xnnn Ynnn Znnn Cnnn Snnn`

Parameters
:   `Pnnn` Trigger value
:   `Xnnn` Probe X offset^1^
:   `Ynnn` Probe Y offset^1^
:   `Znnn` Trigger Z height
:   `Cnnn` Temperature coefficient(s) of trigger height^2^
:   `Snnn` Calibration temperature^2^
:   `Tnnn` (RepRapFirmware 1.17 and later) Z probe type to which these
    parameters apply, defaults to the current Z probe type as defined by
    `M558 P` parameter

Examples

`G31 P500 Z2.6`\
`G31 X16.0 Y1.5`

When used on its own this reports whether the Z probe is triggered, or
gives the Z probe value in some units if the probe generates height
values. If combined with a Z and P field (example: `G31 P312 Z0.7`) this
will set the Z height to 0.7mm when the Z-probe value reaches 312 when a
`G28 Z0` (zero Z axis) command is sent. The machine will then move a
further -0.7mm in Z to place itself at Z = 0. This allows non-contact
measuring probes to approach but not touch the bed, and for the gap left
to be allowed for. If the probe is a touch probe and generates a simple
0/1 off/on signal, then `G31 Z0.7` will tell the RepRap machine that it
is at a height of 0.7mm when the probe is triggered.

In RepRapFirmware, separate `G31` parameters may be defined for
different probe types (i.e. 0+4 for switches, 1+2 for IR probes and 3
for alternative sensors). To specify which probe you are setting
parameters for, send a
[M558](G-code#M558:_Set_Z_probe_type "M558"){.wikilink} command to
select the probe type before sending the `G31` command, or use the `T`
parameter.

In Repetier, `G31` supports no parameters and simply prints the high/low
status of the Z probe.

Notes

^1^X and Y offsets of the Z probe relative to the print head (i.e. the
position when the empty tool is selected) can be specified in
RepRapFirmware. This allows you to calculate your probe coordinates
based on the geometry of the bed, without having to correct them for Z
probe X and Y offset.

^2^In RepRapFirmware, additional parameters \'S\' (bed temperature in
^o^C at which the specified `Z` parameter is correct, default is current
bed temperature) and \'C\' (temperature coefficient of `Z` parameter in
mm/^o^C, default zero) can be set for the alternative (ultrasonic)
sensor. This is useful for probes that are affected by temperature such
as PINDA. RepRapFirmware 3.1 and later allow both first and second order
temperature coefficients to be specified, e.g. C0.015:0.001.

#### G31: Dock Z Probe sled {#g31_dock_z_probe_sled}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{no}}<sup>1</sup> | repetier={{no}} | druid={{no}} | smoothie={{no}} | reprapfirmware={{no}} | klipper={{no}} | bfb={{no}} | grbl={{no}} | machinekit={{no}} | makerbot={{no}} | redeem={{yes}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Notes

In Prusa Firmware this G-code is deactivated by default, must be turned
on in the source code.^1^

#### G32: Probe Z and calculate Z plane {#g32_probe_z_and_calculate_z_plane}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no|G29}} | prusa={{no|G29}} | buddy={{no|G29}} | repetier={{yes|0.92.8+}} | druid={{no}} | smoothie={{yes}} | reprapfirmware={{yes}} | klipper={{no}} | bfb={{no}} | grbl={{no}} | machinekit={{no}} | makerbot={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Usage

`G32           ; Probe and calculate`\
`G32 Snnn      ; Each firmware has its own parameters`\
`G32 Snnn Pnnn ; Refer to their specific documentation`

This command is implemented as a more sophisticated form of bed leveling
(which uses a transformation matrix or motorized correction.
Smoothieware uses this code instead of
[\`G29\`](#G29:_Detailed_Z-Probe "`G29`"){.wikilink}.

Each firmware behaves differently. For example, Repetier firmware allows
for motorized rotation of the bed whilst ReprapFirmware probes the bed
with a transformation matrix.

##### Probe and calculate in Reprapfirmware {#probe_and_calculate_in_reprapfirmware}

RepRapFirmware executes macro file `bed.g` in response to the G31
command. The `bed.g` file is typically used to probe the bed and then
perform delta calibration if the printer is a delta, or to perform
individual leadscrew adjustment to level the bed if the printer has
multiple independently-controlled Z motors, or to advise the user on how
much to adjust each bed levelling adjustment screw.

##### Probe and calculate in Repetier firmware {#probe_and_calculate_in_repetier_firmware}

This command probes the bed at 3 or more pre-defined points and
implements bed leveling compensation by either moving the A axis during
printing (as with regular bed leveling, `G29`) or by tilting the bed
with motors.

Parameters
:   `Snnn` Bed leveling method
:   `Pnnn` Bed correction method

The values for Snnn and Pnnn are as follows:

:   `S0` This method measures at the 3 probe points and creates a plane
    through these points. If you have a really planar bed this gives the
    optimum result. The 3 points must not be in one line and have a long
    distance to increase numerical stability.
:   `S1` This measures a grid. Probe point 1 is the origin and points 2
    and 3 span a grid. We measure BED_LEVELING_GRID_SIZE points in each
    direction and compute a regression plane through all points. This
    gives a good overall plane if you have small bumps measuring
    inaccuracies.
:   `S2` Bending correcting 4 point measurement. This is for
    cantilevered beds that have the rotation axis not at the side but
    inside the bed. Here we can assume no bending on the axis and a
    symmetric bending to both sides of the axis. So probe points 2 and 3
    build the symmetric axis and point 1 is mirrored to 1m across the
    axis. Using the symmetry we then remove the bending from 1 and use
    that as plane.
:   `P0` Use a rotation matrix. This will make z axis go up/down while
    moving in x/y direction to compensate the tilt. For multiple
    extruders make sure the height match the tilt of the bed or one will
    scratch. This is the default.
:   `P1` Motorized correction. This method needs a bed that is fixed on
    3 points from which 2 have a motor to change the height. The
    positions are defined in firmware by BED_MOTOR_1_X, BED_MOTOR_1_Y,
    BED_MOTOR_2_X, BED_MOTOR_2_Y, BED_MOTOR_3_X, BED_MOTOR_3_Y Motor 2
    and 3 are the one driven by motor driver 0 and 1. These can be extra
    motors like Felix Pro 1 uses them or a system with 3 z axis where
    motors can be controlled individually like the Sparkcube does. This
    method requires a Z max endstop.

#### G32: Undock Z Probe sled {#g32_undock_z_probe_sled}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{no}}<sup>1</sup> | buddy={{no}} | smoothie={{no}} | repetier={{no}} | druid={{no}} | reprapfirmware={{no}} | klipper={{no}} | bfb={{no}} | grbl={{no}} | machinekit={{no}} | makerbot={{no}} | redeem={{yes}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Notes

In Prusa Firmware this G-code is deactivated by default, must be turned
on in the source code.^1^

#### G33: Firmware dependent {#g33_firmware_dependent}

##### G33: Measure/List/Adjust Distortion Matrix (Repetier - Redeem) {#g33_measurelistadjust_distortion_matrix_repetier___redeem}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{yes|0.92.8+}} | druid={{no}} | smoothie={{no}} | reprapfirmware={{no}} | klipper={{no}} | bfb={{no}} | grbl={{no}} | machinekit={{no}} | makerbot={{no}} | redeem={{yes}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Usage
:   `G33`
:   `G33 Lnnn`
:   `G33 Rnnn`
:   `G33 Xnnn Ynnn Znnn`

Parameters
:   `L0` List distortion matrix in a report
:   `R0` Reset distortion matrix
:   `X[pos] Y[pos] Z[zCorrection]` Set correction for nearest point

Examples

`G33`\
`G33 R0`

When used with no parameters, `G33` will measure a grid of points and
store the distortion dips and valleys in the bed surface, and then
enable software distortion correction for the first few or several
layers. The values will be stored in EEPROM if enabled in firmware. You
must previously have `G28` homed, and your Z minimum/maximum height must
be set correctly for this to work. Use the optional parameters to list,
reset or modify the distortion settings. Distortion correction behavior
can be later turned on or off by code `M323`.

##### G33: Delta Auto Calibration (Marlin 1.1.x - MK4duo) {#g33_delta_auto_calibration_marlin_1.1.x___mk4duo}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | druid={{no}} | smoothie={{no}} | reprapfirmware={{yes|Use G32}} | bfb={{no}} | machinekit={{no}} | makerbot={{no}} | grbl={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```
End-stops and tower angle corrections are normalized **(P0)**;

Performs a 1-4-7 point calibration of delta height **(P1)**, end-stops,
delta radius **(P2)** and tower angle corrections **(P\>=3)** by a least
squares iteration process based on the displacement method.

Usage
:   `G33`
:   `G33 Pn T Cx.xx Fn Vn E O Rx.xx`

Parameters
:   `Pn` Number of probe points: n\*n (n= 0-10), when P is omitted the
    default set in Configuration.h is used.
:   `T` Do not calibrate tower angle corrections (if used with P\>=3);
    do not use the probe points near the towers, but the probe points
    opposite to the towers (if used with P=2)
:   `Cx.xx` Force the iterations to stop when a standard deviation from
    the zero plane less then x.xx mm is achieved; when C is omitted the
    iterations go on until the best possible standard deviation is
    reached.
:   `Fn` Force to run at least n iterations (n=1-30) and take the best
    result
:   `Vn` Verbose level: (n=0-3) 0 = dry run without calibration;
    1(default) = settings at start and end; 2 = settings at all
    iterations; 3 = settings and probe results
:   `E` Engage the probe for each point
:   `O` Do not probe at the required kinematic points but at positions
    offseted to the probe-offsets ^1^
:   `R` Temporary reduce the size of the probe grid by the specified
    amount (mm) ^1^

<!-- -->

Notes

^1^ since 2.0.9.2

Examples

***`G33 : calibrates with the default settings.`***\
`G33 Auto Calibrate`\
`Checking... AC`\
`.Height:297.77    Ex:+0.00  Ey:+0.00  Ez:+0.00    Radius:100.00`\
`.Tower angle :    Tx:+0.00  Ty:+0.00  Tz:+0.00`\
`Iteration : 01                                    std dev:0.306`\
`Iteration : 02                                    std dev:0.049`\
`Iteration : 03                                    std dev:0.033`\
`Iteration : 04                                    std dev:0.031`\
`Calibration OK                                    rolling back.`\
`.Height:297.69    Ex:-0.10  Ey:-0.12  Ez:+0.00    Radius:100.91`\
`.Tower angle :    Tx:-0.03  Ty:+0.25  Tz:+0.00`\
`Save with M500 and/or copy to Configuration.h`

***`G33 P6 V0 : probes 36 points in dry run mode.`***\
`G33 Auto Calibrate`\
`Checking... AC (DRY-RUN)`\
`.Height:297.77    Ex:+0.00  Ey:+0.00  Ez:+0.00    Radius:100.00`\
`.Tower angle :    Tx:+0.00  Ty:+0.00  Tz:+0.00`\
`.      c:+0.03     x:+0.32   y:+0.34   z:+0.41`\
`.                 yz:+0.37  zx:+0.32  xy:+0.17`\
`End DRY-RUN                                       std dev:0.306`

***`G33 P4 C0.05 T : probes 16 points and`***\
`                 `***`stops when a standard deviation of 0.05mm is reached;`***\
`                 `***`calibrates delta height, endstops and delta radius,`***\
`                 `***`leaves the tower angle corrections unaltered.`***\
`G33 Auto Calibrate`\
`Checking... AC`\
`.Height:297.78    Ex:+0.00  Ey:+0.00  Ez:+0.00    Radius:100.00`\
`Iteration : 01                                    std dev:0.317`\
`Iteration : 02                                    std dev:0.059`\
`Calibration OK                                    std dev:0.042`\
`.Height:297.66    Ex:-0.17  Ey:-0.13  Ez:+0.00    Radius:100.91`\
`Save with M500 and/or copy to Configuration.h`

***`G33 P2 : probes center and tower positions and`***\
`         `***`calibrates delta height, endstops and delta radius.`***\
`G33 Auto Calibrate`\
`Checking... AC`\
`.Height:297.78    Ex:+0.00  Ey:+0.00  Ez:+0.00    Radius:100.00`\
`Iteration : 01                                    std dev:0.374`\
`Iteration : 02                                    std dev:0.054`\
`Iteration : 03                                    std dev:0.007`\
`Calibration OK                                    rolling back.`\
`.Height:297.68    Ex:-0.14  Ey:-0.14  Ez:+0.00    Radius:101.23`\
`Save with M500 and/or copy to Configuration.h`

***`G33 P1 : probes the center and calibrates the delta height only.`***\
`G33 Auto Calibrate`\
`Checking... AC`\
`.Height:261.40                                Offset:+0.30`\
`Calibration OK                                std dev:0.000`\
`.Height:261.58                                Offset:+0.10`\
`Save with M500 and/or copy to Configuration.h`

*note: Height = delta height; Ex, Ey, Ez = end-stop corrections; Radius
= delta radius; Tx, Ty, Tz = tower angular corrections; c, x, y, z, yz,
zx, xy = probe results at center, towers and opposite to towers; std dev
= standard deviation of the probe results towards the zero plane.*

#### G34: Z Stepper Auto-Align {#g34_z_stepper_auto_align}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|2.0.4+}} | prusa={{no}} | buddy={{no}} | smoothie={{no}} | repetier={{no}} | druid={{no}} | reprapfirmware={{yes|Use M671 and G32}} | klipper={{no}} | bfb={{no}} | grbl={{no}} | machinekit={{no}} | makerbot={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
Use multiple Z steppers and a probe to align Z axis connection points.
See `M422` for other options.

Example

`G34 I3 T0.8 A1.5 ; 3 iterations, Target Accuracy 0.8, Amplification 1.5`

#### G34: Calculate Delta Height from toolhead position (DELTA) {#g34_calculate_delta_height_from_toolhead_position_delta}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | smoothie={{no}} | repetier={{no}} | druid={{no}} | reprapfirmware={{no}} | klipper={{no}} | bfb={{no}} | grbl={{no}} | machinekit={{no}} | makerbot={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Example

`G34`

The values specified are added to the calculated end stop position when
the axes are referenced. The calculated value is derived from the
distance of the toolhead from the current axis zero point. The user
would typically place the toolhead at the zero point of the axis and
issue the `G34` command. This value can be saved to EEPROM using the
`M500` command.

#### G38.x Straight Probe (CNC specific) {#g38.x_straight_probe_cnc_specific}

##### G38.2 probe toward workpiece, stop on contact, signal error if failure {#g38.2_probe_toward_workpiece_stop_on_contact_signal_error_if_failure}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|1.1.0+}} | prusa={{no}} | buddy={{no}} | reprapfirmware={{yes|3.0+}} | druid={{no}} | smoothie={{yes}} | bfb={{no}} | grbl={{yes}} | machinekit={{yes}} | makerbot={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```
Monitors probe input while moving linearly towards the specified
coordinates, stopping upon detecting contact or reaching specified
coordinates.

Usage
:   `G38.2 Xnnn Ynnn Znnn Fnnn`

Parameters
:   `Xnnn` target X coordinate
:   `Ynnn` target Y coordinate
:   `Znnn` target Z coordinate
:   `Fnnn` Feedrate in mm/min

Example

`G38.2 Z0`\
`G38.2 X50`\
`G38.2 Z10 Y10`

##### G38.3 probe toward workpiece, stop on contact {#g38.3_probe_toward_workpiece_stop_on_contact}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|1.1.0+}} | prusa={{no}} | buddy={{no}} | reprapfirmware={{yes|3.0+}} | druid={{no}} | smoothie={{yes}} | bfb={{no}} | grbl={{yes}} | machinekit={{yes}} | makerbot={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```
##### G38.4 probe away from workpiece, stop on loss of contact, signal error if failure {#g38.4_probe_away_from_workpiece_stop_on_loss_of_contact_signal_error_if_failure}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|2.0.0+}} | prusa={{no}} | buddy={{no}} | reprapfirmware={{yes|3.0+}} | druid={{no}} | bfb={{no}} | grbl={{yes}} | machinekit={{yes}} | makerbot={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
##### G38.5 probe away from workpiece, stop on loss of contact {#g38.5_probe_away_from_workpiece_stop_on_loss_of_contact}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|2.0.0+}} | prusa={{no}} | buddy={{no}} | reprapfirmware={{yes|3.0+}} | druid={{no}} | bfb={{no}} | grbl={{yes}} | machinekit={{yes}} | makerbot={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
#### G40: Compensation Off (CNC specific) {#g40_compensation_off_cnc_specific}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | druid={{no}} | reprapfirmware={{no}} | smoothie={{no}} | klipper={{no}} | bfb={{no}} | grbl={{yes}} | machinekit={{yes}} | makerbot={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{yes}} }}
```
`G40` turns off cutter compensation. If tool compensation was on the
next move must be a linear move and longer than the tool diameter. It is
OK to turn compensation off when it is already off.
<http://www.linuxcnc.org/docs/2.5/html/gcode/tool_compensation.html>

#### G42: Move to Grid Point {#g42_move_to_grid_point}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|1.1.2+}} | prusa={{no}} | buddy={{yes}} | repetier={{no}} | druid={{no}} | smoothie={{no}} | reprapfirmware={{no}} | klipper={{no}} | bfb={{no}} | machinekit={{no}} | makerbot={{no}} | grbl={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```
`G42` does a fast move in XY to any of the intersection points in the
bed calibration grid. This is useful during calibration to align the
nozzle or probe.

Parameters
:   `Inn` Grid X index (zero-based). If omitted, the nearest latitude.
:   `Jnn` Grid Y index (zero-based). If omitted, the nearest longitude.
:   `P` Probe flag. Moves the probe to the grid point (instead of the
    nozzle).
:   `Fnnn` Feedrate (mm/min)

Example

`G42 I3 J4 P F3000 ; Move the probe to grid coordinate 3, 4`

#### G53..59: Coordinate System Select (CNC specific) {#g53..59_coordinate_system_select_cnc_specific}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|2.0.0+}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | druid={{no}} | reprapfirmware={{yes|1.21+}} | smoothie={{yes}} | klipper={{no}} | bfb={{no}} | grbl={{yes}} | makerbot={{no}} | machinekit={{yes}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{yes}} }}
```
G53 refers to the native machine coordinate system, while the remaining
coordinate systems are typically used to define the offset to the origin
of specific parts.

See
[linuxcnc.org](http://linuxcnc.org/docs/html/gcode/g-code.html#gcode:g54-g59.3)
for more help

Not all builds of RepRapFirmware support these commands. For those that
do (e.g. Duet WiFi/Ethernet and Duet 3), from firmware version 2.02 the
workplace coordinate offsets are included in the data saved to
config-override.g by the M500 command.

Marlin supports these commands when enabled with the #define
CNC_COORDINATE_SYSTEMS option in Configuration_adv.h.

#### G60: Save / Restore position {#g60_save_restore_position}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|2.0.2+}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | druid={{yes}} | reprapfirmware={{yes|1.21+}} | smoothie={{no}} | klipper={{no}} | bfb={{no}} | grbl={{no}} | machinekit={{no}} | redeem={{no}} | makerbot={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```
Use this command to save the current position to a memory slot, restore
(and move to) a saved position, or delete a previously-saved position.
When moving to a saved position, you can choose which axes to move, and
some firmwares allow you to specify an offset distance for each axis.
See usage notes for each firmware below.

G60 S Usage:
:   `G60 Snn`

Parameters
:   `Snn` `<nn>`{=html} specifies a memory slot \# (0-based) to save
    into (default 0)

- **RepRapFirmware**: RRF 1.21 has 3 slots (0..2). RRF 2.02 adds two
  more slots (4..5) skipping slot index 3. When a print is paused the
  coordinates are saved to slot 1 automatically, and at the start of a
  tool change the coordinates are saved to slot 2 automatically. Use G0
  or G1 with the R0, R1 or R2 parameter to move the current tool to a
  saved position.

<!-- -->

- **Marlin**: The number of save slots is defined with
  `SAVED_POSITIONS`.

<!-- -->

- **Druid**: This firmware always has 64 slots (0..63).

G60 Q Usage:
:   `G60 Qnnn Fnnn X Y Z ... E`

Move back to a saved position. Specify one or more axes to restore
unless all axes should be restored.

Parameters
:   `Qnnn` - From slot \# 0-63 (required)
:   `Fnnn` - Feedrate (units/min)
:   `X` - Flag to restore X
:   `Y` - Flag to restore Y
:   `Z` - Flag to restore Z
:   `E` - Flag to restore E

- Other axis letters may be included for fancier robots. If no axes are
  specified with `G60 Qnn` then all axes are restored.

<!-- -->

- **Marlin:** Put a value next to an axis letter to specify an offset to
  add to the position before moving. The E axis is restored but never
  actually moved by this command.

G60 D Usage:
:   `G60 Dnnn` - Delete content of slot number nnn (0\...63)
:   `G60 D` - if D is provided without a slot number, all 64 slots will
    be deleted.

<!-- -->

Notes:
:   Only one of S, Q, or D may be used in the command. If more than one
    is present, the whole command will be ignored.

<!-- -->

Examples

`G60 S0                 ; Save current position to slot #0`\
`G60 S63                ; Save current position to slot #63`\
`G60 Q55                ; Move to the position stored in slot #55 `\
`G60 Q10 F20000 X Y     ; Move XY to the position stored in slot #10, with feedrate 20000 units/min. `\
`G60 Q0 X               ; Move X to the position saved in slot #0`\
`G60 D0                 ; Delete the position saved in slot #0`\
`G60 D                  ; Delete all saved positions from all slots`\
`G60                    ; List all saved positions`

#### G61: Restore saved position {#g61_restore_saved_position}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|2.0.2+}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | druid={{no}} | reprapfirmware={{no}} | smoothie={{no}} | klipper={{no}} | bfb={{no}} | grbl={{no}} | machinekit={{no}} | redeem={{no}} | makerbot={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
Use this command to restore (and move to) a saved position, optionally
specifying which axes to restore, with an optional offset for each axis.

Usage
:   `G61 Snn`

Parameters
:   `Snn` `<nn>`{=html} specifies memory slot \# (0-based) to restore
    from (default 0)

Move back to the position that was saved in the given slot. If nothing
was saved in the slot, do nothing.

:   `G61 Snn Fnnn X Y Z E`

Move back to a saved position, specifying one or more axes to restore,
with optional offset. The E axis is restored but never actually moved by
this command.

Parameters
:   `Snnn` - From slot \# 0-63 (required)
:   `Fnnn` - Feedrate (units/min)
:   `X` - Flag to restore X axis, with optional X offset
:   `Y` - Flag to restore Y axis, with optional Y offset
:   `Z` - Flag to restore Z axis, with optional Z offset
:   `E` - Flag to restore E axis, with optional E offset

Other axis letters may be included for fancier robots. If no axes are
specified then all axes are restored.

Put a value next to an axis letter to specify the offset to add to the
position before moving / restoring.

Examples

`G61 S15                ; Move to the position from slot #15`\
`G61 S10 F20000 X3 Y    ; Move XY to the XY position from slot #10, shifting X by 3, with feedrate 20000 units/min`\
`G61 S0 X               ; Move X to the X position from slot #0`

#### G68: Coordinate rotation {#g68_coordinate_rotation}

```{=mediawiki}
{{Firmware Support | druid={{no}} | reprapfirmware={{yes|3.4 and later}} }}
```

Usage
:   `G68 Xnnn Ynnn Rnnnn [I]`
:   `G68 Annn Bnnn Rnnnn [I]`

Parameters
:   `Xnnn, Ynnn...` Centre coordinates to rotate about
:   `Annn` first centre coordinate in the selected plane (e.g.
    equivalent to Xnnn if the selected plane is XY)
:   `Bnnn` second centre coordinate in the selected plane (e.g.
    equivalent to Ynnn if the selected plane is XY)
:   `Rnnn` angle to rotate in degrees. Positive angles rotate
    anticlockwise when viewing the selected plane from above.
:   `I` if this parameter is present, the R parameter is added to the
    existing rotation instead of being absolute

Rotates the coordinate system in the current plane as selected by G17,
G18 or G19. You may either specify the coordinates of the two axes of
the selected plan (e.g. X and Y if using the default XY plane or after
G17) or you may specify A and B coordinates.

RepRapFirmware implements G68 for the XY plane only.

#### G69: Cancel coordinate rotation {#g69_cancel_coordinate_rotation}

```{=mediawiki}
{{Firmware Support | druid={{no}} | reprapfirmware={{yes|3.4 and later}} }}
```

Usage
:   `G69`

This cancels any coordinate rotation that was set up by G68.

#### G75: Print temperature interpolation {#g75_print_temperature_interpolation}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{yes}} | buddy={{no}} | smoothie={{no}} | repetier={{no}} | druid={{no}} | reprapfirmware={{no}} | klipper={{no}} | bfb={{no}} | grbl={{no}} | machinekit={{no}} | makerbot={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
Show/print PINDA temperature interpolating.

Usage
:   `G75`

#### G76: PINDA probe temperature calibration {#g76_pinda_probe_temperature_calibration}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}}<sup>1</sup> | prusa={{yes}} | buddy={{no}} | smoothie={{no}} | repetier={{no}} | druid={{no}} | reprapfirmware={{partial|Use G31}} | klipper={{no}} | bfb={{no}} | grbl={{no}} | machinekit={{no}} | makerbot={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
This G-code is used to calibrate the temperature drift of the PINDA
(inductive Sensor).

The PINDAv2 sensor has a built-in thermistor which has the advantage
that the calibration can be done once for all materials.

The Original i3 Prusa MK2/s uses PINDAv1 and this calibration improves
the temperature drift, but not as good as the PINDAv2.

Usage
:   `G76`
:   `G76 B`^1^
:   `G76 P`^1^

<!-- -->

Parameters
:   `B` Calibrate bed only ^1^
:   `P` Calibrate probe only ^1^

<!-- -->

Example

`G76`\
\
`echo PINDA probe calibration start`\
`echo start temperature: 35.0°`\
`echo ...`\
`echo PINDA temperature -- Z shift (mm): 0.---`

Notes^1^

Marlin requires `PROBE_TEMP_COMPENSATION`.

This process can take a very long time. The timeout is currently set to
15min to allow the parts to fully heat up and cool down.

Use `M500` to save the result to EEPROM.

At this moment it is only supported in Marlin bugfix-2.0.x branch.

#### G80: Cancel Canned Cycle (CNC specific) {#g80_cancel_canned_cycle_cnc_specific}

```{=mediawiki}
{{Firmware Support | marlin={{no}} | prusa={{no}} | buddy={{no}} | reprapfirmware={{no}} | druid={{no}} | grbl={{yes}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
It cancel canned cycle modal motion. G80 is part of modal group 1, so
programming any other G code from modal group 1 will also cancel the
canned cycle.

#### G80: Mesh-based Z probe {#g80_mesh_based_z_probe}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{partial|G29}} | prusa={{yes}} | buddy={{yes}}<sup>3</sup> | smoothie={{no}} | repetier={{no}} | druid={{no}} | reprapfirmware={{no}} | klipper={{no}} | bfb={{no}} | grbl={{no}} | machinekit={{no}} | makerbot={{no}} | redeem={{no}} | mk4duo={{partial|G29}} | yaskawa={{no}} }}
```
Default 3x3 grid can be changed on MK2.5/s and MK3/s to 7x7 grid.

Parameters
:   *This command can be used without any additional parameters.*
:   `N` Number of mesh points on x axis. Default is 3. Valid values are
    3 and 7.
:   `C` Probe retry counts. Default is value stored in EEPROM. Valid
    values are 1 to 10.
:   `O` Return to origin. Default is 1. Valid values are 0 (false) and 1
    (true). ^2^
:   `M` Use magnet compensation. Will only be used if number of mesh
    points is set to 7. Default is value stored in EEPROM. Valid values
    are 0 (false) and 1 (true). ^2^

Using the following parameters enables additional \"manual\" bed
leveling correction. Valid values are -100 microns to 100 microns.

:   `L` Left Bed Level correct value in um.
:   `R` Right Bed Level correct value in um.
:   `F` Front Bed Level correct value in um.
:   `B` Back Bed Level correct value in um.

The following parameters are used to define the area used by the print:

:   `X` area lower left point X coordinate ^2^
:   `Y` area lower left point Y coordinate ^2^
:   `W` area width (on X axis) ^2^
:   `H` area height (on Y axis) ^2^

^1^Prusa Firmware till version 3.13.3

:   `R` Probe retries. Default 3 max. 10 ^1^
:   `V` Verbosity level 1=low, 10=mid, 20=high.It can be only used if
    firmware has been compiled with SUPPORT_VERBOSITY active. ^1^

^2^Prusa Firmware from version 3.14.0

^3^Prusa MK3.5, MK3.9 and MK4

#### G81: Mesh bed leveling status {#g81_mesh_bed_leveling_status}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{partial|M420}} | prusa={{yes}} | buddy={{no|M420}} | smoothie={{no}} | repetier={{no}} | druid={{no}} | reprapfirmware={{no}} | klipper={{no}} | bfb={{no}} | grbl={{no}} | machinekit={{no}} | makerbot={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
Prints mesh bed leveling status and bed profile if activated.

Usage
:   `G81`

<!-- -->

Notes

Equivalent to `M420 V` in Marlin Firmware (and possibly [G29
T](G-code#G29:_Detailed_Z-Probe "G29 T"){.wikilink} depending on
leveling system).

#### G82: Single Z probe at current location {#g82_single_z_probe_at_current_location}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{partial|G30}} | prusa={{yes}}<sup>1</sup> | buddy={{no|G30}} | smoothie={{no}} | repetier={{no}} | druid={{no}} | reprapfirmware={{partial|G30}} | klipper={{no}} | bfb={{no}} | grbl={{no}} | machinekit={{no}} | makerbot={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
WARNING! USE WITH CAUTION! If you\'ll try to probe where is no leveling
pad, nasty things can happen!

Usage
:   `G82`

<!-- -->

Notes

In Prusa Firmware this G-code is deactivated by default, must be turned
on in the source code.^1^

#### G83: Babystep in Z and store to EEPROM {#g83_babystep_in_z_and_store_to_eeprom}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{yes}}<sup>1</sup> | buddy={{no}} | smoothie={{no}} | repetier={{no}} | druid={{no}} | reprapfirmware={{no}} | klipper={{no}} | bfb={{no}} | grbl={{no}} | machinekit={{no}} | makerbot={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Usage
:   `G83`

<!-- -->

Notes

In Prusa Firmware this G-code is deactivated by default, must be turned
on in the source code.^1^

#### G84: UNDO Babystep Z (move Z axis back) {#g84_undo_babystep_z_move_z_axis_back}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{yes}} <sup>1</sup> | buddy={{no}} | smoothie={{no}} | repetier={{no}} | druid={{no}} | reprapfirmware={{no}} | klipper={{no}} | bfb={{no}} | grbl={{no}} | machinekit={{no}} | makerbot={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Usage
:   `G84`

<!-- -->

Notes

In Prusa Firmware this G-code is deactivated by default, must be turned
on in the source code.^1^

#### G85: Pick best babystep {#g85_pick_best_babystep}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{yes}}<sup>1</sup> | budddy={{no}} | smoothie={{no}} | repetier={{no}} | druid={{no}} | reprapfirmware={{no}} | klipper={{no}} | bfb={{no}} | grbl={{no}} | machinekit={{no}} | makerbot={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Usage
:   `G85`

<!-- -->

Notes

In Prusa Firmware this G-code is deactivated by default, must be turned
on in the source code.^1^

#### G86: Disable babystep correction after home {#g86_disable_babystep_correction_after_home}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{yes}} | buddy={{no}} | smoothie={{no}} | repetier={{no}} | druid={{no}} | reprapfirmware={{no}} | klipper={{no}} | bfb={{no}} | grbl={{no}} | machinekit={{no}} | makerbot={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
This G-code will be performed at the start of a calibration script.

Usage
:   `G86`

#### G87: Enable babystep correction after home {#g87_enable_babystep_correction_after_home}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{yes}} | buddy={{no}} | smoothie={{no}} | repetier={{no}} | druid={{no}} | reprapfirmware={{no}} | klipper={{no}} | bfb={{no}} | grbl={{no}} | machinekit={{no}} | makerbot={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
This G-code will be performed at the end of a calibration script.

Usage
:   `G87`

#### G88: Reserved {#g88_reserved}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{yes}}<sup>1</sup> | buddy={{no}} | smoothie={{no}} | repetier={{no}} | druid={{no}} | reprapfirmware={{no}} | klipper={{no}} | bfb={{no}} | grbl={{no}} | machinekit={{no}} | makerbot={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Usage
:   `G88`

<!-- -->

Notes

This G-code currently does not do anything.

#### G90: Set to Absolute Positioning {#g90_set_to_absolute_positioning}

```{=mediawiki}
{{Firmware Support | fived={{yes}} | teacup={{yes}} | sprinter={{yes}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | repetier={{yes}} | druid={{yes}} | smoothie={{yes}} | reprapfirmware={{yes}} | klipper={{yes}} | bfb={{yes}} | machinekit={{yes}} | grbl={{yes}} | redeem={{yes}} | makerbot={{yes}} | mk4duo={{yes}} | yaskawa={{yes}} }}
```

Example

`G90`

All coordinates from now on are absolute relative to the origin of the
machine. (This is the RepRap default.)

#### G91: Set to Relative Positioning {#g91_set_to_relative_positioning}

```{=mediawiki}
{{Firmware Support | fived={{yes}} | teacup={{yes}} | sprinter={{yes}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | repetier={{yes}} | druid={{yes}} | smoothie={{yes}} | reprapfirmware={{yes}} | klipper={{yes}} | bfb={{no}} | machinekit={{yes}} | grbl={{yes}} | redeem={{yes}} | makerbot={{yes}} | mk4duo={{yes}} | yaskawa={{yes}} }}
```

Example

`G91`

All coordinates from now on are relative to the last position. Note:
RepRapFirmware latest revision firmware uses `M83` to set the extruder
to relative mode: extrusion is NOT set to relative by ReprapFirmware on
`G91`: only X,Y and Z are set to relative. By contrast, Marlin (for
example) DOES also set extrusion to relative on a `G91` command, as well
as setting X, Y and Z.

#### G92: Set Position {#g92_set_position}

```{=mediawiki}
{{Firmware Support | fived={{yes}} | teacup={{yes}} | sprinter={{yes}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | repetier={{yes}} | druid={{yes}} | smoothie={{yes}} | reprapfirmware={{yes}} | klipper={{yes}} | bfb={{yes}} | machinekit={{yes}} | makerbot={{yes}} | grbl={{yes}} | redeem={{yes}} | mk4duo={{yes}} | yaskawa={{yes}} }}
```

Parameters
:   *This command can be used without any additional parameters.*
:   `Xnnn` new X axis position
:   `Ynnn` new Y axis position
:   `Znnn` new Z axis position
:   `Ennn` new extruder position

Example

`G92 X10 E90`

Allows programming of absolute zero point, by reseting the current
position to the values specified. This would set the machine\'s X
coordinate to 10, and the extrude coordinate to 90. No physical motion
will occur.

A `G92` without coordinates will reset all axes to zero on some
firmware. This does not apply to RepRapFirmware.

##### G92.x: Reset Coordinate System Offsets (CNC specific) {#g92.x_reset_coordinate_system_offsets_cnc_specific}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{partial|1.1.6+}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | druid={{no}} | reprapfirmware={{no}} | smoothie={{yes}} | klipper={{no}} | bfb={{no}} | grbl={{yes}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Usage
:   `G92.1` - Reset axis offsets (and parameters 5211-5219) to zero.
    (`X Y Z A B C U V W`)
:   `G92.2` - Reset axis offsets to zero

#### G93: Feed Rate Mode (Inverse Time Mode) (CNC specific) {#g93_feed_rate_mode_inverse_time_mode_cnc_specific}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | druid={{no}} | reprapfirmware={{yes|3.5+}} | smoothie={{no}} | klipper={{no}} | bfb={{no}} | grbl={{yes}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{yes}} }}
```
`G93` is Inverse Time Mode. In inverse time feed rate mode, an `F` word
means the move should be completed in (one divided by the `F` number)
minutes. For example, `F2.0` means the move should be completed in a
half a minute.

When the inverse time feed rate mode is active, an `F` word must appear
on every line which has a `G1`, `G2`, or `G3` motion, and an `F` word on
a line that does not have `G1`, `G2`, or `G3` is ignored. Being in
inverse time feed rate mode does not affect `G0` (rapid move) motions.

#### G94: Feed Rate Mode (Units per Minute) (CNC specific) {#g94_feed_rate_mode_units_per_minute_cnc_specific}

```{=mediawiki}
{{Firmware Support | reprapfirmware={{yes|3.5+}} | grbl={{yes}} | redeem={{no}} | druid={{no}} | mk4duo={{no}} | yaskawa={{yes}} }}
```
G94 is Units per Minute Mode. In units per minute feed mode, an F word
is interpreted to mean the controlled point should move at a certain
number of inches per minute, millimeters per minute, or degrees per
minute, depending upon what length units are being used and which axis
or axes are moving.

#### G98: Activate farm mode {#g98_activate_farm_mode}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{yes}} | buddy={{no}} | smoothie={{no}} | repetier={{no}} | druid={{no}} | reprapfirmware={{no}} | klipper={{no}} | bfb={{no}} | grbl={{no}} | machinekit={{no}} | makerbot={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
Enable Prusa-specific Farm functions and g-code.

Usage

`G98`

Notes

Set of internal Prusa commands

`PRUSA [ Ping | PRN | FAN | fn | thx | uvlo | fsensor_recover | MMURES | RESET | fv | M28 | SN | Fir | Rev | Lang | Lz | Beat | FR ]`

Parameters
:   `Ping`
:   `PRN` Prints revision of the printer.
:   `FAN` Prints fan details.
:   `fn` Prints farm number.
:   `thx`
:   `uvlo` Resets UVLO aka Power Panic and continues SD print.
:   `fsensor_recover` Filament sensor recover - restore print and
    continue.
:   `MMURES` Reset MMU.
:   `Reset` Resets Printer.
:   `fv` ??? get file version. ???
:   `M28` M28 write to SD.
:   `SN` Get serial number from 32U2 processor. Typical format of S/N
    is:CZPX0917X003XC13518
:   `Fir` Prints firmware version.
:   `Rev` Prints filament size, elelectronics, nozzle type.
:   `Lang` Reset the language.
:   `Lz` ??? maybe resets Live Z values to 0 ???
:   `Beat` Kick farm link timer.
:   `FR` Full factory reset.
:   `nozzle set 'diameter'` Set nozzle diameter.
:   `nozzle D'diameter'` Check nozzle diameter.
:   `nozzle` Print nozzle diameter

#### G99: Deactivate farm mode {#g99_deactivate_farm_mode}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{yes}} | buddy={{no}} | smoothie={{no}} | repetier={{no}} | druid={{no}} | reprapfirmware={{no}} | klipper={{no}} | bfb={{no}} | grbl={{no}} | machinekit={{no}} | makerbot={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Usage

`G99`

#### G100: Calibrate floor or rod radius {#g100_calibrate_floor_or_rod_radius}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{yes|0.92+}} | druid={{no}} | smoothie={{no}} | reprapfirmware={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | klipper={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `X` Flag to set floor for X axis
:   `Y` Flag to set floor for Y axis
:   `Z` Flag to set floor for Z axis
:   `Rnnn` Radius to add

Examples

`G100 X Y Z ; set floor for argument passed in. Number ignored and may be absent.`\
`G100 R5    ; Add 5 to radius. Adjust to be above floor if necessary`\
`G100 R0    ; Set radius based on current z measurement. Moves all axes to zero`

#### G130: Set digital potentiometer value {#g130_set_digital_potentiometer_value}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | druid={{no}} | reprapfirmware={{no}} | smoothie={{no}} | klipper={{no}} | grbl={{no}} | bfb={{no}} | machinekit={{no}} | makerbot={{yes}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Example

`G130 X10 Y18 Z15 A20 B12`

Set the digital potentiometer value for the given axes. This is used to
configure the current applied to each stepper axis. The value is
specified as a value from 0-127; the mapping from current to
potentimeter value is machine specific.

#### G131: Remove offset {#g131_remove_offset}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{yes|0.91+}} | druid={{no}} | smoothie={{no}} | reprapfirmware={{no}} | klipper={{no}} | bfb={{no}} | grbl={{no}} | machinekit={{no}} | makerbot={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
#### G132: Calibrate endstop offsets {#g132_calibrate_endstop_offsets}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{yes|0.91+}} | druid={{no}} | smoothie={{no}} | reprapfirmware={{no}} | klipper={{no}} | grbl={{no}} | bfb={{no}} | machinekit={{no}} | makerbot={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
#### G133: Measure steps to top {#g133_measure_steps_to_top}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{yes|0.91+}} | druid={{no}} | smoothie={{no}} | reprapfirmware={{no}} | klipper={{no}} | grbl={{no}} | bfb={{no}} | machinekit={{no}} | makerbot={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
#### G161: Home axes to minimum {#g161_home_axes_to_minimum}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{yes}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | druid={{no}} | smoothie={{no}} | reprapfirmware={{no}} | klipper={{no}} | grbl={{no}} | bfb={{no}} | machinekit={{no}} | makerbot={{yes}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `X` Flag to home the X axis to its minimum position
:   `Y` Flag to home the Y axis to its minimum position
:   `Z` Flag to home the Z axis to its minimum position
:   `Fnnn` Desired feedrate for this command

Example

`G161 X Y Z F1800`

Instruct the machine to home the specified axes to their minimum
position. Similar to `G28`, which decides on its own in which direction
to search endstops.

#### G162: Home axes to maximum {#g162_home_axes_to_maximum}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{yes}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | druid={{no}} | smoothie={{no}} | reprapfirmware={{no}} | klipper={{no}} | grbl={{no}} | bfb={{no}} | machinekit={{no}} | makerbot={{yes}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `X` Flag to home the X axis to its maximum position
:   `Y` Flag to home the Y axis to its maximum position
:   `Z` Flag to home the Z axis to its maximum position
:   `Fnnn` Desired feedrate for this command

Example

`G162 X Y Z F1800`

Instruct the machine to home the specified axes to their maximum
position.

#### G425: Perform auto-calibration with calibration cube {#g425_perform_auto_calibration_with_calibration_cube}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|2.0.0+}} | prusa={{no}} | buddy={{yes}} | repetier={{no}} | druid={{no}} | smoothie={{no}} | klipper={{no}} | reprapfirmware= {{no}} | bfb={{no}} | grbl={{no}} | machinekit={{no}} | makerbot={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
This performs an automatic calibration of backlash, positional errors
and nozzle offset by touching the nozzle on the sides of a bed mounted,
electrically conductive cube, washer or bolt.

Parameters
:   `B` Perform calibration of backlash only.
:   `Tnnn` Perform calibration of toolhead only.
:   `V` Probe cube and print position, error, backlash and hotend
    offset.
:   `Unnn` Uncertainty, how far to start probe away from the cube (mm)

<!-- -->

Examples (Marlin)

`G425                ; Perform full calibration sequence`\
`T1                  ; Switch to second nozzle`\
`G425 V              ; Validate by showing report for T1`\
`T0                  ; Switch to second nozzle`\
`G425 V              ; Validate by showing report for T0`

## M-commands {#m_commands}

#### M0: Stop or Unconditional stop {#m0_stop_or_unconditional_stop}

```{=mediawiki}
{{Firmware Support | fived={{yes}} | teacup={{yes}} | sprinter={{no}} | marlin={{yes}} | prusa={{yes}}<sup>3</sup> | buddy={{yes}} | repetier={{no}} | druid={{no}} | smoothie={{no}} | reprapfirmware={{yes}} | klipper={{no}} | bfb={{no}} | machinekit={{yes}} | makerbot={{no}} | grbl={{yes}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{yes}} }}
```

Parameters
:   *This command can be used without any additional parameters.*
:   `Pnnn` Time to wait, in milliseconds^1^
:   `Snnn` Time to wait, in seconds^2^

Example

`M0`

The RepRap machine finishes any moves left in its buffer, then shuts
down. All motors and heaters are turned off. It can be started again by
pressing the reset button on the master microcontroller, although this
step is not mandatory on RepRapFirmware. See also `M1`, `M112`.

The Marlin Firmware does wait for user to press a button on the LCD, or
a specific time. \"M0 P2000\" waits 2000 milliseconds, \"M0 S2\" waits 2
seconds.

RepRapFirmware executes cancel.g if this file is present, if the print
is paused and if the axes are homed. Otherwise stop.g is run and the
drives are put into idle mode. Also the heaters are turned off if no
\'H1\' parameter is specified.

Notes

^1^Not available in RepRapFirmware, but as a work-around `G4` can be run
before `M0`.

^2^Only available on Marlin and Prusa Firmware.

^3^\"Wait for user \...\" is shown on LCD in Prusa Firmware.

#### M1: Sleep or Conditional stop {#m1_sleep_or_conditional_stop}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{yes}}<sup>1</sup> | buddy={{yes}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes}} | klipper={{yes}} | bfb={{no}} | makerbot={{no}} | machinekit={{no}} | grbl={{yes}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{yes}} }}
```

Example

`M1`\
`M1 Hello world `^`1`^` `

The RepRap machine finishes any moves left in its buffer, then shuts
down. All motors and heaters are turned off. It can still be sent G and
M codes, the first of which will wake it up again. See also `M0`,
`M112`.

The Marlin does the same as `M0`.

In Prusa 8-bit Firmware ^1^ the `M1` needs at least a *space* behind the
command to be executed correctly. It can be used the same as
`M0 P``<ms>`{=html} or `M0 S``<seconds>`{=html} but will ignore the
following \"message\".

Prusa Firmware 8-bit example

`M1 S5`` will wait for 5 seconds and show in the LCD status line "Waiting for user..." the same as ``M0 S5`\
`M1 Hello world`` will show in the LCD status line "Hello world" and wait until the user press the LCD knob.`\

If Marlin is emulated in RepRapFirmware, this does the same as
[M25](G-code#M25:_Pause_SD_print "M25"){.wikilink} if the code was read
from a serial or Telnet connection, else the macro file `sleep.g` is run
before all heaters and drives are turned off.

#### M2: Program End {#m2_program_end}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{yes}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | klipper={{no}} | bfb={{no}} | machinekit={{no}} | grbl={{yes}} | makerbot={{yes}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{yes}} }}
```

Example

`M2`

Teacup firmware does the same as `M84`.

#### M3: Spindle On, Clockwise (CNC specific) {#m3_spindle_on_clockwise_cnc_specific}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{yes}} | sprinter={{no}} | marlin={{yes}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{yes}} | smoothie={{yes}} | reprapfirmware={{yes}} | klipper={{no}} | bfb={{no}} | machinekit={{no}} | makerbot={{no}} | grbl={{yes}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{yes}} }}
```

Parameters
:   `Snnn` Spindle RPM

Example

`M3 S4000`

The spindle is turned on with a speed of 4000 RPM.

Teacup firmware turn extruder on (same as `M101`).

RepRapFirmware interprets this code only if in CNC mode (`M453`), in
laser mode (`M452`) or if a Roland mill has been configured. You must
always provide an S parameter with this command to specify the required
spindle speed pr laser power. In RepRapFirmware 2.05RC2 and later, and
RepRapFirmware 3.0beta13 and later, in laser mode (M452) the laser will
only fire during G1/G2/G2 moves.

In Repetier-Firmware in laser mode you need `S0`..`S255` to set laser
intensity. Normally you use `S255` to turn it on full power for moves.
Laser will only fire during `G1`/`G2`/`G3` moves and in laser mode
(`M452`).

#### M4: Spindle On, Counter-Clockwise (CNC specific) {#m4_spindle_on_counter_clockwise_cnc_specific}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{yes}} | reprapfirmware={{no}} | smoothie={{no}} | klipper={{no}} | bfb={{no}} | machinekit={{no}} | makerbot={{no}} | grbl={{yes}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{yes}} }}
```

Example

`M4 S4000`

The spindle is turned on with a speed of 4000 RPM.

#### M5: Spindle Off (CNC specific) {#m5_spindle_off_cnc_specific}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{yes}} | sprinter={{no}} | marlin={{yes}} | prusa={{no}} | buddy={{no}} | repetier={{yes}} | reprapfirmware={{yes}} | smoothie={{yes}} | bfb={{no}} | machinekit={{no}} | grbl={{yes}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{yes}} }}
```

Example

`M5`

The spindle is turned off.

Teacup firmware turn extruder off (same as `M103`).

#### M6: Tool change {#m6_tool_change}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{yes}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{no}} | reprapfirmware={{no}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{yes}} }}
```

Example

`M6`

#### M7: Mist Coolant On (CNC specific) {#m7_mist_coolant_on_cnc_specific}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{yes}}: Use M106 | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | grbl={{yes}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{yes}} }}
```

Example

`M7`

Mist coolant is turned on (if available)

Teacup firmware turn on the fan, and set fan speed (same as `M106`).

#### M8: Flood Coolant On (CNC specific) {#m8_flood_coolant_on_cnc_specific}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{yes}}: Use M106 | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | grbl={{yes}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{yes}} }}
```

Example

`M8`

Flood coolant is turned on (if available)

#### M9: Coolant Off (CNC specific) {#m9_coolant_off_cnc_specific}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{yes}}: Use M106 | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | grbl={{yes}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{yes}} }}
```

Example

`M9`

All coolant systems are turned off.

#### M10: Vacuum On (CNC specific) {#m10_vacuum_on_cnc_specific}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{yes}}: Use M106 | sprinter={{no}} | marlin={{yes|2.0.8+}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{yes}} }}
```

Example

`M10`

Dust collection vacuum system turned on.

#### M11: Vacuum Off (CNC specific) {#m11_vacuum_off_cnc_specific}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{yes}}: Use M106 | sprinter={{no}} | marlin={{yes|2.0.8+}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{yes}} }}
```

Example

`M11`

Dust collection vacuum system turned off.

#### M13: Spindle on (clockwise rotation) and coolant on (flood) {#m13_spindle_on_clockwise_rotation_and_coolant_on_flood}

```{=mediawiki}
{{Firmware Support | fived={{???}}
```
\| teacup={{???}} \| sprinter={{???}} \| marlin=`{{no}}`{=mediawiki} \|
prusa=`{{no}}`{=mediawiki} \| buddy=`{{no}}`{=mediawiki} \|
repetier={{???}} \| reprapfirmware={{???}} \| smoothie={{???}} \|
bfb={{???}} \| machinekit={{???}} \| redeem={{???}} \| mk4duo={{???}} \|
yaskawa=`{{yes}}`{=mediawiki} }}

This one M-code does the work of both M03 and M08. It is not unusual for
specific machine models to have such combined commands, which make for
shorter, more quickly written programs.

Example

`M13`

#### M16: Expected Printer Check {#m16_expected_printer_check}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|1=(2.0+)}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```
Do a case-sensitive comparison between the string argument and the
configured `MACHINE_NAME`. If the machine name doesn\'t match, halt the
printer so that a reset is required. This safety feature is meant to
prevent G-code sliced for a specific machine from being used on any
other machine. In Marlin this feature is enabled with
`EXPECTED_PRINTER_CHECK`.

Example

`M16 Cookie Monster`

#### M17: Enable/Power all stepper motors {#m17_enablepower_all_stepper_motors}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{yes|1=(automatic)}} | sprinter={{no}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | druid={{yes}} | repetier={{no}} | reprapfirmware={{yes|3.3 and later}} | smoothie={{yes}} | bfb={{no}} | machinekit={{no}} | redeem={{yes}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   *This command can be used without any additional parameters.^1^*
:   `X` X axis
:   `Y` Y axis
:   `Z` Z axis
:   `E` All extruders

<!-- -->

Example

`M17`\
`M17 X E0`\

Powers on stepper motors.

Notes

^1^Ability to specify axes was added to Marlin 2.0 and may not be
available on other firmware implementations.

#### M18: Disable all stepper motors {#m18_disable_all_stepper_motors}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{yes}}: Use M2 | sprinter={{no}} | marlin={{yes|M84}} | prusa={{yes|M84}}<sup>3</sup> | buddy={{yes}} | druid={{yes}} | repetier={{no}} | smoothie={{yes}} | reprapfirmware={{yes}} | klipper={{yes}} | bfb={{no}} | machinekit={{no}}  | makerbot={{yes}} | redeem={{yes}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   *This command can be used without any additional parameters.^13^*
:   `X` X axis
:   `Y` Y axis
:   `Z` Z axis
:   `E` Extruder drive(s)^2^
:   `S` Seconds^3^

Examples

`M18`\
`M18 X E0`

Disables stepper motors and allows axes to move \'freely.\'

On Marlin, `M18` is a synonym of `M84`, so it can also be used to
configure or disable the idle timeout.

Examples

`M18 S10  ; Idle steppers after 10 seconds of inactivity`\
`M18 S0   ; Disable idle timeout`

Notes

^1^Some firmware implementations do not support parameters to be passed,
but at least Marlin and RepRapFirmware do.

^2^RepRapFirmware allows stepper motors to be disabled selectively. For
example, `M18 X E0:2` will disable the X, extruder 0 and extruder 2
motors.

^3^In Prusa Firmware this command can be used to set the stepper
inactivity timeout (\`S\`) or to disable steppers
(\`X\`,\`Y\`,\`Z\`,\`E\`)

#### M20: List SD card {#m20_list_sd_card}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{yes}} | sprinter={{yes}} | marlin={{yes}}<sup>4</sup> | prusa={{yes}}<sup>4</sup> | buddy={{yes}} | repetier={{yes}} | smoothie={{yes}} | reprapfirmware={{yes}}<sup>1,2</sup> | klipper={{yes}}<sup>3</sup> | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   *This command can be used without any additional parameters.*
:   `Snnn` Output style^1^
:   `Rnnn` File number to start at^1^
:   `Cnnn` Maximum number of files to return^1^
:   `P"ddd"` Directory to list^2^
:   `L` Reports long filenames instead of just short filenames. Requires
    host software parsing (Cap:EXTENDED_M20).^4^
:   `T` Report timestamps as well. The value is one uint32_t encoded as
    hex. Requires host software parsing (Cap:EXTENDED_M20).^4^

<!-- -->

Examples

`M20`\
`M20 S2 P"/gcodes/subdir"`\
`M20 L `^`4`^\
`M20 T `^`4`^

This code lists all files in the root folder or G-code directory of the
SD card to the serial port. One name per line, like:

`SQUARE.G`\
`SQCOM.G`\
`ZCARRI~2.GCO`\
`CARRIA~1.GCO`

Please note that a file list response is usually encapsulated. Standard
configurations of RepRapFirmware mimic this style in emulation mode:

`Begin file list:`\
`SQUARE.G`\
`ZCARRI~2.GCO`\
`End file list`\
`ok`

The file size may be appended as an integer representing the size in
bytes:

`Begin file list:`\
`SQUARE.G 1234`\
`ZCARRI~2.GCO 234`\
`End file list `\
`ok`

At least OctoPrint also supports an additional format showing the
file\'s long name (see also M33) after the size:

`Begin file list:`\
`SQUARE.G 1234 SQUARE.G`\
`ZCARRI~2.GCO 234 ZCARRIAGE_V2.GCO`\
`End file list `\
`ok`

If RepRapFirmware emulates no firmware compatibility, a typical response
looks like:

`G-code files:`\
`"Traffic cone.g","frog.gcode","calibration piece.g"`

Note that some firmwares list file names in upper case, but - when sent
to the `M23` command (below) they must be in lower case. Teacup and
RepRapFirmware have no such trouble and accept both. RepRapFirmware
always returns long filenames in the case in which they are stored.

Notes

^1^RepRapFirmware specific: If the S2 parameter is used then the file
list (or as much as can be fitted in the output buffer) is returned in
JSON format as a single array called \"files\" with each name that
corresponds to a subdirectory preceded by an asterisk, and the directory
is returned in variable \"dir\". The optional R parameter is the file
number to start at, default 0. The JSON response also returns value
\"next\" which is the number of the first file that wasn\'t returned, or
0 if the last file in the folder was included in the response. This
allows the caller to enumerate all files even if there are very many, by
making successive M20 S2 calls with each call using R from the \"next\"
value in the previous response, until \"next\" is zero. In RRF 3.6.0 and
later the C parameter can be used to limit the maximum number of files
that RRF returns in each response.

Example

`M20 S2 P/gcodes`\
`{"dir":"\/gcodes","first":0,"files":["4-piece-1-2-3-4.gcode","Hinged_Box.gcode","Hollow_Dodecahedron_190.gcode","*Calibration pieces"],"next":0}`

Example for `M20 L`^4^

`Begin file list`\
`TEST1.GCO 1234 "TEST1.GCO"`\
`DIR_ENTER: /TESTFO~1/ "test folder"`\
`DIR_EXIT`\
`LFNFIL~1.GCO 56789 "LFN file.gcode"`\
`End file list`

Example for `M20 L T`^4^

`Begin file list`\
`TEST1.GCO 1234 0x52936b00 "TEST1.GCO"`\
`DIR_ENTER: /TESTFO~1/ "test folder"`\
`DIR_EXIT`\
`LFNFIL~1.GCO 56789 0x52936b08 "LFN file.gcode"`\
`End file list`

Example for `M20 T`^4^

`Begin file list`\
`TEST1.GCO 1234 0x52936b00`\
`DIR_ENTER: /TESTFO~1/ "test folder"`\
`DIR_EXIT`\
`LFNFIL~1.GCO 56789 0x52936b08`\
`End file list`

^2^This parameter is only supported by RepRapFirmware and defaults to
the 0:/gcodes directory, which is the directory that printable gcode
files are normally stored in.

^3^On Klipper, a virtual SD card is required for this to work.

^4^The timestamp is a combination of both the date and time into a
single integer and printed as a hex.

#### M21: Initialize SD card {#m21_initialize_sd_card}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{yes}} | sprinter={{yes}} || marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | repetier={{yes}} | druid={{yes}}<sup>2</sup>| smoothie={{yes}} | reprapfirmware={{yes}} | klipper={{yes}}<sup>1</sup> | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   `Pnnn` SD card number (RepRapFirmware only, default 0)

Examples

`M21`\
`M21 P1`

The specified SD card is initialized. If an SD card is loaded when the
machine is switched on, this will happen by default. SD card must be
initialized for the other SD functions to work.

Marlin 2.0.9.4 added `S` and `U` parameters to mount the SD Card or USB
drive, respectively. Hosts can look for
\"[`Cap:MULTI_VOLUME:1`](Cap:MULTI_VOLUME:1)\".

Notes

^1^On Klipper, a virtual SD card is required for this to work.

^2^On Druid:

` M21 is named "Mount Media"`\
` M21 P0 or S = Mount external SD CARD `\
` M21 P1 or M = Mount onboard Micro Sd-Card`\
` M21 P2 or U = Mount USB Flash Drive`\
` M21         = Mount current volume`

#### M22: Release SD card {#m22_release_sd_card}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{yes}} | sprinter={{yes}} || marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | druid={{yes}} | repetier={{yes}} | smoothie={{no}} | reprapfirmware={{yes}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   `Pnnn` SD card number (RepRapFirmware only, default 0)

Examples

`M22`\
`M22 P1`

The specified SD card is released, so further (accidental) attempts to
read from it are guaranteed to fail. Helpful, but not mandatory before
removing the card physically.

#### M23: Select SD file {#m23_select_sd_file}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{yes}} | sprinter={{yes}} || marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | repetier={{yes}} | smoothie={{yes}} | reprapfirmware={{yes}} | klipper={{yes}}<sup>1</sup> | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Example

`M23 filename.gco`

The file specified as filename.gco (8.3 naming convention is supported)
is selected ready for printing. RepRapFirmware supports long filenames
as well as 8.3 format.

Notes

^1^On Klipper, a virtual SD card is required for this to work.

#### M24: Start/resume SD print {#m24_startresume_sd_print}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{yes}} | sprinter={{yes}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | repetier={{yes}} | smoothie={{yes}} | reprapfirmware={{yes}} | klipper={{yes}}<sup>1</sup> | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{yes}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Example

`M24`

The machine prints from the file selected with the `M23` command. If the
print was previously paused with `M25`, printing is resumed from that
point. To restart a file from the beginning, use `M23` to reset it, then
`M24`.

When this command is used to resume a print that was paused,
RepRapFirmware runs macro file `resume.g` prior to resuming the print.

Notes

^1^On Klipper, a virtual SD card is required for this to work.

#### M25: Pause SD print {#m25_pause_sd_print}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{yes}} | sprinter={{yes}} || marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | repetier={{yes}} | smoothie={{yes}} | reprapfirmware={{yes}} | klipper={{yes}}<sup>1</sup> | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{yes}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Example

`M25`

The machine pauses printing at the current position within the file. To
resume printing, use
[M24](G-code#M24:_Start.2Fresume_SD_print "M24"){.wikilink}. Do not use
this code within a GCode file to pause the print at that point, use
[M226](G-code#M226:_Gcode_Initiated_Pause "M226"){.wikilink} instead.

Prior to pausing, RepRapFirmware runs macro file `pause.g`. This allows
the head to be moved away from the print, filament to be retracted, etc.

RepRapFirmware 1.20 and later also save the current state of the print
to file /sys/resurrect.g. This is so that if the printer is turned off
after pausing, the print can subsequently be resumed.

Without any parameters it will park the extruder to default or last set
position. The default pause position will be set during power up and a
reset, the new pause positions aren\'t permanent.

Usage
:   `M25 [ X | Y | Z | S ]` ^2^

<!-- -->

Parameters
:   `X` X position to park ^2^
:   `Y` Y position to park ^2^
:   `Z` Z raise before park ^2^
:   `S` Set values \[S0 = set to default values \| S1 = set values\]
    without pausing ^2^

<!-- -->

Notes

^1^On Klipper, a virtual SD card is required for this to work.

^2^Prusa Firmware equivalent to M125 and M601

#### M26: Set SD position {#m26_set_sd_position}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{yes}} || marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | repetier={{yes}} | reprapfirmware={{yes}} | klipper={{yes}}<sup>1</sup> | smoothie={{partial|aborts}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   `Snnn` File position from start of file in bytes
:   `Pnnn` (Optional, RepRapFirmware only) Fraction of the first move to
    be skipped, default 0.0, must be less than 1.0
:   `Xnnn,Ynnn,Znnn` (Optional, RepRapFirmware only) If the command at
    the specified file position is a G2 or G3 command and the P
    parameter is nonzero then two of these (e.g. X and Y if the XY plane
    is selected) are used to provide the coordinates of the centre of
    the arc.

Example
:   M26 S49315

Set the file offset in bytes from the start of the SD card file selected
by M23. The offset must correspond to the start of a G-code command.

RepRapFirmware uses this command as part of the procedure to recover a
job following a power failure.

Notes

^1^On Klipper, a virtual SD card is required for this to work.

#### M27: Report SD print status {#m27_report_sd_print_status}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{yes}} || marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | repetier={{yes}} | reprapfirmware={{yes}} | klipper={{yes}}<sup>1</sup> | smoothie={{yes}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   **C** Report the open file\'s name and long name (Marlin 1.1.9 and
    up)
:   **Sn** Set the auto-report interval (Marlin 1.1.9 and up)

<!-- -->

Example

`M27`

Report SD print status.

Marlin and RepRapFirmware report the number of bytes processed in this
format, which can be processed by Pronterface:

`SD printing byte 2134/235422`

If no file is being printed, only this message is reported:

`Not SD printing.`

In Marlin 1.1.9 and up `M27 C` reports the open file\'s DOS 8.3 name and
long filename, if any.

Example

`M27 C`

`Current file: filena~1.gco Filenagotcha.gcode`

In Marlin 1.1.9 and up `M27 Sn` sets the auto-report interval. This
requires the `AUTO_REPORT_SD_STATUS` configuration option to be enabled.
Marlin reports this capability in `M115` as
`Cap: AUTO_REPORT_SD_STATUS 1` when this option is available.

Example

`M27 S2 ; Report the SD card status every 2 seconds`

Notes

^1^On Klipper, a virtual SD card is required for this to work.

#### M28: Begin write to SD card {#m28_begin_write_to_sd_card}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{yes}} || marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | repetier={{yes}} | reprapfirmware={{yes}} | smoothie={{yes}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Example

`M28 filename.gco`

File specified by filename.gco is created (or overwritten if it exists)
on the SD card and all subsequent commands sent to the machine are
written to that file.

#### M29: Stop writing to SD card {#m29_stop_writing_to_sd_card}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{yes}} || marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | repetier={{yes}} | reprapfirmware={{yes}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Example

`M29 filename.gco`

File opened by `M28` command is closed, and all subsequent commands sent
to the machine are executed as normal.

#### M30: Delete a file on the SD card {#m30_delete_a_file_on_the_sd_card}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{yes}} || marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | repetier={{yes}} | reprapfirmware={{yes}} | smoothie={{yes}} | bfb={{no}} | machinekit={{no}} | grbl={{yes}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Example

`> M30 filename.gco`\
`> filename.gco is deleted.`

##### M30: Program Stop {#m30_program_stop}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} || marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | grbl={{yes}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{yes}} }}
```
\- For Yaskawa and in grbl - Same as M2 in Yaskawa G-code

Example

M30 ; Exchange pallet shuttles and end the program. Pressing cycle start
will start the program at the beginning of the file.

#### M31: Output time since last `M109` or SD card start to serial {#m31_output_time_since_last_m109_or_sd_card_start_to_serial}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Example

`M31`

The response looks like:

` echo:54 min, 38 sec`

#### M32: Select file and start SD print {#m32_select_file_and_start_sd_print}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | repetier={{no}} | smoothie={{yes}} | reprapfirmware={{yes}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Example

`M32 filename.gco`

It can be used when printing from SD card and does the same as `M23` and
`M24`.

tba available in marlin(14/6/2014)

#### M33: Get the long name for an SD card file or folder {#m33_get_the_long_name_for_an_sd_card_file_or_folder}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{no|Not required}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
Get the long name for a file or folder on the SD card from a dos path.
Introduced in Marlin firmware 1.1.0 September 2015.

Example input:

`M33 miscel~1/armchair/armcha~1.gco`

Example output:

`/Miscellaneous/Armchair/Armchair.gcode`

#### M33: Stop and Close File and save restart.gcode {#m33_stop_and_close_file_and_save_restart.gcode}

```{=mediawiki}
{{Firmware Support | reprapfirmware={{no}}: Use M25 | marlin={{no}} | prusa={{no}} | buddy={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```
Stop the printing from SD and save all position in restart.gcode for
restart printing in future

#### M34: Set SD file sorting options {#m34_set_sd_file_sorting_options}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{no}} | druid={{yes}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   **S1** Enable sorting
:   **S0** Disable sorting
:   **F-1** Folders first, followed by the files (both group,
    alphabetically)
:   **F0** Folders and files together, listed alphabetically
:   **F1** Files first, followed by folders (both group, alphabetically)

Enable and disable SD card file-sorting, and/or set the folder sorting
order. Proposed by Marlin firmware, May 2015.

#### M35: Upload firmware NEXTION from SD {#m35_upload_firmware_nextion_from_sd}

```{=mediawiki}
{{Firmware Support | marlin={{no}} | druid={{no}} | prusa={{no}} | buddy={{no}} | mk4duo={{yes}} }}
```
#### M36: Return file information {#m36_return_file_information}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes}} | bfb={{no}} | machinekit={{no}} | makerbot={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Example
:   M36 filename.gco
:   M36

Returns information in JSON format for the specified SD card file (if a
filename was provided) or for the file currently being printed. A sample
response is:

:   {\"err\":0,\"size\":436831,\"fileName\":\"EscherLizardModified.gcode\",\"lastModified\":\"2017-09-21T16:58:07\",\"height\":5.20,\"layerHeight\":0.20,\"printTime\":660,\"simulatedTime\":1586,\"filament\":\[1280.7\],\"generatedBy\":\"Simplify3D(R)
    Version 4.0.0\"}

The \"err\" field is zero if successful, nonzero if the file was not
found or an error occurred while processing it. The \"size\" field
should always be present if the operation was successful. The presence
or absence of other fields depends on whether the corresponding values
could be found by reading the file. The \"filament\" field is an array
of the filament lengths required from each spool. The size is in bytes,
the times are in seconds, all other values are in mm. \"printTime\" is
the printing time estimated by the slicer, \"simulationTime\" is the
time measured when the print was simulated by the firmware. The fields
may appear in any order, and additional fields may be present. Versions
of RepRapFirmware prior to 3.4 do not provide the \"fileName\" field if
information for a specific file was requested.

RepRapFirmware 3.4 and later also return information about thumbnail
imaged embedded in the GCode file via an additional JSON field
\"thumbnails\". A sample value for this field is:

:   \"thumbnails\":\[{\"width\":32,\"height\":32,\"fmt\":\"qoi\",\"offset\":103,\"size\":2140},{\"width\":220,\"height\":220,\"fmt\":\"qoi\",\"offset\":2384,\"size\":25464}\]

The \"fmt\" field denotes the encoding of the thumbnail and is either
\"png\" or \"qoi\". The \"thumbnails\" field is omitted entirely if
there are no thumbnails embedded in the GCode file.

#### M36.1: Return embedded thumbnail data {#m36.1_return_embedded_thumbnail_data}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes|3.4 and later}} | bfb={{no}} | machinekit={{no}} | makerbot={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   **P\"filename\"** Name of the GCode file from which thumbnail data
    is to be retrieved
:   **Snnnn** Byte offset into the file at which thumbnail data is to be
    fetched

This command is used to return the data for an thumbnail image in a
GCode file. The offset value should be either the offset of the start of
data for a thumbnail as returned by the M36 command, or the value
returned in the \"next\" field by a previous M36.1 command. The response
is in JSON format. Here is a sample response:

:   {fileName\":\"EscherLizardModified.gcode\",\"offset\":103,\"data\":\"cW9pZgAAACA\....AAAAB\",\"next\":0,err\":
    0}

The \"fileName\" and \"offset\" values are as given in the command.
\"data\" is part or all of the base64-encoded thumbnail data starting at
that offset. \"next\" is zero if there is no more data for that
thumbnail, otherwise not all the thumbnail data was returned and
\"next\" is the byte offset in the file of the rest of the thumbnail
data. \"err\" is 0 if the command was successful, otherwise \"err\" is
nonzero and the other fields may or may not be present.

#### M37: Simulation mode {#m37_simulation_mode}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   **S1** Enter simulation mode
:   **S0** Leave simulation mode
:   **P\"filename\"** (optional) Simulate printing a file from SD card

Examples
:   M37 S1
:   M37 P\"MyModel.g\"

Used to switch between printing mode and simulation mode. Simulation
mode allows the electronics to compute an accurate printing time, taking
into account the maximum speeds, accelerations etc. that are configured.

M37 S1 enters simulation mode. All G and M codes will not be acted on,
but the time they would take to execute will be calculated.

M37 S0 leaves simulation mode and prints the total time taken by
simulated moves since entering simulation mode.

M37 with no S parameter prints the time taken by the simulation, from
the time it was first entered using M37 S1, up to the current point (if
simulation mode is still active) or the point that the simulation was
ended (if simulation mode is no longer active).

M37 P\"filename\" enters simulation mode, prints the specified file,
exits simulation mode, reports the print time, and appends it to the
G-code file as a comment for later retrieval.

#### M38 Compute SHA1 hash of target file {#m38_compute_sha1_hash_of_target_file}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
Used to compute a hash of a file on the SD card. Examples:

`> M38 gcodes/myfile.g`\
`> Cannot find file`\
`> M38 www/reprap.htm`\
`> 91199139dbfadac15a18cfb962dfd4853db83999`

Returns a hexadecimal string which is the SHA1 of the file. If the file
cannot be found, then the string \"Cannot find file\" is returned
instead.

#### M39 Report SD card information {#m39_report_sd_card_information}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes}}: 1.20.1 and later | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   **Pn** SD slot number, default 0
:   **Sn** Response format. S0 returns a plain text response, S2 returns
    a response in JSON format.

Examples
:   **M39** ; report information for SD card 0 in plain text format
:   **M39 P1 S2** ; report information for SD card 1 in JSON format

This command returns information about the SD card in the specified slot
in the requested format. At least the following is returned:

- Whether or not a usable card is present in the slot
- The capacity of the card in bytes (if a card is present)
- The amount of free space on the card in bytes (if a card is present)

The JSON response has the following format (more fields may be added in
future):

`{"SDinfo":{"slot":0,"present":1,"capacity":4294967296,"free":2147485184,"speed":20971520,"clsize":32768}}`

The capacity, free space and cluster size are in bytes, and the
interface speed is in bytes/second.

#### M40: Eject {#m40_eject}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{partial|Use macro file M40.g}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
If your RepRap machine can eject the parts it has built off the bed,
this command executes the eject cycle. This usually involves cooling the
bed and then performing a sequence of movements that remove the printed
parts from it. The X, Y and Z position of the machine at the end of this
cycle are undefined (though they can be found out using the `M114`
command, q.v.).

See also `M240` and `M241` below.

#### M41: Loop {#m41_loop}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{partial|No, use 'while' command}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Example

`M41`

If the RepRap machine was building a file from its own memory such as a
local SD card (as opposed to a file being transmitted to it from a host
computer) this goes back to the beginning of the file and runs it again.
So, for example, if your RepRap is capable of ejecting parts from its
build bed then you can set it printing in a loop and it will run and
run. Use with caution - the only things that will stop it are:

1.  When you press the reset button,
2.  When the build material runs out (if your RepRap is set up to detect
    this), and
3.  When there\'s an error (such as a heater failure).

#### M42: Switch I/O pin {#m42_switch_io_pin}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{yes}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | repetier={{yes}} | smoothie={{no}} | reprapfirmware={{yes}} | bfb={{no}} | machinekit={{no}} | makerbot={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   `Pnnn` Pin number
:   `Snnn` Pin value

Example

`M42 P7 S255`

`M42` switches a general purpose I/O pin. Use `M42 Px Sy` to set pin x
to value y, when omitting Px the LEDPIN will be used.

In Teacup, general purpose devices are handled like a heater, see [
M104](#M104:_Set_Extruder_Temperature " M104"){.wikilink}.

In Marlin Firmware, pin numbers for 32-bit processors are in the form
PORT \* 100 + PIN. So pin P1_02 on LPC1768 can be set with
`M42 P102 S1`.

Marlin 1.x includes an `I` parameter to permit setting \"volatile\" pins
that Marlin is using.

Marlin 2.0.5.2 - 2.0.9.3 uses the `M` parameter to set the pin mode:
0=INPUT, 1=OUTPUT, 2=INPUT_PULLUP, 3=INPUT_PULLDOWN. In Marlin 2.0.9.4
and up the `T` parameter is used instead.

In RepRapFirmware, the S field may be in the range 0..1 or 0..255. The
pin reference is an internal firmware reference named \"digital pin\",
see [Duet pinout](Duet_pinout "Duet pinout"){.wikilink}. It maps on
different connector pins depending the hardware. On Duet 0.6 and 0.8.5
hardware using pre-1.16 firmware, the supported pin numbers and their
names on the expansion connector are:

  P    Name    Expansion Port Pin
  ---- ------- --------------------
  16   TXD1    11
  17   RXD1    12
  18   TXD0    13
  19   RXD0    14
  20   TWD1    35
  21   TWCK1   36
  23   PA14    10
  36   PC4     18
  52   AD14    41
  67   PB16    32

  : Duet M42 P value to Expansion Port Pin Mapping

In firmware 1.16, the pin numbering has changed.

  P    Name          Expansion Port Pin
  ---- ------------- --------------------
  60   PA10/RXD0     14
  61   PA11/TXD0     13
  62   PA12/RXD1     12
  63   PA13/TXD1     11
  64   PA14/RTS1     10
  65   PB12/TWD1     35
  66   PB13/TWCK1    36
  67   PB16/DAC1\*   32
  68   PB21/AD14     41
  69   PC4           18

  : Duet 0.6 and 0.8.5 v1.16+ M42 P value to Expansion Port Pin Mapping

- Also used as CS signal on external SD card socket

  P    Signal Name   Expansion Connector Label   Expansion Pin
  ---- ------------- --------------------------- ---------------
  60   CS5           CS5                         50
  61   CS6           E3_STOP                     9
  62   CS7           E4_STOP                     14
  63   CS8           E5_STOP                     19

  : Duet WiFi v1.16+ M42 P value to Expansion Port Pin Mapping

See [Using servos and controlling unused I/O
pins](https://duet3d.com/wiki/Using_servos_and_controlling_unused_I/O_pins)
for all pin definitions.

Pre-1.16 example:

`M42 P20 S1 ;set the connector pin 35 to high.`

On RADDS hardware running RepRapFirmware-dc42, the supported Arduino Due
pin numbers and their names are:

5 TIOA6, 6 PWML7, 39 PWMH2, 58 AD3, 59 AD2, 66 DAC0, 67 DAC1, 68 CANRX0,
69 CANTX0, 70 SDA1, 71 SCL1, 72 RX LED, 73 TX LED.

See also `M583`.

#### M43: Stand by on material exhausted {#m43_stand_by_on_material_exhausted}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | grbl={{no}} | sprinter={{no}} | marlin={{partial|M600}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | klipper={{no}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | makerbot={{no}} | yaskawa={{no}} }}
```

Example

`M43`

If your RepRap can detect when its material runs out, this decides the
behaviour when that happens. The X and Y axes are zeroed (but not Z),
and then the machine shuts all motors and heaters off except the heated
bed, the temperature of which is maintained. The machine will still
respond to G and M code commands in this state.

#### M43: Pin report and debug {#m43_pin_report_and_debug}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | grbl={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | klipper={{no}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | makerbot={{no}} | yaskawa={{no}} }}
```

Usage
:   `M43 En Pnnn Wn In`

Parameters
:   `En` Enable / disable background endstop monitoring
:   `Pnnn` Pin to read or watch. If omitted, read/watch all pins
:   `Wn` bool watch pins -reporting changes- until reset, click, or
    `M108`
:   `In` bool Flag to ignore pin protection

<!-- -->

Note
:   You must have `PINS_DEBUGGING` uncommented in your
    `Configuration_adv.h` file for M43 to work.

#### M44: Codes debug - report codes available {#m44_codes_debug___report_codes_available}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | grbl={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | klipper={{no}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | makerbot={{no}} | yaskawa={{no}} }}
```
In MK4duo you must enable `FASTER_GCODE_EXECUTE` to get this G-code.

Parameters
:   `In` G-code list
:   `Jn` M-code list

#### M44: Reset the bed skew and offset calibration {#m44_reset_the_bed_skew_and_offset_calibration}

```{=mediawiki}
{{Firmware Support | prusa={{yes}} }}
```
Resets the bed skew and offset calibration on Prusa i3
MK2/s,MK2.5/s,MK3/s.

#### M45: Bed skew and offset with manual Z up {#m45_bed_skew_and_offset_with_manual_z_up}

```{=mediawiki}
{{Firmware Support | prusa={{yes}} }}
```
Runs the xyz calibration on Prusa i3 MK2/s,MK2.5/s,MK3/s.

Parameters
:   `Vnn` Verbosity level 1, 10 and 20 (low, mid, high). Only when
    SUPPORT_VERBOSITY is defined. This parameter is optional.

#### M46: Show the assigned IP address {#m46_show_the_assigned_ip_address}

```{=mediawiki}
{{Firmware Support | reprapfirmware={{yes|Use M552}} | prusa={{yes}} | buddy={{yes}} }}
```
Reports the assigned IP address of a Toshiba FlashAir on Prusa i3
MK2/s,MK2.5/s,MK3/s. At this moment it is deactivated.

#### M47: Show end stops dialog on the display {#m47_show_end_stops_dialog_on_the_display}

```{=mediawiki}
{{Firmware Support | prusa={{yes}} }}
```
Show end stops dialog on the display on Prusa i3 MK2/s,MK2.5/s,MK3/s.

#### M48: Measure Z-Probe repeatability {#m48_measure_z_probe_repeatability}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{yes}}<sup>1</sup> | buddy={{no}} | repetier={{no}} | reprapfirmware={{partial|Use macro M48.g}} | smoothie={{yes}} | bfb={{no}} | grbl={{no}} | machinekit={{no}} | makerbot={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   `Pnnn` number of points
:   `Xnnn` position on the X axis
:   `Ynnn` position on the Y axis
:   `Vnnn` verbosity
:   `E` engage
:   `Lnnn` legs of travel
:   `S` schizoid

As with `G29`, the E flag causes the probe to stow after each probe.

The S flag will result is a random sized, 5 pointed star, being traced
(X and Y axis) between each sample. Usually a user will get worse
repeat-ability numbers with S specified because the X axis and Y axis
movements will add to the machine\'s positioning errors.

Prusa specific ^1^

This function assumes the bed has been homed. Specifically, that a G28
command as been issued prior to invoking the M48 Z-Probe repeatability
measurement function. Any information generated by a prior G29 Bed
leveling command will be lost and need to be regenerated.

The number of samples will default to 10 if not specified. You can use
upper or lower case letters for any of the options EXCEPT n. n must be
in lower case because Marlin uses a capital N for its communication
protocol and will get horribly confused if you send it a capital N.

Usage

`M48 nAA Xnnnn Ynnnn Vn Lnn`

Parameters
:   `nAA` number(AA) of samples, default=10 (valid values between 4 and
    50)
:   `Xnnn` X position for samples
:   `Ynnn` Y position for samples
:   `Vn` Verbosity level 1-4 (low to highest)
:   `Lnn` Legs of travel 1-15

#### M49: Set G26 debug flag {#m49_set_g26_debug_flag}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | smoothie={{no}} | repetier={{no}} | reprapfirmware={{no}} | klipper={{no}} | bfb={{no}} | grbl={{no}} | machinekit={{no}} | makerbot={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Usage
:   M49 S1 ; Enable G26 verbose debug output

#### M70: Display message {#m70_display_message}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no|M117}} | prusa={{no}} | buddy={{no}} | repetier={{no|M117}} | smoothie={{no|M117}} | reprapfirmware={{no|M117}} | klipper={{no|M117}} | bfb={{no}} | grbl={{no}} | machinekit={{no}} | makerbot={{yes}} | redeem={{no|M117}} | mk4duo={{no}} | yaskawa={{no|M117}} }}
```

Example

`M70 P200 Message`

Display a message on the LCD. `P` is the time to display message for.

#### M72: Firmware dependent {#m72_firmware_dependent}

##### M72: Play a tone or song {#m72_play_a_tone_or_song}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no|M300}} | prusa={{no|M300}} | buddy={{no|M300}} | repetier={{no}} | reprapfirmware={{no|M300}} | smoothie={{no}} | klipper={{no}} | bfb={{no}} | grbl={{no}} | machinekit={{no}} | makerbot={{yes}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}}: See M300 }}
```

Example

`M72 P2`

Instruct the machine to play a preset song. Acceptable song IDs are
machine specific. P is the ID of the song to play.

##### M72: Set/get Printer State {#m72_setget_printer_state}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{yes}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | klipper={{no}} | bfb={{no}} | grbl={{no}} | machinekit={{no}} | makerbot={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
Without any parameter get printer state

:   `0` NotReady Used by PrusaConnect
:   `1` IsReady Used by PrusaConnect
:   `2` Idle
:   `3` SD printing finished
:   `4` Host printing finished
:   `5` SD printing
:   `6` Host printing

<!-- -->

Usage
:   `M72 [ S ]`

<!-- -->

Parameters
:   `S` Set printer state 0 = not_ready, 1 = ready

#### M73: Set/Get build percentage {#m73_setget_build_percentage}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{yes}}<sup>1</sup> | buddy={{yes}} | repetier={{no}} | reprapfirmware={{yes|3.3 and later}} | smoothie={{no}} | bfb={{no}} | grbl={{no}} | machinekit={{no}} | makerbot={{yes}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Example

`M73 P50`

Tell the firmware the current build progress percentage. The machine is
expected to display this on its display. If the percentage is exactly 0
a \"Build Start\" notification is sent to the host. If the percentage is
exactly 100 a \"Build End\" notification is sent to the host.

Use \"M73\" by itself to get a report of the current print progress.

Prusa specific^1^

Prusa firmware shows percent done, time remaining and time to
change/pause/user interaction.

Usage

`M73 P R Q S C`^`1`^` D`^`1`^

Parameters
:   *This command can be used without any additional parameters.*
:   `P` Percent in normal mode
:   `R` Time remaining in normal mode (minutes)
:   `Q` Percent in silent mode
:   `S` Time remaining in silent mode (minutes)
:   `C` Time to change/pause/user interaction in normal mode
    (minutes)^1^
:   `D` Time to change/pause/user interaction in silent mode
    (minutes)^1^

Examples

`M73`\
`echo NORMAL MODE: Percent done: ---%; print time remaining in mins: -----"`\
`echo SILENT MODE: Percent done: ---%; print time remaining in mins: -----"`\
\
`Prusa Firmware 3.10.0+`^`1`^\
`echo NORMAL MODE: Percent done: ---%; print time remaining in mins: -----; Change in mins: -----"`^`1`^\
`echo SILENT MODE: Percent done: ---%; print time remaining in mins: -----; Change in mins: -----"`^`1`^

#### M74: Set weight on print bed {#m74_set_weight_on_print_bed}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{yes}} | smoothie={{no}} | repetier={{no}} | reprapfirmware={{no}} | klipper={{no}} | bfb={{no}} | grbl={{no}} | machinekit={{no}} | makerbot={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `W` Set the total mass in grams of everything that is currently on
    the bed.

<!-- -->

Example

`M74 W100`

Tell the firmware the current weight of 100g on the bed.

#### M75: Start the print job timer {#m75_start_the_print_job_timer}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | smoothie={{no}} | druid={{yes}} | repetier={{no}} | reprapfirmware={{no}} | klipper={{no}} | bfb={{no}} | grbl={{no}} | machinekit={{no}} | makerbot={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```
#### M76: Pause the print job timer {#m76_pause_the_print_job_timer}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | smoothie={{no}} | druid={{yes}} | repetier={{no}} | reprapfirmware={{no}} | klipper={{no}} | bfb={{no}} | grbl={{no}} | machinekit={{no}} | makerbot={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```
#### M77: Stop the print job timer {#m77_stop_the_print_job_timer}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | smoothie={{no}} | druid={{yes}} | repetier={{no}} | reprapfirmware={{no}} | klipper={{no}} | bfb={{no}} | grbl={{no}} | machinekit={{no}} | makerbot={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```
#### M78: Show statistical information about the print jobs {#m78_show_statistical_information_about_the_print_jobs}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | smoothie={{no}} | repetier={{no}} | reprapfirmware={{no}} | klipper={{no}} | bfb={{no}} | grbl={{no}} | machinekit={{no}} | makerbot={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```
#### M79: Start host timer {#m79_start_host_timer}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{yes}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | klipper={{no}} | bfb={{no}} | grbl={{no}} | machinekit={{no}} | makerbot={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
Start the printer-host enable keep-alive timer. While the timer has not
expired, the printer will enable host specific features.

Usage
:   `M79 [ S ]`

<!-- -->

Parameters
:   `S` Quoted string containing two characters e.g. \"PL\"

#### M80: ATX Power On {#m80_atx_power_on}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup=automatic | sprinter={{yes}} | marlin={{yes}} | prusa={{yes}}<sup>1</sup> | buddy={{yes}} | druid={{no}} | repetier={{yes}} | smoothie={{no}} | reprapfirmware={{yes}} | bfb={{no}} | grbl={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   `C"port_name"` (RepRapFirmware 3.4 and later only) Name of the pin
    used to control the power supply, default \"pson\"

<!-- -->

Examples

`M80           ; Turn on the power supply`\
`M80 S         ; Report power supply state (Marlin 1.1.1)`\
`M80 C"!pson"  ; invert the PS_ON output for Meanwell power supplies`

Turns on the ATX power supply from standby mode to fully operational
mode. No-op on electronics without standby mode.

Notes

- Marlin requires the `POWER_SUPPLY` configuration option to be set to a
  non-zero value to enable `M80`.
- Some firmwares (e.g., [ Teacup](Teacup_Firmware " Teacup"){.wikilink})
  handle power on/off automatically, so this is redundant there. Also,
  see [RAMPS wiring for ATX
  on/off](http://forums.reprap.org/read.php?219,132664).
- Prusa requires `defined (PS_ON_PIN)` and `PS_ON_PIN` must be set.^1^

#### M81: ATX Power Off {#m81_atx_power_off}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup=automatic | sprinter={{yes}} | marlin={{yes}} | prusa={{yes}}<sup>1</sup> | buddy={{yes}} | druid={{no}} | repetier={{yes}} | smoothie={{no}} | reprapfirmware={{yes}} | bfb={{no}} | grbl={{no}} | machinekit={{no}} | redeem={{yes}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   **P** quit the daemon (redeem only)
:   **R** restart the daemon (redeem only)
:   **Sn** n=0 turn power off immediately (default), n=1 turn power off
    when all thermostatic fans have turned off (RepRapFirmware 1.20 and
    later only)

Examples
:   M81 ; turn power off immediately
:   M81 S1 ; turn power off when everything has cooled down
    (RepRapFirmware)

Turns off the ATX power supply. Counterpart to `M80`.

Notes

- Prusa requires `defined (PS_ON_PIN)` and `PS_ON_PIN` must be set to
  Power off.^1^

#### M82: Set extruder to absolute mode {#m82_set_extruder_to_absolute_mode}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{yes}} | sprinter={{yes}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | druid={{yes}} | repetier={{yes}} | smoothie={{yes}} | reprapfirmware={{yes}} | klipper={{yes}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{yes}} }}
```

Example

`M82`

Makes the extruder interpret extrusion as absolute positions.

This is the default in repetier and for Yaskawa controllers.

#### M83: Set extruder to relative mode {#m83_set_extruder_to_relative_mode}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{yes}} | sprinter={{yes}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | druid={{yes}} | repetier={{yes}} | smoothie={{yes}} | reprapfirmware={{yes}} | klipper={{yes}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{yes}} }}
```

Example

`M83`

Makes the extruder interpret extrusion values as relative positions.

Note that the Ultimaker 3 will revert back to absolute extrusion after
each tool change.

#### M84: Stop idle hold {#m84_stop_idle_hold}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{yes}} | sprinter={{yes}} | marlin={{yes}} | prusa={{yes}}<sup>2</sup> | buddy={{yes}} | repetier={{yes}} | smoothie={{yes}} | reprapfirmware={{yes}} | klipper={{yes}}<sup>3</sup> | bfb={{no}} | machinekit={{no}} | redeem={{yes}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   *This command can be used without any additional parameters.*
:   `Innn` Reset flags^1^

Example

`M84`

Stop the idle hold on all axis and extruder. In some cases the idle hold
causes annoying noises, which can be stopped by disabling the hold. Be
aware that by disabling idle hold during printing, you will get quality
issues. This is recommended only in between or after printjobs.

On Marlin, Repetier and RepRapFirmware, `M84` can also be used to
configure or disable the idle timeout. For example, \"M84 S10\" will
idle the stepper motors after 10 seconds of inactivity. \"M84 S0\" will
disable idle timeout; steppers will remain powered up regardless of
activity. For Yaskawa systems M84 is not applicable due to servo motors
not producing the annoying noises.

Notes

^1^RepRapFirmware-dc42 and other firmware may not support this
parameter.

^2^Prusa firmware uses `M84` similar to
[G-code#M18:\_Disable_all_stepper_motors](G-code#M18:_Disable_all_stepper_motors "G-code#M18:_Disable_all_stepper_motors"){.wikilink}

^3^On Klipper `M84` is equivalent to
[G-code#M18:\_Disable_all_stepper_motors](G-code#M18:_Disable_all_stepper_motors "G-code#M18:_Disable_all_stepper_motors"){.wikilink}

Prusa Usage
:   `M84 E S X Y Z`

<!-- -->

Prusa Parameters
:   *This command can be used without any additional parameters.^2^*
:   `E` Extruder drive(s)^2^
:   `S` Seconds
:   `X` X axis
:   `Y` Y axis
:   `Z` Z axis

#### M85: Set Inactivity Shutdown Timer {#m85_set_inactivity_shutdown_timer}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{yes}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | repetier={{yes}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Example

`M85 S30`

Set Inactivity Shutdown Timer with parameter S`<seconds>`{=html}. \"M85
S0\" will disable the inactivity shutdown time (default)

#### M86: Set Safety Timeout {#m86_set_safety_timeout}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|2.1.3}} | prusa={{yes}} | buddy={{yes}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} | makerbot={{no}} | grbl={{no}} }}
```

Usage
:   `M86 Snnnn`

Parameters
:   `S` Seconds
:   `T` Trigger Temperature (Marlin)
:   `E` Extruder Idle Temperature (Marlin)
:   `B` Bed Idle Temperature (Marlin)

Similar to `M85` but applies to the \"safety timer\" in Prusa and Marlin
Firmware.

Set the Safety Timeout in seconds. **M86 S0** will disable the safety
timer.

When the safety timer expires, heatbed and nozzle target temperatures
are set to zero (Prusa Firmware) or idle temperatures (Marlin).

In Marlin Firmware the Hotend Idle Timeout is active whenever the hotend
temperature goes above the trigger value and the timer gets reset
whenever the extruder or other axes move. So if the machine is sitting
idle for the timeout period (set by **M86 T**) the machine will reduce
the hotend and bed temperatures to those set by **M86 E** and **M86 B**.
These settings are saved to the EEPROM by **M500** and reset to
configuration defaults by **M502**.

#### M87: Cancel Safety Timer {#m87_cancel_safety_timer}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|2.1.3}} | prusa={{no}} | buddy={{no}} | klipper={{no}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} | makerbot={{no}} | grbl={{no}} }}
```

Usage
:   `M87`

Cancels the safety timer. Equivalent to `M86 S0`.

#### M92: Set axis_steps_per_unit {#m92_set_axis_steps_per_unit}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{yes}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | druid={{yes}} | repetier={{yes}} | smoothie={{yes}} | reprapfirmware={{yes}} | bfb={{no}} | machinekit={{no}} | redeem={{yes}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   `Xnnn` Steps per unit for the X drive
:   `Ynnn` Steps per unit for the Y drive
:   `Znnn` Steps per unit for the Z drive
:   `Ennn` Steps per unit for the extruder drive(s)
:   `Snnn` Defines in which microstepping the above steps per unit are
    given. If omitted it will use the microstepping currently set by
    M350.^1^

Examples

`M92 X87.489 Y87.489 Z87.489`\
`M92 E420:420`

Allows programming of steps per unit (usually mm) for motor drives.
These values are reset to firmware defaults on power on, unless saved to
EEPROM if available (`M500` in Marlin) or in the configuration file
(config.g in RepRapFirmware). Very useful for calibration.

RepRapFirmware will report the current steps/mm if you send `M92`
without any parameters. For Yaskawa systems M92/M93 is not applicable
due to use of servo motors.

Notes

^1^ Only available in RepRapFirmware \>=2.03

#### M93: Send axis_steps_per_unit {#m93_send_axis_steps_per_unit}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{yes}} | marlin ={{no}} | smoothie={{no}} | reprapfirmware={{yes|Use M92}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
#### M98: Call Macro/Subprogram {#m98_call_macrosubprogram}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes}} | bfb={{no}} | machinekit={{no}} | makerbot={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{yes}} }}
```

Parameters
:   `Pnnn` Macro filename. In RepRapFirmware 3 this must be enclosed in
    double-quote characters. In RepRapFirmware 2 the double-quote
    characters are optional.

Example

`M98 Pmymacro.g`\
`M98 P"mymacro.g"`

Runs the macro in the file mymacro.g. In conventional G Codes for CNC
machines the `P` parameter normally refers to a line number in the
program itself (P2000 would run the Macro starting at line O2000, say).
For RepRap, which almost always has some sort of mass storage device
inbuilt, it simply refers to the name of a G-code file that is executed
by the `G98` call. That G-code file does not need to end with an `M99`
(return) as the end-of-file automatically causes a return.
RepRapFirmware supports nested macro calls up to a depth of 5.

Certain machine parameters are saved at the start of the macro call and
restored at the end. For RepRapFirmware these are: axis movement
relative/absolute mode, extruder movement absolute/relative mode, feed
rate, inches/mm setting, and whether or not volumetric extrusion is
selected. This allows the macro to change these settings without
affecting the subsequent behaviour of the calling file.

RepRapFirmware also allows the filename to include a path to a
subdirectory. For relative paths, the default folder is /sys, but some
implementations may check the /macros directory too. Absolute file paths
are supported by RepRapFirmware too.

#### M99: Return from Macro/Subprogram {#m99_return_from_macrosubprogram}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes}} | bfb={{no}} | machinekit={{no}} | makerbot={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{yes}} }}
```

Example

`M99`

Returns from an `M98` call.

RepRapFirmware closes the currently active macro file. If a nested macro
is being run, RepRapFirmware goes up one stack level.

#### M101: Turn extruder 1 on (Forward), Undo Retraction {#m101_turn_extruder_1_on_forward_undo_retraction}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{yes}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | druid={{no}} | reprapfirmware={{yes}}: 1.17c and later | smoothie={{no}} | bfb={{yes}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
In Teacup firmware: If a DC extruder is present, turn that on. Else,
undo filament retraction, which means, make the extruder ready for
extrusion. Complement to `M103`.

In BFB/RapMan: Turn extruder on (forward/filament in).

In RepRapFirmware: undo filament retraction. The length and speed are
set by the `M207` command. RepRapFirmware supports this command for
compatibility with Simplify3D.

In other firmwares: Deprecated. Regarding filament retraction, see
`G10`, `G11`, `M207`, `M208`, `M227`, `M228`, `M229`.

#### M102: Turn extruder 1 on (Reverse) {#m102_turn_extruder_1_on_reverse}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | klipper={{no}} | druid={{no}} | makerbot={{no}} | grbl={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{yes}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
In BFB/RapMan firmware: Turn extruder on Reverse (Still to add)

#### M102: Configure Distance Sensor {#m102_configure_distance_sensor}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|2.1.1}} | klipper={{no}} | druid={{no}} | makerbot={{no}} | grbl={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
For Marlin\'s `BD_SENSOR` option, configure the sensor.

:   `M102 S<10ths>` : Set adjustable Z height in 10ths of a mm (e.g.,
    \'`M102 S4`\' enables adjusting for Z \<= 0.4mm.)
:   `M102 S0` : Disable adjustable Z height.

<!-- -->

Negative S values are commands:
:   `M102 S-1` : Read sensor information
:   `M102 S-5` : Read raw Calibration data
:   `M102 S-6` : Start Calibration

#### M103: Turn all extruders off, Extruder Retraction {#m103_turn_all_extruders_off_extruder_retraction}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{yes}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{yes}}: 1.17c and later | smoothie={{no}} | bfb={{yes}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
In Teacup firmware: If a DC extruder is present, turn that off. Else,
retract the filament in the hope to prevent nozzle drooling. Complement
to `M101`.

In BFB/RapMan firmware: Turn extruder off.

In RepRapFirmware: retract filament. The length and speed are set by the
`M207` command. RepRapFirmware supports this command for compatibility
with Simplify3D.

In other firmwares: Deprecated. Regarding filament retraction, see
`G10`, `G11`, `M207`, `M208`, `M227`, `M228`, `M229`.

#### M104: Set Extruder Temperature {#m104_set_extruder_temperature}

```{=mediawiki}
{{Firmware Support | fived={{yes}} | teacup={{yes}} | sprinter={{yes}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | druid={{yes}} | repetier={{yes}} | smoothie={{yes}} | reprapfirmware={{yes}} | klipper={{yes}} | bfb={{yes}} | machinekit={{yes}} | makerbot={{yes}} | redeem={{yes}} | mk4duo={{yes}} | yaskawa={{yes}} }}
```

Parameters
:   `C` Use fan for cooling (Buddy only)
:   `Dnnn` Display temperature (Buddy only)
:   `Snnn` Target temperature
:   `Rnnn` Idle temperature (Only MK4duo)

<!-- -->

Example

`M104 S190`\
`M104 S190 R170`

Set the temperature of the current extruder to 190^o^C and return
control to the host immediately (*i.e.* before that temperature has been
reached by the extruder). See also
[M109](G-code#M109:_Set_Extruder_Temperature_and_Wait "M109"){.wikilink}.

See also using
[G10](G-code#G10:_Set_tool_Offset_and.2For_workplace_coordinates_and.2For_tool_temperatures "G10"){.wikilink}.
Deprecation of `M104` is [ subject to
discussion](Talk:G-code#M104_.26_M109_Deprecation,_G10_Introduction " subject to discussion"){.wikilink}.
\--[Traumflug](User:Traumflug "Traumflug"){.wikilink} 11:33, 19 July
2012 (UTC)

##### M104 in Marlin Firmware {#m104_in_marlin_firmware}

See [Marlin Wiki](http://marlinfw.org/docs/gcode/M104.html). In Marlin
Firmware, using `M104` with no parameters will turn off the heater for
the current extruder. This is also the case for `M104 S` without a
number after the `S` parameter.

##### M104 in Teacup Firmware {#m104_in_teacup_firmware}

In Teacup Firmware, `M104` can be additionally used to handle all
devices using a temperature sensor. It supports the additional `P`
parameter, which is a zero-based index into the list of sensors in
config.h. For devices without a temp sensor, see [
M106](#M106:_Fan_On " M106"){.wikilink}.

Example

`M104 P1 S100`

Set the temperature of the device attached to the second temperature
sensor to 100°C.

##### M104 in RepRapFirmware and Klipper {#m104_in_reprapfirmware_and_klipper}

RepRapFirmware and some other firmwares support the optional `T`
parameter (as generated by slic3r) to specify which tool the command
applies to.

#### M105: Get Extruder Temperature {#m105_get_extruder_temperature}

```{=mediawiki}
{{Firmware Support | fived={{yes}} | teacup={{yes}} | sprinter={{yes}} | marlin={{yes}} | prusa={{yes}}<sup>1</sup> | buddy={{yes}} | druid={{yes}}<sup>2</sup> | repetier={{yes}} | smoothie={{yes}} | reprapfirmware={{yes}} | klipper={{yes}} | bfb={{no}} | machinekit={{no}} | redeem={{yes}} | makerbot={{yes}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   *This command can be used without any additional parameters.*

Examples

`M105`

Request the temperature of the current extruder, the build base and the
build chamber in degrees Celsius. The temperatures are returned to the
host computer. For example, the line sent to the host in response to
this command can look like:

`ok T:201 B:117`\
`ok T:201 /202 B:117 /120`\
`ok T:201 /202 B:117 /120 C:49.3 /50`\
`ok T:201 /202 T0:110 /110 T1:23 /0 B:117 /120 C:49.3 /50`\
`ok T0:110 /110 T1:23 /0 B:117 /120`\
`ok T:20.2 /0.0 B:19.1 /0.0 T0:20.2 /0.0 @:0 B@:0 P:19.8 A:26.4`

The parameters mean the following:

- T, T0, \..., Tn - extruder temperature. In a single extruder setup,
  only T will be reported. Some firmware variants will report no T0 in
  multi extruder setups - in that case T is to be considered the
  temperature of the first tool. Otherwise, T should be considered the
  temperature of the currently selected tool (which will be repeated in
  one of the Tn entries)
- B - bed temperature
- C - chamber temperature
- @ - Hotend power
- B@ - Bed power
- P - PINDAv2 actual (Prusa MK2.5/s MK3/s only)^1^
- A - Ambient actual (Prusa MK3/s only)^1^

A temperature report will usually include actual and target temperature
for all available heaters, with the format being \"actual/target\" or -
for some firmware variants - \"actual /target\". During a blocking
heatup some firmware variants only report the temperature tuple for the
heater that is currently in blocking heatup state.

Note that temperatures can be reported as integers or floats. There
sadly are a lot of interpretations of how an M105 response should look
like across firmware variants, making parsing them potentially tricky.

Expansion/generalization of `M105` to be considered using S1 parameter
as noted in [Pronterface I/O
Monitor](Pronterface_I/O_Monitor "Pronterface I/O Monitor"){.wikilink}

In Repetier and MK4duo you can add X0 (X1 MK4duo) to get raw values as
well:

    M105 X0
    ==> 11:05:48.910 : T:23.61 /0 @:0 T0:23.61 /0 @0:0 RAW0:3922 T1:23.89 /0 @1:0 RAW1:3920

Recent versions of RepRapFirmware also report the current and target
temperatures of all active heaters.

------------------------------------------------------------------------

^1^Druid firmware

***Temperature actual/target in Celcius** (actual with one decimal ,
target is integer)*

- **T0:** in a single extruder systems,
- **T0:** and **T1:** in dual extruder systems.
- **B:** for Heated bed
- **C:** for Heated chamber

***Power applied** (PWM value 0-255)*

- **\@0: and \@1:** for Hotends
- **B@:** for Heated bed
- **C@:** for Heated chamber

*Active or not, the values for all available heaters on the system are
sent.*

Examples

<!-- -->

:   T0:27.8/0 \@0:0
:   T0:27.7/0 B:21.6/0 \@0:0 B@:0
:   T0:27.8/0 T1:27.8/210 B:21.6/0 C:85.0/0 \@0:0 \@1:255 B@:0 C@:0

#### M106: Fan On {#m106_fan_on}

```{=mediawiki}
{{Firmware Support | fived={{yes}} | teacup={{yes}} | sprinter={{yes}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | repetier={{yes}} | smoothie={{yes}} | reprapfirmware={{yes}} | klipper={{yes}} | bfb={{yes}} | machinekit={{yes}} | redeem={{yes}} | mk4duo={{yes}} | yaskawa={{yes}} }}
```

Parameters
:   `Pnnn` Fan number (optional, defaults to 0)^2^
:   `Snnn` Fan speed (0 to 255; RepRapFirmware also accepts 0.0 to 1.0))

Extra Parameters
:   `Innn` Invert signal, or disable fan^1^ ^3^
:   `Fnnn` Set fan PWM frequency, in Hz^1^ ^3^
:   `Lnnn` Set minimum fan speed (0 to 255 or 0.0 to 1.0)^1^ ^3^
:   `Xnnn` Set maximum fan speed (0 to 255 or 0.0 to 1.0)^1^ ^3^
:   `Bnnn` Blip time - fan will be run at full PWM for this number of
    seconds when started from standstill^1^
:   `Hnn:nn:nn...` Select heaters monitored when in thermostatic mode^1^
    ^3^
:   `Rnnn` Restore fan speed to the value it has when the print was
    paused^1^
:   `Tnnn` Set thermostatic mode trigger temperature
:   `Cnnn` Set custom name (RRF \> 2.01 only)^1^

Example

`M106 S127`

Examples (RepRapFirmware)

`M106 P1 I1 S87`\
`M106 P1 T45 H1:2`\
`M106 P2 B0.1 L0.05`

The first example turns on the default cooling fan at half speed. The
second one inverts the cooling fan signal of the second fan and sets its
value to 1/3 of its maximum. The third one sets the second fan to a
thermostatic fan for heaters 1 and 2 (e.g. the extruder heaters in a
dual-nozzle machine) such that the fan will be on when either hot end is
at or above 45C.

Mandatory parameter \'S\' declares the PWM value (0-255). `M106 S0`
turns the fan off. In some implementations like RepRapFirmware the PWM
value may alternatively be specified as a real fraction: `M106 S0.7`.

Notes

^1^These parameters are only available in RepRapFirmware.

^2^Marlin 1.0 to 1.1.6 only supports a single fan. Marlin 1.1.7 and up
supports up to 3 fans.

^3^These parameters are only available in MK4duo.

##### M106 in RepRapFirmware {#m106_in_reprapfirmware}

If an `S` parameter is provided but no other parameter is present, then
the speeds of the print cooling fans associated with the current tool
will be set (see the `F` parameter in the `M563` command). If no tool is
active then the speed of Fan 0 will be set. Either way, the speed is
remembered so that it can be recalled using the `R2` parameter (see
below).

If no `S` parameter is given but the R1 parameter is used, the fan speed
when the print was last paused will be set. If the `R2` parameter is
used, then the speeds of the print cooling fans associated with the
current tool will be set to the remembered value (see above).

The `T` and `H` parameters allow a fan to be configured to operate in
thermostatic mode, for example to use one of the fan channels to control
the hot end fan. In this mode the fan will be fully on when the
temperature of any of the heaters listed in the `H` parameter is at or
above the trigger temperature set by the `T` parameter, and off
otherwise. Thermostatic mode can be disabled using parameter H-1.

The `B` parameter sets the time for which the fan will be operated at
full PWM when started from cold, to allow low fan speeds t be used. A
value of 0.1 seconds is usually sufficient.

The `L` parameter defines the minimum PWM value that is usable with this
fan. If a lower value is commanded that is not zero, it will be rounded
up to this value. The `X` parameter defines the maximum PWM value that
is allowed for this fan. If a higher value is commanded, it will be
rounded down to this value.

The `I` parameter causes the fan output signal to be inverted if its
value is greater than zero. This makes the cooling fan output suitable
for feeding the PWM input of a 4-wire fan via a diode. If the parameter
is present and zero, the output is not inverted. If the `I` parameter is
negative then in RRF 1.16 and later the fan is disabled, which frees up
the pin for use as a general purpose I/O pin that can be controlled
using `M42`.

##### M106 in Teacup Firmware {#m106_in_teacup_firmware}

Additionally to the above, Teacup Firmware uses `M106` to control
general devices. It supports the additional `P` parameter, which is an
zero-based index into the list of heaters/devices in config.h.

Example

`M106 P2 S255`

Turn on device #3 at full speed/wattage.

**Note**: When turning on a temperature sensor equipped heater with
`M106` and `M104` at the same time, temperature control will override
the value given in `M106` quickly.

*Note well:* **The ambiguous text in the note above needs to be reworded
by someone who knows the actual functioning. Below is my interpretation
based on language use, not practical experience or code inspection.**

**Note:** *If `M104` is (or becomes) active on a heater (or other
device) with a feedback sensor it will correct any `M106` initiated
control output value change in the time it takes for the PID (of other
feedback) loop to adjust it back to minimum error. It may not be easy to
observe a change in the temperature (process value) due to this brief
change in the control value*

#### M107: Fan Off {#m107_fan_off}

```{=mediawiki}
{{Firmware Support | fived={{yes}} | teacup={{no}} | sprinter={{yes}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | repetier={{yes}} | druid={{yes}} | smoothie={{yes}} | reprapfirmware={{yes}} | klipper={{yes}} | bfb={{yes}} | machinekit={{yes}} | redeem={{yes}} | mk4duo={{yes}} | yaskawa={{yes}} }}
```
Deprecated in Teacup firmware and in RepRapFirmware. Use `M106 S0`
instead.

#### M108: Cancel Heating {#m108_cancel_heating}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | repetier={{no}} | prusa={{no}} | buddy={{yes}} | smoothie={{no}} | reprapfirmware={{yes}} | bfb={{yes}} | machinekit={{no}} | redeem={{yes}} | mk4duo={{yes}} | yaskawa={{no}} }}
```
Breaks out of an `M109` or `M190` wait-for-temperature loop, continuing
the print job. Use this command with caution! If cold extrusion
prevention is enabled (see `M302`) and the temperature is too low, this
will start \"printing\" without extrusion. If cold extrusion prevention
is disabled and the hot-end temperature is too low, the extruder may
jam.

This command was introduced in Marlin 1.1.0. As with other emergency
commands \[e.g., `M112`\] this requires the host to leave space in the
command buffer, or the command won\'t be executed until later.

Recent versions of Marlin introduce `EMERGENCY_PARSER`, which overcomes
the buffer limitation by watching the incoming serial stream. Commands
M108, M112, M410, and M876 can all be intercepted by the emergency
parser, so it is recommended to enable this feature.

#### M108: Set Extruder Speed (BFB) {#m108_set_extruder_speed_bfb}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{no}} | bfb={{yes}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
Sets speed of extruder motor. (Deprecated in FiveD firmware, see `M113`)

#### M109: Set Extruder Temperature and Wait {#m109_set_extruder_temperature_and_wait}

```{=mediawiki}
{{Firmware Support | fived={{yes}} | teacup={{no|not needed}} | sprinter={{yes}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | repetier={{yes}} | smoothie={{yes}} | reprapfirmware={{yes}} | klipper={{yes}} | bfb={{no}} | machinekit={{yes}} | makerbot={{yes}} | redeem={{yes}} | mk4duo={{yes}} | yaskawa={{yes}} }}
```

Parameters
:   `C` Use fan for cooling (Buddy only)
:   `Snnn` minimum target temperature, waits until heating
:   `Rnnn` maximum target temperature, waits until cooling (Sprinter)
:   `Rnnn` accurate target temperature, waits until heating and cooling
    (Marlin and MK4duo)
:   `Tn` tool number (RepRapFirmware and Klipper), optional

Example

`M109 S215`

##### M109 in Teacup {#m109_in_teacup}

Not needed. To mimic Marlin behaviour, use [
M104](#M104:_Set_Extruder_Temperature " M104"){.wikilink} followed by [
M116](#M116:_Wait " M116"){.wikilink}.

##### M109 in Marlin, MK4duo, Sprinter (ATmega port), RepRapFirmware, Prusa {#m109_in_marlin_mk4duo_sprinter_atmega_port_reprapfirmware_prusa}

Set extruder heater temperature in degrees celsius and wait for this
temperature to be achieved.

Example

`M109 S185`

RepRapFirmware also supports the optional `T` parameter (as generated by
slic3r) to specify which tool the command refers to (see below).

##### M109 in Sprinter (4pi port) {#m109_in_sprinter_4pi_port}

Parameters: `S` (optional), set target temperature value. If not
specified, waits for the temperature set by [
M104](#M104:_Set_Extruder_Temperature " M104"){.wikilink}. `R`
(optional), sets target temperature range maximum value.

Example

`M109 S185 R240 ; set extruder temperature to 185 and wait for the temperature to be between 185 - 240.`

If you have multiple extruders, use `T` or `P` parameter to specify
which extruder you want to set/wait.

Another way to do this is to use [
G10](#G10:_Tool_Offset " G10"){.wikilink}.

##### M109 in MakerBot {#m109_in_makerbot}

Example

`M109 S70 T0`

Sets the target temperature for the current build platform. S is the
temperature to set the platform to, in degrees Celsius. T is the
platform to heat.

##### M109 in Klipper {#m109_in_klipper}

According to the
[documentation](https://www.klipper3d.org/G-Codes.html), Klipper will
wait for the specified temperature to settle, i.e. it will wait until it
goes back down in case it overshoots. Klipper also supports the optional
`T` parameter to specify which tool the command refers to (see above).

#### M110: Set Current Line Number {#m110_set_current_line_number}

```{=mediawiki}
{{Firmware Support | fived={{yes}} | teacup={{no|not needed}} | sprinter={{no}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | druid={{yes}} | repetier={{yes}} | reprapfirmware={{yes}} | smoothie={{yes}} | bfb={{no}} | machinekit={{no}} | redeem={{yes}} | mk4duo={{yes}} | yaskawa={{no}} }}
```
This command is used for host handshaking, error detection, and resend
requests in host-driven print jobs when line numbers are used. See the
G-code protocol described above.

Parameters
:   `Nnnn` Line number

Example

`M110 N123`

This example sets the current command line number to 123. Thus the
expected next line after this command will be 124.\
In Marlin 2.1.3 and up `M110` with no parameter reports the current
command line number.

#### M111: Set Debug Level {#m111_set_debug_level}

```{=mediawiki}
{{Firmware Support | fived={{yes}} | teacup={{experimental|Debug}} | sprinter={{no}} | marlin={{yes}} | prusa={{no}}<sup>2</sup> | buddy={{yes}} | repetier={{yes}} | smoothie={{no}} | reprapfirmware={{yes}} | bfb={{no}} | machinekit={{no}} | redeem={{yes}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   `Pnnn` Debug module^1^
:   `Snnn` Debug on/off

Examples

`M111 S6`\
`M111 P1 S1`

Enable or disable debugging features in the firmware. The implementation
may look different per firmware.

Notes

^1^This parameter is only available in RepRapFirmware.

^2^Prusa fimrware use D-codes/commands for debugging.

##### M111 in RepRapFirmware {#m111_in_reprapfirmware}

RepRapFirmware allows debugging to be set for each module. If the
optional \'P\' parameter is not specified, debugging will be enabled for
all modules. For a list of modules, send `M111 S1 P15`.

##### M111 in Repetier {#m111_in_repetier}

Set the level of debugging information transmitted back to the host to
level 6. The level is the OR of three bits:

`#define DEBUG_ECHO (1<<0)`\
`#define DEBUG_INFO (1<<1)`\
`#define DEBUG_ERRORS (1<<2)`\
`#define DEBUG_DRYRUN (1<<3) // repetier-firmware`\
`#define DEBUG_COMMUNICATION (1<<4) // repetier-firmware`

Thus 6 means send information and errors, but don\'t echo commands.
(This is the RepRap default.)

For firmware that supports ethernet and web interfaces `M111 S9` will
turn web debug information on without changing any other debug settings,
and `M111 S8` will turn it off. Web debugging usually means that HTTP
requests will be echoed to the USB interface, as will the responses.

#### M112: Full (Emergency) Stop {#m112_full_emergency_stop}

```{=mediawiki}
{{Firmware Support | fived={{yes}} | teacup={{yes}} | sprinter={{no}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | repetier={{yes}} | druid={{yes}} | smoothie={{yes}} | reprapfirmware={{yes}} | klipper={{yes}} | bfb={{no}} | machinekit={{no}} | redeem={{yes}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Example

`M112`

Any moves in progress are immediately terminated, then RepRap shuts
down. All motors and heaters are turned off. It can be started again by
pressing the reset button on the master microcontroller. See also `M0`
and `M1`.

Please note while many systems termed this an Emergency Stop, this
terminology is regulated in many regions with specific requirements
behind its use. Marlin 2.0.x has renamed this to Full Stop.
RepRapFirmware has indicated an intention to make a similar change as
well. This stop function is NOT implemented in a Category 0 or 1 stop
fashion or with fail-safe hardware compliying with PLd or better. The
function as implemented is a category 2 software stop with no
redundancies.

#### M113: Set Extruder PWM {#m113_set_extruder_pwm}

```{=mediawiki}
{{Firmware Support | fived={{yes}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{no}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Example

`M113`

Set the PWM for the currently-selected extruder. On its own this command
sets RepRap to use the on-board potentiometer on the extruder controller
board to set the PWM for the currently-selected extruder\'s stepper
power. With an S field:

M113 S0.7

it causes the PWM to be set to the `S` value (70% in this instance).
`M113 S0` turns the extruder off, until an `M113` command other than
`M113 S0` is sent.

#### M113: Host Keepalive {#m113_host_keepalive}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|1.1.9+}} | prusa={{yes}} | buddy={{yes}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{no}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```
During some lengthy processes, such as G29, Marlin may appear to the
host to have "gone away." The "host keepalive" feature will send
messages to the host when Marlin is busy or waiting for user response so
the host won't try to reconnect.

Usage
:   `M113 Snnn`

Parameters
:   `Snnn` keepalive interval to set

Examples

`M113 S2`

#### M114: Get Current Position {#m114_get_current_position}

```{=mediawiki}
{{Firmware Support | fived={{yes}} | teacup={{yes}} | sprinter={{yes}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | repetier={{yes}} | druid={{yes}} | smoothie={{yes}} | reprapfirmware={{yes}} | klipper={{yes}} | bfb={{no}} | machinekit={{no}} | makerbot={{yes}} | redeem={{yes}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Example

`M114`

This causes the RepRap machine to report its current X, Y, Z and E
coordinates to the host.

For example, the machine returns a string such as:

`ok C: X:0.00 Y:0.00 Z:0.00 E:0.00`

In Marlin first 3 numbers is the position for the planner. The other
positions are the positions from the stepper function. This helps for
debugging a previous stepper function bug.

`X:0.00 Y:0.00 RZ:0.00 LZ:0.00 Count X:0.00 Y:0.00 RZ:41.02 LZ:41.02`

#### M115: Get Firmware Version and Capabilities {#m115_get_firmware_version_and_capabilities}

```{=mediawiki}
{{Firmware Support | fived={{yes}} | teacup={{yes}} | sprinter={{yes}} | marlin={{yes}} | prusa={{yes}}<sup>2</sup> | buddy={{yes}} | repetier={{yes}} | druid={{yes}} | smoothie={{yes}} | klipper={{yes}} | reprapfirmware={{yes}} | bfb={{no}} | machinekit={{no}} | makerbot={{no}} | redeem = {{yes}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   *This command can be used without any additional parameters.*
:   `Bnnn` (RepRapFirmware 3 only) Expansion board number (typically the
    CAN address) for which the firmware version is requested, default 0
    (i.e. main board)
:   `Pnnn` Electronics type^1^
:   `V` Report the Prusa version number^2^
:   `Unnnnnn` Check the firmware version provided^2^

Examples

`M115`\
`M115 P2`

Request the Firmware Version and Capabilities of the current
microcontroller The details are returned to the host computer as
key:value pairs separated by spaces and terminated with a linefeed.

sample data from firmware:

`ok PROTOCOL_VERSION:0.1 FIRMWARE_NAME:FiveD FIRMWARE_URL:http%3A//reprap.org MACHINE_TYPE:Mendel EXTRUDER_COUNT:1`

This `M115` code is inconsistently implemented, and should not be relied
upon to exist, or output correctly in all cases. An initial
implementation was committed to svn for the FiveD Reprap firmware on 11
Oct 2010. Work to more formally define protocol versions is currently
(October 2010) being discussed. See
[M115_Keywords](M115_Keywords "M115_Keywords"){.wikilink} for one draft
set of keywords and their meanings. See the `M408` command for a more
comprehensive report on machine capabilities supported by
RepRapFirmware.

Notes

^1^This parameter is supported only in RepRapFirmware and can be used
tell the firmware about the hardware on which it is running. If the `P`
parameter is present then the integer argument specifies the hardware
being used. The following are currently supported:

`M115 P0   Automatic board type selection if supported, or default if not`\
`M115 P1   Duet 0.6`\
`M115 P2   Duet 0.7`\
`M115 P3   Duet 0.85`

^2^These parameters are only supported in Prusa Firmware. Parameter
`Unnnnnn` will check the firmware version provided. If the firmware
version provided by the U code is higher than the currently running
firmware, it will pause the print for 30s and ask the user to upgrade
the firmware.

sample data `M115`:

`FIRMWARE_NAME:Prusa-Firmware 3.8.1 based on Marlin FIRMWARE_URL:`[`https://github.com/prusa3d/Prusa-Firmware`](https://github.com/prusa3d/Prusa-Firmware)` PROTOCOL_VERSION:1.0 MACHINE_TYPE:Prusa i3 MK3S EXTRUDER_COUNT:1 UUID:00000000-0000-0000-0000-000000000000`

sample data `M115 V`

`3.8.1`

sample data on display for 30s or user interaction`M115 U3.8.2-RC1`

`New firmware version availible:`\
`3.8.2-RC1`\
`Please upgrade.`

#### M116: Wait {#m116_wait}

```{=mediawiki}
{{Firmware Support | fived={{yes}} | teacup={{yes}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{yes}} | smoothie={{no}} | reprapfirmware={{yes}} | bfb={{no}} | machinekit={{no}} | makerbot={{yes}} | redeem={{yes}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   *This command can be used without any additional parameters.^1^*
:   `Pnnn` Tool number
:   `Hnnn` Heater number
:   `Cnnn` Chamber number

Examples

`M116`\
`M116 P1`

Wait for *all* temperatures and other slowly-changing variables to
arrive at their set values if no parameters are specified. See also
`M109`.

Notes

^1^Most implementations don\'t support any parameters, but
RepRapFirmware version 1.04 and later supports an optional \'P\'
parameter that is used to specify a tool number. If this parameter is
present, then the system only waits for temperatures associated with
that tool to arrive at their set values. This is useful during tool
changes, to wait for the new tool to heat up without necessarily waiting
for the old one to cool down fully.

Recent versions of RepRapFirmware also allow a list of the heaters to be
specified using the \'H\' parameter, and if the \'C\' parameter is
present, this will indicate that the chamber heater should be waited
for.

#### M117: Get Zero Position {#m117_get_zero_position}

```{=mediawiki}
{{Firmware Support | fived={{yes}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | makerbot={{no}}: See M70 | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Example

`M117`

This causes the RepRap machine to report the X, Y, Z and E coordinates
*in steps not mm* to the host that it found when it last hit the zero
stops for those axes. That is to say, when you zero X, the
`<i>`{=html}x`</i>`{=html} coordinate of the machine when it hits the X
endstop is recorded. This value should be 0, of course. But if the
machine has drifted (for example by dropping steps) then it won\'t be.
This command allows you to measure and to diagnose such problems. (E is
included for completeness. It doesn\'t normally have an endstop.)

#### M117: Display Message {#m117_display_message}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{yes}}<sup>1</sup> | buddy={{yes}} | repetier={{yes}} | smoothie={{yes}} | reprapfirmware={{yes}} | klipper={{yes}} | bfb={{no}} | machinekit={{no}} | makerbot={{no}} | redeem={{yes}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Example

`M117 Hello World`

This causes the given message to be shown in the status line on an
attached LCD. The above command will display Hello World. If
RepRapFirmware is used and no LCD is attached, this message will be
reported on the web interface.

Notes

In Prusa Firmware it is also used to display internal messages on
LCD.^1^

In RepRapFirmware the message may optionally be enclosed in
double-quotation marks. Doing this is recommended, to clarify the extent
of the text to be displayed.

#### M118: Echo message on host {#m118_echo_message_on_host}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|1.1.4+}} | prusa={{no}} | buddy={{yes}} | repetier={{no}} | reprapfirmware={{yes}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | klipper={{yes}} | yaskawa={{no}} }}
```
Use this code to print a visible message to the host console, preceded
by \'echo:\'.

Parameters
:   `Pn` (RepRapFirmware only) Message targets(s): 0 = generic
    \[default\], 1 = USB, 2 = LCD, 3 = HTTP, 4 = Telnet
:   `S"msg"` (RepRepFirmware only) Message to send

Example (Marlin)

`M118 Color changing to blue`

Example (RepRapFirmware)

`M118 P2 S"Color changing to blue"`

#### M118: Negotiate Features {#m118_negotiate_features}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Example

`M118 P42`

This M-code is for future proofing. NO firmware or hostware supports
this at the moment. It is used in conjunction with `M115`\'s FEATURES
keyword.

See
[Protocol_Feature_Negotiation](Protocol_Feature_Negotiation "Protocol_Feature_Negotiation"){.wikilink}
for more info.

#### M119: Get Endstop Status {#m119_get_endstop_status}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{yes}} | sprinter={{yes}} | klipper={{yes}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | repetier={{yes}} | smoothie={{yes}} | reprapfirmware={{yes}} | bfb={{no}} | machinekit={{no}} | redeem={{yes}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Example

`M119`

Returns the current state of the configured X, Y, Z endstops. Takes into
account any \'inverted endstop\' settings, so one can confirm that the
machine is interpreting the endstops correctly.

In redeem, `M119` can also be used to invert end stops.

Example

`M119 X1 1`

This will invert end stop X1 (Inverted means switch is connected in
Normally Open state (NO))

#### M120: Push {#m120_push}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{yes}} | reprapfirmware={{yes}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Example

`M120`

Push the state of the RepRap machine onto a stack. Exactly what
variables get pushed depends on the implementation (as does the depth of
the stack - a typical depth might be 5). A sensible minimum, however,
might be

- Current feedrate
- Whether moves are relative or absolute
- Whether extrusion is relative or absolute

RepRapFirmware calls this automatically when a macro file is run. In
addition to the variables above, it pushes the following values on the
stack:

- Whether the units are inches or mm
- Whether or not volumetric extrusion is in use
- The selected plane (see G17/G18/G19) for G2/G3 moves

#### M121: Pop {#m121_pop}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{yes}} | reprapfirmware={{yes}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Example

`M121`

Recover the last state pushed onto the stack. RepRapFirmware calls this
automatically when execution of a macro file terminates.

#### M120: Enable endstop detection {#m120_enable_endstop_detection}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{yes|M121}} | buddy={{yes}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{no}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```
#### M121: Disable endstop detection {#m121_disable_endstop_detection}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{yes|M120}} | buddy={{yes}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{no}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```
#### M122: Firmware dependent {#m122_firmware_dependent}

##### M122: Diagnose (RepRapFirmware) {#m122_diagnose_reprapfirmware}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   **Bmmm** Expansion board number for which diagnostics are requested,
    default 0 which means main board
:   **Pnnn** Optional parameter to specify what diagnostics are
    required. Caution: some values of P will crash the firmware
    deliberately to test error handling! See the Duet3D wiki for more
    details.
:   **\"DSF\"** Immediate DSF diagnostics (RRF3/Duet3 only with attached
    SBC)
:   `P200` - **LPC and STM32 Port Only** Outputs the configuration of
    all the pins allocated by the firmware and board.txt

<!-- -->

Example
:   M122

Sending an `M122` causes the RepRap to transmit diagnostic information,
for example via a USB serial link.

If RepRapFirmware is used and debugging is enabled for the Network
module, this will also print LWIP stats to the host via USB.

##### M122: Set Software Endstop (MK4duo) {#m122_set_software_endstop_mk4duo}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{no}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```
Disabled or Enabled Software Endstop M122 S\<0/1\>

##### M122: Debug Stepper drivers (Marlin) {#m122_debug_stepper_drivers_marlin}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{no}} | buddy={{yes}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{no}} | bfb={{no}} | makerbot={{no}} | grbl={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
Get diagnostic info about L6470 or Trinamic stepper drivers having a
UART or SPI interface.

With Trinamic drivers there are some extra parameters, and depending on
the configuration either basic or detailed information will be reported.
Use parameters `X`, `Y`, `Z`, etc. to limit the report only to the
specified steppers, otherwise all steppers are reported. Pass `I` to
re-initialize the drivers. Use parameter `S` to sample at regular
intervals. The `P` parameter can be used to set the sample interval in
milliseconds.

Example

`M122`

#### M123: Firmware dependent {#m123_firmware_dependent}

##### M123: Tachometer value (RepRap, Prusa & Marlin) {#m123_tachometer_value_reprap_prusa_marlin}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}}<sup>2</sup> | prusa={{yes}}<sup>1</sup> | buddy={{yes}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
Sending a `M123` causes the RepRap to transmit filament tachometer
values from all extruders.

Sending a `M123` is used in Prusa firmware to report fan speeds and fan
pwm values.^1^

Sending a `M123` is used in Marlin firmware to report only extruders
fans speeds and pwm values.^2^

Usage

`M123`

Parameters^2^
:   `Sn` autoreport every n seconds (0 to disable)

<!-- -->

Prusa firmware output^1^:
:   `E0: - Hotend fan speed in RPM`
:   `PRN1: - Part cooling fans speed in RPM`
:   `E0@: - Hotend fan PWM value`
:   `PRN1@: - Part cooling fan PWM value`

<!-- -->

Examples^1^

`echo E0:3240 RPM PRN1:4560 RPM E0@:255 PRN1@:255`

Examples^2^

`echo E0:7040 RPM E0@:255`

##### M123: Endstop Logic (MK4duo) {#m123_endstop_logic_mk4duo}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{no}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   `Xn` X Logic
:   `Yn` Y Logic
:   `Zn` Z Logic
:   `In` X2 Logic
:   `Jn` Y2 Logic
:   `Kn` Z2 Logic
:   `Pn` Probe Logic
:   `Dn` Door Logic

<!-- -->

Examples

`M123 ; Print Status`\
`M123 X1 Y1 Z0 P0`

#### M124: Firmware dependent {#m124_firmware_dependent}

##### M124: Immediate motor stop {#m124_immediate_motor_stop}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
Immediately stops all motors.

##### M124: Set Endstop Pullup {#m124_set_endstop_pullup}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   `Xn` X Pullup on/off
:   `Yn` Y Pullup on/off
:   `Zn` Z Pullup on/off
:   `In` X2 Pullup on/off
:   `Jn` Y2 Pullup on/off
:   `Kn` Z2 Pullup on/off
:   `Pn` Probe Pullup on/off
:   `Dn` Door Pullup on/off

<!-- -->

Examples

`M124 ; Print Status`\
`M124 X1 Y1 Z0 P0`

#### M125: Firmware dependent {#m125_firmware_dependent}

##### M125: Park Head {#m125_park_head}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{no}} | buddy={{yes}} | druid={{no}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
Save the current nozzle position and move to the configured park
position.

Usage
:   `M125 [L | P | X | Y |Z ]`

<!-- -->

Parameters
:   `L` Retract length
:   `P` Always show a prompt and await a response ^1^
:   `X` X position to park
:   `Y` Y position to park
:   `Z` Z raise before park

^1^ Not in Prusa Buddy firmware

##### M125: Pause print {#m125_pause_print}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{yes}} | buddy={{yes}} | druid={{no}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
Without any parameters it will park the extruder to default or last set
position. The default pause position will be set during power up and a
reset, the new pause positions aren\'t permanent.

Usage
:   `M125 [ X | Y | Z | S ]`

<!-- -->

Parameters
:   `X` X position to park
:   `Y` Y position to park
:   `Z` Z raise before park
:   `S` Set values \[S0 = set to default values \| S1 = set values\]
    without pausing

Equivalent to M601 and M25 in Prusa Firmware

#### M126: Open Valve {#m126_open_valve}

```{=mediawiki}
{{Firmware Support | fived={{yes}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | makerbot={{yes}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Example

`M126 P500`

Open the extruder\'s valve (if it has one) and wait 500 milliseconds for
it to do so.

##### M126 in MakerBot {#m126_in_makerbot}

Example

`M126 T0`

Enables an extra output attached to a specific toolhead (e.g. fan)

#### M127: Close Valve {#m127_close_valve}

```{=mediawiki}
{{Firmware Support | fived={{yes}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | makerbot={{yes}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Example

`M127 P400`

Close the extruder\'s valve (if it has one) and wait 400 milliseconds
for it to do so.

##### M127 in MakerBot {#m127_in_makerbot}

Example

`M127 T0`

Disables an extra output attached to a specific toolhead (e.g. fan)

#### M128: Extruder Pressure PWM {#m128_extruder_pressure_pwm}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Example

`M128 S255`

PWM value to control internal extruder pressure. `S255` is full
pressure.

#### M129: Extruder pressure off {#m129_extruder_pressure_off}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Example

`M129 P100`

In addition to setting Extruder pressure to 0, you can turn the pressure
off entirely. P400 will wait 100ms to do so.

#### M130: Set PID P value {#m130_set_pid_p_value}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{yes}} | sprinter={{no}} | marlin={{no|M301}} | prusa={{no|M301}} | buddy={{no|M301}} | reprapfirmware={{no|M301}} | repetier={{no}} | smoothie={{no|M301}} | bfb={{no}} | grbl={{no}} | machinekit={{no}} | makerbot={{no}} | redeem={{yes|M301}} | mk4duo={{no}} | yaskawa={{no|M301}} }}
```

Parameters
:   `Pnnn` heater number
:   `Snnn` proportional (Kp)

Example

`M130 P0 S8.0  ; Sets heater 0 P factor to 8.0`

Teacup can control multiple heaters with independent PID controls. For
the default shown at
<https://github.com/Traumflug/Teacup_Firmware/blob/master/config.default.h>,
heater 0 is the extruder (P0), and heater 1 is the bed (P1).

Teacup\'s PID proportional units are in pwm/255 counts per quarter C, so
to convert from counts/C, you would divide by 4. Conversely, to convert
from count/qC to count/C, multiply by 4. In the above example, S=8
represents a Kp=8\*4=32 counts/C.

#### M131: Set PID I value {#m131_set_pid_i_value}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{yes}} | sprinter={{no}} | marlin={{no|M301}} | prusa={{no|M301}} | buddy={{no|M301}} | reprapfirmware={{no|M301}} | repetier={{no}} | smoothie={{no|M301}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{yes|M301}} | mk4duo={{no}} | yaskawa={{no|M301}} }}
```

Parameters
:   `Pnnn` heater number
:   `Snnn` integral (Ki)

Example

`M131 P1 S0.5  ; Sets heater 1 I factor to 0.5`

Teacup\'s PID integral units are in pwm/255 counts per (quarter
C\*quarter second), so to convert from counts/qCqs, you would divide by
16. Conversely, to convert from count/qCqs to count/Cs, multiply by 16.
In the above example, S=0.5 represents a Ki=0.5\*16=8 counts/Cs.

#### M132: Set PID D value {#m132_set_pid_d_value}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{yes}} | sprinter={{no}} | marlin={{no|M301}} | prusa={{no|M301}} | buddy={{no|M301}} | reprapfirmware={{no|M301}} | repetier={{no}} | smoothie={{no|M301}} | bfb={{no}} | grbl={{no}} | machinekit={{no}} | makerbot={{yes}} | redeem={{yes|M301}} | mk4duo={{no}} | yaskawa={{no|M301}} }}
```

Parameters
:   `Pnnn` heater number
:   `Snnn` derivative (Kd)

Example

`M132 P0 S24  ; Sets heater 0 D factor to 24.0`

Teacup\'s PID derivative units are in pwm/255 counts per (quarter degree
per 2 seconds), so to convert from counts/C, you would divide by 4.
Conversely, to convert from count/qC to count/C, multiply by 8. In the
above example, S=24 represents a Kd=24\*8=194 counts/(C/s).

##### M132 in MakerBot {#m132_in_makerbot}

Example

`M132 X Y Z A B`

Loads the axis offset of the current home position from the EEPROM and
waits for the buffer to empty.

#### M133: Set PID I limit value {#m133_set_pid_i_limit_value}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{yes}} | sprinter={{no}} | marlin={{no|M301}} | prusa={{no|M301}} | buddy={{no|M301}} | reprapfirmware={{no|M301}} | repetier={{no}} | smoothie={{no}} | bfb={{no}} | grbl={{no}} | machinekit={{no}} | makerbot={{yes}} | redeem={{no|M301}} | mk4duo={{no}} | yaskawa={{no|M301}} }}
```

Parameters
:   `Pnnn` heater number
:   `Snnn` integral limit (Ki)

Example

`M133 P1 S264  ; Sets heater 1 I limit value to 264`

Teacup\'s PID integral limit units are in quarter-C\*quarter-seconds, so
to convert from C-s, you would multiply by 16. Conversely, to convert
from qC\*qs to C\*s, divide by 16. In the above example, S=264
represents an integral limit of 16.5 C\*s.

##### M133 in MakerBot {#m133_in_makerbot}

Wait for the toolhead to reach its target temperature.

Parameters
:   `Tnn` : Extruder to wait for
:   `Pnn` : Time limit, in seconds

<!-- -->

Example

`M133 T0 P500 ; Wait for Tool 0 to reach target. Fail after 8:20.`

#### M134: Write PID values to EEPROM {#m134_write_pid_values_to_eeprom}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{yes}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}}: See M504 | reprapfirmware={{no}}: See M500 | bfb={{no}} | machinekit={{no}} | makerbot={{yes}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Example

`M134`

##### M134 in MakerBot {#m134_in_makerbot}

Example

`M134 T0 P500`

Instruct the machine to wait for the platform to reach its target
temperature. T is the platform to wait for. P if present, sets the time
limit.

#### M135: Set PID sample interval {#m135_set_pid_sample_interval}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{yes}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | makerbot={{yes}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `Snnn` Heat sample time in seconds

Example

`M135 S300`

Set the PID to measure temperatures and calculate the power to send to
the heaters every 300ms.

##### M135 in MakerBot {#m135_in_makerbot}

Example

`M135 T0`

Instructs the machine to change its toolhead. Also updates the State
Machine\'s current tool_index. T is the toolhead for the machine to
switch to and the new tool_index for the state machine to use.

#### M136: Print PID settings to host {#m136_print_pid_settings_to_host}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{experimental|Debug}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{yes|M301}} | smoothie={{no}} | bfb={{no}} | grbl={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Example

`M136 P1  ; print heater 0 PID parameters to host`

#### M140: Set Bed Temperature (Fast) {#m140_set_bed_temperature_fast}

```{=mediawiki}
{{Firmware Support | fived={{yes}} | teacup={{yes}} | sprinter={{yes}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | repetier={{yes}} | smoothie={{yes}} | reprapfirmware={{yes}} | klipper={{yes}} | bfb={{no}} | machinekit={{yes}} | makerbot={{yes}} | redeem={{yes}} | mk4duo={{yes}} | yaskawa={{yes}} }}
```

Parameters
:   `Pnnn` Bed heater index^1^
:   `Hnnn` Heater number^1^
:   `Tnnn` Tool number^2^
:   `Snnn` Active/Target temperature
:   `Rnnn` Standby temperature^1^ ^2^

Example

`M140 S55`

Set the temperature of the build bed to 55^o^C and return control to the
host immediately (*i.e.* before that temperature has been reached by the
bed).

Notes

^1^ These parameters are only supported in RepRapFirmware.
RepRapFirmware allows the bed heater to be switched off if the absolute
negative temperature (-273.15) is passed as target temperature. In this
case the current bed temperature is not affected:

`M140 S-273.15`

^2^ These parameters are only supported in MK4duo for Idle temperature

`M140 S60 R30`\
`M140 T1 S60 R30`

There is an optional R field that sets the bed standby temperature:
`M140 S65 R40`.

Recent versions of RepRapFirmware also provide an optional \'H\'
parameter to set the hot bed heater number. If no heated bed is present,
a negative value may be specified to disable it.

#### M141: Set Chamber Temperature (Fast) {#m141_set_chamber_temperature_fast}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{yes|1=uses M104}} | sprinter={{no}} | marlin={{yes}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes}} | bfb={{no}} | machinekit={{yes}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   `Pnnn` Chamber index^1^
:   `Hnnn` Heater number^1^
:   `Tnnn` Tool number^2^
:   `Snnn` Active/Target temperature
:   `Rnnn` Standby temperature^1^ ^2^

Examples

`M141 S30`\
`M141 H0`

Set the temperature of the chamber to 30^o^C and return control to the
host immediately (*i.e.* before that temperature has been reached by the
chamber).

Notes

^1^ These parameters are only supported in RepRapFirmware and work just
like in M140.

^2^ These parameters are only supported in MK4duo and work just like in
M140.

#### M142: Firmware dependent {#m142_firmware_dependent}

##### M142: Holding Pressure {#m142_holding_pressure}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{no}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Example

`M142 S1`

Set the holding pressure of the bed to 1 bar.

The holding pressure is in bar. For hardware which only has on/off
holding, when the holding pressure is zero, turn off holding, when the
holding pressure is greater than zero, turn on holding.

##### M142: Set Cooler Temperature (Fast) {#m142_set_cooler_temperature_fast}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | redeem={{no}} | machinekit={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   `Tnnn` Tool number
:   `Snnn` Active/Target temperature
:   `Rnnn` Standby temperature

Examples

`M142 S60`\
`M142 S60 R30`\
`M141 T1 S60 R30`

Set the temperature of the cooler

#### M143: Firmware dependent {#m143_firmware_dependent}

##### M143: Set Laser Cooler Temperature (Fast) {#m143_set_laser_cooler_temperature_fast}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|2.0.8+}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | redeem={{no}} | machinekit={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `Snnn` Target temperature

Examples

`M143 S80`

Set the target temperature of the laser cooler and return immediately.
Use `M193` to set and wait for the temperature to be reached.

##### M143: Maximum heater temperature {#m143_maximum_heater_temperature}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `H` Heater number (RepRapFirmware 1.17 and later, default 1 which is
    normally the first hot end)
:   `S` Maximum temperature

Examples

`M143 S275      ; set the maximum temperature of the hot-end to 275°C`\
`M143 H0 S125   ; set the maximum bed temperature to 125C`

The default maximum temperature for all heaters was 300°C prior to
RepRapFirmware version 1.13, and 262°C from 1.13 onwards. From
RepRapFirmware 1.17 onwards, the default maximum temperatures are 262C
for extruders and 125C for the bed.

When the temperature of the heater exceeds this value, countermeasures
will be taken.

#### M144: Bed Standby {#m144_bed_standby}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{yes}} | smoothie={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   **Pnn** Bed heater number, default 0
:   **Sn** 0 = set bed heater to standby (default), 1 = set bad heater
    active

Example

`M144`

Switch the bed heater to its standby temperature. `M140 S1` turns it
back to its active temperature.

#### M146: Set Chamber Humidity {#m146_set_chamber_humidity}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}}  | reprapfirmware={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `Rnnn` Relative humidity in percent

Example

`M146 R60`

Set the relative humidity of the chamber to 60% and return control to
the host immediately (*i.e.* before that humidity has been reached by
the chamber).

#### M149: Set temperature units {#m149_set_temperature_units}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `C` Flag to treat temperature as degrees Celsius
:   `K` Flag to treat temperature as Kelvin

Example

`M149 K`

It affects the `S` or `R` values in the codes `M104`, `M109`, `M140`,
`M141`, `M143`, `M190` and `G10.` The default is `M149 C`.

#### M150: Set LED color {#m150_set_led_color}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{no}}<sup>1</sup> | buddy={{yes}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes|See below}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   `Rnnn` Red component
:   `Unnn` Green component
:   `Bnnn` Blue component
:   `Wnnn` White component (Marlin)
:   `Pnnn` Brightness (0-255) (Marlin, also RepRapFirmware 2.03 and
    later)
:   `P` Set full brightness (Marlin)
:   `Snnn` (RepRapFirmware) Number of individual LEDs to set to these
    colours
:   `Fn` (RepRapFirmware) Following command action. F0 (default) means
    this is the last command for the LED strip, so the next M150 command
    starts at the beginning of the strip. F1 means further M150 commands
    for the remainder of the strip follow this one.
:   `Xn` (RepRapFirmware) LED type: X0 (default) = DotStar, X1 =
    NeoPixel. This parameter is remembered from one call to the next, so
    it only needs to be given once.
:   `Ynn` (RepRapFirmware) Brightness, 0-31 (alternative to P 0-255)
:   `Qnnn` (RepRapFirmware) Use specified SPI frequency (in Hz) instead
    of default frequency. This parameter is only processed if X
    parameter also present. When using NeoPixels, only frequencies
    between about 2.5MHz and 4MHz will work.

Example

`M150 R255 U128 B192`

Example (RepRapFirmware)

`M150 X1 F3000000         ; set LED type to NeoPixel and set SPI frequency to 3MHz`\
`M150 R255 P128 S20 F1    ; set first 20 LEDs to red, half brightness, more commands for the strip follow`\
`M150 U255 B255 P255 S20  ; set next 20 LEDs to cyan, full brightness, finished programming LED strip`

Set BlinkM, Neopixel, and/or other LED light color and intensity with
RGBW component values from 0 to 255. Some LCD controllers use this
interface for a backlight. Firmware may override the set color to
indicate the current printer status.

RepRapFirmware uses this command to control DotStar or NeoPixel LED
strips on controllers that provide a connector for this purpose. When
using NeoPixel strips there is a firmware-dependent maximum number of
LEDs in the strip supported determined by the size of the DMA buffer.

Notes

In Prusa Firmware this G-code is deactivated by default, must be turned
on in the source code.^1^

#### M154: Auto Report Position {#m154_auto_report_position}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|2.0.8.1}} | klipper={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
Hosts normally monitor printer position by sending `M114` every couple
of seconds. This adds more serial traffic and fails if the command queue
is full. `M154` reduces traffic by setting the firmware to report the
\'projected\' position at regular intervals. This behavior is disabled
by default for best compatibility with existing hosts. If the firmware
supports `M154` the output of `M115` will report the `AUTOREPORT_POS`
capability.

Usage
:   `M154 Snnn` : Set the auto-report interval in seconds. Set the
    interval to 0 to disable.

#### M155: Automatically send temperatures {#m155_automatically_send_temperatures}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|1.1.0+}} | prusa={{yes}}<sup>1</sup> | buddy={{yes}} | repetier={{yes}} | smoothie={{no}} | reprapfirmware={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   `Snnn` enable sending temperatures = 1, disable = 0
:   `Snnn` Interval in seconds between auto-reports. S0 to disable.
    (Marlin) Prusa has a Maximum: 255^1^
:   `Cnn` Activate auto-report function (bit mask). Default is
    temperature.^1^

<!-- -->

C bitmap^1^
:   `bit 0 = Auto-report temperatures`
:   `bit 1 = Auto-report fans`
:   `bit 2 = Auto-report position`
:   `bit 3 = free`
:   `bit 4 = free`
:   `bit 5 = free`
:   `bit 6 = free`
:   `bit 7 = free`

<!-- -->

Examples

`M155 S1 ; Enable temperature report (Marlin: every 1 second)`\
`M155 S0 ; Stop reporting temperatures`\
`M155 S4 ; Report temperatures every 4 seconds (Marlin)`\
`M155 S4 C7; Reports temperatures, fans and position every 4 seconds (Prusa)`^`1`^

Hosts normally monitor printer temperatures by sending `M105` every
couple of seconds. This not only adds serial traffic but it will fail
whenever the command queue is full. `M155` addresses these problems by
telling the firmware to automatically report temperatures at regular
intervals. This behavior is disabled by default for best compatibility
with existing hosts. If the firmware supports `M155` the output of
`M115` will report the `AUTOREPORT_TEMP` capability:

[`Cap:AUTOREPORT_TEMP:1`](Cap:AUTOREPORT_TEMP:1)

Prusa Firmware 3.10.0+ also adds capabilities:

[`Cap:AUTOREPORT_FANS:1`](Cap:AUTOREPORT_FANS:1)\
[`Cap:AUTOREPORT_POSITION:1`](Cap:AUTOREPORT_POSITION:1)\
[`Cap:EXTENDED_M20:1`](Cap:EXTENDED_M20:1)

#### M160: Number of mixed materials {#m160_number_of_mixed_materials}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{no}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Example

`M160 S4`

This command has been superseded by the tool definition command `M563`
(see below).

Set the number of materials, N, that the current extruder can handle to
the number specified. The default is 1.

When N \>= 2, then the E field that controls extrusion requires N values
separated by colons \":\" after it like this:

`M160 S4`\
`G1 X90.6 Y13.8 E2.24:2.24:2.24:15.89`\
`G1 X70.6 E0:0:0:42.4`\
`G1 E42.4:0:0:0`

The second line moves straight to the point (90.6, 13.8) extruding a
total of 22.4mm of filament. The mix ratio for the move is
0.1:0.1:0.1:0.7.

The third line moves back 20mm in X extruding 42.4mm of filament.

The fourth line has no physical effect.

#### M163: Set weight of mixed material {#m163_set_weight_of_mixed_material}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|1.1.0+}} | prusa={{no}} | buddy={{no}} | repetier={{yes|0.92+}} | smoothie={{no}} | reprapfirmware={{partial|M567}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   `Snnn` extruder number
:   `Pnnn` weight

Set weight for this mixing extruder drive.\
`<small>`{=html}See *[Repetier Color
Mixing](Repetier_Color_Mixing "Repetier Color Mixing"){.wikilink}* for
more informations.`</small>`{=html}

#### M164: Store weights {#m164_store_weights}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|1.1.0+}} | prusa={{no}} | buddy={{no}} | repetier={{yes|0.92}} | smoothie={{no}} | reprapfirmware={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   `Snnn` virtual extruder number
:   `Pnnn` store to eeprom (P0 = no, P1 = yes)

Store weights as virtual extruder S.

#### M165: Set multiple mix weights {#m165_set_multiple_mix_weights}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|1.1.0+}} | prusa={{no}} | buddy={{no}} | repetier={{no}}: | smoothie={{no}} | reprapfirmware={{partial|M567}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters `A B C D H I`
:   `A[factor]` Mix factor for extruder stepper 1
:   `B[factor]` Mix factor for extruder stepper 2
:   `C[factor]` Mix factor for extruder stepper 3
:   `D[factor]` Mix factor for extruder stepper 4
:   `H[factor]` Mix factor for extruder stepper 5
:   `I[factor]` Mix factor for extruder stepper 6

- Set multiple mix factors for a mixing extruder.
- Factors that are left out will be set to 0.
- All factors together must add up to 1.0.

#### M190: Wait for bed temperature to reach target temp {#m190_wait_for_bed_temperature_to_reach_target_temp}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no|M116}} | sprinter={{yes}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | repetier={{yes}} | smoothie={{yes}} | reprapfirmware={{yes}} | klipper={{yes}} | bfb={{no}} | machinekit={{yes}} | redeem={{yes}} | mk4duo={{yes}} | yaskawa={{yes}} }}
```

Parameters
:   `Snnn` minimum target temperature, waits until heating
:   `Rnnn` accurate target temperature, waits until heating and cooling
    (Marlin and Prusa)

Example

`M190 S60`

Wait for the bed temperature to reach 60 degrees, printing out the
temperatures once per second.

#### M191: Wait for chamber temperature to reach target temp {#m191_wait_for_chamber_temperature_to_reach_target_temp}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|2.0.0+}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes|1.17+}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{yes}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Example

`M191 S60`

Set the temperature of the build chamber to 60 °C and wait for the
temperature to be reached.

Parameters
:   `Snnn` minimum target temperature, waits until heating
:   `Rnnn` accurate target temperature, waits until heating and cooling
    (Marlin)

#### M192: Wait for Probe Temperature {#m192_wait_for_probe_temperature}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{no}} | bfb={{no}} | machinekit={{no}} | makerbot={{no}} | grbl={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
Use `M192` to dwell until the probe is at or above a given temperature.

#### M193: Set Laser Cooler Temperature {#m193_set_laser_cooler_temperature}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|2.0.8+}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | redeem={{no}} | machinekit={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `Snnn` Target temperature

Examples

`M193 S65`

Set the target temperature of the laser cooler and wait for the
temperature to be reached. Use `M143` to set the temperature and return
immediately. If the Emergency Parser is enabled you can use `M108` to
break out of the wait loop.

#### M200: Set filament diameter {#m200_set_filament_diameter}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | repetier={{yes}} | smoothie={{yes}} | reprapfirmware={{yes|1.19+}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{yes}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```
Volumetric Extrusion is a firmware mode (and an option you can set in
some slicers) wherein all extrusion amounts are specified as a volume
---using cubic millimeters or inches (i.e., mm^3^ or in^3^)--- instead
of a linear distance. This makes it possible to use the same G-code with
any filament diameter.

`M200` tells the firmware what the filament diameter is, and (if
non-zero) to enable Volumetric Extrusion.

Send `M200` without parameters to get the current Volumetric Extrusion
state and filament diameters.

Note that slicer-commanded retraction amounts must also be specified in
mm^3^ since the E axis is interpreted as a volume. However, when using
Firmware Retraction (`G10` / `G11`) the retractions specified by `M207`
are still set in linear units.

Parameters (Marlin)
:   `D[linear]` Set the filament diameter in current units. If non-zero,
    enable Volumetric Extrusion.
:   `T[index]` Select the target extruder. If omitted, the active
    extruder.
:   `S[bool]` Enable or Disable Volumetric Extrusion (without modifying
    the filament diameter).
:   `L[limit]` Set the Maximum Extrusion Volume in mm^3^ per second.
    (Ignores units set by `G20`.) Use `L0` for no limit.

Examples (Marlin)

`M200 D0       ; Disable Volumetric Extrusion on all extruders`\
`M200 D1.75    ; Set filament diameter for the current extruder to 1.75mm`\
`M200 T1 D2.85 ; Set filament diameter for E2 to 1.75mm`\
`M200 T1 L12   ; Set Maximum Extrusion Volume for E2 to 12mm`^`3`^\
`M200 S1       ; Enable Volumetric Extrusion using the last-set diameters`

Parameters (RepRapFirmware)
:   `Daaa:bbb:ccc...` Set filament diameter to aaa for extruder 1, bbb
    for extruder 2, etc. In RepRapFirmware 3.4 and earlier, if any of
    aaa, bbb etc. are zero then Volumetric Extrusion is disabled for
    that extruder.
:   `Daaa` Set filament diameter for all extruders.
:   `S[bool]` Enable or disable volumetric extrusion for this input
    channel (RepRapFirmware 3.5 and later)

Examples (RepRapFirmware)

`M200 D0               ; Disable volumetric extrusion on all extruders (RRF 3.4 and earlier)`\
`M200 S0               ; Disable volumetric extrusion for tis input channel (RRF 3.5 and later)`\
`M200 D1.75            ; Set all extruder filament diameters to 1.75mm`\
`M200 D1.75:3.0:1.75   ; Set extruder 0 to 1.75mm, E1 to 3.0mm and the rest to 1.75mm`

#### M201: Set max acceleration {#m201_set_max_acceleration}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{yes}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | repetier={{yes}} | smoothie={{no}} | reprapfirmware={{yes}} | klipper={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{yes}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   `Xnnn` Acceleration for X axis in units/s^2^
:   `Ynnn` Acceleration for Y axis in units/s^2^
:   `Znnn` Acceleration for Z axis in units/s^2^
:   `Ennn` Acceleration for the active or specified extruder in
    units/s^2^

Example

`M201 X1000 Y1000 Z100 E2000`

Set the acceleration that axes can do in units/s^2^.

The `M201` command is intended to define the machine\'s physical limits.
Slicers should use the `M204` command to define accelerations for a job
and leave `M201` settings to the user.

RepRapFirmware specific: Multiple colon-separated E values can be
provided, so that different extruders can use different accelerations.
If a single E value is provided, that value is applied to all extruders.
The values must be provided in mm/sec\^2 even if G20 has been used to
set units to inches. M201 without parameters reports the current
settings.

#### M201.1: Set reduced acceleration for special move types {#m201.1_set_reduced_acceleration_for_special_move_types}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes|3.4 and later}} | klipper={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `Xnnn` Acceleration for X axis in units/s^2^
:   `Ynnn` Acceleration for Y axis in units/s^2^
:   `Znnn` Acceleration for Z axis in units/s^2^
:   `Ennn:nnn...` Acceleration for the extruders in units/s^2^

Example

`M201.1 X500 Y500 Z20 E500:500`

Set the acceleration that axes should use for special types of move that
should be done using reduced acceleration.

RepRapFirmware specific: these values are used for probing moves
(because some types of Z probe can be triggered by high acceleration at
the start of the move) and for moves that involve stall detection
endstops (because high acceleration can bring the motor close to
stalling). If a single E value is provided, that value is applied to all
extruders. The values must be provided in mm/sec\^2 even if G20 has been
used to set units to inches. M201.1 without parameters reports the
current settings.

#### M202: Set max travel acceleration {#m202_set_max_travel_acceleration}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{yes}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | repetier={{yes}} | smoothie={{no}} | reprapfirmware={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```
Set max travel acceleration in units/s\^2 for travel moves
(`M202 X1000 Y1000`). *Unused in Marlin!!*

#### M203: Firmware dependent {#m203_firmware_dependent}

##### M203: Set maximum feedrate {#m203_set_maximum_feedrate}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{yes}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | repetier={{yes}} | smoothie={{yes}} | reprapfirmware={{yes}} | klipper={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   `Xnnn` Maximum feedrate for X axis
:   `Ynnn` Maximum feedrate for Y axis
:   `Znnn` Maximum feedrate for Z axis
:   `Ennn` Maximum feedrate for extruder drives
:   `Innn` (RepRapFirmware) Minimum feed rate (optional)

Example

`M203 X6000 Y6000 Z300 E10000`

Sets the maximum feedrates that your machine can do in mm/min. (Marlin
uses mm/sec).

This command is intended to define the machine limits. Slicers should
not generate M203 commands, instead they should use the F parameter on
G0, G1 etc. command to specify the requested speeds.

##### M203 (Repetier): Set temperature monitor {#m203_repetier_set_temperature_monitor}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{yes}} | smoothie={{no}} | reprapfirmware={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
Set temperature monitor to `Sx`. Repetier Firmware only.

#### M204: Firmware dependent {#m204_firmware_dependent}

##### M204: Set default acceleration {#m204_set_default_acceleration}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{yes}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | repetier={{no}} | smoothie={{yes}} | reprapfirmware={{yes|1.18+}} | klipper={{yes}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | druid={{yes}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters (RepRapFimware)
:   `Pnnn` Acceleration for printing moves
:   `Tnnn` Acceleration for travel moves

Example

`M204 P500 T2000`

Accelerations set with `M204` apply to the move as a whole based on the
type of move. Use `M201` to set limits for each axis individually. Both
of these limits will be applied during printing.

Parameters (MK4duo)
:   `Pnnn` Acceleration for printing moves
:   `Vnnn` Acceleration for travel moves
:   `Rnnn` Acceleration for Retraction for Tools with T code

Example

`M204 P500 V2000 T0 R5000`

**Other firmwares:**

:   `S[accel]` Set Acceleration for normal moves in units/s^2^
:   `T[accel]` Set Acceleration for retract/recover moves in units/s^2^
:   `B[ms]` Set Minimum Segment Time to prevent planner starvation.

**Marlin notes:** Since version 1.0.2-1 the `M204` options are:

:   `P[accel]` Set Acceleration for Printing moves. (i.e., Any XYZ
    motion plus E.)
:   `R[accel]` Set Acceleration for Retract moves. (i.e., E-axis only
    moves.)
:   `T[accel]` Set Acceleration for Travel moves. (i.e., without E
    movement)

<!-- -->

Example

Set the acceleration for printing movements to 800mm/s\^2, for travels
to 3000mm/s\^2 and for retracts to 9000mm/s\^2.

`M204 P800 T3000 R9000`

##### M204: Set PID values {#m204_set_pid_values}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{yes}} | smoothie={{no}} | reprapfirmware={{no}} | klipper={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | druid={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Usage

`M204 X[Kp] Y[Ki] Z[Kd]`

Set one or more PID parameters. Values are 100 \* real value.

#### M205: Firmware dependent {#m205_firmware_dependent}

##### M205: Advanced settings {#m205_advanced_settings}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{yes}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | repetier={{yes}} | reprapfirmware={{partial|M566}} | klipper={{no}} | smoothie={{yes}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Sprinter / Marlin:
:   Minimum travel speed = `S[printing]` `T[travel]`
:   `B[min segment time] X[max XY jerk] Z[max Z jerk] E[max E jerk]`

<!-- -->

Sprinter / Marlin Example:

`M205 X30 Z5 ; Set X/Y Jerk to 30mm/s, Z jerk to 5mm/s`

**Smoothieware** uses a different algorithm:
[1](https://onehossshay.wordpress.com/2011/09/24/improving_grbl_cornering_algorithm/)

:   X\[xy junction deviation\] Z\[z junction deviation\] S\[minimum
    planner speed\].
:   Z junction deviation only applies to z only moves
:   0 disables junction deviation for Z
:   -1 uses global junction deviation

<!-- -->

Smoothie example:

`M205 X0.05  ; set X/Y Junction Deviation`

##### M205: EEPROM Report {#m205_eeprom_report}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{yes}} | smoothie={{no}} | reprapfirmware={{no}} | klipper={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | druid={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
Output EEPROM settings. Repetier Firmware only.

#### M206: Firmware dependent {#m206_firmware_dependent}

##### M206: Offset axes {#m206_offset_axes}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{yes}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | repetier={{no}} | reprapfirmware={{yes}} | smoothie={{yes}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{yes}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   `Xnnn` X axis offset
:   `Ynnn` Y axis offset
:   `Znnn` Z axis offset

Example

`M206 X10.0 Y10.0 Z-0.4`

The values specified are added to the endstop position when the axes are
referenced. The same can be achieved with a `G92` right after homing
(`G28`, `G161`).

With Marlin firmware, the current values can read from the machine with
a bare `M206` command and be saved to EEPROM using the `M500` command.
(See also `M290`: Babystepping)

A similar command is `G10`, aligning these two is [ subject to
discussion](Talk:G-code#M104_.26_M109_Deprecation,_G10_Introduction " subject to discussion"){.wikilink}.

With Marlin 1.0.0 RC2 a negative value for z lifts(!) your printhead.

In builds of RepRapFirmware that support CNC workplace coordinates,
using this command is equivalent to using G10 L2 P1 to set the
coordinate offsets for workplace 1.

##### M206: Set EEPROM value {#m206_set_eeprom_value}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{yes}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
Set a Repetier Firmware EEPROM value.

Parameters
:   `T[type]` Value type
:   `P[pos]` Value position
:   `[S(long)]` An integer value
:   `[X(float)]` A float value

<!-- -->

Example

`M206 T3 P39 X19.9 ; Set Jerk to 19.9`

#### M207: Firmware dependent {#m207_firmware_dependent}

##### M207: Set retract length {#m207_set_retract_length}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | repetier={{no}} | smoothie={{yes}} | reprapfirmware={{yes}} | bfb={{no}} | grbl={{no}} | machinekit={{yes}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{yes}} }}
```

Parameters
:   `Snnn` positive length to retract, in mm
:   `Rnnn` positive or negative additional length to un-retract, in mm
    (RepRapFirmware only)
:   `Fnnn` retraction feedrate, in mm/min
:   `Tnnn` feedrate for un-retraction if different from retraction,
    mm/min (RepRapFirmware 1.16 and later only)
:   `Znnn` additional zlift/hop

Example

`M207 S4.0 F2400 Z0.075`

Set the retract length used by the `G10` and `G11` commands. Units are
in mm regardless of `M200` setting.

Machinekit uses different parameters and speed units for `M207`. Use `P`
to set retract length in mm. Use `Q` to set retract velocity in mm/s.
For firmware retraction Machinekit uses `G22` and `G23` in place of
`G10` and `G11`.

##### M207 Calibrate Z axis with Z max endstop {#m207_calibrate_z_axis_with_z_max_endstop}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{yes|Use G1 S3 ...}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Example

`M207`

After placing the tip of the nozzle in the position you expect to be
considered Z=0, issue this command to calibrate the Z axis. It will
perform a z axis homing routine and calculate the distance traveled in
this process. The result is stored in EEPROM as z_max_length. For using
this calibration method the machine must be using a Z MAX endstop.

This procedure is usually more reliable than mechanical adjustments of a
Z MIN endstop.

##### M207 (Repetier): Set jerk without saving to EEPROM {#m207_repetier_set_jerk_without_saving_to_eeprom}

```{=mediawiki}
{{Firmware Support | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{yes}} | smoothie={{no}} | reprapfirmware={{partial|M566}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
Repetier Firmware only. Change the maximum instantaneous speed change
(\"jerk\") values, but don\'t store the change in EEPROM.

Since Repetier 0.91 December 2013
\[//github.com/repetier/Repetier-Firmware/blob/d86da831853288d4a10fb0584d006c7763ca2bb6/src/ArduinoAVR/Repetier/Repetier.ino#102\]
(if not earlier)

Parameters
:   `Xnnn` Temporarily set XY jerk in mm/s
:   `Znnn` Temporarily set Z jerk in mm/s
:   `Ennn` Temporarily set Extruder jerk in mm/s

<!-- -->

Example

`M207 X10  ; Change the X/Y Jerk to 10mm/s`

#### M208: Firmware dependent {#m208_firmware_dependent}

##### M208: Set unretract length {#m208_set_unretract_length}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | repetier={{no}} | smoothie={{yes}} | reprapfirmware={{yes|Use M207}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   `Snnn` positive length surplus to the `M207 Snnn`, in mm
:   `Fnnn` feedrate, in mm/sec

Sets the \"recover\" (aka \"unretract\") length.

##### M208 (RepRapFirmware): Set axis max travel {#m208_reprapfirmware_set_axis_max_travel}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `Snnn` 0 = set axis maximum (default), 1 = set axis minimum
:   `Xnnn` X axis limit
:   `Ynnn` Y axis limit
:   `Znnn` Z axis limit

Example
:   M208 X200 Y200 Z90 ; set axis maxima
:   M208 X-5 Y0 Z0 S1 ; set axis minima

The values specified set the software limits for axis travel in the
specified direction. The axis limits you set are also the positions
assumed when an endstop is triggered.

#### M209: Enable automatic retract {#m209_enable_automatic_retract}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | repetier={{yes}} | smoothie={{no}} | reprapfirmware={{no}} | bfb={{no}} | machinekit={{no}} | makerbot={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```
With automatic retract detection, G-code generated by slicers without
`G10`/`G11` support can take advantage of Firmware Retraction. The
firmware converts E-only moves into retract/recover moves, using the
firmware\'s tuned lengths and feedrates in place of the original E
moves.

Example

`M209 S1`

The `S` parameter turns Automatic Retract Detection on (1) or off (0).

#### M210: Set homing feedrates {#m210_set_homing_feedrates}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|2.1.3+}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Example

`M210 X1000 Y1500`

Set the feedrates used for homing to the values specified in mm per
minute.

If the machine is set to inches mode (e.g., with `G20`), this command
may treat input values as inches-per-minute.

#### M211: Disable/Enable software endstops {#m211_disableenable_software_endstops}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{no}} | buddy={{yes}} | repetier={{no}} | reprapfirmware={{partial|Use M564}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
The boolean value S 1=enable or 0=disable controls state of software
endstop.

The boolean value X, Y or Z 1=max endstop or 0=min endstop selects which
endstop is controlled.

Example

`M211 X1 Y1 Z1 S0`

Disables X,Y,Z max endstops

Example

`M211 X0 S1`

Enables X min endstop

Example

`M211`

Prints current state of software endstops.

#### M212: Set Bed Level Sensor Offset {#m212_set_bed_level_sensor_offset}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{partial}}* | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{partial|Use G31}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
This G-Code command is known to be available in the newer versions of
PrintrBot\'s branch of Marlin. It may not be available in other
firmware.

Example

`M212 Z-0.2`

Set the Z home to 0.2 mm lower than where the sensor says Z home is.
This is extremely useful when working with printers with hard-to-move
sensors, like the PrintrBot Metal Plus.

PrintrBot suggests that the user make minor (0.1-0.2) adjustments
between attempts and immediately executes `M500` & `M501` after setting
this.

#### M214: Set Arc configuration values {#m214_set_arc_configuration_values}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{yes}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Usage
:   `M214 [P] [S] [N] [R] [F]`

<!-- -->

Parameters
:   `Pnnn` A float representing the max and default millimeters per arc
    segment. Must be greater than 0.
:   `Snnn` A float representing the minimum allowable millimeters per
    arc segment. Set to 0 to disable
:   `Nnnn` An int representing the number of arcs to draw before
    correcting the small angle approximation. Set to 0 to disable.
:   `Rnnn` An int representing the minimum number of segments per arcs
    of any radius, except when the results in segment lengths greater
    than or less than the minimum and maximum segment length. Set to 0
    to disable.
:   `Fnnn` An int representing the number of segments per second, unless
    this results in segment lengths greater than or less than the
    minimum and maximum segment length. Set to 0 to disable.

Prusa Firmware for MK3S/+, MK2.5/S only!

#### M217: Toolchange Parameters {#m217_toolchange_parameters}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{no}} | buddy={{yes}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{partial|Use tool change files}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
If arguments are given, sets tool-change retract and prime length (mm),
prime feedrate (mm/min), retract feedrate (mm/min), and park
position/raise (mm) or Z raise (mm): S`<length>`{=html}
P`<prime_speed>`{=html} R`<retract_speed>`{=html} X`<xpos>`{=html}
Y`<ypos>`{=html} Z`<zraise>`{=html}. XY arguments require
**SINGLENOZZLE_SWAP_PARK**. If no arguments are given, reports current
values. Currently used to set the `SINGLENOZZLE` tool-change options in
Marlin 2.0 and up. May be extended for other tool-changing systems in
the future.

#### M218: Set Hotend Offset {#m218_set_hotend_offset}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{no}} | buddy={{yes}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{partial|Use G10}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```
Sets hotend offset (in mm): T`<extruder_number>`{=html}
X`<offset_on_X>`{=html} Y`<offset_on_Y>`{=html}.

Example

`M218 T1 X50 Y0.5`

#### M220: Set speed factor override percentage {#m220_set_speed_factor_override_percentage}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{yes}} | sprinter={{yes}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | repetier={{yes}} | smoothie={{yes}} | reprapfirmware={{yes}} | klipper={{yes}} | bfb={{no}} | machinekit={{no}} | redeem={{yes}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   `Snnn` Speed factor override percentage (0..100 or higher)

Example

`M220 S80`

Sets the speed factor override percentage.

#### M221: Set extrude factor override percentage {#m221_set_extrude_factor_override_percentage}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{yes}} | sprinter={{yes}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | repetier={{yes}} | smoothie={{yes}} | reprapfirmware={{yes}} | bfb={{no}} | machinekit={{no}} | redeem={{yes}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   `Snnn` Extrude factor override percentage (0..100 or higher),
    default 100%
:   `Dnnn` Extruder drive number (RepRapFirmware only), default 0

Example

`M221 S70`\
`M221 S95 D1`

Sets extrude factor override percentage. In the case of RepRapFirmware,
sets the extrusion factor percentage for the specified extruder drive
only.

#### M220: Turn off AUX V1.0.5 {#m220_turn_off_aux_v1.0.5}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{yes}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
#### M221: Turn on AUX V1.0.5 {#m221_turn_on_aux_v1.0.5}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{yes}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
#### M222: Set speed of fast XY moves {#m222_set_speed_of_fast_xy_moves}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{yes}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
#### M223: Set speed of fast Z moves {#m223_set_speed_of_fast_z_moves}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{yes}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
#### M224: Enable extruder during fast moves {#m224_enable_extruder_during_fast_moves}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{yes}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
#### M225: Disable on extruder during fast moves {#m225_disable_on_extruder_during_fast_moves}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{yes}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
#### M226: G-code Initiated Pause {#m226_g_code_initiated_pause}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes}} | bfb={{yes}} | machinekit={{yes}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Example

`M226`

Initiates a synchronous pause (pauses after all previous commands from
the same stream have been completed). That is, program execution is
stopped and the printer waits for user interaction. This matches the
behaviour of `M1` in the [NIST RS274NGC G-code
standard](http://www.nist.gov/manuscript-publication-search.cfm?pub_id=823374)
and `M0` in Marlin firmware.

#### M226: Wait for pin state {#m226_wait_for_pin_state}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | repetier={{yes}} | reprapfirmware={{no|see M577}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   `Pnnn` pin number
:   `Snnn` pin state

Example

`M226 P2 S1`

Wait for a pin to be in some state.

#### M227: Enable Automatic Reverse and Prime {#m227_enable_automatic_reverse_and_prime}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Example

`M227 P1600 S1600`

P and S are steps.

\"Reverse and Prime\" means, the extruder filament is retracted some
distance when not in use and pushed forward the same amount before going
into use again. This shall help to prevent drooling of the extruder
nozzle. Teacup firmware implements this with `M101`/`M103`.

#### M228: Disable Automatic Reverse and Prime {#m228_disable_automatic_reverse_and_prime}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Example

`M228`

See also `M227`.

#### M229: Enable Automatic Reverse and Prime {#m229_enable_automatic_reverse_and_prime}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Example

`M229 P1.0 S1.0`

`P` and `S` are extruder screw rotations. See also `M227`.

#### M230: Disable / Enable Wait for Temperature Change {#m230_disable_enable_wait_for_temperature_change}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{no}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Example

`M230 S1`

`S1` Disable wait for temperature change `S0` Enable wait for
temperature change

#### M231: Set OPS parameter {#m231_set_ops_parameter}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{yes}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
`M231 S[OPS_MODE] X[Min_Distance] Y[Retract] Z[Backslash] F[RetractMove]`

#### M232: Read and reset max. advance values {#m232_read_and_reset_max._advance_values}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{yes}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
#### M240: Trigger camera {#m240_trigger_camera}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{no}}<sup>1</sup> | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Example

`M240`

Triggers a camera to take a photograph. (Add to your per-layer G-code.)

Notes

In Prusa Firmware this G-code is deactivated by default, must be turned
on in the source code.^1^

#### M240: Start conveyor belt motor / Echo off {#m240_start_conveyor_belt_motor_echo_off}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{experimental|Debug: Echo off}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | reprapfirmware={{no}} | repetier={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Example

`M240`

The conveyor belt allows to start mass production of a part with a
reprap.

Echoing may be controlled in some firmwares with `M111`.

#### M241: Stop conveyor belt motor / echo on {#m241_stop_conveyor_belt_motor_echo_on}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{experimental|Debug: Echo on}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Example

`M241`

Echoing may be controlled in some firmwares with `M111`.

#### M245: Start cooler {#m245_start_cooler}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|Use M143/M193}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{yes|Use M106}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Example

`M245`

used to cool parts/heated-bed down after printing for easy remove of the
parts after print

#### M246: Stop cooler {#m246_stop_cooler}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|Use M143/M193}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{yes|Use M106}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Example

`M246`

#### M250: Set LCD contrast {#m250_set_lcd_contrast}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | repetier={{no}} | reprapfirmware={{partial|Use M918}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | makerbot={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Example

`M250 C20`

Sets LCD contrast C`<contrast value>`{=html} (value 0..63), if
available.

#### M256: Set LCD brightness {#m256_set_lcd_brightness}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|2.0.9.3}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | makerbot={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} | grbl={{no}} | klipper={{no}} }}
```

Example

`M256 B128`

Set the LCD brightness B`<brightness value>`{=html} (value 0..255), if
available.

#### M251: Measure Z steps from homing stop (Delta printers) {#m251_measure_z_steps_from_homing_stop_delta_printers}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{yes}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Examples

`M251 S0 ; Reset`\
`M251 S1 ; Print`\
`M251 S2 ; Store to Z length (also EEPROM if enabled)`

(This is a Repetier-Firmware only feature.)

#### M260: i2c Send Data {#m260_i2c_send_data}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|1.1.0+}} | prusa={{no}} | buddy={{yes}} | repetier={{no}} | reprapfirmware={{yes|1.21+}} | smoothie={{no}} | bfb={{no}} | grbl={{no}} | machinekit={{no}} | makerbot={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```
Buffer and send data over the i2c bus. Use `A` to set the address from
0-127. Add up to 32 bytes to the buffer with each `B`. Send and reset
the buffer with `S`.

Parameters (Marlin, MK4duo)
:   **Ann** I2C address
:   **Bnn** Byte to buffer or send
:   **S** If present, sends the bytes that have been buffered

Examples

`M260 A5 B65 S ; Send 'A' to Address 5 now`\
`M260 A0       ; Set address to 0 (broadcast)`\
`M260 B77  ; M`\
`M260 B97  ; a`\
`M260 B114 ; r`\
`M260 B108 ; l`\
`M260 B105 ; i`\
`M260 B110 ; n`\
`M260 S1   ; Send the current buffer`

Parameters (RepRapFirmware)
:   **Ann** I2C address
:   **Bnn:nn:nn\...** Bytes to send
:   **Snn** Number of bytes to receive (RepRapFirmware 2.02 and later)
:   **V\"name\"** (optional, RepRapFirmware 3.6) variable to store the
    received data into. Ignored unless a nonzero S parameter was
    provided.

<!-- -->

Examples

`M260 A5 B65                    ; Send 'A' to address 5`\
`M260 A{0x7F} B65               ; Send 'A' to address 7F (hex)`\
`M260 A0 B82:101:112:82:97:112  ; Send 'RepRap' to address 0`

RepRapFirmware does not use the S parameter to mean send the current
buffer, instead the address and all the bytes to send are specified in a
single command.

#### M260.1: Modbus Write register(s) {#m260.1_modbus_write_registers}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{yes|3.6+}} | smoothie={{no}} | bfb={{no}} | grbl={{no}} | machinekit={{no}} | makerbot={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters (provisional, RepRapFirmware)
:   **Pnn** Serial port to send/receive through, numbered as in M575 (1
    = first aux port, 2 = second aux port). The port must already have
    been set to Modbus mode using M575.
:   **Ann** Modbus slave device address
:   **Rnn** First Modbus register number to send data to
:   **Bnn:nn:nn\...** 16-bit words to send

<!-- -->

Examples

`M260 A5 R10 B956               ; write 956 to register 10 of the device at address 5`\
`M260 A8 R20 B123:456           ; write 123 to register 20 and 456 to register 21 of the device at address 8`

#### M261: i2c Request Data {#m261_i2c_request_data}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|1.1.0+}} | prusa={{no}} | buddy={{yes}} | repetier={{no}} | reprapfirmware={{yes|1.21+}} | smoothie={{no}} | bfb={{no}} | grbl={{no}} | machinekit={{no}} | makerbot={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```
Request data (synchronously) from an i2c slave device. This command in
basic form simply relays the received data to the host.

Parameters
:   **Ann** I2C device address
:   **Bnn** How many bytes to request
:   **Snn** (Marlin 2.0.9.3) Style of output: 0 = Raw (default), 1 =
    Bytes (hex), 2 = 1-2 byte (integer), 3 = Bytes (decimal)
:   **V\"name\"** (optional, RepRapFirmware 3.6 and later) name of
    variable to receive data into. If this parameter is not present then
    the data read is output to the console.

Examples

`M261 A99 B5                          ; Request/get 5 bytes from I2C address 99 and print them as-is.`\
`M261 A32 B7 S1                       ; (Marlin) Request/get 7 bytes from Address 32 and print them as space-delimited hex bytes.`\
`M261 A80 R10 B2 V"var.modbusData"    ; (RepRapFirmware) Read registers 10 and 11 from I2C address 80 and store the result in var.modbusData`

Both `M260` and `M261` are commands demonstrating use of the i2c bus
(TWIBus class) in Marlin Firmware. Developers and vendors can make
Marlin an i2c master device by enabling `EXPERIMENTAL_I2CBUS`, and
Marlin can act as a slave device by setting `I2C_SLAVE_ADDRESS` from
8-127. This class can be used to divide up processing responsibilities
between multiple instances of Marlin running on multiple boards. For
example, one board might control a Z axis with 4 independent steppers to
create a self-leveling system, or a second board could drive the
graphical display while the first board handles printing.

#### M261.1: Modbus Read Input Registers {#m261.1_modbus_read_input_registers}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{yes|3.6+}} | smoothie={{no}} | bfb={{no}} | grbl={{no}} | machinekit={{no}} | makerbot={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
Request data (synchronously) from a Modbus slave device.

Parameters (provisional)
:   **Ann** Modbus device address
:   **Bnn** How many 16-bit registers to request
:   **Pnn** Port to request data through, same numbering as in M575
    command (1 = first aux port, 2 = second aux port). The port must
    already have been put into Modbus mode using M575.
:   **Rnn** Register number to start from
:   **V\"name\"** (optional) name of variable to receive data into. If
    this parameter is not present then the data read is output to the
    console.

<!-- -->

Examples

`M261 P1 A80 R10 B2 V"var.modbusData" ; (RepRapFirmware) Read registers 10 and 11 from Modbus station 80 via the first aux port and store the result in var.modbusData`

#### M280: Set servo position {#m280_set_servo_position}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{no}}<sup>1</sup> | buddy={{no}} | repetier={{partial|Use M340}} | reprapfirmware={{yes|1.16+}} | smoothie={{no}} | bfb={{no}} | machinekit={{yes}} | redeem={{yes}} | mk4duo={{yes}} | yaskawa={{no}} }}
```
Set servo position absolute.

Parameters
:   `Pnnn` Servo index
:   `Snnn` Angle or microseconds
:   `I1` Invert polarity (RepRapFirmware only)

Example

`M280 P1 S50`

Marlin and RepRapFirmware treat `S` values below 200 as angles, and 200
or greater as the pulse width in microseconds.

In RepRapFirmware, the servo index is the same as the pin number for the
`M42` command. See
<https://duet3d.com/wiki/Using_servos_and_controlling_unused_I/O_pins>
for details.

RepRapFirmware supports the optional I1 parameter, which if present
causes the polarity of the servo pulses to be inverted compared to
normal for that output pin. The `I` parameter is not remembered between
`M280` commands (unlike the `I` parameter in `M106` commands), so if you
need inverted polarity then you must include I1 in every `M280` command
you send.

  P                                                 Name         Expansion Port Pin
  ------------------------------------------------- ------------ --------------------
  Use M307 H# A-1 C-1 D-1 before using these pins                
  3                                                 PC23_PWML6   21
  4                                                 PC22_PWML5   22
  5                                                 PC21_PWML4   23

  : Duet 0.8.5 M280 P value to Expansion Port Pin Mapping

On the Duet 0.6, pin 18 is controlled by heater 2. On the 0.8.5, pin 18
is controlled by heater 6, but is also shared with fan1. In order to use
this pin, the fan must be disabled (`M106 P1 I-1`). See [Using servos
and controlling unused I/O
pins](https://duet3d.com/wiki/Using_servos_and_controlling_unused_I/O_pins)

Notes

In Prusa Firmware this G-code is deactivated by default, must be turned
on in the source code.^1^

#### M281: Set Servo Angles {#m281_set_servo_angles}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|2.0}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{no}} | klipper={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
Set the angles for a servo\'s deployed (or selected) and stowed (or
unselected) states. To activate this command in Marlin enable the
`EDITABLE_SERVO_ANGLES` option.

Parameters
:   `P[index]` - Servo Index
:   `L[angle]` - Deployed / Selected Angle
:   `U[angle]` - Stowed / Unselected Angle

<!-- -->

Example

`M281 P0 L30 U90`

#### M282: Detach Servo {#m282_detach_servo}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|2.0.9.2}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{no}} | klipper={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
Detach servo. This disables the servo until its next move. To activate
this command in Marlin enable the `SERVO_DETACH_GCODE` option.

Parameters
:   `Pnnn` Servo index

Example

`M282 P1`

#### M290: Babystepping {#m290_babystepping}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|1.1.7+}} | prusa={{no}} | buddy={{yes}} | repetier={{yes}} | smoothie={{no}} | reprapfirmware={{yes|1.18+}} | bfb={{no}} | grbl={{no}} | machinekit={{no}} | makerbot={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters (RepRapFirmware)
:   `Snnn` Amount to baby step Z in mm. Positive values raise the head,
    negative values lower it.
:   `Xnnn, Ynnn, ...` Amount to baby step other axes in mm (optional,
    supported in later RepRapFirmware versions)
:   `Znnn` Synonym for S (RepRapFirmware 1.21 and later)
:   `Rn` (Optional, RepRapFirmware 1.21 and later) R1 = relative (add to
    any existing babystep amount, the default), R0 = absolute (set
    babystepping offset to the specified amount)

Examples

`M290 S0.05  ; babystep the head up 0.05mm`\
`M290 R0 S0  ; clear babystepping (RepRapFirmware 1.21 and later only)`

Parameters (Repetier)
:   `Znnn` Amount to baby step in mm. Positive values raise the head,
    negative values lower it.

Examples

`M290 S0.05  ; babystep the head up 0.05mm`

Additional Parameters (Marlin 1.1.7 and later)
:   `Xnnn` Amount to babystep X in current units. (Requires
    `BABYSTEP_XY`)
:   `Ynnn` Amount to babystep Y in current units. (Requires
    `BABYSTEP_XY`)
:   `Znnn` Amount to babystep Z in current units. Synonym for \'`S`\'
    parameter.

Example

`M290 X0.2 Z0.05 ; Babystep X by 0.2mm, Z by 0.05mm`

This command tells the printer to move the axis (or axes) transparently
to the motion system. This is like physically moving the axes by force,
but much nicer to the machine.

In RepRapFirmware `M290` with no parameters reports the accumulated baby
stepping offset. Marlin doesn\'t track accumulated babysteps.

In RepRapFirmware 1.19 and earlier, the babystepping offset is reset to
zero when the printer is homed or the bed is probed. In RepRapFirmware
1.21 and later, homing and bed probing don\'t reset babystepping, but
you can reset it explicitly using M290 R0 S0.

Note: If the `BABYSTEP_ZPROBE_OFFSET` option is used in Marlin, this
command also affects the Z probe offset (as set by `M851`) and that
offset *will* be saved to EEPROM.

#### M291: Display message and optionally wait for response {#m291_display_message_and_optionally_wait_for_response}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes|1.19+}} | bfb={{no}} | machinekit={{no}} | makerbot={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `P"message"` The message to display, which must be enclosed in
    double quotation marks. If the message itself contains a double
    quotation mark, use two double quotation marks to represent it.
:   `R"message"` Optional title for the message box. Must be enclosed in
    double quotation marks too.
:   `Sn` Message box mode (defaults to 1)
:   `Tn` Timeout in seconds, only legal for S=0 and S=1. The message
    will be cancelled after this amount of time, if the user does not
    cancel it before then. A zero or negative value means that the
    message does not time out (it may still be cancelled by the user if
    it has a Close button). In RepRapFirmware, the default timeout for
    messages that do not require acknowledgement is 10 seconds.
:   `Zn` 0 = no special action, 1 = display Z jog buttons alongside the
    message to allow the user to adjust the height of the print head

Examples

`M291 P"Please do something and press OK when done" S2`\
`M291 P"This message will be closed after 10 seconds" T10`

This command provides a more flexible alternative to M117, in particular
messages that time out, messages that suspend execution until the user
acknowledges them, and messages that allow the user to adjust the height
of the print head before acknowledging them.

Allowed message box modes include:

`0. No buttons are displayed (non-blocking)`\
`1. Only "Close" is displayed (non-blocking)`\
`2. Only "OK" is displayed (blocking, send M292 to resume the execution)`\
`3. "OK" and "Cancel" are displayed  (blocking, send M292 to resume the execution or M292 P1 to cancel the operation in progress)`

The combination S0 T0 is not permitted, because that would generate a
message box with no close button and that never times out, which would
lock up the user interface.

Duet Web Control 2.0.3 and later supports HTML in the message body.

#### M292: Acknowledge message {#m292_acknowledge_message}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes|1.19+}} | bfb={{no}} | machinekit={{no}} | makerbot={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `Pn` Whether the current operation shall be cancelled. Only legal if
    M291 was called with S=3 (optional)

This command is sent by the user interface when the user acknowledges a
message that was displayed because of a M291 command with parameter S=2
or S=3.

#### M293: Babystep Z+ {#m293_babystep_z}

```{=mediawiki}
{{Firmware Support | marlin={{yes|2.1.3}} | reprapfirmware={{no}} | klipper={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | druid={{no}} | mk4duo={{no}} | makerbot={{no}} | grbl={{no}} | sprinter={{no}} | bfb={{no}} | fived={{no}} | machinekit={{no}} | | redeem={{no}} | teacup={{no}} | yaskawa={{no}} }}
```
Babystep Z upward by one increment according to settings. Requires
`EP_BABYSTEPPING`. With \`EMERGENCY_PARSER\` babystepping is
asynchronous and doesn\'t rely on the queue.

#### M294: Babystep Z- {#m294_babystep_z_}

```{=mediawiki}
{{Firmware Support | marlin={{yes|2.1.3}} | reprapfirmware={{no}} | klipper={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | druid={{no}} | mk4duo={{no}} | makerbot={{no}} | grbl={{no}} | sprinter={{no}} | bfb={{no}} | fived={{no}} | machinekit={{no}} | | redeem={{no}} | teacup={{no}} | yaskawa={{no}} }}
```
Babystep Z downward by one increment according to settings. Requires
`EP_BABYSTEPPING`. With \`EMERGENCY_PARSER\` babystepping is
asynchronous and doesn\'t rely on the queue.

#### M300: Play beep sound {#m300_play_beep_sound}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{yes}}<sup>1</sup> | buddy={{yes}} | repetier={{yes}} | smoothie={{no}} | reprapfirmware={{yes}} | klipper={{partial|Needs macro}}<sup>2</sup> | bfb={{no}} | machinekit={{yes}} | makerbot={{yes}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   `Snnn` frequency in Hz
:   `Pnnn` duration in milliseconds
:   `Vnnn` volume in rage 0 - 1
:   `Cnnn` custom buzzer port (only in RRF 3.6 or later, must be
    PWM-capable)

Example

`M300 S300 P1000`

Play beep sound, use to notify important events like the end of
printing. [R2C2
electronics](R2C2_RepRap_Electronics "R2C2 electronics"){.wikilink}.

If an LCD device is attached to RepRapFirmware, a sound is played via
the add-on touch screen control panel. Else the web interface will play
a beep sound.

Notes

^1^In Prusa Firmware the defaults are 100Hz and 1000ms, so that `M300`
without parameters will beep for a second.

^2^Klipper does not support `M300` by default, however it can be easily
added as a [G-code
macro](https://github.com/KevinOConnor/klipper/blob/master/config/sample-macros.cfg)

#### M301: Set PID parameters {#m301_set_pid_parameters}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no|See M130-M133}} | sprinter={{yes}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | repetier={{yes}} | smoothie={{yes}} | reprapfirmware= {{yes}} | bfb={{no}} | machinekit={{no}} | redeem={{yes}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   `Hnnn` heater number (Smoothie uses \'S\', Redeem uses \'E\')
:   `Pnnn` proportional (Kp)
:   `Innn` integral (Ki)
:   `Dnnn` derivative (Kd)

Examples

`M301 H1 P1 I2 D3 ; Marlin, RepRapFirmware`\
`M301 S0 P30 I10 D10 ; Smoothie`\
`M301 E0 P30 I10 D10 ; Redeem (E = Extruder, -1=Bed, 0=E, 1=H, 2=A, 3=B, 4=C, default = 0)`

Sets Proportional (P), Integral (I) and Derivative (D) values for hot
end. See also [PID Tuning](PID_Tuning "PID Tuning"){.wikilink}.

##### MK4duo

H\[heaters\] H = 0-5 Hotend, H = -1 BED, H = -2 CHAMBER, H = -3 COOLER

##### Marlin

Hot end only; see `M304` for bed PID. H is the heater number, default 1
(i.e. first extruder heater).

##### RepRapFirmware 1.15 onwards {#reprapfirmware_1.15_onwards}

In RepRapFirmware 1.15 and later the M301 is supported as described
above, but it is not normally used. Instead the heater model is defined
by M307 or found by auto tuning, and the firmware calculates the PID
parameters from the model. An M301 command can be used in config.g after
the M307 command for that heater to override the firmware-computed PID
parameters.

##### RepRapFirmware 1.09 to 1.14 inclusive {#reprapfirmware_1.09_to_1.14_inclusive}

- `H` Is the heater number, and is compulsory. H0 is the bed, H1 is the
  first hot end, H2 the second etc.
- `P` Interprets a negative P term as indicating that bang-bang control
  should be used instead of PID (not recommended for the hot end, but OK
  for the bed heater).
- `I` Integral value
- `D` Derivative value
- `T` Is the approximate additional PWM (on a scale of 0 to 255) needed
  to maintain temperature, per degree C above room temperature. Used to
  preset the I-accumulator when switching from heater fully on/off to
  PID.
- `S` PWM scaling factor, to allow for variation in heater power and
  supply voltage. Is designed to allow a correction to be made for a
  change in heater power and/or power supply voltage without having to
  change all the other parameters. For example, an S factor of 0.8 means
  that the final output of the PID controller should be scaled to 0.8
  times the standard value, which would compensate for a heater that is
  25% more powerful than the standard one or a supply voltage that is
  12.5% higher than standard.
- `W` Wind-up. Sets the maximum value of I-term, must be high enough to
  reach 245C for ABS printing.
- `B` PID Band. Errors larger than this cause heater to be on or off.

An example using all of these would be:

`M301 H1 P20 I0.5 D100 T0.4 S1 W180 B30`

##### Smoothie

`S0` is 0 for the hotend, and 1 for the bed, other numbers may apply to
your configuration, depending on the order in which you declare
temperature control modules.

##### Other implementations {#other_implementations}

W: Wind-up. Sets the maximum value of I-term, so it does not overwhelm
other PID values, and the heater stays on. (Check firmware support -
Sprinter, Marlin?)

Example

`M301 W125`

##### Teacup

See `M130`, `M131`, `M132`, `M133` for
[Teacup](Teacup "Teacup"){.wikilink}\'s codes for setting the PID
parameters.

#### M302: Allow cold extrudes {#m302_allow_cold_extrudes}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | repetier={{yes|0.92+}} | smoothie={{no}} | reprapfirmware= {{yes}}<sup>1</sup> | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   `Snnn` Cold extrude minimum temperature (also in RepRapFirmware 2.02
    and later)
:   `Pnnn` Cold extrude allow state (RepRapFirmware)
:   `Rnnn` Cold retraction minimum temperature (RepRapFirmware 2.02 and
    later)

<!-- -->

Examples (RepRapFirmwre)

`M302       ; Report current state`\
`M302 P1    ; Allow cold extrusion`\
`M302 S120 R110 ; Allow extrusion starting from 120°C and retractions already from 110°C`

Examples (Others)

`M302 S0    ; Allow extrusion at any temperature`\
`M302 S170  ; Allow extrusion above 170`

This tells the printer to allow movement of the extruder motor above a
certain temperature, or if disabled, to allow extruder movement when the
hotend is below a safe printing temperature.

Notes

^1^RepRapFirmware uses the `P[0|1]` parameter instead of
`S[temperature]`, and for `M302` with no parameters it will report the
current cold extrusion state.

#### M303: Run PID tuning {#m303_run_pid_tuning}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{yes}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | repetier={{yes}} | smoothie={{yes}} | reprapfirmware={{yes|1.15+}} | bfb={{no}} | machinekit={{no}} | redeem={{yes}} | mk4duo={{yes}} | yaskawa={{no}} }}
```
[PID Tuning](PID_Tuning "PID Tuning"){.wikilink} refers to a control
algorithm used in some repraps to tune heating behavior for hot ends and
heated beds. This command generates Proportional (Kp), Integral (Ki),
and Derivative (Kd) values for the hotend or bed (E-1). Send the
appropriate code and wait for the output to update the firmware.

Hot end usage:

`M303 S``<temperature>`{=html}` C``<cycles>`{=html}

Bed usage (repetier, not sure whether cycles work here):

`M303 P1 S``<temperature>`{=html}

Bed usage (others):

`M303 E-1 C``<cycles>`{=html}` S``<temperature>`{=html}

Example

`M303 C8 S175`

Smoothie\'s syntax, where `E0` is the first temperature control module
(usually the hot end) and `E1` is the second temperature control module
(usually the bed):

`M303 E0 S190`

In RepRapFirmware, this command computes the process model parameters
(see `M307`), which are in turn used to calculate the PID constants. H
is the heater number, P is the PWM to use (default 0.5), and S is the
maximum allowable temperature (default 225). Tuning is performed
asynchronously. Run `M303` with no parameters to see the current tuning
state or the last tuning result.

Example

`M303 H1 P0.4 S240 ; tune heater 1 using 40% PWM, quit if temperature exceeds 240C`

Notes

In Marlin Firmware you can add the `U1` parameter to apply the PID
results to current settings upon completion.

#### M304: Set PID parameters - Bed {#m304_set_pid_parameters___bed}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | smoothie={{no|M301}} | reprapfirmware={{yes}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes|M301}} }}
```

Parameters
:   `Pnnn` proportional (Kp)
:   `Innn` integral (Ki)
:   `Dnnn` derivative (Kd)

Examples

`M304 P1 I2 D3 ; set kP=3, kI=2, kD=3`\
`M304 P1 I2 D3 T0.7 B20 W127 ; RepRapFirmware`\
`M304          ; Report parameters`

Sets Proportional, Integral and Derivative values for bed.
RepRapFirmware interprets a negative P term as indicating that bang-bang
control should be used instead of PID. In RepRapFirmware, this command
is identical to `M301` except that the `H` parameter (heater number)
defaults to zero.

See also [PID Tuning](PID_Tuning "PID Tuning"){.wikilink}.

##### M304 in RepRapPro version of Marlin: Set thermistor values {#m304_in_reprappro_version_of_marlin_set_thermistor_values}

In the RepRapPro version of Marlin (
<https://github.com/reprappro/Marlin> ) `M304` is used to set thermistor
values (as `M305` is in later firmwares). RRP Marlin calculates
temperatures on the fly, rather than using a temperature table. `M304`
Sets the parameters for temperature measurement.

Example

`M304 H1 B4200 R4800 T100000`

This tells the firmware that for heater 1 (`H` parameter: 0 = heated
bed, H = first extruder), the thermistor beta (`B` parameter) is 4200,
the thermistor series resistance (`R` parameter) is 4.8Kohms, the
thermistor 25C resistance (`T` parameter) is 100Kohms. All parameters
other than H are optional. If only the `H` parameter is given, the
currently-used values are displayed. They are also displayed within the
response to `M503`.

#### M305: Set thermistor and ADC parameters {#m305_set_thermistor_and_adc_parameters}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | smoothie={{yes}} | reprapfirmware={{yes}} | bfb={{no}} | grbl={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   `Pnnn` Heater number, or virtual heater number
:   `S"name"` Heater name (optional, RepRapFirmware only)
:   `Tnnn` (for thermistor sensors) Thermistor resistance at 25^o^C
:   `T"c"` (for MAX31856-based thermocouple sensors) The thermistor type
    letter, default K
:   `Bnnn` Beta value, or the reciprocal of the Steinhart-Hart
    thermistor model B coefficient
:   `Cnnn` Steinhart-Hart C coefficient (MK4duo and RepRapFirmware 1.17
    and later), default 0
:   `Rnnn` Series resistor value
:   `Lnnn` ADC low offset correction, default 0
:   `Hnnn` ADC high offset correction, default 0
:   `Xnnn` Heater ADC channel, or thermocouple or PT100 or current loop
    adapter channel, defaults to the same value as the `P` parameter
:   `Fnn` (where nn is 50 or 60) If the sensor interface uses a MAX31856
    thermocouple chip or MAX31865 PT100 chip, this is the local mains
    frequency. Readings will be timed to optimise rejection of
    interference at this frequency.

Example

`M305 P1 T100000 R1000 B4200`

Sets the parameters for temperature measurement. The example above tells
the firmware that for heater 1 (`P` parameter: 0 = heated bed, 1 = first
extruder) the thermistor 25C resistance (`T` parameter) is 100Kohms, the
thermistor series resistance (`R` parameter) is 1Kohms, the thermistor
beta (`B` parameter) is 4200. All parameters other than P are optional.
If only the `P` parameter is given, the existing values are displayed.

Example

`M305 P1 T100000 R1000 B4200 H14 L-11 X2`

The H correction affects the reading at high ADC input voltages, so it
has the greatest effect at low temperatures. The L correction affects
the reading at low input voltages, which correspond to high
temperatures.

The `X` parameter tells the firmware to use the thermistor input
corresponding to a different heating channel. RepRapFirmware also allow
an external SPI thermocouple interface (such as the MAX31855) or PT100
interface (MAX31865) to be configured. MAX31855 thermocouple channels
are numbered from 100, MAX31856 thermocouple channels are numbered from
150, PT100 channels from 200 and current loop channels from 300. Channel
1000 is the CPU temperature indication, 1001 is the temperature of the
hottest stepper motor driver on the main board, and 1001 is the
temperature of the hottest drivers on the expansion board.

In the above example, the ADC high end correction (`H` parameter) is 14,
the ADC low end correction (`L` parameter) is -11, and thermistor input
#2 is used to measure the temperature of heater #1.

#### M306: Set home offset calculated from toolhead position {#m306_set_home_offset_calculated_from_toolhead_position}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{yes}} | reprapfirmware={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Example

`M306 Z0`

The values specified are added to the calculated end stop position when
the axes are referenced. The calculated value is derived from the
distance of the toolhead from the current axis zero point.

The user would typically place the toolhead at the zero point of the
axis and issue the `M306` command.

This value can be saved to EEPROM using the `M500` command (as `M206`
value).

Implemented in Smoothieware

#### M307: Set or report heating process parameters {#m307_set_or_report_heating_process_parameters}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes|1.15+}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `Hn` Heater number (0 is usually the bed heater)
:   `Annn` gAin, expressed as ultimate temperature rise obtained in degC
    divided by the PWM fraction. For example, if G=180 then at 50% PWM
    the ultimate temperature rise would be 90C.
:   `Cnnn` dominant time Constant of the heating process in seconds
:   `Dnnn` Dead time in seconds

Four optional additional parameters help control the heating process:
:   `Fnnn` PWM frequency to use (not supported in RepRapFirmware 3, use
    M950 instead).
:   `Bn` selects Bang-bang control instead of PID if non-zero. Default
    at power-up is 0 for extruder heaters, 1 for bed and chamber
    heaters.
:   `Snnn` maximum PWM to be used used with this heater on a scale of 0
    to 1. Default 1.0.
:   `Vnnn` VIN supply voltage at which the A parameter was calibrated
    (RepRapFirmware 1.20 and later). This allows the PID controller to
    compensate for changes in supply voltage. A value of zero (the
    default) disables compensation for changes in supply voltage.

Examples

`M307 H0 ; report the process parameters for heater 0`\
`M307 H1 A346.2 C140 D5.3 B0 S0.8 V23.8 ; set process parameters for heater 1, use PID, and limit heater 1 PWM to 80%`

Each heater and its corresponding load may be approximated as a first
order process with dead time, which is characterised by the gain, time
constant and dead time parameters. The model can used to calculate
optimum PID parameters, using different values for the heating or
cooling phase and the steady state phase. It is also used to better
detect heater faults. In future it may be used to calculate feed-forward
terms to better respond to changes in the load. Normally these model
parameters are found by auto tuning - see `M303`.

RepRapFirmware 1.16 and later allow the PID controller for a heater to
be disabled by setting the `A`, `C`, and `D` parameters to -1. This
frees up the corresponding heater control pin for use as a general
purpose I/O pin to use with the M42 or M280 command. In RepRapFirmware
3, M950 should be used to free up the pin instead.

#### M308: Set or report sensor parameters {#m308_set_or_report_sensor_parameters}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes|3.0+}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Common Parameters
:   `Sn` Sensor number
:   `P"pin_name"` The name of the control board pin that this sensor
    uses. For thermistors it is the thermistor input pin name. For
    sensors connected to the SPI bus it is the name of the output pin
    used as the chip select.
:   `Y"sensor_type"` The sensor and interface type, e.g. \"thermistor\",
    \"pt1000\", \"rtdmax31865\", \"max31855\", \"max31856\",
    \"linear-analog\", \"dht22-temp\", \"dht22-humidity\",
    \"current-loop-pyro\"
:   `A"name"` Sensor name (optional), displayed in the web interface

Additional parameters for thermistors
:   `Tnnn` (for thermistor sensors) Thermistor resistance at 25^o^C
:   `Bnnn` Beta value, or the reciprocal of the Steinhart-Hart
    thermistor model B coefficient
:   `Cnnn` Steinhart-Hart C coefficient, default 0
:   `Rnnn` Series resistor value
:   `Lnnn` ADC low offset correction, default 0 (ignored if the hardware
    supports automatic ADC gain and offset calibration)
:   `Hnnn` ADC high offset correction, default 0 (ignored if the
    hardware supports automatic ADC gain and offset calibration)

Additional parameters for PT1000 sensors
:   `Rnnn` Series resistor value
:   `Lnnn` ADC low offset correction, default 0 (ignored if the hardware
    supports automatic ADC gain and offset calibration)
:   `Hnnn` ADC high offset correction, default 0 (ignored if the
    hardware supports automatic ADC gain and offset calibration)

Additional parameters for MAX31856-based thermocouple sensors
:   `T"c"` The thermistor type letter, default K
:   `Fnn` (where nn is 50 or 60) The local mains frequency. Readings
    will be timed to optimise rejection of interference at this
    frequency.

Additional parameters for MAX31865-based PT100 sensors
:   `Rnnn` Series resistor value
:   `Fnn` (where nn is 50 or 60) The local mains frequency. Readings
    will be timed to optimise rejection of interference at this
    frequency.

Additional parameters for linear analog sensors
:   `Fn` F0 = unfiltered (fast response), F1 = filtered (slower
    response, but noise reduced and ADC oversampling used to increase
    resolution)
:   `Lnnn` The temperature or other value when the ADC output is zero
:   `Hnnn` The temperature or other value when the ADC output is full
    scale

This code replaces M305 in RepRapFirmware 3. In earlier versions of
RepRapFirmware, sensors only existed in combination with heaters, which
necessitated the concept of a \"virtual heater\" to represent a sensor
with no associated heater (e.g. MCU temperature sensor). RepRapFirmware
3 allows sensors to be defined independently of heaters. The association
between heaters and sensors is defined using M950.

M308 can be used in the following ways:

`M308 Snn Y"type" P"pin" [other parameters] ; delete sensor nn if it exists, create a new one with default settings, and configure it using the other parameters`\
`M308 Snn ; report the settings of sensor nn`\
`M308 A"name" ; report the settings of the first sensor named "name"`\
`M308 Snn [any other parameters except Y] ; amend the settings of sensor nn`

Sensor type names obey the same rules as pin names, i.e. case is not
significant, neither are hyphen and underscore characters.

#### M309: Set or report heater feedforward {#m309_set_or_report_heater_feedforward}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes|3.4+}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   **Pn** Tool number
:   **Saaa:bbb:ccc\...** Feedforward coefficients. The number of
    coefficients provided must equal the number of heaters configured
    for the tool when it was created (see M563).

If the P parameter is not provided, the current tool is assumed. If the
S parameter is not provided, the existing coefficients are reported.

The units of **S** are PWM fraction (on a scale of 0 to 1) per mm/sec of
filament forward movement.

#### M310: Temperature model settings {#m310_temperature_model_settings}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{yes}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Usage
:   `M310` ; report values
:   `M310 [ A ]` ; autotune C+R values
:   `M310 [ F ]` ; force model self-test state
:   `M310 [ S ]` ; set 0=disable 1=enable
:   `M310 [ I ] [ R ]` ; set resistance at index
:   `M310 [ P | C ]` ; set power, capacitance
:   `M310 [ B | E | W ]` ; set beeper, warning and error threshold
:   `M310 [ T ]` ; set ambient temperature correction

<!-- -->

Parameters
:   `A` autotune C+R values
:   `F` force model self-test state (0=off 1=on) during autotune using
    current values
:   `Snnn` set 0=disable 1=enable
:   `Innn` resistance index position (0-15)
:   `Rnnn` resistance value at index (K/W; requires :`Innn`)
:   `Pnnn` power (W)
:   `Cnnn` capacitance (J/K)
:   `Bnnn` beep and warn when reaching warning threshold 0=disable
    1=enable (default: 1)
:   `Ennn` error threshold (K/s; default in variant)
:   `Wnnn`\' warning threshold (K/s; default in variant)
:   `Tnnn` ambient temperature correction (K; default in variant)

Prusa Firmware for MK3S/+, MK2.5/S only!

#### M320: Activate autolevel (Repetier) {#m320_activate_autolevel_repetier}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{yes}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Usage
:   `M320`
:   `M320 S1`

Parameters
:   `Snnn` if greater than 0, activate and store persistently in EEPROM

Examples

`M320    ; temporarily activate auto leveling`\
`M320 S1 ; permanently activate auto leveling`

Parameter `Snnn` is optional.

(Repetier only)

#### M321: Deactivate autolevel (Repetier) {#m321_deactivate_autolevel_repetier}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{yes}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Usage
:   `M321`
:   `M321 S1`

Parameters
:   `Snnn` if greater than 0, deactivate and store persistently in
    EEPROM

Examples

`M321    ; temporarily deactivate auto leveling`\
`M321 S1 ; permanently deactivate auto leveling`

Parameter `Snnn` is optional.

(Repetier only)

#### M322: Reset autolevel matrix (Repetier) {#m322_reset_autolevel_matrix_repetier}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{yes}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Usage
:   `M322`
:   `M322 S1`

Parameters
:   `Snnn` if greater than 0, also reset the matrix values saved EEPROM

Examples

`M322    ; temporarily reset auto level matrix`\
`M322 S1 ; permanently reset auto level matrix`

Parameter `Snnn` is optional.

(Repetier only)

#### M323: Distortion correction on/off (Repetier) {#m323_distortion_correction_onoff_repetier}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{yes}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Usage
:   `M323`
:   `M323 Snnn`
:   `M323 Snnn Pnnn`

Parameters
:   `Snnn` 0 (disable correction) or 1 (enable correction)
:   `Pnnn` 1 (store correction state persistently in EEPROM)

Examples

`M323       ; Show if distortion correction is enabled`\
`M323 S0    ; Disable distortion correction temporarily`\
`M323 S1 P1 ; Enable distortion correction permanently`

(Repetier only) Controls distortion correction feature after having set
it up using `G33.`

#### M340: Control the servos {#m340_control_the_servos}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{yes}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
(Repetier only ,Marlin see
[M280](Gcode#M280:_Set_servo_position "M280"){.wikilink})

M340 P`<servoId>`{=html} S`<pulseInUS>`{=html} / ServoID = 0..3
pulseInUs = 500..2500

Servos are controlled by a pulse width normally between 500 and 2500
with 1500ms in center position. 0 turns servo off.

#### M350: Set microstepping mode {#m350_set_microstepping_mode}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | druid={{no}} | repetier={{yes}} | reprapfirmware={{yes}} | smoothie={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{yes}} | mk4duo={{yes}} | yaskawa={{no}} }}
```
Sets microstepping mode.

Warning: Steps per unit remains unchanged; except that in RepRapFirmware
the steps/mm will be adjusted automatically.

Usage
:   `M350 Snn Xnn Ynn Znn Enn Bnn`

Parameters
:   *Not all parameters need to be used, but at least **one** should be
    used. As with other commands, RepRapFirmware reports the current
    settings if no parameters are used*.
:   `Snn` Set stepping mode for all drivers (not supported by
    RepRapFirmware)
:   `Xnn` Set stepping mode for the X axis
:   `Ynn` Set stepping mode for the Y axis
:   `Znn` Set stepping mode for the Z axis
:   `Enn` Set stepping mode for Extruder 0 (for RepRapFirmware use
    `Enn:nn:nn` etc. for multiple extruders)
:   `Bnn` Set stepping mode for Extruder 1 (not supported by
    RepRapFirmware, see above)
:   `Inn` Enable (nn=1) or disable (nn=0) microstep interpolation mode
    for the specified drivers, if they support it (RepRapFirmware only)

Modes (nn)
:   1 = full step
:   2 = half step
:   4 = quarter step
:   8 = 1/8 step
:   16 = 1/16 step
:   64 = 1/64 step
:   128 = 1/128 step
:   256 = 1/256 step

Examples

`M350 S16    ; reset all drivers to the default 1/16 micro-stepping - not supported by RepRapFirmware`\
`M350 Z1     ; set the Z-axis' driver to use full steps`\
`M350 E4 B4  ; set both extruders to use quarter steps - Marlin/Repetier`\
`M350 E4:4:4 ; set extruders 0-2 to use quarter steps - RepRapFirmware`

#### M351: Toggle MS1 MS2 pins directly {#m351_toggle_ms1_ms2_pins_directly}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Example

`M351`

#### M355: Turn case lights on/off {#m355_turn_case_lights_onoff}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no|use M106}} | sprinter={{no}} | marlin={{yes|1.1.0+}} | prusa={{no}} | buddy={{yes}} | druid={{no}} | repetier={{yes|0.92.2+}} | smoothie={{no}} | reprapfirmware={{no}} | bfb={{no}} | grbl={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Examples

`M355 S1 ; Enable lights`\
`M355 S0 ; Disable lights`\
`M355    ; Report status`\
`M355 P0 ; Turn light off`\
`M355 P128 ; Turn light on with half power`\
`M355 P255 ; Turn light on with full power`

Every call or change over LCD menu sends a state change for connected
hosting software like:

`Case lights on`\
`Case lights off`\
`No case lights`

#### M360: Report firmware configuration {#m360_report_firmware_configuration}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no|M503}} | prusa={{no|M503}} | buddy={{no|M503}} | repetier={{yes|0.92.2+}} | smoothie={{no}} | reprapfirmware={{no}} | bfb={{no}} | grbl={{no}} | machinekit={{no}} | redeem={{no}} | druid={{yes}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Target

This command helps hosting software to detect configuration details,
which the user would need to enter otherwise. It should reduce
configuration time considerably if supported.

Example

`M360`

Response:

<!-- -->

    Config:Baudrate:250000
    Config:InputBuffer:127
    Config:NumExtruder:2
    Config:MixingExtruder:0
    Config:HeatedBed:0
    Config:SDCard:1
    Config:Fan:1
    Config:LCD:1
    Config:SoftwarePowerSwitch:1
    Config:XHomeDir:-1
    Config:YHomeDir:-1
    Config:ZHomeDir:-1
    Config:SupportG10G11:1
    Config:SupportLocalFilamentchange:1
    Config:CaseLights:0
    Config:ZProbe:1
    Config:Autolevel:0
    Config:EEPROM:1
    Config:PrintlineCache:24
    Config:JerkXY:30.00
    Config:JerkZ:0.30
    Config:RetractionLength:3.00
    Config:RetractionLongLength:13.00
    Config:RetractionSpeed:40.00
    Config:RetractionZLift:0.00
    Config:RetractionUndoExtraLength:0.00
    Config:RetractionUndoExtraLongLength:0.00
    Config:RetractionUndoSpeed:0.00
    Config:XMin:0.00
    Config:YMin:0.00
    Config:ZMin:0.00
    Config:XMax:250.00
    Config:YMax:150.00
    Config:ZMax:90.00
    Config:XSize:250.00
    Config:YSize:150.00
    Config:ZSize:90.00
    Config:XPrintAccel:250.00
    Config:YPrintAccel:250.00
    Config:ZPrintAccel:100.00
    Config:XTravelAccel:250.00
    Config:YTravelAccel:250.00
    Config:ZTravelAccel:100.00
    Config:PrinterType:Cartesian
    Config:MaxBedTemp:120
    Config:Extr.1:Jerk:50.00
    Config:Extr.1:MaxSpeed:100.00
    Config:Extr.1:Acceleration:10000.00
    Config:Extr.1:Diameter:0.00
    Config:Extr.1:MaxTemp:220
    Config:Extr.2:Jerk:50.00
    Config:Extr.2:MaxSpeed:100.00
    Config:Extr.2:Acceleration:10000.00
    Config:Extr.2:Diameter:0.00
    Config:Extr.2:MaxTemp:220

#### SCARA calibration codes (Morgan) {#scara_calibration_codes_morgan}

In order to ease calibration of Reprap Morgan, the following M-codes are
used to set the machine up
`{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{partial}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | druid={{no}} | smoothie={{yes}} | reprapfirmware={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | mk4duo={{partial}} }}`{=mediawiki}

#### M360: Move to Theta 0 degree position {#m360_move_to_theta_0_degree_position}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{no}} | smoothie={{yes}} | reprapfirmware={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{experimental}} }}
```
The arms move into a position where the Theta steering arm is parallel
to the top platform edge. The user then calibrates the position by
moving the arms with the jog buttons in software like pronterface until
it is perfectly parallel. Using `M114` will then display the calibration
offset that can then be programmed into the unit using `M206` (Home
offset) X represents Theta.

Smoothieware: `M360 P0` will take the current position as parallel to
the platform edge, and store the offset in the homing trim offset (M666)
No further user interaction is needed.

#### M361: Move to Theta 90 degree position {#m361_move_to_theta_90_degree_position}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{no}} | smoothie={{yes}} | reprapfirmware={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{experimental}} }}
```
Theta move to 90 degrees with platform edge. User calibrates by using
jog arms to place exactly 90 degrees. Steps per degree can then be read
out by using `M114`, and programmed using `M92`. X represents Theta.
Program Y (Psi) to the same value initially. Remember to repeat `M360`
after adjusting steps per degree.

Smoothieware: `M360 P0` will accept the current position as 90deg to
platform edge. New steps per angle is calculated and entered into memory
(M92) No further user interaction is required, except to redo `M360`.

#### M362: Move to Psi 0 degree position {#m362_move_to_psi_0_degree_position}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{no}} | smoothie={{yes}} | reprapfirmware={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{experimental}} }}
```
Arms move to Psi 0 degree. Check only after other Theta calibrations

#### M363: Move to Psi 90 degree position {#m363_move_to_psi_90_degree_position}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{no}} | smoothie={{yes}} | reprapfirmware={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{experimental}} }}
```
Arms move to Psi 90 degree. Check only after other Theta calibrations

#### M364: Move to Psi + Theta 90 degree position {#m364_move_to_psi_theta_90_degree_position}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | druid={{no}} | smoothie={{yes}} | reprapfirmware={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{experimental}} }}
```
Move arms to form a 90 degree angle between the inner and outer Psi
arms. Calibrate by moving until angle is exactly 90 degree. Read out
with `M114`, and calibrate value into Home offset `M206`. Psi is
represented by Y.

Smoothieware: `M364 P0` will accept the current position as 90deg
between arms. The offset is stored as a trim offset (M666) and no
further user interaction is required except to save all changes via
`M500`.

#### M365: SCARA scaling factor {#m365_scara_scaling_factor}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{no}} | smoothie={{yes}} | reprapfirmware={{yes|Use M579}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{experimental}} }}
```
Adjust X Y and Z scaling by entering the factor. 100% scaling (default)
is represented by 1

#### M366: SCARA convert trim {#m366_scara_convert_trim}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{no}} | smoothie={{yes}} | reprapfirmware={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
Executing this command translates the calculated trim values of the
SCARA calibration to real home offsets. This prevents the home and trim
movement after calibration.

#### M370: Morgan manual bed level - clear map {#m370_morgan_manual_bed_level___clear_map}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{no}} | smoothie={{yes}} | reprapfirmware={{partial|Use M557}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
Clear the map and prepare for calibration

Usage
:   `M370`
:   `M370 X[divisions] Y[divisions]`

Without parameters is defaults to `X5 Y5` (25 calibration points) When
specifying parameters, uneven numbers are recommended.

#### M371: Move to next calibration position {#m371_move_to_next_calibration_position}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{no}} | smoothie={{yes}} | reprapfirmware={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
Move to the next position for calibration. User moves the bed towards
the hotend until it just touches

#### M372: Record calibration value, and move to next position {#m372_record_calibration_value_and_move_to_next_position}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{no}} | smoothie={{yes}} | reprapfirmware={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
The position of the bed is recorded and the machine moves to the next
position. Repeat until all positions programmed

#### M373: End bed level calibration mode {#m373_end_bed_level_calibration_mode}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{no}} | smoothie={{yes}} | reprapfirmware={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
End calibration mode and enable z correction matrix. Does not save
current matrix

#### M374: Save calibration grid {#m374_save_calibration_grid}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{no}} | smoothie={{yes}} | reprapfirmware={{yes|1.17+}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
Saves the calibration grid.

Parameters
:   `extension` (Smoothieware only) Extension of the grid file
:   `P"filename"` (RepRapFirmware only) Name of the file to save to
:   `Z` (Smoothieware only) Also save the `M206` Z homing offset into
    the grid file

Usage (Smoothieware)

`M374`\
`M374 ``<file extension>`{=html}` Z`

Usage (RepRapFirmware)

`M374`\
`M374 P"MyAlternateHeightMap.csv"`

In Smoothieware, without parameters this saves the grid into the default
grid file that gets loaded at boot. The optional parameter specifies the
extension of the grid file - useful for special grid files such as for a
special print surface like a removable print plate. Addition of Z will
additionally save the `M206 Z` homing offset into the grid file.

In RepRapFirmware, this saves the grid parameters and height map into
the specified file, or the default file `heightmap.csv` if no filename
was specified. To load the height map automatically at startup, use
command `M375` in the config.g file.

#### M375: Display matrix / Load Matrix {#m375_display_matrix_load_matrix}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{no}} | smoothie={{yes}} | reprapfirmware={{yes|1.17+}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
Displays the bed level calibration matrix (Marlin), or loads the grid
matrix file (Smoothieware and RepRapFirmware)

Parameters
:   `extension` (Smoothieware only)
:   `P"filename"` (RepRapFirmware only)

Usage

`M375`\
`M375 [file extension] ; (Smoothieware only)`\
`M375 P"MyAlternateHeightMap.csv" ; (RepRapFirmware only)`

Without parameters loads default grid, and with specified extension or
specified filename attempts to load the specified grid. If not available
will not modify the current grid. In Smoothieware, if Z was saved with
the grid file, it will load the saved Z with the grid.

#### M376: Set bed compensation taper {#m376_set_bed_compensation_taper}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no|M420Z}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{no}} | smoothie={{yes}} | reprapfirmware={{yes|1.17+}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `Hnnn` Height (mm) over which to taper off the bed compensation

Example

`M376 H10`

This command specifies that bed compensation should be tapered off over
the specified height, so that no bed compensation is applied at and
above that height. If H is zero or negative then no tapering is applied,
so compensation is performed throughout the entire print.

If the firmware does not adjust the extrusion amount to compensate for
the changing layer height while tapering is being applied, you will get
under- or over-extrusion. Using a large taper height will reduce this
effect. For example, if the taper height is 50 times the largest bed
height error, then under- or over-extrusion will be limited to 2%.

#### M380: Activate solenoid {#m380_activate_solenoid}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{no}} | buddy={{no}} | druid={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Example

`M380`

Activates solenoid on active extruder.

#### M381: Disable all solenoids {#m381_disable_all_solenoids}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{no}} | buddy={{no}} | druid={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Example

`M381`

#### M400: Wait for current moves to finish {#m400_wait_for_current_moves_to_finish}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no|use G4}} | sprinter={{yes}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | druid={{yes}} | repetier={{yes}} | reprapfirmware={{yes}} | klipper={{yes}} | smoothie={{yes}} | bfb={{no}} | machinekit={{yes}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Example

`M400`

Finishes all current moves and and thus clears the buffer. That\'s
identical to `G4 P0` for Teacup printers.

#### M401: Deploy Z Probe {#m401_deploy_z_probe}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{no}} | buddy={{no}} | druid={{no}} | reprapfirmware={{yes}} | smoothie={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   **P** Probe number, default 0 (RepRapFirmware)
:   **S** Set BLTouch HS Mode (Marlin 2.0.9.3+ with `BLTOUCH` enabled.)
:   **H** Report current BLTouch HS Mode (Marlin 2.0.9.4+ with `BLTOUCH`
    enabled.)

Example

`M401`\
`M401 P1`

Deploy the z-probe (if present). In RepRapFirmware this command runs the
macro file **sys/deployprobe#.g** (where \# is the probe number) if it
exists, otherwise it runs **sys/deployprobe.g** if it exists.

#### M402: Stow Z Probe {#m402_stow_z_probe}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{no}} | buddy={{no}} | druid={{no}} | reprapfirmware={{yes}} | smoothie={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   **P** (RepRapFirmware only) Probe number, default 0

Example

`M402`\
`M402 P1`

Raise z-probe if present. In RepRapFirmware this runs macro file
**sys/retractprobe#.g** (where \# is the probe number) if it exists,
otherwise **sys/retractprobe.g** if it exists.

#### M403: Set filament type (material) for particular extruder and notify the MMU {#m403_set_filament_type_material_for_particular_extruder_and_notify_the_mmu}

```{=mediawiki}
{{Firmware Support | marlin={{yes}} | druid={{no}} | prusa={{yes}} | buddy={{yes}} }}
```

Parameters
:   `E` Extruder number
:   `F` Filament type

Currently three different materials are needed (default, flex and PVA).

And storing this information for different load/unload profiles etc. in
the future firmware does not have to wait for \"ok\" from MMU.

#### M404: Filament diameter {#m404_filament_diameter}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   `Nnnn` Filament diameter (in mm)
:   `Dnnn` Nozzle diameter (in mm)^1^

Examples

`M404 N1.75`\
`M404 N3.0 D1.0`

Specifies the nominal filament diameter (typically 3mm or 1.75mm) or
displays the nominal filament diameter if no parameters are provided.

Notes

^1^While Marlin only accepts the \'N\' parameter, older versions of
RepRapFirmware allowed the nozzle diameter (in mm) to be specified via
the \'D \'parameter. This value was used to help detect the first layer
height when files are parsed. Newer version of RepRapFirmware ignore the
D parameter.

#### M405: Filament Sensor on {#m405_filament_sensor_on}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes|Use M591}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Example

`M405`

Turn on Filament Sensor extrusion control. Optional
D`<delay in cm>`{=html} to set delay in centimeters between sensor and
extruder.

#### M406: Filament Sensor off {#m406_filament_sensor_off}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{no}} | reprapfirmware={{yes|Use M591}} | smoothie={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Example

`M406`

Turn off Filament Sensor extrusion control.

#### M407: Display filament diameter {#m407_display_filament_diameter}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{yes}} | buddy={{no}} | druid={{no}} | repetier={{no}} | smoothie={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | reprapfirmware={{yes}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Example

`M407`

Displays measured filament diameter. In RepRapFirmware, `M407` does the
same as `M404`.

#### M408: Report JSON-style response {#m408_report_json_style_response}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{partial|Deprecated}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```
**This command is deprecated in RepRapFirmware 3.3 and later. Support
for it will be removed in a future release. Use M409 instead.**

Parameters
:   `Snnn` Response type
:   `Rnnn` Response sequence number

Example

`M408 S0`

Report a JSON-style response by specifying the desired type using the
\'S\' parameter. The following response types are supported:

- Type 0 is a short-form response, similar to the response used by older
  versions of the web interface.
- Type 1 is like type 0 except that static values are also included.
- Type 2 is similar to the response provided by the web server for Duet
  Web Control.
- Type 3 is an extended version of type 2 which includes some additional
  parameters that aren\'t expected to change very frequently.
- Type 4 is an extended version of type 2 which may be used to poll for
  current printer statistics.
- Type 5 reports the current machine configuration.

Here is an example of a typical type 0 response:

`{"status":"I","heaters":[25.0,29.0,28.3],"active":[-273.1,0.0,0.0],"standby":[-273.1,0.0,0.0],"hstat":[0,2,1],"pos":[-11.00,0.00,0.00],"extr":[0.0,0.0],`\
` "sfactor":100.00, "efactor":[100.00,100.00],"tool":1,"probe":"535","fanPercent":[75.0,0.0],"fanRPM":0,"homed":[0,0,0],"fraction_printed":0.572}`

The response is set as a single line with a newline character at the
end. The meaning of the fields is:

`status:  I=idle, P=printing from SD card, S=stopped (i.e. needs a reset), C=running config file (i.e starting up), A=paused, D=pausing, R=resuming from a pause, B=busy (e.g. running a macro), F=performing firmware update`\
`heaters: current heater temperatures, numbered as per the machine (typically, heater 0 is the bed)`\
`active:  active temperatures of the heaters`\
`standby: standby temperatures of the heaters`\
`hstat:   status of the heaters, 0=off, 1=standby, 2=active, 3=heater fault. Heater 0 is normally the bed heater, heaters 1, 2.. are the extruder heaters.`\
`pos:     the X, Y and Z (and U, V, W if present) axis positions of the current tool (if a tool is selected), or of the print head reference point if no tool is selected`\
`extr:    the positions of the extruders`\
`sfactor: the current speed factor (see ``M220`` command)`\
`efactor: the current extrusion factors (see ``M221`` command), one value per extruder`\
`tool:    the selected tool number. A negative number typically means no tool selected.`\
`probe:   the Z-probe reading`\
`fanPercent: the speeds of the controllable fans, in percent of maximum`\
`fanRPM:  the print cooling fan RPM`\
`homed:   the homed status of the X, Y and Z axes (and U, V, W if they exist), or towers on a delta. 0=axis has not been homed so position is not reliable, 1=axis has been homed so position is reliable.`\
`fraction_printed: the fraction of the file currently being printed that has been read and at least partially processed.`\
`message: the message to be displayed on the screen (only present if there is a message to display)`\
`timesLeft: an array of the estimated remaining print times (in seconds) calculated by different methods. These are currently based on the proportion of the file read,`\
`           the proportion of the total filament consumed, and the proportion of the total layers already printed. Only present if a print from SD card is in progress.`\
`seq:     the sequence number of the most recent non-trivial G-code response or error message. Only present if the ``R`` parameter was provided and the current sequence number is greater than that.`\
`resp:    the most recent non-trivial G-code response or error message. Only present if the ``R`` parameter was provided and the current sequence number is greater.`

The type 1 response comprises these fields plus some additional ones
that do not generally change and therefore do not need to be fetched as
often. The extra fields include:

`myName:  the name of the printer`\
`firmwareName: the name of the firmware, e.g. "RepRapFirmware", "Smoothieware" or "Repetier"`\
`geometry: one of "cartesian", "delta", "corexy, "corexz" etc.`\
`axes:    the number of axes`\
`volumes: the number of SD card slots available`\
`numTools:   the number of available tools numbered contiguously starting from 0`

The fields may be in any order in the response. Other implementations
may omit fields and/or add additional fields.

For a more detailed comparison of type 2 - 5, see
[RepRap_Firmware_Status_responses](RepRap_Firmware_Status_responses "RepRap_Firmware_Status_responses"){.wikilink}.

PanelDue currently uses only `M408 S0` and `M408 S1`.

#### M409: Query object model {#m409_query_object_model}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes|3.01 and later}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `K"key"` Key string, default empty
:   `F"flags"` Flags string, default empty
:   `Rnnn` Pass through request to RepRapFirmware (only for SBC mode,
    v3.5.2 or later)
:   `Innn` Increment sequence number of the given key (reserved for
    internal usage ONLY)

Examples

`M409 K"move.axes" F"f"     ; report all frequently-changing properties of all axes`\
`M409 K"move.axes[0] F"v"   ; report all properties of the first axis, including values not normally reported`\
`M409 K"move.axes[].homed"  ; for all axes, report whether it is homed`\
`M409 K"#move.axes"         ; report the number of axes`\
`M408 F"f"                  ; report all values that are likely to have changed recently`\
`M409 F"v"                  ; report the entire object model (caution, this may be very large!)`

The key string is just the path to the Object Model (OM) variables
wanted, with the following extensions:

- An element that is an array may be followed by either \[*number*\] to
  select just one element, or by \[\] to select all elements and report
  the results as an array
- The path may be preceded by \# in which case the path must refer to an
  array and just the number of array elements is returned

An empty key string selects the entire object model.

The flags string may include one or more of the following:

`d#: (depth) return the OM to depth d# where # is a sequence of digits. The default depth is 1 if the key is empty or not provided (because the returned object would be very large, perhaps too large to send), otherwise a large value (larger than the maximum depth of anything in the OM).`\
`f: (frequent) return only those values in the object model that typically change frequently during a job. User interfaces can use M409 with this flag to stay up to date.`\
`n: (null) include fields with null values (null fields are normally omitted, but null array elements are never omitted) `\
`v: (verbose) include values that are rarely needed and not normally returned (e.g. controller electronics and firmware limits)`

The response is a JSON object of the following form:

{\"key\":\"*key*\",\"flag\'\":\"*flags*\",\"result\":*object-value*}

The key and flags fields are as provided in the M409 command. If the key
string is malformed or refers to a property that does not exist in the
object model, the result field is **null**.

RepRapFirmware on network-enabled electronics also provides the same
functionality via the rr_model call to the HTTP API.

#### M410: Quick-Stop {#m410_quick_stop}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|1.1.0-RC2+}} | prusa={{no}} | buddy={{yes}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes|Use M112}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```
This command does a quick stop of all stepper motors and aborts all
moves in the planner. This command is only intended for emergency
situations, and due to the instant stop the actual stepper positions may
be shifted. Note that if \`EMERGENCY_PARSER\` is disabled, the response
may be delayed while the command buffer is being queued. If a print job
is in progress, it will continue, so it is important to suspend the
print job before using this command.

#### M412: Disable Filament Runout Detection {#m412_disable_filament_runout_detection}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|2.0+}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes|Use M591}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
Enable or disable filament runout detection. When filament sensors are
enabled, the firmware responds to a filament runout by running the
configured G-code (usually `M600` Filament Change). When filament runout
detection is disabled, no action will be taken on filament runout.

Usage: `M412 S[on|off]`

If no \'S\' parameter is given, this command reports the current state
of filament runout detection.

Examples
:   `M412 S1` *Enable filament runout detection*
:   `M412 S0` *Disable filament runout detection*
:   `M412` *Report the current filament runout detection state*

#### M413: Power-Loss Recovery {#m413_power_loss_recovery}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|2.0+}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes|Use M911}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
Enable or disable the **Power-loss Recovery** feature. When this feature
is enabled, the state of the current print job (SD card only) will be
saved to a file on the SD card. If the machine crashes or a power outage
occurs, the firmware will present an option to Resume the interrupted
print job. In Marlin 2.0 the `POWER_LOSS_RECOVERY` option must be
enabled.

This feature operates without a power-loss detection circuit by writing
to the recovery file periodically (e.g., once per layer), or if a
`POWER_LOSS_PIN` is configured then it will write the recovery info only
when a power-loss is detected. The latter option is preferred, since
constant writing to the SD card can shorten its life, and the print will
be resumed where it was interrupted rather than repeating the last
layer. (Future implementations may allow use of the EEPROM or the
on-board SD card.)

Usage: `M413 S[on|off]`

If no \'S\' parameter is given, this command reports the current state
of Power-loss Recovery.

Examples
:   `M413 S1` *Enable power-loss recovery*
:   `M413 S0` *Disable power-loss recovery*
:   `M413` *Report the current power-loss recovery state*

#### M415: Host Rescue {#m415_host_rescue}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{yes}} | smoothie={{no}} | reprapfirmware={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
The host rescue G-code is essential to enabling host software to recover
from a lost connection or power loss. With this solution the firmware
stores the last received coordinate and current position in EEPROM. Once
the host reconnects, the firmware reports this recovery information.
From the last-received coordinate the host can determine the last line
that was processed. Firmware should move the extruder to a parking
position if commands stop arriving during an active print job (with
heaters still on). Once the host starts sending new commands the
firmware should restore the last position. Host and firmware developers
can work together to optimize this solution.

If the firmware supports this solution it should announce it with the
capability: [`Cap:HOST_RESCUE:1`](Cap:HOST_RESCUE:1)

Examples\
`M415 S1` *Enable host rescue system*\
`M415 S0` *Disable host rescue system*\
`M415 Z[zpos]` *Set Z position as if homed*\
`M415` *Report rescue state*

Every call to M415 reports the state. Answers are

RESCUE_STATE: OFF

Nothing stored. Print finished.

RESCUE_STATE: LX:121.97 LY:143.33 LZ:3.30 LE:1.84 LT:0 X:0.00 Y:240.00
Z:13.30 E:1.84

Print was interrupted. Coordinates with leading L are last received
positions, LT is active extruder. Normal coordinates are current
position and can be omitted, if the move did not finish due to power
loss.

On a power loss the firmware should respond with `POWERLOSS_DETECTED` as
early as possible to give host time to flush log as it is likely host
will also go down very soon.

Support is available in Repetier-Firmware 1.0.4 or higher.
Repetier-Server 0.91.0 is the first to use this concept and can be used
to validate implementation.

#### M416: Power loss {#m416_power_loss}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{yes}} | smoothie={{no}} | reprapfirmware={{no}} | bfb={{no}} | machinekit={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
Host tells firmware that it will loose power. This is the solution in
case a connected host has a power loss detection and firmware does not.
Firmware should return the message `POWERLOSS_DETECTED` and do whatever
firmware is supposed to do in that case. In combination with host rescue
it should store positions, disable heaters, go to park position.

#### M420: Firmware dependent {#m420_firmware_dependent}

##### M420: Set RGB Colors as PWM (MachineKit) {#m420_set_rgb_colors_as_pwm_machinekit}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{yes}} | mk4duo={{no}} | yaskawa={{no}} }}
```
Usage:
`M420 R[Red PWM (0-255)] E[Green PWM (0-255)] B[Blue PWM (0-255)]`

Example

`M420 R255 E255 B255`

Set the color of your RGB LEDs that are connected to PWM-enabled pins.
Note, the Green color is controlled by the `E` value instead of the G
value due to the G code being a primary code that cannot be overridden.

In Marlin `M420` is Enable/Disable Mesh Leveling (with current values)
S1=enable S0=disable

##### M420: Leveling On/Off/Fade (Marlin) {#m420_leveling_onofffade_marlin}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | druid={{no}} | repetier={{no}} | reprapfirmware={{yes|Use G29 and M376}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```
Enable/Disable Bed Leveling (using the current stored grid or mesh).

Usage
:   `M420 S[bool] Z[float]`

<!-- -->

Examples

`M420 S1  ; Enable compensation using current grid/mesh`\
`M420 Z10 ; Gradually reduce compensation until Z=10`

Marlin 1.1.0 adds the `Z` parameter to set the \"fade\" height. This
requires the `ENABLE_LEVELING_FADE_HEIGHT` option.

When the `Z` fade height value is set non-zero, bed compensation will
gradually reduce up to the given height, and cease completely above that
height.

##### M420: Mesh bed leveling status {#m420_mesh_bed_leveling_status}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{yes}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | klipper={{no}} | bfb={{no}} | grbl={{no}} | machinekit={{no}} | makerbot={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
Prints mesh bed leveling status and bed profile if activated.

Usage
:   `M420`

Equivalent to `G81`

#### M421: Set a Mesh Bed Leveling Z coordinate {#m421_set_a_mesh_bed_leveling_z_coordinate}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} |  makerbot={{no}} | grbl={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
Set a single Z coordinate in the Mesh, Bilinear or UBL Leveling grid.
Requires `MESH_BED_LEVELING` or `AUTO_BED_LEVELING_BILINEAR` or
`AUTO_BED_LEVELING_UBL`.

I & J are the index for the X and Y axis respectively.

Usage
:   `M421 I[index] J[index] Z[float]` to set an absolute value to a mesh
    point

or

:   `M421 I[index] J[index] Q[float]` to offset a mesh point by a
    specified value

#### M422: Set a G34 Point {#m422_set_a_g34_point}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|2.0.4+}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{no}} | smoothie={{no}} | klipper={{no}} | reprapfirmware={{no}} | bfb={{no}} | machinekit={{no}} | makerbot={{no}} | grbl={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
Set a single XY coordinate to be used by `G34` for Z Stepper Alignment.

Usage
:   `M422 S[index] X[pos] Y[pos]`

#### M423: X-Axis Twist Compensation {#m423_x_axis_twist_compensation}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|2.0.9.4+}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{no}} | smoothie={{no}} | klipper={{no}} | reprapfirmware={{no}} | bfb={{no}} | machinekit={{no}} | makerbot={{no}} | grbl={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
Reset, set, or report X-Axis Twist Compensation data that will be used
by subsequent `G29` commands to compensate for a twisted X-axis.

Parameters
:   `R` Flag to reset the X-twist data to configured defaults.
:   `X[index]` Zero-based index into the X-twist data array. (`Z` is
    also required)
:   `Z[offset]` An offset value to set. (`X` is also required)
:   `A[start]` Set the starting X position.
:   `I[spacing]` Set the X spacing distance.

<!-- -->

Usage
:   `M423` to report the current X-twist data to the host console.
:   `M423 R` to reset X-twist data to the configured defaults.
:   `M423 X[index] Z[offset]` to set an offset value.
:   `M423 A[start] I[spacing]` to set the X-start position and X-spacing
    distance.

#### M424: Global Z Offset {#m424_global_z_offset}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|2.1.2+}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{no}} | smoothie={{no}} | klipper={{no}} | reprapfirmware={{no}} | bfb={{no}} | machinekit={{no}} | makerbot={{no}} | grbl={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
Set or report the global Z offset for the leveling mesh. The command
`G29` will set this automatically to an average mesh value to allow for
\"leveling fade\" with a biased mesh. In Marlin this feature requires
the `GLOBAL_MESH_Z_OFFSET` option.

Parameters
:   `Z` New global offset value to apply.

<!-- -->

Usage
:   `M424` to report the current global mesh Z offset.
:   `M424 Z[offset]` to set the global mesh Z offset.

#### M425: Backlash Correction {#m425_backlash_correction}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|2.0.0+}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware= {{Yes|3.5.0+}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `Fnnn` Enable/disable/fade-out backlash correction (0.0 = none to
    1.0 = 100%)
:   `Snnn` Distance over which backlash correction is spread^1^ (mm)
:   `Xnnn` Set the backlash distance on X (mm; 0 to disable)
:   `Ynnn` Set the backlash distance on Y (mm; 0 to disable)
:   `Znnn` Set the backlash distance on Z (mm; 0 to disable)
:   `X` Use measured value for backlash on X (if available)
:   `Y` Use measured value for backlash on Y (if available)
:   `Z` Use measured value for backlash on Z (if available)

<!-- -->

Examples (Marlin)

`M425                ; Report current state`\
`M425 Z              ; Use measured value of backlash on Z`\
`M425 F1 S3          ; Full backlash compensation while smoothing over 3mm.`\
`M425 F0.5 S0.0      ; Compensate for 50% of the backlash with no smoothing`\
`M425 X0.1 Y0.2 Z0.3 ; Set backlash to specific values for all axis`

Notes

^1^ In Marlin, backlash compensation works by adding extra steps to one
or more segments after a motor direction reversal. With smoothing off,
this can cause blemishes on the print. Enabling smoothing will cause
those extra steps to be spread over multiple segments, minimizing
artifacts.

#### M450: Report Printer Mode {#m450_report_printer_mode}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{yes}} | reprapfirmware={{yes|1.20+}} | smoothie={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Usage
:   `M450`

<!-- -->

Example

`> M450`\
`> PrinterMode:FFF`

Printers can be used for different task by exchanging the toolhead.
Depending on the tool, a different behavior of some commands can be
expected. This command reports the current working mode. Possible
answers are:

:   PrinterMode:FFF
:   PrinterMode:Laser
:   PrinterMode:CNC

#### M451: Select FFF Printer Mode {#m451_select_fff_printer_mode}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{yes}} | reprapfirmware={{yes|1.20+}} | smoothie={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Usage
:   `M451`

<!-- -->

Example

`> M451`\
`> PrinterMode:FFF`

Switches to FFF mode for filament printing.

#### M452: Select Laser Printer Mode {#m452_select_laser_printer_mode}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{yes}} | reprapfirmware={{yes|1.20+}} | smoothie={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Usage
:   `M452`

<!-- -->

Example

`> M452`\
`> PrinterMode:Laser`

Switches to laser mode. This mode enables handling of a laser pin and
makes sure that the laser is only activated during `G1` moves if laser
was enabled or E is increasing. `G0` moves should never enable the
laser. `M3`/`M5` can be used to enable/disable the laser for moves.

#### M453: Select CNC Printer Mode {#m453_select_cnc_printer_mode}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{yes}} | reprapfirmware={{yes|1.20+}} | smoothie={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Usage
:   `M453`

<!-- -->

Parameters (RepRapFirmware only)

- **Snnn** (optional) Spindle index, defaults to 0. Duet 2 supports 4
  spindles max
- **Pfff:rrr** Logical pin numbers used to drive the spindle motor in
  clockwise and counterclockwise directions. Omit the \":rrr\" part if
  the spindle turns clockwise only.
- **I**n Invert (I1) or don\'t invert (I0, default) the output polarity
- **Rnnn** Spindle RPM that is achieved at full PWM. Used to convert the
  S parameter in M3 and M4 commands to a PWM value.
- **Fnnn** (optional) The PWM frequency to use
- **Tnnn** (optional) Assign spindle to a tool allowing better control
  in DWC

Example

`> M453`\
`> PrinterMode:CNC`

Switches to CNC mode. In this mode `M3`/`M4`/`M5` control the pins
defined for the milling device.

Notes for RepRapFirmware: By default, no output is assigned to the
spindle motor. Logical pin numbers for the P parameters are as defined
for the M42 and M208 commands. If you wish to assign a heater or fan
output to control the spindle motor as in the above example, you must
first disable the corresponding heater (see M307) or fan (see M106).

#### M460: Define temperature range for thermistor-controlled fan {#m460_define_temperature_range_for_thermistor_controlled_fan}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{yes}} | reprapfirmware={{yes|Use M106}} | smoothie={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Usage
:   `M460 X[minTemp] Y[maxTemp]`

<!-- -->

Example

`M460 X50 Y60`

If the firmware has a thermistor controlled fan defined, you can set at
which temperature the fan starts and from which temperature on it should
run with maximum speed.

#### M470: Create Directory on SD-Card {#m470_create_directory_on_sd_card}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{no}} | reprapfirmware={{yes|2.03}} | smoothie={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `P"name"` Name of directory to create

<!-- -->

Usage
:   `M470 P"directory/to/create"`

<!-- -->

Example

`M470 P"/sys/config.d"`

This will create a new directory on the SD-Card. If not otherwise
specified the default root should be the first/internal SD-Card.

#### M471: Rename File/Directory on SD-Card {#m471_rename_filedirectory_on_sd_card}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{no}} | reprapfirmware={{yes}}:2.03 and later | smoothie={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `S"name"` Name of existing file/directory
:   `T"name"` New name of file/directory
:   `Dnnn` Setting this to 1 will delete an existing file that matches
    the T parameter value

<!-- -->

Usage
:   `M471 S"source/name" T"dest/name" D1`

<!-- -->

Example

`M471 S"/sys/config-override.g" T"/sys/config-override.g.bak"`

Rename or move a file or directory. Using the D parameter can delete a
file with the target name. Renaming or moving across directories is
possible though not from one SD-Card to another.

#### M472: Delete File/Directory on SD-Card {#m472_delete_filedirectory_on_sd_card}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{no}} | reprapfirmware={{yes}}:3.5 and later | smoothie={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `P"name"` Name of file/directory to delete
:   `Rn` (optional) R1 = recursive delete

<!-- -->

Example

`M472 P"/gcodes/old_files" R1`

If the R1 parameter is provided and the P parameter is a directory, then
files will be deleted recursively i.e. all contained files and
directories will be deleted too. Otherwise, if \"name\" refers to a
non-empty directory then deletion will fail.

See also M30.

#### M486: Cancel Object {#m486_cancel_object}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{no}} | buddy={{yes}} | repetier={{no}} | druid={{no}} | reprapfirmware={{yes|3.01 and later}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} | makerbot={{no}} | grbl={{no}} }}
```
The `M486` G-code provides an interface to identify objects on the print
bed and cancel them. Basic usage: Use `M486 T` to tell the firmware how
many objects there are, so it can provide an LCD interface. (Otherwise
the firmware counts them up in the first layer.) In every layer of your
G-code, you must preface each object\'s layer slice with `M486 S[index]`
to indicate which object is being printed. The index should be
zero-based. To cancel the first object, use `M486 P0`; to cancel the 5th
object use `M486 P4`; and so on. The \"current\" object is canceled with
`M486 C`.

G-codes associated with the canceled objects are no longer printed.
Firmware supports this feature by ignoring G0-G3/G5 moves in XYZ while
updating F and keeping the E coordinate up-to-date without extruding.

Slicers should number purge towers and other global features with a
negative index (or other flag) to distinguish them from regular print
objects, since it is important to preserve color changes, purge towers,
and brims.

Host software (such as OctoPrint) may be able to cancel individual
objects through a plugin, and in this case they should not use M486 P to
cancel objects (although doing so should cause no harm).

Usage

`M486 T12               ; Total of 12 objects (otherwise the firmware must count)`\
`M486 S3                ; Indicate that the 4th object is starting now`\
`M486 S3 A"cube copy 3" ; Indicate that the 4th object is starting now and name it (RepRapFirmware)`\
`M486 S-1               ; Indicate a non-object, purge tower, or other global feature`\
`M486 P10               ; Cancel object with index 10 (the 11th object)`\
`M486 U2                ; Un-cancel object with index 2 (the 3rd object)`\
`M486 C                 ; Cancel the current object (use with care!)`\
`M486                   ; List the objects on the build plate (RepRapFirmware)`

M486 implementation in RepRapFirmware:
:   If the GCode file being printed contains object label comments (e.g.
    using the \"Label objects\" option in PrusaSlicer) then it is not
    necessary to use M486 S commands to indicate which object is being
    printed. Objects on the build plate will be numbered from 0 in the
    order in which their labels first appear in the file.
:   If you do use M486 S commands in the GCode file instead of object
    label comments, then RepRapFirmware provides an optional A parameter
    to the M486 S command to allow objects to be named. The name of each
    object need only be specified once.
:   M486 without parameters lists the names and approximate locations of
    known objects on the build plate. For the benefit of user
    interfaces, this information may also be retrieved from the object
    model using the M409 command or using the rr_model HTTP API.

#### M493: Fixed-Time Motion Control {#m493_fixed_time_motion_control}

```{=mediawiki}
{{Firmware Support | marlin={{yes|2.1.3}} | reprapfirmware={{no}} | klipper={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | druid={{no}} | mk4duo={{no}} | makerbot={{no}} | grbl={{no}} | sprinter={{no}} | bfb={{no}} | fived={{no}} | machinekit={{no}} | | redeem={{no}} | teacup={{no}} | yaskawa={{no}} }}
```
Use `M493` to enable/disable and set parameters for Fixed-Time Motion
Control (by Ulendo). Requires the `FT_MOTION` feature to be enabled.
Fixed-Time Motion Control supersedes normal motion control when enabled,
and can only be applied to Cartesian and Core motion systems. This is
likely to change in future versions. This motion system implements its
own Linear (Pressure) Advance and Input Shaping, but does not include
proprietary Fast B-Spline (FBS) acceleration. Due to its overhead and
memory requirements (around 11 kilobytes), it requires a fast board with
plenty of RAM.

Parameters

`S``<mode>`{=html}` Set the motion / shaping mode. Shaping requires an X axis, at the minimum.`\
`   0: NORMAL`\
`   1: FIXED-TIME`\
`  10: ZV`\
`  11: ZVD`\
`  12: EI`\
`  13: 2HEI`\
`  14: 3HEI`\
`  15: MZV`

`P``<bool>`{=html}` Enable (1) or Disable (0) Linear Advance pressure control`\
`K``<gain>`{=html}` Set Linear Advance gain`

`D``<mode>`{=html}` Set Dynamic Frequency mode`\
`   0: DISABLED`\
`   1: Z-based (Requires a Z axis)`\
`   2: Mass-based (Requires X and E axes)`

`A``<Hz>`{=html}` Set static/base frequency for the X axis`\
`F``<Hz>`{=html}` Set frequency scaling for the X axis`\
`B``<Hz>`{=html}` Set static/base frequency for the Y axis`\
`H``<Hz>`{=html}` Set frequency scaling for the Y axis`

#### M500: Store parameters in non-volatile storage {#m500_store_parameters_in_non_volatile_storage}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{yes}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | druid={{yes}} | repetier={{yes}} | smoothie={{yes}} | reprapfirmware={{yes}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Example

`M500`

Save current parameters to EEPROM, SD card, Flash memory or other
non-volatile storage.

In [Redeem](Redeem "Redeem"){.wikilink} any parameters set through
G/M-codes which is different than what is read from the config files,
are stored back to the local config. For instance setting stepper
current and microstepping through `M906` and `M907` followed by `M500`
will update /etc/redeem/local.cfg.

In [Druid Firmware](Druid_Firmware "Druid Firmware"){.wikilink}, because
of the small size for parameter storage (512 bytes), a 128K flash memory
sector is used as permanent storage. The sector can be partially written
256 times (512 bytes per backup) before requiring a complete sector
wipe, to restart the same process again. (That was 1 write cycle). The
flash memory minimum write cycles guaranteed for the STM32F407 MCU by ST
Microelectronics are 10000, yielding a total of 2.56 million times,
parameters can be saved.

Also with [Druid Firmware](Druid_Firmware "Druid Firmware"){.wikilink},
you no longer have to worry about saving your newly modified settings.
Druid firmware save them in a temporary file as you make them. At every
Boot, it loads the settings from the FLASH memory block, and also read
the temp file and apply the previously modified settings to the RAM,
seamlessly. When the size of the temporary file is above the limit set
by the users, or when using `M500`, Druid Firmware merge theses changes
and write all settings to the next 512 byte block in the flash, and
delete the temporary file.

In [Druid Firmware](Druid_Firmware "Druid Firmware"){.wikilink}, users
will only have to use `M500`, to immediately force the merging of the
temporary file with the current settings, in which, all changed
parameters are saved, before the file limit size is reached (as
explained in previous paragraph)

#### M501: Read parameters from EEPROM {#m501_read_parameters_from_eeprom}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{yes}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | druid={{yes}} | repetier={{yes}} | reprapfirmware={{yes}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   `Snnn` Enable auto-save (only RepRapFirmware)

<!-- -->

Example

`M501`

Set the active parameters to those stored in the EEPROM, SD card or
other non-volatile storage. This is useful to revert parameters after
experimenting with them.

RepRapFirmware versions prior to 1.17 allows \"S1\" to be passed, which
forces parameters to be automatically saved to EEPROM when they are
changed.

In RepRapFirmware 1.17 and later, the parameters are saved in file
sys/config-override.g on the SD card.

#### M502: Restore Default Settings {#m502_restore_default_settings}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{yes}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | repetier={{yes}} | reprapfirmware={{yes}} | bfb={{no}} | machinekit={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Example

`M502`

This command resets all tunable parameters to their default values, as
set in the firmware\'s configuration files. This doesn\'t reset any
parameters stored in the EEPROM, so it must be followed with `M500` to
reboot with default settings.

#### M503: Report Current Settings {#m503_report_current_settings}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{yes}} | marlin={{yes}} | prusa={{yes}} | buddy={{yes}} | druid={{yes}} | 
 reprapfirmware={{yes}} | bfb={{no}} | grbl={{no}} | machinekit={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Examples

`M503 ; Output current settings`\
`M503 S0 ; Settings as G-code only (Marlin 1.1)`

This command asks the firmware to reply with the current print settings
as set in memory. Settings will differ from EEPROM contents if changed
since the last load / save. The reply output includes the G-Code
commands to produce each setting. For example, Steps-Per-Unit values are
displayed as an `M92` command.

RepRapFirmware outputs the content of the configuration file, but note
that it may be truncated if it is too long.

#### M504: Validate EEPROM {#m504_validate_eeprom}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|1.1.9+}} | prusa={{no}} | buddy={{yes}} | repetier={{no}} | reprapfirmware={{no|Not needed}} | smoothie={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Examples

`M504 ; Check EEPROM`

This command checks the contents of EEPROM for correct version, size,
and checksum and reports the result.

#### M505: Firmware dependent {#m505_firmware_dependent}

##### M505: Clear EEPROM and RESET Printer {#m505_clear_eeprom_and_reset_printer}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} |  makerbot={{no}} | grbl={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```
This command erase all EEPROM and reset the board.

##### M505: Set configuration file folder {#m505_set_configuration_file_folder}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{no}} | reprapfirmware={{yes|2.03}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} |  makerbot={{no}} | grbl={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   **P\"name\"** ; name of folder, default path is */sys/* if it is a
    relative path

Example
:   **M505 P\"experimental\"** ; change config file path from */sys/* to
    */sys/experimental/*

Following this command, files that would normally be fetched from /sys/
(for example, homing files and system macro files in RepRapFirmware) are
fetched from the specified folder instead. Any such files that are
already being executed will continue to run.

This command can be used to allow multiple configurations to be
maintained easily. In RepRapFirmware the file */sys/config/g* can
contain just these two lines:

`M505 P"config1"`\
`M98 P"config.g"`

The first line changes the config file folder to */sys/config1* and the
second one executes file *config.g* in that folder. To select an
alternative configuration, only the first line needs to be edited.

##### M505: Set a named EEPROM value {#m505_set_a_named_eeprom_value}

```{=mediawiki}
{{Firmware Support | marlin={{no}} | reprapfirmware={{no}} | klipper={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | druid={{no}} | mk4duo={{no}} | makerbot={{no}} | grbl={{no}} | sprinter={{no}} | bfb={{no}} | fived={{no}} | machinekit={{no}} | | redeem={{no}} | teacup={{no}} | yaskawa={{no}} }}
```
Use `M505 varname value` to directly set and store a named variable and
value to EEPROM. The variable name can be up to 31 characters in length
and the value can be up to 63 characters. Be careful with this G-code
because a larger name or value can cause some versions of Buddy firmware
to crash.

#### M509: Force language selection {#m509_force_language_selection}

```{=mediawiki}
{{Firmware Support | druid={{no}} | prusa={{yes}} }}
```
Resets the language to English. Only on Original Prusa i3 MK2.5/s and
MK3/s with multiple languages.

#### M510: Lock Machine {#m510_lock_machine}

```{=mediawiki}
{{Firmware Support | druid={{yes}} | marlin={{yes}}: 2.0.6.1 }}
```
Lock the machine. When the machine is locked a passcode is required to
unlock it. Use `M511 P` with your passcode to unlock the machine. In
Marlin this feature is enabled with the `PASSWORD_FEATURE` option.

In Druid, this feature is always enabled.

#### M511: Unlock Machine with Passcode {#m511_unlock_machine_with_passcode}

```{=mediawiki}
{{Firmware Support | druid={{yes}} | marlin={{yes}}: 2.0.6.1 }}
```
Check the given passcode and unlock the machine if it is correct.
Otherwise, delay for a period of time before allowing another attempt.
In Marlin this feature is enabled with the `PASSWORD_FEATURE` option.

Parameters
:   **P\"passcode\"** ; a numeric passcode to try

<!-- -->

Notes

In Druid, this feature is always enabled.

M511 \"12PWS5pb\" Between double quote.

`               Fixed length = 8 Char.`\
`               Valid Characters (a-z A-Z 0-9)`\
`               Always case-sensitive, regardless of Gcode Parser Case sensitivity option (M544)`

#### M512: Set Passcode {#m512_set_passcode}

```{=mediawiki}
{{Firmware Support | marlin={{yes}}: 2.0.6.1 | druid={{yes}} | }}
```
Check the given passcode (`P`) and if it is correct clear the passcode.
If `S` is given, set a new passcode. In Marlin this feature is enabled
with the `PASSWORD_CHANGE_GCODE` option.

Parameters
:   **P\"oldpass\"** ; the current numeric passcode
:   **S\"newpass\"** ; a new numeric passcode

<!-- -->

Notes

In Druid, we use similar procedures to create, modify the password, but
it is never saved, instead it is a one-way cryptographic hash generated
from it, that is saved inside the MCU, to insure maximum security.
Before setting a password, the user must make a backup of its PUID (a 96
bit serial number unique to every STMicroelectronics MCU). If the
password is lost, the only solution is to enter the PUID, on our website
www.druid3d.com in the members area. A one-way cryptographic hash will
be generated from the provided PUID, and will be available as a text
file and as a string. When this file is added to the external SD CARD.
The Bootloader, that is looking for it at every boot, will find it, and
will verify that it matches the one it will generate from the internal
PUID. Verified in a few microseconds, both will be erased, from the RAM
and the SD card, then it will remove the password, unlock the machine.
This is the most secure way of protecting a device. Any other system is
hackable in a few minutes. (See also M513, to remove password, with
either current or \"PW Removal HASH String\" )

M512 \"PASSWORD ; set new password, if none already set.

M512 \"curPW001/NEWnew02\" ; set new password, if current match.

(between double quote, separated by a slash \'/\' or a space \' \' )
Fixed length = 8 Char, Valid Characters (a-z A-Z 0-9), Always
case-sensitive, regardless of Gcode Parser Case sensitivity option
(M544)

#### M513: Remove Password {#m513_remove_password}

```{=mediawiki}
{{Firmware Support | marlin={{???}}
```
: 2.0.6.1 \| druid=`{{yes}}`{=mediawiki} \| }}

Example with Druid firmware
:   **M513 \"currpass\"** ; the current password (if known)
:   **M513 \"0446759DBDC230122126F5AC\"** ; 24 char.\"PW Removal HASH
    String\", generated from MCU PUID.

visit www.druid3D.com to generate your unique Password Removal HASH
String.

#### M524: Abort SD Printing {#m524_abort_sd_printing}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|2.0.0+}} | prusa={{no}} | buddy={{no}} | druid={{yes}} | repetier={{yes|2.0.0+}} | reprapfirmware={{partial|Use M25 then M0}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Example

`M524`

If an SD print is in progress, this command aborts the print, just as if
you had selected \"Stop print\" from the LCD menu.

#### M530: Enable printing mode {#m530_enable_printing_mode}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{yes}} | reprapfirmware={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | mk4duo={{yes}} | yaskawa={{no}}<sup>1</sup> }}
```

Example

`M530 S1 L270`

This command tells the firmware that a print has started (`S1`) or ended
(`S0`). The `L` parameter sets the number of layers. `L0` denotes
unknown layer count. This enables the firmware to switch into a special
print display mode to show print progress. Firmware should indicate the
presence of this feature by responding to `M115` with an additional
line:

[`Cap:PROGRESS:1`](Cap:PROGRESS:1)

Notes

^1^In MK4duo this command starts print counters for statistics. It also
turns off a 30-minute timer for the heaters. If the timer reaches 30,
turn off all the heaters.

#### M531: Set print name {#m531_set_print_name}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{yes}} | reprapfirmware={{no}} | bfb={{no}} | machinekit={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Example

`M531 Demo Model`

Sets the name of the currently printed object. Should follow `M530 S1`
for correct display.

#### M532: Set print progress {#m532_set_print_progress}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no|M73}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{yes}} | reprapfirmware={{yes|Use M73}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Example

`M532 X23.7 L56`

Sets the print progress (X = 0..100) and currently printed layer (L).
Should be send every 0.1% progress change on every layer change.

#### M540: Set MAC address {#m540_set_mac_address}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `Pnnn` The MAC address

Examples

`M540 P0xBE:0xEF:0xDE:0xAD:0xFE:0xED`\
`M540 PDE:AD:BE:EF:CA:FE`

Sets the [MAC address](http://en.wikipedia.org/wiki/MAC_address) of the
RepRap. This should be done before any other network commands. The MAC
address is six one-byte hexadecimal numbers separated by colons. The 0x
prefix is optional in later firmware revisions.

All devices running on the same network shall all have different MAC
addresses. For your printers, changing the last digit is sufficient.

This command is only needed when using older electronics that doesn\'t
provide a unique MAC address, for example Duet 0.6 and Duet 0.8.5.

#### M540 in Marlin/Druid/MK4duo: Enable/Disable \"Stop SD Print on Endstop Hit\" {#m540_in_marlindruidmk4duo_enabledisable_stop_sd_print_on_endstop_hit}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{no}}<sup>1</sup> | buddy={{yes}} | repetier={{no}} | druid={{yes}} | smoothie={{no}} | reprapfirmware={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   `Snnn` state, S1=enable, S0=disable

Example

`M540 S1`

Notes

In Prusa Firmware this G-code is deactivated by default, must be turned
on in the source code.^1^

#### M544: Gcode Parser Options {#m544_gcode_parser_options}

```{=mediawiki}
{{Firmware Support | fived={{???}}
```
\| teacup={{???}} \| sprinter={{???}} \| klipper={{???}} \|
marlin={{???}} \| buddy={{???}} \| prusa={{???}} \| repetier={{???}} \|
druid=`{{yes}}`{=mediawiki} \| smoothie={{???}} \|
reprapfirmware={{???}} \| bfb={{???}} \| grbl={{???}} \|
makerbot={{???}} \| machinekit={{???}} \| redeem={{???}} \|
mk4duo={{???}} \| yaskawa={{???}} }}

Parameters
:   **Snnn** S1=case insensitive, S0=case sensitive
:   **S** Report current case state.
:   **L** List all supported Gcodes
:   **K** List all Druid proprietary MMM commands (Media and Memory
    Management)

#### M550: Set Name {#m550_set_name}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|2.1.3}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | druid={{yes}} | smoothie={{no}} | reprapfirmware={{yes}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   `Pnnn` Machine name

Example

`M550 PGodzilla`

Sets the name of the RepRap to (in this case) Godzilla. The name can be
any string of printable characters except \';\', which still means start
comment.

#### M551: Set Password {#m551_set_password}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}}: Use M512 | prusa={{no}} | buddy={{no}} | repetier={{no}} | druid={{yes}}: M512 | smoothie={{no}} | reprapfirmware={{yes}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   `Pnnn` Password

Example

`M551 Pmy-very-secret-word`

On machines that need a password to activate them, set that password.
The code \'P\' is not part of the password. Note that as this is sent in
clear it does not (nor is it intended to) offer a very high level of
security. But on machines that are (say) on a network, it prevents idle
messing about by the unauthorised. The password can contain any
printable characters except \';\', which still means start comment.

Note for RepRapFirmware: If the specified password differs from the
default one (i.e. reprap), the user will be asked to enter it when a
connection is established via HTTP or Telnet. For FTP, the password must
always be passed explicitly.

#### M552: Set IP address, enable/disable network interface {#m552_set_ip_address_enabledisable_network_interface}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|2.0.8}} | prusa={{yes}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   `Innn` (Optional) Number of the network interface to manage
    (defaults to 0)
:   `Pnnn` IP address, 0.0.0.0 means acquire an IP address using DHCP
:   `Snnn` (optional) -1 = reset network interface, 0 = disable
    networking, 1 = enable networking as a client, 2 = enable networking
    as an access point (WiFi-enabled electronics only)
:   `Rnnn` (optional, RepRapFirmware 1.17 and earlier only) HTTP port,
    default 80

Example

`M552 P192.168.1.14`

Sets the IP address of the machine to (in this case) 192.168.1.14. If
the `S` parameter is not present then the enable/disable state of the
network interface is not changed.

In RepRapFirmware 1.18 and later the HTTP port address is set using the
`M586` command, so the `R` parameter of this command is no longer
supported.

M552 with no parameters reports the current network state and IP
address.

#### M553: Set Netmask {#m553_set_netmask}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|2.0.8}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   `Innn` (Optional) Number of the network interface to manage
    (defaults to 0)
:   `Pnnn` Net mask

Example

`M553 P255.255.255.0`

Sets the network mask of the RepRap machine to (in this case)
255.255.255.0. A restart may be required before the new network mask is
used. If no \'P\' field is specified, this echoes the existing network
mask configured.

Recent RepRapFirmware versions allow the IP configuration to be changed
without a restart.

#### M554: Set Gateway and/or DNS server {#m554_set_gateway_andor_dns_server}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|2.0.8}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   `Innn` (Optional) Number of the network interface to manage
    (defaults to 0)
:   `Pnnn` Gateway
:   `Snnn` (Optional) DNS server (only supported by DSF 3.3 with DuetPi
    system config plugin)

Example

`M554 P192.168.1.1`

Sets the Gateway IP address of the RepRap machine to (in this case)
192.168.1.1. A restart may be required before the new gateway IP address
is used. If no \'P\' field is specified, this echoes the existing
Gateway IP address configured.

Recent RepRapFirmware versions allow the IP configuration to be changed
without a restart.

#### M555: Set compatibility {#m555_set_compatibility}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   `Pnnn` Emulation type

Example

`M555 P1`

For firmware that can do it, the firmware is set to a mode where its
input and (especially) output behaves exactly like other established
firmware. The value of the \'P\' argument is:

  --------- ---------------------------------------------------------------
  P value   Firmware
  0         Native (i.e. whatever the firmware actually is)
  1         [RepRapFirmware](RepRapFirmware "RepRapFirmware"){.wikilink}
  2         [Marlin](Marlin "Marlin"){.wikilink}
  3         [Teacup](Teacup "Teacup"){.wikilink}
  4         [Sprinter](Sprinter "Sprinter"){.wikilink}
  5         [Repetier](Repetier "Repetier"){.wikilink}
  6         [Marlin](Marlin "Marlin"){.wikilink} with changes for nanoDLP
  --------- ---------------------------------------------------------------

#### M555: Set Bounding Box {#m555_set_bounding_box}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{yes}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `Xnnn` Minimum X coordinate
:   `Ynnn` Minimum Y coordinate of model
:   `Wnnn` X size of model (max - min X coordinate)
:   `Hnnn` Y size of model (max - min Y coordinate)

<!-- -->

Example

`M555 X10 Y20 W30 H40`

Tells the printer about the size of the model. The XL uses this
information to save power for smaller models by only heating the area
under it.

#### M556: Axis compensation {#m556_axis_compensation}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   `Snnn` Height of the measured distances
:   `Xnnn` Deviation in X direction
:   `Ynnn` Deviation in Y direction
:   `Znnn` Deviation in Z direction
:   `Pnnn` Apply XY compensation to Y axis instead of X (defaults to 0,
    requires RRF 3.2-b4 or newer)

Example

`M556 S100 X0.7 Y-0.2 Z0.6`

![Image denoting how to determine the S parameter for G-code
M556](CalibrationAngle.png "Image denoting how to determine the S parameter for G-code M556")

Though with care and adjustment a RepRap can be set up with its axes at
right-angles to each other within the accuracy of the machine, who wants
to bother with care and adjustment when the problem can be solved by
software? This tells software the tangents of the angles between the
axes of the machine obtained by printing then measuring a test part. The
`S` parameter (100 here) is the length of a triangle along each axis in
mm. The X, Y and Z figures are the number of millimeters of the short
side of the triangle that represents how out of true a pair of axes is.
The X figure is the error between X and Y, the Y figure is the error
between Y and Z, and the Z figure is the error between X and Z. Positive
values indicate that the angle between the axis pair is obtuse, negative
acute.

#### M557: Set Z probe point or define probing grid {#m557_set_z_probe_point_or_define_probing_grid}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{yes}} | reprapfirmware={{yes}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters to define `G32` probe points (Cartesian/CoreXY printers only, no longer supported in RepRapFirmware)
:   `Pnnn` Probe point number
:   `Xnnn` X coordinate
:   `Ynnn` Y coordinate

Example

`M557 P1 X30 Y40.5`

Parameters to define `G29` probe grid (all values in mm)
:   `Xaaa:bbb` Minimum and maximum X coordinates to probe
:   `Yaaa:bbb` Minimum and maximum Y coordinates to probe
:   `Rnnn` Radius to probe
:   `Snn` or `Sxx:yy` Probe point spacing
:   `Pnn` or `Pxx:yy` Number of probe points in each direction
    (RepRapFirmware 2.02 and later) - use instead of specifying the
    spacing

Examples

`M557 X0:200 Y0:220 S20`\
`M557 R150 S15`

Set the points at which the bed will be probed to compensate for its
plane being slightly out of horizontal.

The first form defines the points for for `G32` bed probing. The `P`
value is the index of the point (indices start at 0) and the `X` and `Y`
values are the position to move extruder 0 to to probe the bed. An
implementation should allow a minimum of three points (P0, P1 and P2).
This just records the point coordinates; it does not actually do the
probing. See
[G32](G-code#G32:_Probe_Z_and_calculate_Z_plane "G32"){.wikilink}.
Defining the probe points in this way is no longer supported by
RepRapFirmware, you should define them in a bed.g file instead.

The second form defines the grid for `G29` bed probing. For Cartesian
printers, specify minimum and maximum `X` and `Y` values to probe and
the probing interval. For Delta printers, specify the probing radius. If
you define both, the probing area will be the intersection of the
rectangular area and the circle. There is a firmware-dependent maximum
number of probe points supported, which may be as low as 100.

#### M558: Set Z probe type {#m558_set_z_probe_type}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes}} | bfb={{no}} || grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   `Knn` Z probe number (optional, default 0)
:   `Pnnn` Z probe type
:   `Fnnn` Feed rate (i.e. probing speed, mm/min)
:   `Hnnn` Dive height (mm)
:   `Innn` Invert (I1) or do not invert (I0) the Z probe reading
    (RepRapFirmware 1.16 and later)
:   `Rnnn` Z probe recovery time after triggering, default zero
    (seconds) (RepRapFirmware 1.17 and later)^1^
:   `Tnnn` Travel speed to and between probe points (mm/min)
:   `Annn` Maximum number of times to probe each point, default 1
    (RepRapFirmware 1.21 and later)
:   `Snnn` Tolerance when probing multiple times, default 0.03
    (RepRapFirmware 1.21 and later)
:   `Bn` B1 turns off all heaters during probing moves and during the
    probe recovery time (RepRapFirmware 1.21 and later)

Obsolete parameters
:   `Xnnn` If nonzero, use probe for homing X axis (RepRapFirmware 1.19
    and earlier only)
:   `Ynnn` If nonzero, use probe for homing Y axis (RepRapFirmware 1.19
    and earlier only)
:   `Znnn` If nonzero, use probe for homing Z axis (RepRapFirmware 1.19
    and earlier only)

Example

`M558 P1 F500 T5000 H3`

A Z probe may be a switch, an IR proximity sensor, or some other device.
This selects which to use:

:   P0 indicates that no Z probe is present
:   P1 indicates an unmodulated IR probe, or any other probe type that
    emulates an unmodulated IR probe (probe output is an analog signal
    that rises with decreasing nozzle height above the bed). If there is
    a control signal to the probe, it is driven high when the probe type
    is P1
:   P2 specifies a modulated IR probe, where the modulation is commanded
    directly by the main board firmware using the control signal to the
    probe
:   P3 selects an alternative Z probe similar to P1 but the control
    signal to the probe low
:   P4 selects a switch for bed probing (on the Duet, this must be
    connected to the E0 endstop pins)
:   P5 (from RepRapFirmware 1.14) selects a switch or a digital output
    device to the In pin of the Z-probe connector
:   P6 is as P4 but the switch is connected to and alternative connector
    (on the Duet series, the E1 endstop connector)
:   P7 is as P4 but the switch is connected to and alternative connector
    (on the Duet series, the Z endstop connector)
:   P8 is as P5 but the signal is unfiltered for faster response
:   P9 is as P5 but the probe is deployed and retracted at every probe
    point. This is intended for BLTouch.
:   P10 means use Z motor stall detection as the Z probe trigger.
:   P11 means a scanning Z probe with an analog output (supported from
    RRF 3.5.0-beta.4). Such probes must be calibrated before use (see
    M558.1).

Related codes: G29, G30, G31, G32, M401, M402, M558.1, M558.2.

#### M558.1: Calibrate height vs. reading for analog Z probe {#m558.1_calibrate_height_vs._reading_for_analog_z_probe}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes|3.5.0+}} | bfb={{no}} || grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `Knn` Z probe number (optional, default 0)
:   `Sn.n` Height to scan above and below the trigger height, in mm
:   `Ann.n` (optional) Linear coefficient of the output, in mm per count
:   `Bnn.n` (optional, ignored unless A parameter is also present,
    default 0.0) Quadratic coefficient of the output, in mm\^2 per count
:   `Cnn.n` (optional, ignored unless A parameter is also present,
    default 0.0) Cubic coefficient of the output, in mm\^3 per count

If the A parameter is present then the S parameter is ignored and the
equation to calculate the actual height of the Z probe is set to this:

`height = trigger_height + A * (probe_reading - probe_threshold) + B * (probe_reading - probe_threshold)^2 + C * (probe_reading - probe_threshold)^3`

where trigger_height and probe_threshold are as set by G31.

If the A parameter is not present but the S parameter is present then
the probe is raised or lowered to (trigger_height + S_parameter) at the
current XY position, then readings are taken as the probe is gradually
lowered to (trigger_height - S_parameter). The readings are used to
compute, store and report new values of A, B, C and the trigger
threshold.

If neither the A nor the S parameter is present, the current A, B and C
values are reported.

#### M558.2: Set, report or calibrate drive current for analog Z probe {#m558.2_set_report_or_calibrate_drive_current_for_analog_z_probe}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes|3.5.0+}} | bfb={{no}} || grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `Knn` Z probe number (optional, default 0)
:   `Sn.n` Drive level to set, or -1 to determine automatically. For
    LDC1612-based probes, when setting the current this should be in the
    range 0 to 31.

This command is used to control the drive current of scanning Z probes
that use the LDC1612 chip. If the drive current is set too low, the
sensor will not work when it is close to the bed. If the drive current
is set too high, it will not work when the sensor is distant from the
bed. Use M122 B# (where \# is the CAN address of the board that carries
the sensor) to determine whether the sensor is working normally.

When using this command with S-1 to determine the optimum drive current
automatically, the sensor should first be placed at the lower distance
limit (closest distance from the metal bed surface) of the intended
operating range.

If M558 is used with no S parameter then the current drive level is
reported.

After using M558.2 to change the drive level, M558.1 should be used to
recalibrate the sensor.

#### M558.3: Set touch mode parameters for analog Z probe {#m558.3_set_touch_mode_parameters_for_analog_z_probe}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes|3.6.0+}} | bfb={{no}} || grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters (provisional)
:   `Knn` Z probe number
:   `Sn` Mode to use: 0 = standard mode, 1 = touch mode
:   `Fnnn` Feed rate to use (mm/min) in touch mode
:   `Hn.nn` Nozzle height (mm) to be assumed when touch is detected,
    normally negative
:   `Vn.nn` Sensitivity to touch, between 0 (not at all sensitive) and
    1.0 (very sensitive)

Additional sensitivity parameters may be added in future to provide
better control of touch recognition.

All parameters are optional. If the K parameter is not provided then
probe 0 is assumed. If other parameters are not provided then their
values remain unchanged. If no parameters (except possibly K) are
provided then the existing values are reported.

In standard mode the output of an analog Z probe is compared with the
threshold as the probing move progresses. When the probe output reaches
the threshold, probing stops and the Z height is assumed to be equal to
the trigger height. In RepRapFirmware both the threshold and trigger
height are set using the G31 command.

In touch mode the output of the probe is monitored as the probing move
progresses. When the rate of change reduces sharply (the exact details
depending on the sensitivity parameters) it is assumed hat the nozzle
has contacted the bed. The Z height is assumed to be the value set using
the H parameter.

When an analog Z probe is created using M558, the mode is set to
standard mode, the feed rate in touch mode (M558.3 F parameter) is set
to the feed rate in standard mode (first or only value of the M558 F
parameter) and the touch mode nozzle height and sensitivity assume
default values. Fast-then-slow probing is not available in touch mode.

#### M559: Upload configuration file {#m559_upload_configuration_file}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Example

`M559`

If the RepRap supports it, this uploads a file that is run on re-boot to
configure the machine. This file usually is a special G Code file. After
sending `M559`, the file should be sent, ending with an `M29` (q.v.).

#### M560: Upload web page file {#m560_upload_web_page_file}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Example

`M560`

For RepRaps that have web support and that can be driven by a web
browser, this uploads the file that is the control page for the RepRap.
After sending `M560` the file (usually an HTML file) should be sent,
terminated by the string

    <!-- **EoF** -->

. Clearly that string cannot exist in the body of the file, but can be
put on the end to facilitate this process. This should not be too
serious a restriction\...

#### M561: Set Identity Transform {#m561_set_identity_transform}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{yes}} | reprapfirmware={{yes}} | bfb={{no}} | machinekit={{no}} | redeem={{yes}}  | mk4duo={{no}} | yaskawa={{no}} }}
```

Example

`M561`

This cancels any bed-plane fitting as the result of probing (or anything
else) and returns the machine to moving in the user\'s coordinate
system.

#### M562: Reset temperature fault {#m562_reset_temperature_fault}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes}} | bfb={{no}} | machinekit={{no}} | redeem={{yes}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `Pnnn` Heater number

Example

`M562 P2`

Reset a temperature fault on heater/sensor 2. If the RepRap has switched
off and locked a heater because it has detected a fault, this will reset
the fault condition and allow you to use the heater again. Obviously to
be used with caution. If the fault persists it will lock out again after
you have issued this command. P0 is the bed; P1 the first extruder, and
so on.

Later versions of RepRapFirmware support M562 without the P parameter,
which will reset all heater faults.

#### M563: Define or remove a tool {#m563_define_or_remove_a_tool}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   `Pnnn` Tool number
:   `S"name"` Tool name (optional)
:   `Dnnn` Extruder drive(s)
:   `Hnnn` Heater(s)
:   `Fnnn` Fan(s) to map the print cooling fan to (RepRapFirmware 1.16
    and later)
:   `Xnnn` Axis or axes to map X movement to (RepRapFirmware 1.16 and
    later)
:   `Ynnn` Axis or axes to map Y movement to
:   `Lnnn` Drive to use for filament mapping. By default RRF will use
    the first and only extruder drive if this parameter is not specified
    (supported by RRF \>= 2.02)

Examples

`M563 P0 D0:2:3 H1:3                 ; create a tool using extruder drives 0, 2 and 3 and heaters 1 and 3`\
`M563 P1 D1 H2 X3                    ; create a tool using extruder drive 1 and heater 2 with X movement mapped to the U axis`\
`M563 P2 D0:1 H1:2 X0:3 F0:2         ; create a tool using extruder drives 0 and 1, heaters 1 and 2,`\
`                                    ; with X movement mapped to both X and U axes and fan 0 mapped to fan 0 and fan 2`\
`M563 P3 D0 H1 S"Chocolate extruder" ; create a named tool using extruder drive 0 and heater 1`

Tools are usually (though not necessarily) extruders. The \'P\' field
specifies the tool number. Tool numbers can have any positive integer
value and 0. The \'D\' field specifies the drive(s) used by the tool -
in the first example drives 0, 2 and 3. Drive 0 is the first drive in
the machine after the movement drives (usually X, Y and Z). If there is
no \'D\' field the tool has no drives. The \'H\' field specifies the
tool\'s heaters - in the first example heaters 1 and 3. Heater 0 is
usually the hot bed (if any) so the first extruder heater is usually 1.
If there is no H field the tool has no heaters.

Tools are driven using multiple values in the \'E\' field of `G1`
commands, each controlling the corresponding drive in the \'D\' field
above, as follows:

`G1 X90.6 Y13.8 E2.24:2.24:15.89`\
`G1 X70.6 E0:0:42.4`

The first line moves straight to the point (90.6, 13.8) extruding a
total of 2.24mm of filament from both drives 0 and 2 and 15.98mm of
filament from drive 3. The second line moves back 20mm in X extruding
42.4mm of filament from drive 3.

Alternatively, if the slicer does not support generating `G1` commands
with multiple values for the extrusion amount, the `M567` command can be
used to define a tool mix ratio.

Normally an `M563` command is immediately followed by a `G10` command to
set the tool\'s offsets and temperatures.

It is permissible for different tools to share some (or all) of their
drives and heaters. So, for example, you can define two tools with
identical hardware, but that just operate at different temperatures.

The X mapping option is used to create tools on machines with multiple
independent X carriages. The additional carriages are set up as axes U,
V etc. (see `M584`) and the X mapping option in `M563` defines which
carriage or carriages are used.

If you use the `M563` command with a `P` value for a tool that has
already been defined, that tool is redefined using the new values you
provide.

RepRapFirmware supports an additional form of the `M563` command. The
command:

`M563 S1`

means add 1 (the value of the `S` parameter) to all tool numbers found
in the remainder of the current input stream (e.g. the current file if
the command is read from a file on the SD card), or until a new `M563`
command of this form is executed. The purpose of this is to provide
compatibility between systems in which tool numbers start at 1, and
programs such as slic3r that assume tools are numbered from zero.

Recent versions of RepRapFirmware allow the deletion of existing tools
if `M563` is called in this way:

`M563 P1 D-1 H-1`

#### M564: Limit axes {#m564_limit_axes}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{partial|M211 S}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   `Hnnn` H1 = forbid movement of axes that have not been homed, H0 =
    allow movement of axes that have not been homed (RepRapFirmware 1.21
    and later)
:   `Snnn` S1 = limit movement within axis boundaries, S0 = allow
    movement outside boundaries

Example
:   M564 S0 H0

Allow moves outside the print volume and before homing, or not. If the S
parameter is 0, then you can send G codes to drive the RepRap outside
its normal working volume, and it will attempt to do so. Likewise if the
H parameter is 0 you can move the head or bed along axes that have not
been homed. The default behaviour is S1 H1. On some types of printer
(e.g. Delta and SCARA), movement before homing is prohibited regardless
of the H parameter.

#### M565: Set Z probe offset {#m565_set_z_probe_offset}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{yes}} | reprapfirmware= {{yes|use G31}} | bfb={{no}} | machinekit={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Example

`M565 X3 Y4.5 Z-2.37`

Set the offset from the extruder tip to the probe position. The `X`,
`Y`, and `Z` values are the delta between the extruder and the actual
trigger position of the probe. If the probe trigger point is below the
extruder (typical) the Z offset will be negative. This just records the
point offset; it does not actually do the probing. See `G32`.

#### M566: Set allowable instantaneous speed change {#m566_set_allowable_instantaneous_speed_change}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   `Xnnn` Maximum instantaneous speed change of the X axis (mm/min)
:   `Ynnn` Maximum instantaneous speed change of the Y axis
:   `Znnn` Maximum instantaneous speed change of the Z axis
:   `Ennn` Maximum instantaneous speed change of the extruder drives

Example

`M566 X20 Y20 Z2 E10`

Sets the maximum allowable speed change (sometimes called \'jerk
speed\') of each motor when changing direction.

The model files and gcode files used by repraps generally render circles
and other curves shapes as a sequence of straight line segments. If the
motors were not allowed any instantaneous speed change, they would have
to come to a stop at the junction between each pair of line segments. By
allowing a certain amount of instantaneous speed change, printing speed
can be maintained when the angle between the two line segments is small
enough.

If you set these `X` and `Y` values too low, then the printer will be
slow at printing curves. If they are too high then the printer may be
noisy when cornering and you may suffer ringing and other print
artefacts, or even missed steps.

On very old versions of RepRapFirmware (prior to 1.09), these were also
the minimum speeds of each axis.

#### M567: Set tool mix ratios {#m567_set_tool_mix_ratios}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   `Pnnn` Tool number
:   `Ennn` Mix ratios

Example

`M567 P2 E0.1:0.2:0.1:0.6`

This example sets the mix ratio for tool 2 (the `P` value). When mixing
is then turned on (see `M568`), only single `E` values need to be sent
on a `G1` command (any extra `E` values will be ignored, but are not
illegal):

`G1 X20 E1.3`

This will move to X=20 extruding a total length of filament of 1.3mm.
The first drive of tool 2 will extrude 0.1\*1.3mm, the second 0.2\*1.3mm
and so on. The ratios don\'t have to add up to 1.0 - the calculation
done is as just described. But it is best if they do.

See also `M568`.

#### M568: Tool settings {#m568_tool_settings}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes|3.3 and later}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   **Pnnn** Tool number. If this parameter is not provided, the current
    tool is assumed.
:   **Rnnn** Standby temperature(s)
:   **Snnn** Active temperature(s)
:   **Fnnn** Spindle RPM, always positive
:   **An** Required heater state: 0 = off, 1 = standby temperature(s), 2
    = active temperature(s)

<!-- -->

Examples:
:   M568 P1 R140 S205 ; set standby and active temperatures for tool 1
:   M568 P0 F5200 ; set spindle RPM for tool 0
:   M568 P2 A1 ; set tool 2 heaters to their standby temperatures

RepRapFirmware will report the tool parameters if only the tool number
is specified.

The R value is the standby temperature in °C that will be used for the
tool, and the S value is its operating temperature. If you don\'t want
the tool to be at a different temperature when not in use, set both
values the same.

Temperatures set with M568 do not wait for the heaters to reach temp
before proceeding. In order to wait for the temp use a M116 command
after the M568 to wait for temps to be reached.

#### M568: Turn off/on tool mix ratios (obsolete meaning in old RepRapFirmware versions) {#m568_turn_offon_tool_mix_ratios_obsolete_meaning_in_old_reprapfirmware_versions}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```
This command is obsolete. When using a tool defined as a mixing
extruder, RepRapFirmware applies the mix ratio defined by M567 whenever
only one E parameter is provided in G1 commands. When multiple
colon-separated E values are provided in the G1 command, they will be
used as the individual amounts to extrude.

#### M569: Stepper driver control {#m569_stepper_driver_control}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   `Pnn` Motor driver number
:   `Sn` Direction of movement of the motor(s) attached to this driver:
    0 = backwards, 1 = forwards (default 1)
:   `Rn` Driver enable polarity: 0 = active low, 1 = active high
    (default 0)
:   `Tnn` Minimum driver step pulse width and interval in microseconds
    (RepRapFirmware 1.14 and later)
:   `Taa:bb:cc:dd` Minimum driver step pulse width, step pulse interval,
    direction-to-step setup time and step-to-direction hold time, in
    microseconds (RepRapFirmware 1.21 and later)
:   `Dnn` Stepper driver mode (RepRapFirmware 2.0 and later): 0=constant
    off time, 1=random off time, 2=spread cycle, 3=stealthChop, 4=closed
    loop
:   `Fnn` (firmware 2.02 and later) Off-time in the chopper control
    register, 1 to 15
:   `Bnn` (firmware 2.02 and later) Blanking time (tbl) in the chopper
    control register, 0 to 3. See the TMC driver datasheet.
:   `Yaa:bb` or `Yaa:bb:cc` (firmware 2.02 and later) Hysteresis start,
    end and decrement values in the chopper control register. See the
    TMC driver datasheet for the meaning.
:   `Cnnn` Custom chopper control register value (RepRapFirmware 2.0 and
    later). **Do not change this value without having a good
    understanding of the stepper driver driver chip!**
:   `Hnn` (firmware 2.02 and later) t_high parameter for those stepper
    driver chips that support it (e.g. TMC2208, 2224). Send M569 P#
    (where \# is the driver number) with no additional parameters to see
    how this translates into mm/sec. See also the V parameter.
:   `Vnnn` (firmware 2.02 and later) tpwmthrs parameter for those
    stepper driver chips that support it (e.g. TMC2208, 2224). This is
    the interval in clock cycles between 1/256 microsteps below which
    the drivers will switch from stealthChop to to spreadCycle mode.
    Only applies when the driver is configured in stealthChop mode.
    Typical value are from 100 (high speed) to 4000 (low speed). Send
    M569 P# (where \# is the driver number) with no additional
    parameters to see how this translates into axis speed in mm/sec.

Example

`M569 P0 S0               ; reverse the direction of the motor attached to driver 0`\
`M569 P5 R1 T2.5:2.5:5:0  ; driver 5 requires an active high enable, 2.5us minimum step pulse, 2.5us minimum step interval, 5us DIR setup time and no hold time`

Notes

All parameters except P are optional. For any parameter that is not
provided, the corresponding value will not be changed.

The T parameters are intended for use with external stepper drivers.
Currently, RepRapFirmware only remembers the highest `T` parameters seen
in any M569 command, and applies those values to all drivers for which
any nonzero `T` parameters were specified.

The modes (D parameter) supported by various stepper driver chips are:

:   TMC2130, TMC2160, TMC5160: modes 0,1,2,3 (Duet 3 EXP1HCL board also
    supports mode 4)
:   TMC2660: modes 0,1,2
:   TMC2208/2209/2224: modes 2,3 (mode 3 is stealthChop2)

Some versions of RepRapFirmware prior to 1.14 also provided `X`, `Y`,
`Z` and `E` parameters to allow the mapping from axes and extruders to
stepper driver numbers to be changed. From 1.14 onward, this
functionality is provided by M584 instead.

#### M569.1: Stepper driver closed loop configuration {#m569.1_stepper_driver_closed_loop_configuration}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `Pn` or `Pn.n` Motor driver number, or board address and driver
    number
:   `Sn` Mode: 0=open loop (default), 1=closed loop (requires an encoder
    to be selected, see the T parameter)
:   `Tn` Encoder type: 0=none, 1=linear quadrature encoder on axis,
    2=quadrature encoder on motor shaft, 3=AS5047D encoder on motor
    shaft, 4=TLI5012B encoder on motor shaft
:   `En.n` Encoder counts per mm (linear encoder) or per rotation
    (rotary encoder). Only used if the encoder type is 1 or 2.
:   `Rn.n` Proportional constant
:   `In.n` Integral constant
:   `Dn.n` Derivative constant
:   `Hn` Minimum holding current as a percentage of the configured
    current when operating in closed loop mode

Supported by RepRapFirmware on boards using closed loop drivers.
Switching between open loop and closed loop modes is done using M569.

#### M569.2: Read or write any stepper driver register {#m569.2_read_or_write_any_stepper_driver_register}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `Pnn` Motor driver number
:   `Rnn` Register number, 0-127
:   `Vnnnn` Value to write (optional)

Example
:   `M569.2 P1 R0`

If the V parameter is not provided, this command reads the specified
register and returns the value of that register. If the V parameter is
provided, that value is written to the specified register.

WARNING! Use of M569.2 to write stepper driver registers may result in
damage to the stepper drivers, for example from excessive motor current
or insufficient blanking time.

#### M569.3: Read Motor Driver Encoder {#m569.3_read_motor_driver_encoder}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes}}<sup>1</sup> | klipper={{no}} | bfb={{no}} | machinekit={{no}} | makerbot={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} | grbl={{no}} }}
```
This causes the RepRap machine to report its current motor encoder
positions to the host in units of arc degrees (1/360\'ths of turns),
relative to some reference position that you set with the `S` parameter.

Before the first call with the `S` parameter, the reference is unknown
and arbitrary.

Parameters
:   `Pn` or `Pn.n` Motor driver number, or board address and driver
    number. Several (remote) drivers may be specified, separated by
    colon. No more than number of visible axes, as specified by `M584 P`
    parameter, are allowed.
:   `S` Sets an encoder reference point. Current and subsequent
    `M569.3 Pn.n` calls returns numbers that are relative to the
    `M569.3 Pn.n S` call.

If `P` is not supplied, an error is returned.

A maximum of four CAN-connected drivers can be reached with `M569.3`
counting from machine boot. CAN addresses that fail to respond don\'t
count towards this maximum.

Examples

`M569.3`

`Error: M569: missing parameter 'P'`

`M569.3 P54.0`

`Error: M569.3: Message not received`

`M569.3 P40.0:41.0:42.0:43.0`

`[-155.28, -4089.60, 6842.04, 0.00, ],`

`M569.3 P43.0:41.0:42.0:40.0`

`[0.00, -4089.60, 6842.04, -155.28, ],`

`M569.3 P40.0:41.0:42.0:43.0 S`

`[0.00, 0.00, 0.00, 0.00, ],`

`M569.3 P49.0`

`Error: M569.3: Max CAN addresses we can reference is 4. Can't reference board 49.`

Notes

^1^ Planned for RepRapFirmware 3.4.

#### M569.4: Set Motor Driver Torque Mode {#m569.4_set_motor_driver_torque_mode}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes}}<sup>1</sup> | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
Tell one or more motor drivers to apply a specified torque regardless of
position.

Parameters
:   `Pn` or `Pn.n` Motor driver number, or board address and driver
    number. Can also be a colon separated list of driver numbers.
:   `Tn` Where n is the mode/torque to apply in units of Nm. Newer
    Hangprinters might use units of N.

If `P` or `T` parameter is missing, then no action is taken. The driver
is put back into position mode by requesting a torque smaller than
0.0001 Nm.

Examples

`M569.4`

`Error: M569: missing parameter 'P'`

`M569.4 P40.0:41.0`

`Error: M569: missing parameter 'T'`

`M569.4 P40.0 T0.001`

`0.001000 Nm,`

`M569.4 P40.0:41.0 T0`

`pos_mode, pos_mode,`

Notes

Hangprinter\'s \"torque mode\" is implemented as a ReprapFirmware macro
that depends on M569.4.

Practical torques for tightening lines in daily use tend to lie between
0.1 Nm and 0.001 Nm for a Hangprinter.

^1^ Planned for RepRapFirmware 3.4.

#### M569.5: Collect Data from Closed-loop Driver {#m569.5_collect_data_from_closed_loop_driver}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes|3.4 onwards}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `Pn.n` Motor CAN board address and driver number

Remaining details TBD.

#### M569.6: Execute Closed-loop Driver Tuning Move {#m569.6_execute_closed_loop_driver_tuning_move}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes|3.4 onwards}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `Pn.n` Motor CAN board address and driver number

Remaining details TBD.

#### M569.7: Configure motor brake port {#m569.7_configure_motor_brake_port}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes|3.4 onwards}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `Pn.n` Motor CAN board address (if applicable) and driver number
:   `C"port"` Port name of the brake control port. The port must be on
    the same CAN board as the driver. The CAN address does not need to
    be specified in the port name, but if it is then it must be the same
    as the driver address.

Example
:   `M569.7 P40.0 C"out2" ; driver 0 on board 40 uses port out1 on board 40 to control the brake`

When the motor driver is enabled, the specified output port will be
turned on at the same time to release the brake. When the motor driver
is disabled, the output port will be turned off. Idle current mode does
not count as disabled.

#### M569.8: Read Axis Force {#m569.8_read_axis_force}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes|3.5 onwards}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `Pn` or `Pn.n` Motor driver number, or board address and driver
    number. Can also be a colon separated list of driver numbers.

The readouts are in units of Newtons.

Example

M569.8 P40.0:41.0:42.0:43.0 `[3.52, -0.60, 7.24, -5.84, ],`

#### M569.9: Sets the driver sense resistor and maximum current {#m569.9_sets_the_driver_sense_resistor_and_maximum_current}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes|STM32 Only 3.4.2_102 onwards}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `Pnn` or `Pnn.n` Motor driver number.
:   `Rnnnn` Driver sense resistor value in Ohms.
:   `Snnnn` Driver max current value in Amps.

<!-- -->

Example
:   `M569.9 R0.047 S4 ; driver 0 uses a 47mOhm sense resistor and 4 Amps maximum driver output`

#### M570: Configure heater fault detection {#m570_configure_heater_fault_detection}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters for RepRapFirmware 1.14 and earlier
:   `Snnn` Heater timeout (in seconds)

Example

`M570 S120`

After a heater has been switched on, wait 120 seconds for it to get
close to the set temperature. If it takes longer than this, raise a
heater fault.

Parameters for RepRapFirmware 1.15e and later
:   `Hnnn` Heater number
:   `Pnnn` Time in seconds for which a temperature anomaly must persist
    on this heater before raising a heater fault (default 5 seconds)
:   `Tnnn` Permitted temperature excursion from the setpoint for this
    heater (default 10C)
:   `Snnn` Time in seconds after a heater fault is raised after which
    the print will be abandoned, default 10 minutes (RepRapFirmware 1.20
    and later)

Example

`M570 H1 P4 T15`

**Warning!** Heating fault detection is provided to reduce the risk of
starting a fire if a dangerous fault occurs, for example if the heater
cartridge or thermistor falls out of the heater block. You should not
increase the detection time or permitted temperature excursion without
good reason, because doing so will reduce the protection.

#### M571: Set output on extrude {#m571_set_output_on_extrude}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}}  | reprapfirmware={{yes}} | bfb={{no}} | machinekit={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `Snnn` Output value
:   `Fnnn` Output PWM frequency (RepRapFirmware 1.17 and later)
:   `Pnnn` Logical pin number (RepRapFirmware 1.17 and later), defaults
    to the FAN0 output until `M571` with a `P` parameter has been seen

Example

`M571 P3 F200`\
`M571 S0.5`

This turns the controlled pin output on whenever extrusion is being
done, and turns it off when the extrusion is finished. The output could
control a fan or a stirrer or anything else that needs to work just when
extrusion is happening. It also can be used to control a laser beam. The
`S` parameter sets the value of the PWM to the output. 0.0 is off; 1.0
is fully on.

In RepRapFirmware 1.17 and later you can use the `P` parameter to change
the pin used and you can also set the PWM frequency. Pin numbers are the
same as in the M42 and `M280` commands. The pin you specify must not be
in use for anything else, so if it is normally used as a heater you must
disable the heater first using `M307`, or if it is used for a fan you
must disable the fan using M106 with the I-1 parameter.

#### M572: Set or report extruder pressure advance {#m572_set_or_report_extruder_pressure_advance}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{yes}}<sup>1</sup> | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Prusa Buddy firmware specific^1^

<!-- -->

Parameters
:   `Dnnn` Extruder number
:   `Tnnn` Extruder number (not supported yet)^1^
:   `Snnn` Pressure advance amount (in seconds)
:   `Snnn` Set the pressure advance value. Range is 0. to 1.0 seconds.
    If zero the pressure advance is disabled.^1^
:   `Wnnn` Set a time range in seconds used for calculating the average
    extruder velocity for pressure advance. Range between 0. and 0.2
    Default value is 0.04.^1^

<!-- -->

Example

`M572 D0 S0.1`

`M572 S0.05 `^`1`^

This sets the pressure advance coefficient (`S` parameter) for the
specified extruder (`D` parameter).

Pressure advance causes the extruder drive position to be advanced or
retarded during printing moves by an additional amount proportional to
the rate of extrusion. At the end of a move when the extrusion rate is
decreasing, this may result in the extruder drive moving backwards (i.e.
retracting). Therefore, if you enable this feature, you may need to
reduce the amount of retraction you use in your slicing program to avoid
over-retraction.

With Bowden extruders, an `S` value between 0.1 and 0.5 usually gives
the best print quality. Direct drive extruders typically work best with
lower values such as 0.05.

Older versions of RepRapFirmware used the `P` parameter to specify the
drive number, instead of using D to specify the extruder number.

#### M573: Report heater PWM {#m573_report_heater_pwm}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{partial|3.3.0 and earlier}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   `Pnnn` Heater number

Example

`M573 P1`

This gives a running average (usually taken over about five seconds) of
the PWM to the heater specified by the P field. If you know the voltage
of the supply and the resistance of the heater this allows you to work
out the power going to the heater. Scale: 0 to 1.

In RepRapFirmware 3.3.0 and later the heater PWM can be queried from the
Object Model instead.

#### M574: Set endstop configuration {#m574_set_endstop_configuration}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   **Xnnn** Switch position for X axis
:   **Ynnn** Switch position for Y axis
:   **Znnn** Switch position for Z axis
:   **Snnn** Endstop type: 0 = active low endstop input, 1 = active high
    endstop input, 2 = Z probe, 3 = motor load detection

Example
:   M574 X1 Y2 Z0 S1 ; X endstop at low end, Y endstop at high end, no Z
    endstop, all active high

This defines the position of [
endstop](Glossary_of_Terms#Endstop " endstop"){.wikilink} sensor that
the printer has for each axis: 0 = none, 1 = low end, 2 = high end. The
optional S parameter defines whether the endstop input is active high
(S1, the default), low (S0), or the axes listed use the Z probe for
homing that axis (S2), or motor stall detection (S3). A normally-closed
endstop switch wired in the usual way produces an active high output
(S1). If different axes use different types of endstop sensing, you can
use more than one M574 command.

On delta printers the XYZ parameters refer to the towers, and the
endstops should normally all be high end (i.e. at the top of the
towers).

The S2 and S3 options are supported in RepRapFirmware 1.20 and later.

In RepRapFirmware 1.16 and earlier, the M574 command with E parameter
was used to specify whether a Z probe connected to the E0 endstop input
produces an active high (S1) or active low (S0) output. In
RepRapFirmware 1.17 and later, use the I parameter of the M558 command
instead.

#### M575: Set serial comms parameters {#m575_set_serial_comms_parameters}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|2.0+}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes}} | bfb={{no}} | grbl={{no}} | makerbot-{{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `Pnnn` Serial channel number
:   `Bnnn` Baud rate (optional)
:   `Snnn` Protocol (optional)

Example

`M575 P1 B57600 S1`

This sets the communications parameters of the serial comms channel
specified by the `P` parameter. `P0` specifies the main serial interface
(typically a USB port, or serial-over-USB), while `P1` specifies an
auxiliary serial port (for example, the port used to connect a PanelDue)
and P2 specifies a second auxiliary port if there is one.

The `B` parameter is the required baud rate (this parameter is typically
ignored if the port is a true USB port).

The `S` parameter is a bitmap of protocol features. Bit 0 if set
specifies that only commands that include a valid checksum or CRC should
be accepted from this comms channel. Bit 1 if set specifies that
responses should be sent in raw mode (default is to send them as JSON).
Bit 2 if set specifies that only commands with a valid CRC should be
accepted (this overrides bit 0).

If either the B or the S parameter is missing, the previous value will
be retained, or a default used if the port has not previously been
configured using M575. If both are missing then the existing values are
reported.

#### M576: Set SPI comms parameters {#m576_set_spi_comms_parameters}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes}} | bfb={{no}} | grbl={{no}} | makerbot-{{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `Snnn` Maximum delay between full SPI transfers (in ms, defaults to
    25ms)
:   `Fnnn` Maximum delay between full SPI transfers when a file is open
    (in ms, defaults to 5ms)
:   `Pnnn` Number of events required to skip the delay (defaults to 4)

Example

`M576 S10 ; set data exchange interval to 10ms`

This sets the communications parameters of the SPI channel. Supported in
RRF 3.4 and later in SBC mode.

#### M577: Wait until endstop is triggered {#m577_wait_until_endstop_is_triggered}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes}} | bfb={{no}} | machinekit={{no}}  | makerbot={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `Snnn` Desired endstop level
:   `Xnnn` Select X axis endstop
:   `Ynnn` Select Y axis endstop
:   `Znnn` Select Z axis endstop
:   `Ennn` Select extruder drive endstop

Example

`M577 E0 S1`

Wait for an endstop switch to be pressed. The example above will wait
until the first extruder endstop is triggered.

The following trigger types may be used using the \'S\' parameter:

0: Endstop not hit 1: Low endstop hit 2: High endstop hit 3: Near
endstop (only Z probe)

#### M578: Fire inkjet bits {#m578_fire_inkjet_bits}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes}} | bfb={{no}} | machinekit={{no}}  | makerbot={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `Pnnn` Inkjet head number
:   `Snnn` Bit pattern

Example

`M578 P3 S5`

This fires inkjet head 3 (the P field) using the bit pattern specified
by the S field. The example shown would fire bits 101. If the `P`
parameter is ommitted inkjet 0 is assumed.

This is a version of the M700 command used by the
[Inkshield](Inkshield "Inkshield"){.wikilink}, but unfortunately M700 is
already taken so cannot be used for that in the standard.

#### M579: Scale Cartesian axes {#m579_scale_cartesian_axes}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes}} | bfb={{no}} | machinekit={{no}}  | makerbot={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `Xnnn` Scale factor for X axis
:   `Ynnn` Scale factor for Y axis
:   `Znnn` Scale factor for Z axis

Example

`M579 X1.0127 Y0.998`

On a Cartesian RepRap you can get prints exactly the right size by
tweaking the axis steps/mm using the M92 G Code above. But this does not
work so easily for Delta and other RepRaps for which there is cross-talk
between the axes. This command allows you to adjust the X, Y, and Z axis
scales directly. So, if you print a part for which the Y length should
be 100mm and measure it and find that it is 100.3mm long then you set
Y0.997 (= 100/100.3).

#### M580: Select Roland {#m580_select_roland}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | druid={{no}} | smoothie={{no}} | reprapfirmware={{yes}} | bfb={{no}} | machinekit={{no}}  | makerbot={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `Rnnn` Whether Roland mode should be activated
:   `Pnnn` Initial text to send to the Roland controller

Example

`M580 R1 PVS4;!VZ2;!MC1;`

This is not really anything to do with RepRap, but it is convenient. The
[little Roland
mills](http://www.rolanddg.com/product/3d/3d/mdx-20_15/mdx-20_15.html)
are very widely available in hackerspaces and maker groups, but
annoyingly they don\'t speak G Codes. As all RepRap firmware includes a
G-Code interpreter, it is often easy to add functions to convert G Codes
to [Roland RML
language](http://altlab.org/d/content/m/pangelo/ideas/rml_command_guide_en_v100.pdf).
M580 selects a Roland device for output if the R field is 1, and returns
to native mode if the `R` field is 0. The optional `P` string is sent to
the Roland if `R` is 1. It is permissible to call this repeatedly with
`R` set to 1 and different strings in the `P` field to communicate
directly with a Roland.

#### M581: Configure external trigger {#m581_configure_external_trigger}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes}} | bfb={{no}} | machinekit={{no}}  | makerbot={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `Tnn` Logical trigger number to associate the endstop input(s) with,
    from zero up to a firmware-specific maximum (e.g. 9 for
    RepRapFirmware)
:   `X, Y, Z, E` Selects endstop input(s) to monitor
:   `P` Reserved, may be used in future to allow general I/O pins to
    cause triggers
:   `S` Whether trigger occurs on a rising edge of that input (S1,
    default), falling edge (S0), or ignores that input (S-1). By
    default, all triggers ignore all inputs.
:   `C` Condition: whether to trigger at any time (C0, default) or only
    when printing a file from SD card (C1)

Example

`M581 E1:2 S1 T2 C1   ; invoke trigger 2 when a rising edge is detected on the E1 or E2 endstop input and a file is being printed from SD card`

When `M581` is executed, if the `T` parameter is present but the other
parameters are omitted, the trigger inputs and edge polarities for that
trigger number are reported. Otherwise, the specified inputs and their
polarities are added to the conditions that cause that trigger. Using
`S-1` with no `X`, `Y`, `Z` or `E` parameters sets the trigger back to
ignoring all inputs.

In RepRapFirmware, trigger number 0 causes a full (emergency) stop as if
`M112` had been received. Trigger number 1 causes the print to be paused
as if `M25` had been received. Any trigger number \# greater then 1
causes the macro file `sys/trigger#.g` to be executed. Polling for
further trigger conditions is suspended until the trigger macro file has
been completed. RepRapFirmware does not wait for all queued moves to be
completed before executing the macro, so you may wish to use the `M400`
command at the start of your macro file. If several triggers are
pending, the one with the lowest trigger number takes priority.

#### M582: Check external trigger {#m582_check_external_trigger}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes}} | bfb={{no}} | machinekit={{no}}  | makerbot={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   T Trigger number to poll

Example

`M582 T2 ; check levels of inputs that give rise to trigger #2`

Triggers set up by the M581 command are normally activated only when the
specified inputs change state. This command provides a way of causing
the trigger to be executed if the input is at a certain level. For each
of the inputs associated with the trigger, the trigger condition will be
checked as if the input had just changed from the opposite state to the
current state.

For example, if you use M581 to support an out-of-filament sensor, then
M582 allows you to check for out-of-filament just before starting a
print.

#### M584: Set drive mapping {#m584_set_drive_mapping}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes|1.14+}} | bfb={{no}} | machinekit={{no}}  | makerbot={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `Xnnn` Driver number(s) for X motor(s)
:   `Ynnn` Driver number(s) for Y motor(s)
:   `Znnn` Driver number(s) for Z motor(s)
:   `U,V,W, A, B, Cnnn` Driver number(s) for additional axes U, V, W, A,
    B and C (UVW RepRapFirmware 1.16 and later; ABC RepRapFirmware 1.19
    and later)
:   `Ennn` Driver number(s) for E motor(s)
:   `Pnnn` Number of visible axes, defaults to the total number of axes
    configured.

Example
:   M584 X0 Y1 Z2:3 E4:5:6 ; Driver 0 controls the X motor, 1 controls
    Y, 2 and 3 control Z motors, 4 and 5 control E motors

Assigning a drive using `M584` does not remove its old assignment.
Therefore, if you assign a drive that defaults to being an extruder
drive, you should also assign the extruder drives explicitly as in the
above example. Failure to do so may result in unexpected behaviour.

You can use `M584` to create additional axes - for example, to represent
additional carriages on a machine with multiple independent X carriages.
Additional axes must be created in the order UVWABC. You can hide some
of the last axes you create using the P parameter. Hidden axes have no
homing buttons or jog controls in the user interface.

On the Duet WiFi and Duet Ethernet, if you configure multiple drivers
for an axis, either all of them must be TMC2660 drivers on the Duet or a
Duet expansion board, or none of them must be. This is to facilitate
dynamic microstepping and other features of the TMC2660.

#### M585: Probe Tool {#m585_probe_tool}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes|1.20+}} | bfb={{no}} | machinekit={{no}}  | makerbot={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
In machines with a tool probe this probes the currently selected tool
against it and corrects the offsets set by the G10 command (q.v.).

Parameter must be only one of:
:   `Xnnn`
:   `Y-nnn`
:   `Znnn`

Where the absolute value of `nnn` is the radius of the tool plus the
radius of the probe in that direction. So `M585 X1.5` will set the X
offset of a 1mm diameter tool against a 2mm diameter probe, etc. If the
value of `nnn` is positive the tool is moved in the positive direction
towards the probe until it touches. If it is negative, the tool moves
the other way.

So the process should be:

:   Set the values as closely as known in the `G10` command.
:   Move to a position slightly offset from the probe then execute
    `M585`s in X, Y and Z in the tool selection macro to set them
    precisely.

After this, the `G10` command on its own can be used to report the
values.

#### M586: Configure network protocols {#m586_configure_network_protocols}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes|1.18+}} | bfb={{no}} | machinekit={{no}}  | makerbot={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `Pnn` Protocol: 0 = HTTP or HTTPS, 1 = FTP or SFTP, 2 = Telnet or
    SSH, 3 - multicast discovery protocol (RepRapFirmware 3.4 and
    later), 4 = MQTT (RepRapFirmware 3.5 and later) (where two choices
    are given, which one depends on the `T` parameter)
:   `Snn` 0 = disable this protocol, 1 = enable this protocol
:   `Rnn` TCP port number to use for the specified protocol. Ignored
    unless S = 1. If this parameter is not provided then the default
    port for that protocol and TLS setting is used.
:   `Tnn` 0 = don\'t use TLS, 1 = use TLS. Ignored unless `S` = 1. If
    this parameter is not provided, then TLS will be used if the
    firmware supports it and a security certificate has been configured.
    If `T1` is given but the firmware does not support TLS or no
    certificate is available, then the protocol will not be enabled and
    an error message will be returned.
:   `C"site"` Set or reset allowed site for cross-orgin HTTP requests
    (RRF \> 3.2-b4.1)

M586 with no `S` parameter reports the current support for the available
protocols.

RepRapFirmware 1.18 and later enable only HTTP (or HTTPS if supported)
protocol by default. If you wish to enable FTP and/or Telnet, enable
them using this command once or twice in config.g.

#### M586.4: Configure MQTT server {#m586.4_configure_mqtt_server}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes|3.5+}} | bfb={{no}} | machinekit={{no}}  | makerbot={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   **U\"username\"** The name to use when logging on to the MQTT server
:   **K\"password\"** The password to use when logging on to the MQTT
    server (only valid if the U parameter is also present)
:   **C\"client-id\"** The client ID to use
:   **W\"will-message\"** The will-message to use
:   **T\"topic\"** The topic name to use (only processed if the W
    parameter is also present)
:   **S\"subscription\"** The subscription name to use
:   **Qnn** The quality of service to use, 0 to 2 (only processed if the
    S parameter is also present)
:   **P\"publish\"** Publish the topic if this is set
:   **Rn** 1 = retain, 0 = do not retain (only processed if the P
    parameter is used)
:   **Dn** 1 = duplicate, 0 = don\'t duplicate (only processed if the P
    parameter is used)

\[To be completed\]

#### M587: Store WiFi host network in list, or list stored networks {#m587_store_wifi_host_network_in_list_or_list_stored_networks}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes|1.19+}} | bfb={{no}} | machinekit={{no}}  | makerbot={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `Sccc` Network SSID
:   `Pccc` Network password
:   `Inn.nn.nn.nn` (optional) IP address to use when connected to this
    network. If zero or not specified then an IP address will be
    acquired via DHCP.
:   `Jnn.nn.nn.nn` (optional) Gateway IP address to use when connected
    to this network.
:   `Knn.nn.nn.nn` (optional) Netmask to use when connected to this
    network
:   `Lnn.nn.nn.nn` (optional, supported only by DuetPi + DSF v3.3 or
    newer) DNS server to use
:   `Cnnn` (supported only by DuetPi + DSF v3.3 or newer) Country code
    for the WiFi adapter, only required if not set before

If a password or SSID includes space or semicolon characters then it
must be enclosed in double quotation marks. For security, do not use
this command in the config.g file, or if you do then remove it after
running it once so that the network password is not visible in the file.

`M587` with no parameters lists all stored SSIDs, but not the stored
passwords.

#### M588: Forget WiFi host network {#m588_forget_wifi_host_network}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes|1.19+}} | bfb={{no}} | machinekit={{no}}  | makerbot={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `Sccc` SSID to remove from the networks list

The specified SSID will be removed from the networks list and the
associated password cleared out of EEPROM. If the SSID is given as \*
then all stored networks will be forgotten.

#### M589: Configure access point parameters {#m589_configure_access_point_parameters}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes|1.19+}} | bfb={{no}} | machinekit={{no}}  | makerbot={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `Sccc` The SSID that the WiFi interface should use when it is
    commanded to run as an access point
:   `Pccc` The WiFi password
:   `Inn.nn.nn.nn` The IP address to use

Note: WPA2 security will be used by default.

#### M590: Report current tool type and index {#m590_report_current_tool_type_and_index}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{no}} | bfb={{no}} | machinekit={{no}}  | makerbot={{no}} | grbl={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
Report the current tool type, which may be \"Extruder,\" \"Picker,\"
\"Laser,\" \"Foam Cutter,\" \"Milling,\" or any others implemented by
the machine. Also report the tool index, such as \"0x01\" for the second
extruder.

Example

`> M590`\
`> echo: Extruder 0x00`

#### M591: Configure filament monitoring {#m591_configure_filament_monitoring}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes|1.21+}} | bfb={{no}} | machinekit={{no}}  | makerbot={{no}} | grbl={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
This configures filament sensing for the specified extruder. The sensor
may be a simple filament presence detector, or a device that measures
movement of filament, or both. The action on detecting a filament error
is firmware-dependent, but would typically be to run a macro and/or to
pause the print and display a message.

Parameters
:   **Cnn** Which input the filament sensor is connected to. On Duet
    electronics: 0=X endstop input, 1=Y endstop input, 2=Z endstop
    input, 3=E0 endstop input etc.
:   **Dnn** Extruder drive number (0, 1, 2\...),
:   **Pnn** Type of sensor: 0=none, 1=simple sensor (low signal when
    filament present), 2=simple sensor (high signal when filament
    present), 3=Duet3D rotating magnet sensor, 4=Duet3D rotating magnet
    sensor with microswitch, :**Snn** S0 = disable filament monitoring,
    S1 = enable filament monitoring. Calibration data may be collected
    while printing even when filament monitoring is disabled.

5=Duet3D laser filament monitor, 6=Duet3D laser filament monitor with
microswitch, 7=pulse-generating sensor

Additional parameters for Duet3D laser filament monitor
:   **Raa:bb** Allow the filament movement reported by the sensor to be
    between aa% and bb% of the commanded values; if it is outside these
    values and filament monitoring is enabled, the print will be paused
:   **Enn** minimum extrusion length before a commanded/measured
    comparison is done, default 3mm

<!-- -->

Additional parameters for Duet3D rotating magnet filament monitor
:   **Lnn** Filament movement per complete rotation of the sense wheel,
    in mm
:   **R, E** As for Duet3D laser filament monitor

<!-- -->

Additional parameters for a pulse generating filament monitor
:   **Lnn** Filament movement per pulse in mm
:   **R, E** As for Duet3D laser filament monitor

<!-- -->

Examples
:   M591 D0 C3 P5 S1 R70:130 L24.8 E6.0 ; Duet3D laser sensor for
    extruder drive 0 is connected to E0 endstop input, 24.8mm/rev, 70%
    to 130% tolerance, 6mm detection length
:   M591 D1 ; display filament sensor parameters for extruder drive 1

Note: RepRapFirmware 1.19 and 1.20 also supported filament monitors via
M591, but some of the parameters were different.

#### M592: Configure nonlinear extrusion {#m592_configure_nonlinear_extrusion}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|2.2.0+}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes|1.20.1+}} | bfb={{no}} | machinekit={{no}}  | makerbot={{no}} | grbl={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   **Dnn** Extruder drive number (0, 1, 2\...)
:   **A**nnn A coefficient in the extrusion formula, default zero
:   **B**nnn B coefficient in the extrusion formula, default zero
:   **L**nnn Upper limit of the nonlinear extrusion compensation,
    default 0.2
:   **T** nnn Reserved for future use, for the temperature at which
    these values are valid

Example
:   M592 D0 A0.01 B0.0005 ; set parameters for extruder drive 0
:   M592 D0 ; report parameters for drive 0

Most extruder drives use toothed shafts to grip the filament and drive
it through the hot end. As the extrusion speed increases, so does the
back pressure from the hot end, and the increased back pressure causes
the amount of filament extruded per step taken by the extruder stepper
motor to reduce. This may be because at high back pressures, each tooth
compresses and skates over the surface of the filament for longer before
it manages to bite. See forum post
<http://forums.reprap.org/read.php?262,802277> and the graph at
<http://forums.reprap.org/file.php?262,file=100851,filename=graph.JPG>
for an example.

Nonlinear extrusion compensates for this effect. The amount of extrusion
requested is multiplied by (1 + MIN(L, A\*v + B\*v\^2)) where v is the
requested extrusion speed (calculated from the actual speed at which the
move will take place) in mm/sec.

Nonlinear extrusion is not applied to extruder-only movements such as
retractions and filament loading.

#### M593: Configure Input Shaping {#m593_configure_input_shaping}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}}<sup>2</sup> | prusa={{no}}| buddy={{yes}} <sup>1</sup>| repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes|3.4+}} | bfb={{no}} | machinekit={{no}}  | makerbot={{no}} | grbl={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
Note: RepRapFirmware 2.02 thru 3.2 implemented a primitive form of input
shaping called Dynamic Acceleration Adjustment, supporting just the F
parameter. This support has been replaced in RRF 3.4 and later by the
more sophisticated forms of input shaping described here.

Parameters
:   **P\"type\"** Type of input shaping to use, not case sensitive. RRF
    3.4 supports \"none\", \"zvd\", \"zvdd\", \"zvddd\", \"mzv\",
    \"ei2\", \"ei3\" and \"custom\". RRF 3.3 supports \"none\" or
    \"daa\", and if no P parameter is given but the F parameter is given
    then \"daa\" is assumed for compatibility with previous releases.
:   **Fnnn** Centre frequency of ringing to cancel in Hz
:   **Snnn** (optional) Damping factor of ringing to be cancelled,
    default 0.1.
:   **Lnnn** (optional) Minimum acceleration allowed, default
    10mm/sec\^2. Input shaping will not be applied if it requires the
    average acceleration to be reduced below this value.
:   **Hnn:nn\...** Amplitudes of each impulse except the last, normally
    below 1.0. Only used with P\"custom\" parameter.
:   **Tnn:nn** Durations of each impulse except the last. Only used with
    P\"custom\" parameter.

<!-- -->

Prusa-Buddy Parameters^1^
:   **X** Set the input shaper parameters only for the X axis. Also in
    Marlin 2.x^2^
:   **Y** Set the input shaper parameters only for the Y axis. Also in
    Marlin 2.x^2^
:   **W** Write current input shaper settings to EEPROM.
:   **Dnnn** Set damping ratio. Range 0 to 1. Also in Marlin 2.x^2^
:   **Fnnn** Set frequency. Greater or equal to 0. Also in Marlin 2.x^2^
:   **Tn** Set type. Range 0 to 5.
:   **Rnnn** Set vibration reduction. Greater than 0.

<!-- -->

Examples (RRF 3.4 and later)
:   M593 P\"zvd\" F40.5 ; use ZVD input shaping to cancel ringing at
    40.5Hz
:   M593 P\"none\" ; disable input shaping
:   M593 P\"custom\" H0.4:0.7 T0.0135:0.0135 ; use custom input shaping

Examples (RRF 3.3)
:   M593 P\"daa\" F40.5 ; use DAA to cancel ringing at 40.5Hz
:   M593 P\"none\" ; disable DAA

Examples (Prusa-Buddy)
:   M593 X T2 F50.7
:   M593 Y T2 F40.6

Input shaping is most useful to avoid exciting low-frequency ringing,
for which S-curve acceleration is ineffective and may make the ringing
worse. High-frequency ringing would be better countered by using S-curve
acceleration; however, low-frequency ringing is more of a problem in
most 3D printers.

The ringing frequencies are best measured using an accelerometer, for
which support is provided in RRF 3.3 and later. Alternatively, take a
print that exhibits ringing on the perimeters (for example a cube),
preferably printed single-wall or external-perimeters-first. Divide the
speed at which the outer perimeter was printed (in mm/sec) by the
distance between adjacent ringing peaks (in mm). When measuring the
distance between peaks, ignore peaks close to the corner where the
ringing started (these peaks will be spaced more closely because the
print head will have been accelerating in that area).

Cartesian and CoreXY printers will typically have different frequencies
of ringing for the X and Y axes. Note that X axis ringing causes
artefacts predominantly on the Y face of the test cube, and vice versa.
The more advanced forms of input shaping reduce ringing over a wide
range of frequencies (for example EI3 covers a range of about 3:1) so
that for printers that exhibit significant ringing on both X and Y axes,
it is normally possible to choose a shaper that cancels both.

High X and Y jerk values reduce the effectiveness of input shaping;
therefore you should set the X and Y jerk limits only as high as
necessary to allow curves to be printed smoothly.

#### M594: Enter/Leave Height Following mode {#m594_enterleave_height_following_mode}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes|3.0+}} | bfb={{no}} | machinekit={{no}}  | makerbot={{no}} | grbl={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} | klipper={{no}}}}
```

Parameters
:   **Pn** P1 = enter height following mode, P0 = leave height following
    mode

Height following mode allows the Z position of the tool to be controlled
by a PID controller using feedback from a sensor. See also M951.

If a movement command (e.g. G1) explicitly mentions the Z axis while
height following mode is active, existing moves in the pipeline will be
allowed to complete and the machine allowed to come to a standstill.
Then height following mode will be terminated and the new move executed.

#### M595: Set movement queue length {#m595_set_movement_queue_length}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes|3.2+}} | bfb={{no}} | machinekit={{no}}  | makerbot={{no}} | grbl={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} | klipper={{no}} }}
```

Parameters
:   **Pnn** Maximum number of moves held in the movement queue.
    RepRapFirmware uses this value to determine how many DDA objects to
    allocate.
:   **Snn** (optional) Number of pre-allocated per-motor movement
    objects. If the number of pre-allocated objects is insufficient,
    RepRapFirmware will attempt to allocate additional omnes dynamically
    when they are needed.

Different features of motion control firmware may have competing demands
on microcontroller RAM. In particular, operations that use many short
segments (e.g. laser rastering) need longer movement queues than typical
3D printing, but have fewer motors to control. This command allows the
movement queue parameters to be adjusted so that the queue can be
lengthened if necessary, or kept short if a long movement queue is not
needed and there are other demands on RAM.

M595 without any parameters reports the length of the movement queue and
the number of per-motor movement objects allocated.

#### M596: Select movement queue number {#m596_select_movement_queue_number}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes|3.5+}} | bfb={{no}} | machinekit={{no}}  | makerbot={{no}} | grbl={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} | klipper={{no}} }}
```

Parameters
:   **Pnn** Movement queue number. Queues are numbered 0 (the default
    queue), 1, \...

This command is supported in RepRapFirmware builds that can execute
moves on different axis systems asynchronously, for example for
concurrent printing of two or more different objects. It specifies that
subsequent GCode commands from this input channel should be routed to
the specified movement queue and the tool associated with that queue.

The number of available queues is firmware-dependent but will typically
be 2. Before using a movement queue other than queue 0 it may be
necessary to use M595 to increase the length of that queue, because the
default length of movement queues other than the primary one may be
quite short.

At the start of a file print, queue 0 is selected automatically.

If M596 is used without the P parameter, it reports the current motion
system number for the input channel that the command was received on.

#### M597: Collision avoidance {#m597_collision_avoidance}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes|3.5+}} | bfb={{no}} | machinekit={{no}}  | makerbot={{no}} | grbl={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} | klipper={{no}} }}
```

Parameters
:   **X,Y\...aaa** First axis identifier and value
:   **U,V\...bbb** Second axis identifier and value

Example
:   M597 V0 Y23.5

This configuration command is intended for use in systems having
multiple tool heads that can be moved independently and asynchronously.
The axis letters must be different from each other, so must the values
of *aaa* and *bbb*. Normally, *aaa* will be zero and *bbb* will be
positive. The command specifies that the machine position of the axis
with the higher value must always be at least the difference in values
greater than the position of the other axis. In the above example, the
position of the Y axis must always be at least 23.5mm greater than the
position of the V axis.

When Y and V are driven by independent motion systems and executing
moves independently, in any block of GCode between synchronisation
points, using this example the minimum of all Y coordinates inside the
block (including the initial Y coordinate) must be at least 23.5mm
greater than the maximum of the all V coordinates inside the block. If
this is not the case, the job will be aborted prior to starting the
first move that would cause the conflict.

#### M598: Sync motion systems {#m598_sync_motion_systems}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes|3.5+}} | bfb={{no}} | machinekit={{no}}  | makerbot={{no}} | grbl={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} | klipper={{no}} }}
```
This command has no parameters. It is for systems having multiple motion
systems that can be moved independently and asynchronously. It is only
valid within a job file. It causes the file reader for each motion
system to wait at this instruction until all the file readers have
reached it and all moves queued for any motion system have been
completed.

Example
:   M598 ; wait until all motion systems have finished working on this
    layer
:   G1 Z0.8 ; change Z for next layer

#### M599: Define keepout zone {#m599_define_keepout_zone}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes|3.5+}} | bfb={{no}} | machinekit={{no}}  | makerbot={{no}} | grbl={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} | klipper={{no}} }}
```

Parameters
:   **Pn** Keepout zone number, default 0
:   **Sn** (optional) S1 = activate keepout zone (default if any axes
    are specified), S0 = deactivate keepout zone
:   **X,Y\...aaa:bbb** Axis identifier and limits for that axis

Example
:   M599 X10:25 Y0:20

This command establishes a \"no entry\" zone for the toolhead reference
point. If any G0/G1/G2/G3 move attempts to move the toolhead reference
point inside the no entry zone, the job will be aborted with an error
message.

You may specify any number of axes, up to the number that the machine
has. If no axes are specified and the S parameter is not provided then
the parameters and enabled/disabled state of the existing keepout zone
will be reported.

Movement commands (G0, G1, G2 and G3) will normally be checked before
starting the move.

The number of keepout zones supported is implementation dependent. It
may be just one.

#### M600: Set line cross section {#m600_set_line_cross_section}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | reprapfirmware={{no}} | bfb={{no}} | machinekit={{yes}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Example

`M600 P0.061`

Sets the cross section for a line to extrude in velocity extrusion mode.
When the extruder is enabled and movement is executed the amount of
extruded filament will be calculated to match the specified line cross
section.

#### M600: Filament change pause {#m600_filament_change_pause}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{yes}}<sup>1</sup> | smoothie={{yes}} | reprapfirmware={{yes|2.02 and later}} | bfb={{no}} | machinekit={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```
Pause for filament change.

Parameters
:   `X[pos]`
:   `Y[pos]`
:   `Z[relative lift]`
:   `E[initial retract]`
:   `L[later retract distance for removal]`
:   `AUTO` Automatically (only Prusa Firmware with MMU connected)^1^
:   `N` (no return) Don\'t return to the previous position after
    filament change

<!-- -->

Example

`M600`

In SmoothieWare:

The variable \"after_suspend_gcode\" is run after `M600`.

For example:

after_suspend_gcode G91_G0E-5_G0Z10_G90_G0X-50Y-50 \# gcode to run after
suspend, retract then get head out of way

In RepRapFirmware, `M600` causes macro file filament-change.g to be run
if it exists, otherwise it falls back to pause.g. The parameters in the
`M600` command are ignored.

Notes

In Prusa Firmware this command is also used when the Filament Runout
Sensor triggers. To prevent filament blobs it will raise to 25 mm if it
has been triggered below 25 mm layer height. Default are X=211 mm, Y=0
mm, Z=2 mm, E=-2 mm, L=-80 mm^1^

#### M601: Pause print {#m601_pause_print}

```{=mediawiki}
{{Firmware Support | reprapfirmware={{yes|3.01 and later, or use M226}} | prusa={{yes}} }}
```
Without any parameters it will park the extruder to default or last set
position. The default pause position will be set during power up and a
reset, the new pause positions aren\'t permanent.

Usage
:   `M601 [ X | Y | Z | S ]` ^2^

<!-- -->

Parameters
:   `X` X position to park ^2^
:   `Y` Y position to park ^2^
:   `Z` Z raise before park ^2^
:   `S` Set values \[S0 = set to default values \| S1 = set values\]
    without pausing ^2^

^2^Prusa Firmware equivalent to M25 and M125

#### M602: Resume print {#m602_resume_print}

```{=mediawiki}
{{Firmware Support | reprapfirmware={{yes|Use M24}} | prusa={{yes}} }}
```
Resumes print on Prusa i3 MK2/s,MK2.5/s,MK3/s.

#### M603: Stop print (Prusa i3) {#m603_stop_print_prusa_i3}

```{=mediawiki}
{{Firmware Support | marlin={{no|M524}} | prusa={{yes}} }}
```
Stop print on Prusa i3 MK2/s, MK2.5/s, and MK3/s.

#### M603: Configure Filament Change {#m603_configure_filament_change}

```{=mediawiki}
{{Firmware Support | marlin={{yes}} | prusa={{yes|dev}} | buddy={{yes}} }}
```
This command configures Filament Change behavior in Marlin Firmware and
in Prusa mini firmware under development.

Parameters
:   `T[toolhead]` Select extruder to configure, active extruder if not
    specified (not used yet)
:   `U[distance]` Retract distance for removal, for the specified
    extruder.
:   `L[distance]` Extrude distance for insertion, for the specified
    extruder.

#### M605: Set dual x-carriage movement mode {#m605_set_dual_x_carriage_movement_mode}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | klipper={{no}} | smoothie={{no}} | reprapfirmware={{yes|Use M563}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```
Set Dual X-Carriage movement mode.

Parameters
:   `S[mode]` Mode (see below)
:   `X[duplication x-offset]` Optional X offset for Mode 2
:   `R[duplication temp offset]` Optional temperature difference for
    Mode 2

<!-- -->

Example

`M605 S1 ; Set mode to auto-park`

`M605 S0`: Full control mode. The slicer has full control over
x-carriage movement `M605 S1`: Auto-park mode. The inactive head will
auto park/unpark without slicer involvement `M605 S2 [Xnnn] [Rmmm]`:
Duplication mode. The second extruder will duplicate the first with nnn
millimeters x-offset and an optional differential hotend temperature of
`mmm` degrees. E.g., with \"`M605 S2 X100 R2`\" the second extruder will
duplicate the first with a spacing of 100mm in the x direction and 2
degrees hotter.

RepRapFirmware does not implement M605 because it supports dual carriage
mode, duplication mode, auto park, different temperatures etc. using the
`M563` tool definition command and the tool change macro files.

#### M606: Fork input file reader {#m606_fork_input_file_reader}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | klipper={{no}} | smoothie={{no}} | reprapfirmware={{yes}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `S[mode]` Mode, must be 1 (other values are reserved for future
    use).

Example
:   M606 S1 ; Fork input reader

This command is only supported on firmware configurations that support
two or more motion systems that execute asynchronously with respect to
each other.

If the S1 parameter is present and the command occurs within a job from
SD card or other storage media, it causes the input stream to be forked.
From that point on, each motion system can read and execute commands
from the job file independently of other motion systems. In consequence,
when the movement queue of one motion system becomes full, or one motion
system is waiting for a tool change or other action to complete, the
other motion system(s) can still read and execute commands. In the event
that this command is executed from a job file when the input stream has
already been forked, it is ignored.

If the S1 parameter is present and the command is used from an input
channel other than a file stream then a warning is issued but it is
otherwise ignored.

If this command is run without the S parameter then the firmware just
reports whether a job is being run from storage media, and if so whether
the input stream for that media has been forked.

See also the M596 command that selects a motion system, and the M598
command which is used to synchronise forked input streams at particular
point in the file.

#### M650: Set peel move parameters {#m650_set_peel_move_parameters}

```{=mediawiki}
{{Firmware Support | marlin={{no}} | prusa={{no}} | buddy={{no}} | grbl={{no}} | repetier={{no}} | redeem={{no}}| reprapfirmware={{yes|2.02}} }}
```
This command is sent by nanoDLP to set the parameters for the peel move
used after curing a layer. RepRapFirmware 2.02 ignores it. If using
RepRapFirmware 2.03 or later you can create a empty file M650.g to cause
it to be ignored.

#### M651: Execute peel move {#m651_execute_peel_move}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | klipper={{no}} | smoothie={{no}} | reprapfirmware={{yes|2.02}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
This command is sent by nanoDLP to execute a peel move after curing a
layer. RepRapFirmware 2.02 executes macro /sys/peel-move.g in response
to this command. For RepRapFirmware 2.03 and later, create a macro file
M651.g containing the commands required to execute the peel move.

#### M655: Send request to custom CAN-connected expansion board {#m655_send_request_to_custom_can_connected_expansion_board}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | klipper={{no}} | smoothie={{no}} | reprapfirmware={{yes|3.6}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `Bnn` CAN address of target board
:   `C"nn.string"` Reduced string parameter, for example CAN address and
    port name
:   `A"string"` Normal string parameter
:   `Pnnn` Unsigned integer parameter, maximum 65535
:   `R, S` Signed integer parameters
:   `E, F` Floating point parameters

<!-- -->

Examples

`M655 B10 C"hello world" P1 R-4 E0.123`\
`M655 C"10:pump" P0 S22 F42.1`

This command allows standard main board firmware builds to control
features on custom CAN-connected expansion boards in situations where
standard commands such as M950 and M42 are not suitable, for example
because they do not provide sufficient parameters. The main board
firmware expects to receive a standard reply to it.

All parameters are optional, except that exactly one of B or C must be
present. The C parameter if present must start with the CAN address of
the target board followed by a period. It will be \"reduced\" by
removing this prefix and any underscores or hyphens and converting all
characters to lowercase before sending the request to the target board.

The total number of bytes occupied by the parameters provided, excluding
the B parameter and after reducing the C parameter, must not exceed 60.
The number of bytes in a string parameter is the number of bytes in the
UTF8-encoded string plus 1. The P parameter occupies 2 bytes and the
signed integer and float parameters occupy 4 bytes each.

#### M665: Set delta configuration {#m665_set_delta_configuration}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | klipper={{no}} | smoothie={{yes}} | reprapfirmware={{yes}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   `Lnnn` Diagonal rod length
:   `Rnnn` Delta radius
:   `Snnn` Segments per second^1^
:   `Bnnn` Safe probing radius^2,3^
:   `Hnnn` Delta height defined as nozzle height above the bed when
    homed after allowing for endstop corrections ^2^

<!-- -->

:   `Xnnn` X tower position correction^2,4^
:   `Ynnn` Y tower position correction^2,4^
:   `Znnn` Z tower position correction^2,4^

<!-- -->

:   `Annn` X tower diagonal rod trim.^1^ (Marlin 2.0.6+)
:   `Bnnn` Y tower diagonal rod trim.^1^ (Marlin 2.0.6+)
:   `Cnnn` Z tower diagonal rod trim.^1^ (Marlin 2.0.6+)

<!-- -->

Examples

`M665 L250 R160 S200 ; (Marlin)`\
`M665 L250 R160 B80 H240 X0 Y0 Z0 ; (RepRapFirmware and Marlin 1.1.0)`

Set the delta calibration variables. (See the discussion page for notes
on this implementation.)

Notes

^1^Only supported on Marlin.

^2^Only supported in RepRapFirmware and Marlin 1.1.0.

^3^ In Marlin 1.1.0 sets the radius on which the probe points are taken
for the delta auto calibration routine G33 as well as for the manual LCD
calibration menu.

^4^X, Y and Z tower angular offsets from the ideal (i.e. equilateral
triangle) positions, in degrees, measured anti-clockwise looking down on
the printer. In Marlin 1.1.0 X,Y and Z tower angular offsets will be
rotated so the Z tower angular offset is zero.

#### M666: Set delta endstop adjustment {#m666_set_delta_endstop_adjustment}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{no}} | buddy={{no}} | repetier={{yes}} | smoothie={{yes}} | reprapfirmware={{yes}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   `Xnnn` X axis endstop adjustment
:   `Ynnn` Y axis endstop adjustment
:   `Znnn` Z axis endstop adjustment
:   `Annn` X bed tilt in percent^1^
:   `Bnnn` Y bed tilt in percent^1^

Example

`M666 X-0.1 Y+0.2 Z0`

Sets delta endstops adjustments.

In RepRapFirmware and Repetier, positive endstop adjustments move the
head closer to the bed when it is near the corresponding tower. In
Marlin and Smoothieware, negative endstop corrections move the head
closer to the bed when it is near the corresponding tower.

In Marlin, only negative endstop corrections are allowed. From version
1.1.0 onward positive endstops are allowed to be entered but the
endstops will be normalized to zero or negative and the residue will be
subtracted from the delta height defined in M665.

In Repetier the endstop corrections are expressed in motor steps. In
other firmwares they are expressed in mm.

^1^RepRapFirmware 1.16 and later.

#### M667: Select CoreXY mode {#m667_select_corexy_mode}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   `Snnn` CoreXY mode
:   `Xnnn` X axis scale factor (RepRapFirmware 2.02 and earlier)
:   `Ynnn` Y axis scale factor (RepRapFirmware 2.02 and earlier)
:   `Znnn` Z axis scale factor (RepRapFirmware 2.02 and earlier)

Example

`M667 S1`

`M667 S0` selects Cartesian mode (unless the printer is configured as a
delta using the `M665` command). Forward motion of the X motor moves the
head in the +X direction. Similarly for the Y motor and Y axis, and the
Z motor and Z axis. This is the default state of the firmware on power
up.

`M667 S1` selects CoreXY mode. Forward movement of the X motor moves the
head in the +X and +Y directions. Forward movement of the Y motor moves
the head in the -X and +Y directions.

`M667 S2` selects CoreXZ mode. Forward movement of the X motor moves the
head in the +X and +Z directions. Forward movement of the Z motor moves
the head in the -X and +Z directions.

RepRapFirmware 2.03 and earlier support additional parameters X, Y and Z
may be given to specify factors to scale the motor movements by for the
corresponding axes. For example, to specify a CoreXZ machine in which
the Z axis moves 1/3 of the distance of the X axis for the same motor
movement, use M667 S2 Z3. The default scaling factor after power up is
1.0 for all axes. In RepRapFirmware 2.03 and later, this functionality
is moved to the movement matrix that you can define or alter using the
M669 command.

To change the motor directions, see the M569 command.

#### M668: Set Z-offset compensations polynomial {#m668_set_z_offset_compensations_polynomial}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{partial|dc42-cmm}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
Polynomial compensation is an experimental method to compensate for
geometric distortion of a delta machine Z-plane. After the bed is
compensated with the set of G30 points, there remains error. This method
fits a 6th degree polynomial with independent origins for each order to
the residual error data (using a simulated annealing technique on the
host). The polynomial is communicated and controlled through `M668`.
Because the polynomial takes many floating point operations to compute
each point, the firmware builds a grid of values, and used bi-linear
interpolation to adjust the actual Z-axis offset error estimate.

For the polynomial used, 40 parameters are specified. The `I` parameter
allows the coefficients to be loaded a few at a time, which limits the
size of the G-code string. The index starts with 1, not with 0.

`M668 Ix S[list of values]` sets the polynomial parameters starting at
index x, if index present and != 0.

`M668 R` recomputes the grid based on the current parameters.

`M668 P[0|1]` turns off or on the polynomial compensation.

Typical usage:

`M668 I1 S4.882E-17:0.0`\
`M668 I3 ...`\
`...`\
`M668 R P1`

Which sets the list, computes the interpolation grid, and then enables
compensation.

#### M669: Set kinematics type and kinematics parameters {#m669_set_kinematics_type_and_kinematics_parameters}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes|1.19+}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   **Knnn** Kinematics type: 0 = Cartesian, 1 = CoreXY, 2 = CoreXZ, 3 =
    linear delta, 4 = serial SCARA, 5 = CoreXYU, 6 = Hangprinter, 7 =
    polar, 8 = CoreXYUV, 9 = linear delta + Z axis, 10 = rotary delta,
    11 = MarkForged, 12 = reserved for Collinear Tripteron

Selects the specified kinematics, then uses the other parameters to
configure it. If the K parameter is missing then the other parameters
are used to update the configuration data for the current kinematics. If
no parameters are given then the current kinematics and configuration
parameters are reported

Parameters for generalised Cartesian kinematics (including CoreXY, CoreXZ, MarkForged, CoreXYU etc.)
:   **Xnnn**, **Ynnn**, **Znnn**, **Unnn** etc. (optional) Movement
    matrix coefficients. For example. `X1:-1:0` tells the firmware that
    to move the X axis one unit, the first motor must be moved 1 unit in
    the forwards direction, the second motor 1 unit in the reverse
    direction, and the third motor not at all. Using these coefficients,
    you can specify the kinematics equations for any printer with up to
    10 axes for which the movement of each axis is a linear combination
    of the movements of the individual motors. If these parameters are
    omitted, the defaults for the specified kinematics (K parameter)
    will be used.

<!-- -->

Parameters for serial SCARA kinematics
:   **Pnnn** Proximal arm length (mm)
:   **Dnnn** Distal arm length (mm)
:   **Annn:nnn** Proximal arm joint movement minimum and maximum angles,
    in degrees anticlockwise seen from above relative to the X axis
:   **Bnnn:nnn** Proximal-to-distal arm joint movement minimum and
    maximum angles, in degrees anticlockwise seen from above relative to
    both arms in line
:   **Cnnn:nnn:nnn** Crosstalk factors. The first component is the
    proximal motor steps to equivalent distal steps factor, the second
    is the proximal motor steps to equivalent Z motor steps factor, and
    the third component is the distal motor steps to equivalent Z motor
    steps factor.
:   **Snnn** Segments per second if smooth XY motion is approximated by
    means of segmentation
:   **Tnnn** Minimum segment length (mm) if smooth XY motion is
    approximated by means of segmentation
:   **Xnnn** X offset of bed origin from proximal joint
:   **Ynnn** Y offset of bed origin from proximal joint

Examples

`M669 K4 P300 D250 A-90:90 B-135:135 C0:0:0 S200 X300 Y0`

The minimum and maximum arm angles are also the arm angles assumed by
the firmware when the homing switches are triggered. The P, D, A and B
parameters are mandatory. The C and F parameters default to zero, and
the segmentation parameters default to firmware-dependent values.

Parameters for Polar kinematics
:   **Raaa:bbb** Minimum and maximum radius in mm. If only one value it
    given it will be used as the maximum radius, and the minimum radius
    will be assumed to be zero.\
:   **Hnnn** Radius in mm at which the homing switch is triggered during
    a homing move. If this parameter is not present, the homing switch
    is assumed to trigger at the minimum radius.\
:   **Fnnn** Maximum turntable speed in degrees per second
:   **Annn** Maximum turntable acceleration in degrees per second per
    second
:   **Snnn**, **Tnnn** As for serial SCARA kinematics

#### M670: Set IO port bit mapping {#m670_set_io_port_bit_mapping}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes|1.19+}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   **Pnn:nn:nn\...** List of logical port numbers that bits 0, 1, 2\...
    control
:   **Tnnn** port switching time advance in milliseconds

RepRapFirmware 1.19 and later provides an optional P parameter on the G1
command to allow I/O ports to be set to specified states for the
duration of the move. The argument to the P parameter is a bitmap giving
the required state of each port. The M669 command specifies the mapping
between the bits of that argument and logical port numbers. Optionally,
the T parameter can be used to advance the I/O port switching a short
time before the corresponding move begins.

#### M671: Define positions of Z leadscrews or bed leveling screws {#m671_define_positions_of_z_leadscrews_or_bed_leveling_screws}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no|M422}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes|1.19+}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   **Xnn:nn:nn\...** List of between 2 and 4 X coordinates of the
    leadscrews that drive the Z axis or the bed leveling screws
:   **Ynn:nn:nn\...** List of between 2 and 4 Y coordinates of the
    leadscrews that drive the Z axis or the bed leveling screws
:   **Snn** Maximum correction to apply to each leadscrew in mm
    (optional, default 1.0)
:   **Pnnn** Pitch of the bed leveling screws (not used when bed
    leveling using independently-driven leadscrews). Defaults to 0.5mm
    which is correct for M3 bed leveling screws.

Example
:   M671 X-15.0:100.0:215.0 Y220.0:-20.0:220.0 ; Z leadscrews are at
    (-15,220), (100,-20) and (215,220)

Informs the firmware of the positions of the leadscrews used to
raise/lower the bed or gantry. The numbers of X and Y coordinates must
both be equal to the number of drivers used for the Z axis (see the M584
command). This allows the firmware to perform bed leveling by adjusting
the leadscrew motors individually after bed probing.

For machines without multiple independently-driven Z leadscrews, this
command can be used to define the positions of the bed leveling screws
instead. Then bed probing can be used to calculate and display the
adjustment required to each screw to level the bed. The thread pitch (P
parameter) is used to translate the height adjustment needed to the
number of turns of the leveling screws.

#### M672: Program Z probe {#m672_program_z_probe}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes|1.19+}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   **Snn:nn:nn\...** Sequence of 8-bit unsigned values to send to the
    currently-selected Z probe

Example
:   M671 S50:205

This command is for sending configuration data to programmable Z probes
such as the Duet3D delta effector. The specified command bytes are sent
to the probe. The Duet3D probe stores the configuration data in
non-volatile memory, so there is no need to send this command every time
the probe is used.

#### M673: Align plane on rotary axis {#m673_align_plane_on_rotary_axis}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes|2.02+}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   **U,V,W,A,B,C** Rotary axis letter on which the plane is mounted
:   **Pnnn** Factor to multiply the correction angle (degrees) with
    (defaults to 1)

Example
:   M673 A

This code is intended to align a plane that is mounted on a rotary axis.
To make use of this code it is required to take two probe points via G30
P first. Supported in RepRapFirmware 2.02 and later.

#### M674: Set Z to center point {#m674_set_z_to_center_point}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{partial|TBD}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
This code is intended to determine the Z center point of a stash that is
mounted on a rotary axis. This code is yet to be implemented.

#### M675: Find center of cavity {#m675_find_center_of_cavity}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes|2.02+}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   **X,Y,Z** Axis to probe on
:   **Fnnnn** Probing feedrate
:   **Rnnn** Distance to move away from the lower endstop before the
    next probing move starts

Example
:   M675 X R2 F1200

This code is intended to find the center of a cavity that can be
measured using the configured axis endstop. If using a Z probe for this
purpose, make sure the endstop type for the corresponding axis is
updated before this code is run. Once this code starts, RepRapFirmware
will move to the lower end looking for an endstop to be triggered. Once
it is triggered, the lower position is saved and the axis maximum is
probed. As soon as both triggers have been hit, the center point is
calculated and the machine moves to the calculated point.

#### M700: Level plate {#m700_level_plate}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{partial|M671,G32}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | makerbot={{no}} | grbl={{no}} | redeem={{no}} | mk4duo={{no}} }}
```

Example

`M700`

Script to adjust the plate level.

#### M701: Load filament {#m701_load_filament}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{yes}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{yes|1.19+}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | makerbot={{no}} | grbl={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```
Initiate a filament load. *This command can be used without any
additional parameters.*

Parameters
:   `Snn` Filament to load (RepRapFirmware)
:   `Tnn` Tool to load (Marlin)
:   `Lnn` Length to use for load (Marlin)
:   `Znn` Z raise to perform (Marlin)

<!-- -->

With no parameters:

- RepRapFirmware will report the name of the loaded filament (if any).
- Marlin Firmware initiates a Filament Load.

Examples

`M701`\
`M701 S"PLA" ; Only in RepRapFirmware`\
`M701 T0     ; Only in Marlin.`

RepRapFirmware 1.19 and later implement a filament management mechanism
to load and unload different materials. This code may be used to load a
material for the active tool, however be aware that this code will work
only for tools that have exactly one extruder assigned. When called
RepRapFirmware will\...

1.  Run the macro file \"load.g\" in the subdirectory of the given
    material (e.g. /filaments/PLA/load.g)
2.  Change the filament name of the associated tool, so it can be
    reported back to Duet Web Control

#### M702: Unload filament {#m702_unload_filament}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{yes}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{yes|1.19+}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | makerbot={{no}} | grbl={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```
Initiate a filament unload. *This command can be used without any
additional parameters.* In contrast to `M701` this code is intended to
unload the previously loaded filament from the selected tool.

Parameters
:   `Tnn` Tool to load (Marlin)
:   `Unn` Length to use for unload (Marlin & Prusa Firmware)
:   `Znn` Z raise to perform (Marlin & Prusa Firmware)

<!-- -->

:   `Cnn` Unload the (current) filament only if the MMU is used in Prusa
    Firmware till version 3.12.2

In response to `M702` RepRapFirmware will do the following:

1.  Run the macro file \"unload.g\" in the subdirectory of the given
    material (e.g. `/filaments/PLA/unload.g`)
2.  Change the filament name of the current tool, so it can be reported
    back to Duet Web Control

Examples

`M702         ; Unload filament as previously configured`\
`M702 U420 Z2 ; Unload 420mm (Marlin & Prusa Firmware) with a Z raise of 2mm`

#### M703: Configure Filament {#m703_configure_filament}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{yes}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | makerbot={{no}} | grbl={{no}} | redeem={{no}} | mk4duo={{no}} }}
```
1.  In RepRapFirmware this code is used to apply the configuration of a
    previously loaded filament (see M701). All it does is run
    `/filaments/``<loaded filament>`{=html}`/config.g` which may contain
    codes to set parameters like extrusion factor, retraction distances
    and temperatures. If no filament is assigned to the current tool,
    this code will not generate a warning.

If the filaments feature is used, it is recommended to put this code
into `tpost*.g` to ensure the right filament parameters are set.
Supported in RepRapFirmware 2.02 and newer.

#### M704: Preload_to_MMU {#m704_preload_to_mmu}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{yes}}<sup>1</sup> | buddy={{yes}}<sup>2</sup> | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | makerbot={{no}} | grbl={{no}} | redeem={{no}} | mk4duo={{no}} }}
```
Preload filament to MMU can be used to manually load the filament into
the MMU.

The MMU will engage the slot and turn the MMU idler pulley until the
filament is pushed to the FINDA.

A second unload/load check ensures that the filament is preloaded
correctly to the MMU.

Usage

`M704 [P]`

Parameters
:   `Pnn` Index of slot (zero based from 0 to 4)

<!-- -->

With no parameters:

Does nothing if the `P` parameter is not present or if MMU is not
enabled.

Examples

`M704 P0` ;Start preload procedure at slot 0

Supported on Prusa MK3S+ from firmware version 3.13.0 with MMU firmware
2.1.9 and newer. ^1^

Support for MK4 with MMU TBA^2^

#### M705: Eject filament {#m705_eject_filament}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{yes}}<sup>1</sup> | buddy={{yes}}<sup>2</sup> | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | makerbot={{no}} | grbl={{no}} | redeem={{no}} | mk4duo={{no}} }}
```
Eject filament on MMU moves the selector away from the selected slot and
pushes some mm of filament towards the front. This is useful to inspect
the filament for indents and other issues.

**Attention: User interaction is needed to confirm on LCD or MMU button
that the inspection, maintenance, \... is done! Printer WILL NOT accept
any other gcode.**

Usage

`M705 [P]`

Parameters
:   `Pnn` Index of slot (zero based from 0 to 4)

<!-- -->

With no parameters:

Does nothing if the `P` parameter is not present or if MMU is not
enabled.

Examples

`M705 P0` ;Eject filament at slot 0

Supported on Prusa MK3S+ from firmware version 3.13.0 with MMU firmware
2.1.9 and newer. ^1^

Support for MK4 with MMU TBA^2^

#### M706: Cut filament {#m706_cut_filament}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{yes}}<sup>1</sup> | buddy={{yes}}<sup>2</sup> | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | makerbot={{no}} | grbl={{no}} | redeem={{no}} | mk4duo={{no}} }}
```
Preload filament to MMU can be used to manually load the filament into
the MMU.

The MMU will engage the slot and turn the MMU Idler pulley until the
filament is pushed to the FINDA.

A second unload/load check ensures that the filament is preloaded
correctly to the MMU.

Usage

`M706 [P]`

Parameters
:   `Pnn` Index of slot (zero based from 0 to 4)

<!-- -->

With no parameters:

Does nothing if the `P` parameter is not present or if MMU is not
enabled.

Examples

`M706 P0` ;Cut filament at slot 0

Supported on Prusa MK3S+ from firmware version 3.13.0 with MMU firmware
2.1.9 and newer. ^1^

Support for MK4 with MMU TBA^2^

#### M707: Read from MMU register {#m707_read_from_mmu_register}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{yes}}<sup>1</sup> | buddy={{yes}}<sup>2</sup> | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | makerbot={{no}} | grbl={{no}} | redeem={{no}} | mk4duo={{no}} }}
```
Reads the MMU register.

Usage

`M707 [A]`

Parameters
:   `A0xnn` Address of register in hexadecimal.

<!-- -->

With no parameters:

Does nothing if the `A` parameter is not present or if MMU is not
enabled.

Examples

`M707 A0x1b` ;Read a 8bit integer from register 0x1b and prints the
result onto the serial line.

Supported on Prusa MK3S+ from firmware version 3.13.0 with MMU firmware
2.1.9 and newer. ^1^

Support for MK4 with MMU TBA^2^

#### M708: Write to MMU register {#m708_write_to_mmu_register}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{yes}}<sup>1</sup> | buddy={{yes}}<sup>2</sup> | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | makerbot={{no}} | grbl={{no}} | redeem={{no}} | mk4duo={{no}} }}
```
Write to the MMU register.

Usage

`M708 [A | X]`

Parameters
:   `A0xnn` Address of register in hexadecimal.
:   `Xnnnn` Data to write (16-bit integer). Default value 0.

<!-- -->

With no parameters:

Does nothing if the `A` parameter is not present or if MMU is not
enabled.

Examples

`M708 A0x1b X05` ;Write to register 0x1b the value 05.

Supported on Prusa MK3S+ from firmware version 3.13.0 with MMU firmware
2.1.9 and newer. ^1^

Support for MK4 with MMU TBA^2^

#### M709: MMU power & reset {#m709_mmu_power_reset}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{yes}}<sup>1</sup> | buddy={{yes}}<sup>2</sup> | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | makerbot={{no}} | grbl={{no}} | redeem={{no}} | mk4duo={{no}} }}
```
The MK3S cannot not power off the MMU, but we can en- and disable the
MMU and will be also stored in EEPROM.

The new state of the MMU is stored in printer\'s EEPROM - i.e. if you
disable the MMU via M709, it will not be activated after the printer
resets.

Usage

`M709 [S|X]`

Parameters
:   `Xnnnn` Reset MMU (0:soft reset \| 1:hardware reset \| 42: erase MMU
    eeprom)
:   `Snnnn` En-/disable the MMU (0:off \| 1:on)

<!-- -->

Examples

`M709 X0` ;issue an X0 command via communication into the MMU (soft
reset)

`M709 X1` ;toggle the MMU\'s reset pin (hardware reset)

`M709 X42` ;erase MMU EEPROM

`M709 S1` ;enable MMU

`M709 S0` ;disable MMU

`M709` ;Serial message if en- or disabled ^1^

Supported on Prusa MK3S+ from firmware version 3.13.0 with MMU firmware
2.1.9 and newer. ^1^

Supported on Prusa MK4 from firmware version 5.1.0 with MMU firmware
3.0.1 and newer. ^2^

#### M710: Firmware dependent {#m710_firmware_dependent}

##### M710: Controller Fan settings {#m710_controller_fan_settings}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|2.0.5.2+}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | klipper={{no}} | bfb={{no}} | machinekit={{no}} | makerbot={{no}} | grbl={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   *With no parameters, report current settings.*
:   `A[bool]` Turn Auto Mode on or off.
:   `Snnn` Set the Active Speed (0-255) used when motors are enabled.
:   `Innn` Set the Idle Speed (0-255) used when motors are disabled.
:   `Dnnn` Set the Idle Duration (seconds) to keep the fan running after
    motors are disabled.
:   `R` Reset to defaults.

<!-- -->

Example

`M710 S200 ; Set "active" fan speed to 200`

##### M710: Erase the EEPROM and reset the board {#m710_erase_the_eeprom_and_reset_the_board}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{partial|M999}} | smoothie={{no}} | klipper={{no}} | bfb={{no}} | machinekit={{no}} | makerbot={{no}} | grbl={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
This command only exists in a defunct bq fork of Marlin Firmware.

Example

`M710`

#### M711: Calibrate pressure advance {#m711_calibrate_pressure_advance}

#### M750: Enable 3D scanner extension {#m750_enable_3d_scanner_extension}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{yes|1.18+}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | makerbot={{no}} | grbl={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Example

`M750`

This code may be used as an OEM extension to enable scanner
functionality in the firmware. After a regular start of RepRapFirmware,
the 3D scan extension is disabled by default, but if additional scanner
components are attached, this code may be used to enable certain OEM
functions.

#### M751: Register 3D scanner extension over USB {#m751_register_3d_scanner_extension_over_usb}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{yes|1.18+}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | makerbot={{no}} | grbl={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Example

`M751`

When a 3D scanner board is attached to the USB port, this code is used
to turn on communication between the 3D printing and the scanner board.
If the USB connection is removed while the 3D scanner configuration is
active, the firmware will disable it again and restore the default
communication parameters.

#### M752: Start 3D scan {#m752_start_3d_scan}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{yes|1.18+}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | makerbot={{no}} | grbl={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `Snnn`: Length/degrees of the scan
:   `Rnnn`: Resolution (new in RRF 2.0) \[optional, defaults to 100\]
:   `Nnnn`: Scanner mode (new in RRF 2.0) \[optional, 0=Linear
    (default), 1=Rotary\]
:   `Pnnn`: Filename for the scan

Example

`M752 S300 Pmyscan`

Instruct the attached 3D scanner to initiate a new 3D scan and to upload
it to the board\'s SD card (i.e. in the \"scans\" directory). Before the
SCAN command is sent to the scanner, the macro file \"scan_pre.g\" is
executed and when the scan has finished, the macro file \"scan_post.g\"
is run. Be aware that both files must exist to avoid error messages.

#### M753: Cancel current 3D scanner action {#m753_cancel_current_3d_scanner_action}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{yes|1.18+}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | makerbot={{no}} | grbl={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Example

`M753`

Instruct the attached 3D scanner to cancel the current operation.
Cancelling uploads is not supported.

#### M754: Calibrate 3D scanner {#m754_calibrate_3d_scanner}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{yes|1.18+}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | makerbot={{no}} | grbl={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   **Nnnn** Calibration mode (0=linear \[default\], 1=rotary)

<!-- -->

Example

`M754`

Calibrates the attached 3D scanner. Before the calibration is performed
by the external scanner, \"calibrate_pre.g\" is run and when it is
complete, \"calibrate_post.g\" is executed.

#### M755: Set alignment mode for 3D scanner {#m755_set_alignment_mode_for_3d_scanner}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{yes|1.18+}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | makerbot={{no}} | grbl={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `Pnnn` Whether to turn on (\> 0) or off (\<= 0) the alignment
    feature

Examples

`M755 P1`\
`M755 P0`

Sends the ALIGN ON/OFF command the attached 3D scanner. Some devices
turn on a laser when this command is received. If the \'P\' parameter is
missing, equal to, or less than 0, the alignment feature is turned off.
Depending on whether the alignment is turned on or off, either
align_on.g or align_off.g is executed before the ALIGN command is sent
to the scanner.

#### M756: Shutdown 3D scanner {#m756_shutdown_3d_scanner}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{yes|1.18+}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | makerbot={{no}} | grbl={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Example

`M756`

Sends the SHUTDOWN command the attached 3D scanner.

#### M800: Fire start print procedure {#m800_fire_start_print_procedure}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{partial|bq}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | makerbot={{no}} | grbl={{no}} | redeem={{no}} | mk4duo={{no}} }}
```
^1^ only in bq-Marlin Firmware

Example

`M800`

#### M801: Fire end print procedure {#m801_fire_end_print_procedure}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{partial|bq}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | makerbot={{no}} | grbl={{no}} | redeem={{no}} | mk4duo={{partial|bq}} }}
```
^1^ only in bq-Marlin Firmware

Example

`M801`

#### M808: Set or Goto Repeat Marker {#m808_set_or_goto_repeat_marker}

```{=mediawiki}
{{Firmware Support | fived={{no}} | yaskawa={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|2.0.8}} | druid={{no}} | repetier={{no}} | reprapfirmware={{partial|Planned for 3.3}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | grbl={{no}} | redeem={{no}} | prusa={{no}} | buddy={{no}} | klipper={{no}} | mk4duo={{no}} | makerbot={{no}} }}
```
The `M808 L[count]` command is used in a G-code file to set a Repeat
Marker beginning at the start of the following line. For an SD print,
the firmware will save a marker with the file\'s byte position and the
count given by the `L` parameter. To set an infinite loop use `L0`. To
terminate an infinite loop from the host, `M808 K` will cancel all
current loops.

The `M808` command (no parameters) will cause G-code processing to loop
back to the previous Repeat Marker as many times as specified. Ideally,
each instance of `M808 L` should have a corresponding `M808`.

The number of nested `M808 L` commands is limited to the depth set in
the firmware. To enable this feature in Marlin, define
`GCODE_REPEAT_MARKERS`. Hosts should look for
[`Cap:REPEAT`](Cap:REPEAT). At this time the feature only applies to
printing direct from media and otherwise `M808` is ignored, so host
developers are free to come up with their own approach to these codes
with no nesting limit and make it work with any old firmware.

Example

`M808 L10        ; Set Marker to repeat 10 times`\
`M300 P100 S440  ; Beep!`\
`M300 P10 S0     ; Silence`\
`M808            ; End Marker`

RepRapFirmware processes M808 as follows:

:   \- **M808 S{*ccc*}** translates into **while *ccc*** followed by
    block begin. *ccc* must yield *true* or *false*. For more on
    while-loops and expressions in RepRapFirmware, see
    <https://duet3d.dozuki.com/Wiki/GCode_Meta_Commands>.
:   \- *\'M808 L*nn**\'\' is equivalent to**M808 S{*nn* == 0 \|\|
    iterations \< *nn*}\'\'\'.
:   \- **M808** without S or L parameter ends the block.
:   \- As usual, predefined constant *iterations* reports the number of
    completed iterations of the innermost loop.
:   \- **M808** without S or L parameter when not inside a loop, or any
    M808 command in an input stream other than a SD print file, gives
    rise to an error message.

##### M808 in Marlin 2.0.8 {#m808_in_marlin_2.0.8}

`M808 L         ; Set marker to repeat infinitely`\
`M300 P100 S440 ; Beep!`\
`M300 P10 S0    ; Silence`\
`M808           ; End marker`\
`M808 K         ; Sent from host to cancel the loop`

#### M810-M819: Temporary G-code macros {#m810_m819_temporary_g_code_macros}

```{=mediawiki}
{{Firmware Support | marlin={{yes|2.0.0+}} | reprapfirmware={{no}} | klipper={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | druid={{no}} | mk4duo={{no}} | makerbot={{no}} | grbl={{no}} | sprinter={{no}} | bfb={{no}} | fived={{no}} | machinekit={{no}} | redeem={{no}} | teacup={{no}} | yaskawa={{no}} }}
```
Use the `M810`-`M819` commands to set and execute 10 distinct G-code
"macros." Any G-code following the command defines the macro. To run the
macro just send `M810`-`M819` by itself. Multiple commands must be
separated by the pipe character ('\|'). To run a defined macro type
`M810`-`M819` with no comments.

These macros do not persist after shutdown. They are intended to be
defined and used within a print session.

Define the `M815` macro to do some moves and make a beep:

Example

`M815 G0 X0 Y0|G0 Z10|M300 S440 P50`

Running the macro:

`M815`

#### M820: Report Temporary G-code macros {#m820_report_temporary_g_code_macros}

```{=mediawiki}
{{Firmware Support | marlin={{yes|2.1.3+}} | reprapfirmware={{no}} | klipper={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | druid={{no}} | mk4duo={{no}} | makerbot={{no}} | grbl={{no}} | sprinter={{no}} | bfb={{no}} | fived={{no}} | machinekit={{no}} | redeem={{no}} | teacup={{no}} | yaskawa={{no}} }}
```
Send `M820` to get a report of the macros defined by `M810`-`M819`.

#### M850: Sheet parameters {#m850_sheet_parameters}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{yes}} | buddy={{no}} | druid={{no}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
Get and Set Sheet parameters

Usage
:   `M850 [ S | Z | L | B | P | A ]`

<!-- -->

Parameters
:   `S` Sheet id \[0-7\]
:   `Z` Z offset
:   `L` Label \[aA-zZ, 0-9 max 7 chars\]
:   `B` Bed temp
:   `P` PINDA temp
:   `A` Active \[0\|1\]

#### M851: Set Z-Probe Offset {#m851_set_z_probe_offset}

```{=mediawiki}
{{Firmware Support | marlin={{yes}} | prusa={{yes}} | buddy={{no}} | druid={{wip}} | reprapfirmware={{yes|2.02 and later, or use G31}} | mk4duo={{yes}} | yaskawa={{no}} }}
```
Sets the Z-probe Z offset. This offset is used to determine the actual Z
position of the nozzle when using a probe to home Z with `G28`. This
value may also be used by `G29` to apply correction to the Z position.

This value represents the distance from nozzle to the bed surface at the
point where the probe is triggered. This value will be negative for
typical switch probes, inductive probes, and setups where the nozzle
makes a circuit with a raised metal contact. This setting will be
greater than zero on machines where the nozzle itself is used as the
probe, pressing down on the bed to press a switch (this is a common
setup on Delta machines).

This setting is saved in the EEPROM by M500 and restored by `M501`. The
default (as reset by `M502`) is set by the
`Z_PROBE_OFFSET_FROM_EXTRUDER` setting in Configuration.h.

Note that in Marlin 1.1.0 and later `M851` sets the value literally as
given, while Marlin 1.0.2 negates the absolute value.

The examples below will set the Z-probe Z offset to -4 mm (below the
nozzle):

##### M851 in Marlin 1.0.2 {#m851_in_marlin_1.0.2}

`M851 Z4 ; Set the Z probe offset to -4`

##### M851 in Marlin 1.1.0 {#m851_in_marlin_1.1.0}

`M851 Z-4 ; Set the Z probe offset to -4`

##### M851 in Marlin 2.0.0 {#m851_in_marlin_2.0.0}

`M851 X-22 Y3 Z-4 ; Set the probe XYZ offsets`

##### M851 in MK4duo 4.3.25 {#m851_in_mk4duo_4.3.25}

`M851 X2 Y-5 Z-4 ; Set the probe offset to X=2, Y=-5 and Z=-4`

##### M851 in RepRapFirmware 2.02 and later {#m851_in_reprapfirmware_2.02_and_later}

M851 Znn is implemented for backwards compatibility with other
firmwares. It sets the Z probe trigger in the same way as G31 Z-nn (note
the sign reversal). It also flags the Z-probe G31 parameters as to be
saved in config-override.g if the M500 command is used.

#### M855 Set Axis Length {#m855_set_axis_length}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{no}} | bfb={{no}} | makerbot={{no}} | grbl={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `Xnnnn` Sets X axis length
:   `Ynnnn` Sets Y axis length
:   `Znnnn` Sets Z axis length

#### M860 Wait for Probe Temperature {#m860_wait_for_probe_temperature}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{yes}} | buddy={{no}} | druid={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{no}} | bfb={{no}} | makerbot={{no}} | grbl={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `Snnnn` Target temperature

<!-- -->

Notes

In [Prusa Firmware](Prusa_Firmware "Prusa Firmware"){.wikilink} this
command will wait for the PINDA thermistor to reach a target
temperature.

#### M861 Set Probe Thermal Compensation {#m861_set_probe_thermal_compensation}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{yes}} | buddy={{no}} | druid={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes|Use G31}} | bfb={{no}} | makerbot={{no}} | grbl={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `?` Print current EEPROM offset values
:   `!` Set factory default values
:   `Z` Set all values to 0 (effectively disabling PINDA temperature
    compensation)
:   `S` Microsteps
:   `I` Table index

<!-- -->

Example

`M861 ?`

Results

`PINDA cal status: 1`\
`index, temp, ustep, um`\
`n/a, 35, 0, 0.00`\
`0, 40, 0, 0.00`\
`1, 45, 0, 0.00`\
`2, 50, 0, 0.00`\
`3, 55, 0, 0.00`\
`4, 60, 0, 0.00`

Notes

In [Prusa Firmware](Prusa_Firmware "Prusa Firmware"){.wikilink} this
command will set / read the PINDA temperature compensation offsets.

#### M862: Print checking {#m862_print_checking}

```{=mediawiki}
{{Firmware Support | prusa={{yes}} | buddy={{no}} | druid={{no}} }}
```
Checks the parameters of the printer and gcode and performs
compatibility check

##### M862.1: Check nozzle diameter {#m862.1_check_nozzle_diameter}

```{=mediawiki}
{{Firmware Support | prusa={{yes}} | buddy={{no}} | druid={{no}} }}
```

Parameters
:   `Pnnnn` nnnn = Nozzle diameter 0.25 /0.40 /0.60
:   `Q` Current nozzle diameter

When run with P\<\> argument, the check is performed against the input
value. When run with Q argument, the current value is shown.

Example messages
:   `warn` *Printer nozzle diameter differs from the G-code. Continue?*
:   `strict` *Printer nozzle diameter differs from the G-code. Please
    check the value in settings. Print cancelled.*

##### M862.2: Check model code {#m862.2_check_model_code}

```{=mediawiki}
{{Firmware Support | prusa={{yes}} | buddy={{no}} | druid={{no}} }}
```

Parameters
:   `Pnnnn` nnnn = Prusa model
:   `Q` Current model

When run with P\<\> argument, the check is performed against the input
value. When run with Q argument, the current value is shown.

Accepted printer type identifiers and their numeric counterparts:

`     - MK1         (100)`\
`     - MK2         (200)       `\
`     - MK2MM       (201)     `\
`     - MK2S        (202)      `\
`     - MK2SMM      (203)    `\
`     - MK2.5       (250)     `\
`     - MK2.5MMU2   (20250) `\
`     - MK2.5S      (252)    `\
`     - MK2.5SMMU2S (20252)`\
`     - MK3         (300)`\
`     - MK3MMU2     (20300)`\
`     - MK3S        (302)`\
`     - MK3SMMU2S   (20302)`

Example messages
:   `warn` *G-code sliced for a different printer type. Continue?*
:   `strict` *G-code sliced for a different printer type. Please
    re-slice the model again. Print cancelled.*

##### M862.3: Model name {#m862.3_model_name}

```{=mediawiki}
{{Firmware Support | druid={{no}} | prusa={{yes}} }}
```

Parameters
:   `P"nnnn"` nnnn = Prusa model name
:   `Q` Current model name

When run with P\<\> argument, the check is performed against the input
value. When run with Q argument, the current value is shown.

It accepts text identifiers of printer types too. The syntax of M862.3
is (note the quotes around the type):

:   `M862.3 P "MK3S"`

<!-- -->

Example messages
:   `warn` *G-code sliced for a different printer type. Continue?*
:   `strict` *G-code sliced for a different printer type. Please
    re-slice the model again. Print cancelled.*

##### M862.4: Firmware version {#m862.4_firmware_version}

```{=mediawiki}
{{Firmware Support | prusa={{yes}} | buddy={{no}} | druid={{no}} | reprapfirmware={{yes|Use M115 or object model }} }}
```

Parameters
:   `Pnnnn` nnnn = Prusa firmware version
:   `Q` Current firmware version

When run with P\<\> argument, the check is performed against the input
value. When run with Q argument, the current value is shown.

Example messages
:   `warn` *G-code sliced for a newer firmware. Continue?*
:   `strict` *G-code sliced for a newer firmware. Please update the
    firmware. Print cancelled.*

##### M862.5: Gcode level {#m862.5_gcode_level}

```{=mediawiki}
{{Firmware Support | druid={{no}} | prusa={{yes}} }}
```

Parameters
:   `Pnnnn` nnnn = Gcode level
:   `Q` Current Gcode level

When run with P\<\> argument, the check is performed against the input
value. When run with Q argument, the current value is shown.

Example messages
:   `warn` *G-code sliced for a different level. Continue?*
:   `strict` *G-code sliced for a different level. Please re-slice the
    model again. Print cancelled.*

##### M862.6: Firmware features {#m862.6_firmware_features}

```{=mediawiki}
{{Firmware Support | druid={{no}} | prusa={{no}} | buddy={{yes}} }}
```

Parameters
:   `P"cccc"` cccc = Firmware Features
:   `Q` Current Firmware Features

When run with P\<\> argument, the check is performed against the input
value. When run with Q argument, the current value is shown.

Example messages
:   `always` *G-code isn\'t fully compatible. misssing requested
    features: Input shaper Abort.*

#### M871: PTC Configuration {#m871_ptc_configuration}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{no}} | bfb={{no}} | machinekit={{no}} | makerbot={{no}} | grbl={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
`M871` allows you to modify the Z adjustments corresponding to
temperatures.

Parameters
:   `B` Set the Z adjustment for bed temperature
:   `P` Set the Z adjustment for probe temperature
:   `E` Set the Z adjustment for extruder temperature

<!-- -->

Examples

`M871 B V0.1 I3  ; Set Z adjustment for bed temp index 3 to 0.1`\
`M871 E V-1 I2   ; Set Z adjustment for extruder temp index 3 to -1`

#### M876: Dialog handling {#m876_dialog_handling}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{no}} | buddy={{no}} | druid={{experimental}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes|Use M291}} | bfb={{no}} | machinekit={{no}} | makerbot={{no}} | grbl={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   `Pnnn` signal support for dialog creation on the host = 1, disable =
    0
:   `Snnn` select dialog option nnn (0 based)

Example

`M876 P1`\
`M876 S1`

`M876 S``<n>`{=html} allows selecting an option of a prompt on a
connected host created by the firmware through the corresponding action
commands, see
[G-code#Action_commands](G-code#Action_commands "G-code#Action_commands"){.wikilink}.
The S parameter is the 0-based index of the chosen option - 0 for the
first option provided by the firmware, 1 for the second and so on.

Example: A prompt with three options defined via the firmware and
completed by the host by selecting the second option (\"Home X/Y and
pause print\")

` <<< //action:prompt_begin Filament runout detected. Please choose how to proceed:`\
` <<< //action:prompt_choice Swap filament`\
` <<< //action:prompt_choice Home X/Y and pause print`\
` <<< //action:prompt_choice Abort print`\
` <<< //action:prompt_show`\
` >>> M876 S1`

To indicate the availability of this function, `M115` will add an extra
line:

[`Cap:PROMPT_SUPPORT:1`](Cap:PROMPT_SUPPORT:1)

so hosts know about the presence of the function.

#### M890 Run User Gcode {#m890_run_user_gcode}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes|Use macro file M890.g}} | bfb={{no}} | machinekit={{no}} | makerbot={{no}} | grbl={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   `Snnn` select 1 - 5 User Gcode defined in configuration.

Example

`M890 S2  ; Start User Gcode 2`

#### M900: Set Linear Advance Scaling Factors {#m900_set_linear_advance_scaling_factors}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|1.1.0}} | prusa={{yes}} | buddy={{no}} | druid={{wip}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes|use M572}} | bfb={{no}} | machinekit={{no}} | makerbot={{no}} | grbl={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{yes}} }}
```
Sets the advance extrusion factors for Linear Advance. If any of the
`R`, `W`, `H`, or `D` parameters are set to zero the ratio will be
computed dynamically during printing.

Parameters
:   `K[factor]` Advance K factor
:   `R[ratio]` Set ratio directly (overrides WH/D)
:   `W[width]` `H[height]` `D[diam]` Set ratio from WH/D

Examples

`M900 K0.7 W0.4 H0.1 D1.75 ; Set K and WH/D ratio`\
`M900 R0.025   ; Set the WH/D ratio directly`\
`M900 R0 ; Set to "auto ratio"`

Requires enabling the `LIN_ADVANCE` feature in Marlin 1.1.

The K factor in the M900 command supported by early versions of Marlin
is related to the S factor in the long-established M572 command
supported by RepRapFirmware by the following formula:

`K = S * extruder_steps_per_mm`

More recent versions of Marlin appear to have removed the steps/mm
dependency, so now K = S.

#### M905: Set local date and time {#m905_set_local_date_and_time}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | druid={{yes}}<sup>1</sup> | reprapfirmware={{yes|1.16+}} | bfb={{no}} | machinekit={{no}} | makerbot={{no}} | grbl={{no}}  | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `Pnnn` Set current date in the format YYYY-MM-DD
:   `Snnn` Set current time in the format HH:MM:SS

Example

`M905 P2016-10-26 S00:23:12  `

Updates the machine\'s local date and time or reports them if no
parameters are specified. The time should be specified in 24-hours
format as in \"13:45\" instead of 1:45PM.

Note^1^ in Druid Firmware

<!-- -->

:   minor differences in parameters:
:   `M905 Snnn` Current time in the format HH:MM:SS or HH:MM (Seconds
    can be omitted)
:   `M905 R` Reset the printer to UPTIME (time since power up) and date
    to DEFAULT 2000-01-01
:   When Druid Firmware is used with Repetier Server, the date and time
    are set automatically at each connection.

#### M906: Set motor currents {#m906_set_motor_currents}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{no}} | buddy={{no}} | druid={{partial|USE M907}} | repetier={{no}} | smoothie=M907? | reprapfirmware={{yes}} | bfb={{no}} | machinekit={{no}} | redeem={{yes}} | mk4duo={{no}} | yaskawa={{no}} }}
```
Set the currents to send to the stepper motors for each axis. The values
are the peak current per phase in milliamps (mA).

Parameters
:   `X[current]` X drive motor current
:   `Y[current]` Y drive motor current
:   `Z[current]` Z drive motor current
:   `E[current]` E drive(s) motor current(s)

<!-- -->

RRF additional Parameters:
:   `I[percent]` Motor idle current in percent (0..100)

<!-- -->

Marlin additional Parameters:
:   `ABCUVW...[current]` Motor current for additional axes
:   `I[index]` Specific axis motor index (zero-based) (`I1` for `X2`,
    `Y2`, `Z2`, etc.)
:   `T[index]` Extruder/Tool index (zero-based)

<!-- -->

Marlin with `EDITABLE_HOMING_CURRENT`
:   `M906 H` Treat M906 as an alias for `M920` to set/report Homing
    Current.

<!-- -->

Example (RRF)

`M906 X300 Y500 Z200 E350:350`

In RepRapFirmware the `I` parameter is the percentage of normal that the
motor currents should be reduced to when the printer becomes idle but
the motors have not been switched off. The default value is 30%. On
delta printers in particular you may need to increase it (e.g., to 60%)
to prevent the carriages from dropping when the current is reduced to
the idle value.

#### M907: Set digital trimpot motor current {#m907_set_digital_trimpot_motor_current}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{yes}} | buddy={{no}} | reprapfirmware={{partial|Use M906}} | smoothie={{yes}} | druid={{yes}}<sup>1</sup> | repetier={{yes}} | bfb={{no}} | machinekit={{no}} | redeem={{yes}} | mk4duo={{yes}} | yaskawa={{no}} }}
```
Set digital trimpot motor current using axis codes (`X`, `Y`, `Z`, `E`,
`B`, `S`). In [Repetier](http://reprap.org/wiki/Repetier), it sets the
current in Percent. In
[Redeem](https://bitbucket.org/intelligentagent/redeem/src/6153607ded91c100fb4e41e936e6d045e19eda29/redeem/gcodes/M907.py?at=slave_stepper),
it sets the current in Amps (whereas `M906` uses milliamps).

------------------------------------------------------------------------

*Differences with Druid Firmware*^1^

Parameters
:   `M907 Xnnn` Set X stepper current
:   `M907 Ynnn` Set Y stepper current
:   `M907 Znnn` Set Z stepper current
:   `M907 Annn` Set E0 stepper current
:   `M907 Bnnn` Set E1 stepper current
:   `M907 Innn` Set Idle current % (see note ^2^)
:   `M907 S` Reset all values to Firmware default
:   `M907` Report all values (X,Y,Z,A,B) in mA, and idle (I) as %

*- When setting X,Y,Z,A,B current, The range in which, the values
provided are, will automatically determine their UNITS (Amps, % or mA)
as follow: Values between\...*

:   `0.10 ... 2.50` \--\> Unit is Amps (0.10 A \... 2.50 A)
:   `20 ... 200` \--\> Unit is Percentage (20 % \... 200 %) of nominal
    values set in Druid Firmware
:   `250 ... 2500` \--\> Unit is milliamps (250 mA \... 2500 mA)

*- Any values outside those ranges, will be ignored.*

Exemple

`M907 X800 Y800 A600     ;values are processed as mA`\
`M907 X80 Y80 A120       ;values are processed as % of firmware default`\
`M907 X0.75 Y0.75 Z0.5   ;values are processed as Amps `\
`M907                    ;Report all values (X,Y,Z,A,B) in mA, and idle (I) as %`\
`M907 S                  ;reset all values to Firmware default`

Note^2^

`The percentage parameter "I", is used to lower the current, when the printer is idle, but motors are not switched off. `\
`It Allows positions to be held without heating up the coils. (default is 50%, range is 10% ... 90%)`

#### M908: Control digital trimpot directly {#m908_control_digital_trimpot_directly}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{no}}<sup>1</sup> | druid={{no}} | repetier={{yes|0.92}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```
M908 P`<pin>`{=html} S`<current>`{=html}

Notes

In Prusa Firmware this G-code is deactivated by default, must be turned
on in the source code.^1^

#### M909: Set microstepping {#m909_set_microstepping}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{partial|Use M350}} | druid={{no}} | repetier={{partial|Use M350}} | reprapfirmware={{partial|Use M350}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | redeem={{yes}} | mk4duo={{partial|Use M350}} }}
```

Example

`M909 X3 Y5 Z2 E3`

Set the microstepping value for each of the steppers. In
[Redeem](Redeem "Redeem"){.wikilink} this is implemented as powers of 2
so...

`M909 X2 ; set microstepping on X-axis to 2^2 = 4`\
`M909 Y3 ; set microstepping on Y-axis to 2^3 = 8 etc.`

#### M910: Set decay mode {#m910_set_decay_mode}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{no}} | reprapfirmware={{yes|Use M569}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | redeem={{yes}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Example

`M910 X3 Y5 Z2 E3`

Set the decay mode for each stepper controller The decay mode controls
how the current is reduced and recycled by the H-bridge in the stepper
motor controller. It varies how the implementations are done in silicone
between controllers. Typically you have an on phase where the current
flows in the target current, then an off phase where the current is
reversed and then a slow decay phase where the current is recycled.

#### M910: TMC2130 init {#m910_tmc2130_init}

```{=mediawiki}
{{Firmware Support | prusa={{yes}} }}
```

:   Not active in default, only if TMC2130_SERVICE_CODES_M910_M918 is
    defined in source code.

#### M911: Configure auto save on loss of power (\"power panic\") {#m911_configure_auto_save_on_loss_of_power_power_panic}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes|1.20+}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `Saaa` Auto save threshold in volts. The print will be stopped
    automatically and resume parameters saved if the voltage falls below
    this value. Set to around 1V to 2V lower than the voltage that
    appears at the Duet VIN terminals at full load. A negative or zero
    value disables auto save.
:   `Raaa` Resume threshold in volts. Must be greater than the auto save
    voltage. Set to a high value to disable auto resume.
:   `P"command string"` G-Code commands to run when the print is
    stopped.

<!-- -->

Example

<!-- -->

    M911 S19.8 R22.0 P"M913 X0 Y0 G91 M83 G1 Z3 E-5 F1000"

When the supply voltage falls below the auto save threshold while a
print from SD card is in progress, all heaters will be turned off,
printing will be stopped immediately (probably in the middle of a move),
the position saved, and the specified command string executed. You
should typically do the following in the command string:

- If possible, use M913 to reduce the motor current in order to conserve
  power. For example, on most printers except deltas you can probably
  set the X and Y motor currents to zero.
- Retract a little filament and raise the head a little. Ideally the
  retraction should happen first, but depending on the power reserve
  when low voltage is detected, it may be best to do both
  simultaneously.

M911 with no parameters displays the current enable/disable state, and
the threshold voltages if enabled.

Note: RepRapFirmware 1.19 used different parameters. You are recommended
to upgrade to version 1.20 or later if you wish to use this \"power
panic\" functionality.

#### M911: Set TMC2130 holding currents {#m911_set_tmc2130_holding_currents}

```{=mediawiki}
{{Firmware Support | reprapfirmware={{yes|Use M917}} | prusa={{yes}} }}
```

:   Not active in default, only if TMC2130_SERVICE_CODES_M910_M918 is
    defined in source code.

#### M911: Report TMC Overtemperature Pre-Warn {#m911_report_tmc_overtemperature_pre_warn}

```{=mediawiki}
{{Firmware Support | marlin={{yes}} | reprapfirmware={{no}} | klipper={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | druid={{no}} | mk4duo={{no}} | makerbot={{no}} | grbl={{no}} | sprinter={{no}} | bfb={{no}} | fived={{no}} | machinekit={{no}} | redeem={{no}} | teacup={{no}} | yaskawa={{no}} }}
```
**(Does not apply to STANDALONE stepper drivers.)**

Report TMC stepper driver Overtemperature Pre-Warn flag. This flag is
held by the TMCStepper library, persisting until cleared by `M912`.

#### M912: Set electronics temperature monitor adjustment {#m912_set_electronics_temperature_monitor_adjustment}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | druid={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `Pnnn` Temperature monitor channel, default 0
:   `Snnn` Value to be added to the temperature reading in degC

<!-- -->

Example

`M912 P0 S10.5`

Many microcontrollers used to control 3D printers have built-in
temperature monitors, but they normally need to be calibrated for
temperature reading offset. The `S` parameter specifies the value that
should be added to the raw temperature reading to provide a more
accurate result.

#### M912: Set TMC2130 running currents {#m912_set_tmc2130_running_currents}

```{=mediawiki}
{{Firmware Support | prusa={{yes}} | buddy={{no}} | reprapfirmware={{yes|Use M906}} }}
```

:   Not active in default, only if TMC2130_SERVICE_CODES_M910_M918 is
    defined in source code.

#### M912: Clear TMC Overtemperature Pre-Warn {#m912_clear_tmc_overtemperature_pre_warn}

```{=mediawiki}
{{Firmware Support | marlin={{yes}} | reprapfirmware={{no}} | klipper={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | druid={{no}} | mk4duo={{no}} | makerbot={{no}} | grbl={{no}} | sprinter={{no}} | bfb={{no}} | fived={{no}} | machinekit={{no}} | redeem={{no}} | teacup={{no}} | yaskawa={{no}} }}
```
**(Does not apply to STANDALONE stepper drivers.)**

Clear TMC stepper driver Overtemperature Pre-Warn flags held by the
TMCStepper library. Specify one or more axes \"by name\" using
parameters and values. If no axes are given, clear all pre-warn flags.
Report the current state of these flags with `M911`.

Parameters
:   `X[index], Y[index], ...` Flags for axes to clear. Include an index
    to specify just one axis stepper driver.

<!-- -->

Examples:

<!-- -->

    M912 X          ; clear X and X2
    M912 X1         ; clear X1 only
    M912 X2         ; clear X2 only
    M912 Z E        ; clear Z, Z2, Z3, Z4, and all E
    M912 E1         ; clear E1 only

#### M913: Set motor percentage of normal current {#m913_set_motor_percentage_of_normal_current}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | druid={{partial|USE M907}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{yes}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `X, Y, Z, E` Percentage of normal current to use for the specified
    axis or extruder motor(s)

<!-- -->

Example

`M913 X50 Y50 Z50 ; set X Y Z motors to 50% of their normal current`\
`M913 E30:30 ; set extruders 0 and 1 to 30% of their normal current`

This allows motor currents to be set to a specified percentage of their
normal values as set by `M906`. It can be used (for example) to reduce
motor current during course homing, to make homing quieter or to reduce
the risk of damage to endstops, to reduce motor current when using
sensorless endstops (motor stall detection), and to reduce current while
loading filament to guard against the possibility of feeding too much
filament. Use `M913` again with the appropriate parameters set to 100 to
restore the normal currents.

#### M913: Set Hybrid (PWM) Threshold {#m913_set_hybrid_pwm_threshold}

```{=mediawiki}
{{Firmware Support | marlin={{yes}} | reprapfirmware={{no}} | klipper={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | druid={{no}} | mk4duo={{no}} | makerbot={{no}} | grbl={{no}} | sprinter={{no}} | bfb={{no}} | fived={{no}} | machinekit={{no}} | redeem={{no}} | teacup={{no}} | yaskawa={{no}} }}
```

Usage
:   `M913 [I``<num>`{=html}`] [X``<value>`{=html}`] [Y``<value>`{=html}`] [Z``<value>`{=html}`] [A``<value>`{=html}`] [B``<value>`{=html}`] [C``<value>`{=html}`] [U``<value>`{=html}`] [V``<value>`{=html}`] [W``<value>`{=html}`] [T``<toolindex>`{=html}`] [E``<value>`{=html}`]`

<!-- -->

Parameters
:   `X Y Z A B C U V W` Provide threshold values for one or more axes
:   `I` One-based index for multi-stepper axes, if only one stepper in
    the axis should be modified (Default: change all)
:   `E` Provide a threshold value for one or more extruders / tools
:   `T` Zero-based index of the extruder / tool, if only one should be
    modified (Default: change all)

#### M913: Print TMC2130 currents {#m913_print_tmc2130_currents}

```{=mediawiki}
{{Firmware Support | prusa={{yes}} }}
```

:   Not active in default, only if TMC2130_SERVICE_CODES_M910_M918 is
    defined in source code.

#### M914: Set/Get Expansion Voltage Level Translator {#m914_setget_expansion_voltage_level_translator}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | reprapfirmware={{partial|Alligator build only}} | bfb={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `S` Expansion voltage signal level, must be 3 or 5

<!-- -->

Example

`M914 S5 ; set expansion signal level to 5V`\
`M913 ; report expansion signal voltage level`

#### M914: Set TMC2130 normal mode {#m914_set_tmc2130_normal_mode}

```{=mediawiki}
{{Firmware Support | marlin={{no}} | reprapfirmware={{no}} | klipper={{no}} | prusa={{yes}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | druid={{no}} | mk4duo={{no}} | makerbot={{no}} | grbl={{no}} | sprinter={{no}} | bfb={{no}} | fived={{no}} | machinekit={{no}} | redeem={{no}} | teacup={{no}} | yaskawa={{no}} }}
```
Updates EEPROM only if \"P\" is given, otherwise temporary (lasts until
reset or motor idle timeout)

Usage
:   `M914 [ P | R | Q ]`

<!-- -->

Parameters
:   `P` Make the mode change permanent (write to EEPROM)
:   `R` Revert to EEPROM value
:   `Q` Print effective silent/normal status. (Does not report override)

#### M914: Set StallGuard sensitivity (Homing Threshold) {#m914_set_stallguard_sensitivity_homing_threshold}

```{=mediawiki}
{{Firmware Support | marlin={{yes}} | reprapfirmware={{no}} | klipper={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | druid={{no}} | mk4duo={{no}} | makerbot={{no}} | grbl={{no}} | sprinter={{no}} | bfb={{no}} | fived={{no}} | machinekit={{no}} | redeem={{no}} | teacup={{no}} | yaskawa={{no}} }}
```

Usage
:   `M914 [I``<num>`{=html}`] [X``<value>`{=html}`] [Y``<value>`{=html}`] [Z``<value>`{=html}`] [A``<value>`{=html}`] [B``<value>`{=html}`] [C``<value>`{=html}`] [U``<value>`{=html}`] [V``<value>`{=html}`] [W``<value>`{=html}`]`

<!-- -->

Parameters
:   `X Y Z A B C U V W` Provide current values for one or more axes
:   `I` One-based index for multi-stepper axes, if only one stepper in
    the axis should be modified (default: change all)

#### M915: Configure motor stall detection {#m915_configure_motor_stall_detection}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{yes|1.20+}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   **Pnnn:nnn:\...** Drive number(s) to configure
:   **X,Y,Z,U,V,W,A,B,C** Axes to configure (alternative to using the P
    parameter)
:   **Snnn** Stall detection threshold (-64 to +63, values below -10 not
    recommended)
:   **Fn** Stall detection filter mode, 1 = filtered (one reading per 4
    full steps), 0 = unfiltered (default, 1 reading per full step)
:   **Hnnn** (optional) Minimum motor full steps per second for stall
    detection to be considered reliable, default 200
:   **Tnnn** (optional) Coolstep control register, 16-bit unsigned
    integer
:   **Rn** Action to take on detecting a stall from any of these
    drivers: 0 = no action (default), 1 = just log it, 2 = pause print,
    3 = pause print, execute macro file **/sys/rehome.g**, and resume
    print

Examples
:   M915 P0:2:3 S10 F1 R0
:   M915 X Y S5 R2

This sets the stall detection parameters and optionally the low-load
current reduction parameters for TMC2660, TMC2130 or similar driver
chips. Use either the P parameter to specify which driver number(s) you
want to configure, or the axis names of the axes that those motors drive
(the parameters will then be applied to all the drivers associated with
any of those axes).

If any of the S, F, T and R parameters are absent, the previous values
for those parameters associated with the specified drivers will continue
to be used. If all the parameters are absent, the existing settings for
the specified drives will be reported.

See the Trinamic TMC2660 and TMC2130 datasheets for more information
about the operation and limitations of motor stall detection.

#### M915: Set TMC2130 silent mode {#m915_set_tmc2130_silent_mode}

```{=mediawiki}
{{Firmware Support | reprapfirmware={{yes|Use M569 to select StealthChop mode}} | prusa={{yes}} }}
```
Updates EEPROM only if \"P\" is given, otherwise temporary (lasts until
reset or motor idle timeout)

Usage
:   `M915 [ P | R | Q ]`

<!-- -->

Parameters
:   `P` Make the mode change permanent (write to EEPROM)
:   `R` Revert to EEPROM value
:   `P` Print effective silent/normal status. (Does not report override)

#### M916: Resume print after power failure {#m916_resume_print_after_power_failure}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{yes|1.20+}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   none

Example
:   M916

If the last print was not completed and resume information has been
saved (either because the print was paused or because of a power
failure), then the heater temperatures, tool selection, head position,
mix ratio, mesh bed compensation height map etc. are restored from the
saved values and printing is resumed.

RepRapFirmware also requires macro file **/sys/resurrect-prologue.g** to
be present on the SD card before you can use M915. This file is executed
after the heater temperatures have been set, but before waiting for them
to reach the assigned temperatures. You should put commands in this file
to home the printer as best as you can without disturbing the print on
the bed. To wait for the heaters to reach operating temperature first,
use command M116 at the start of the file.

#### M916: Set TMC2130 Stallguard sensitivity threshold {#m916_set_tmc2130_stallguard_sensitivity_threshold}

```{=mediawiki}
{{Firmware Support | reprapfirmware={{yes|Use M915}} | prusa={{yes}} }}
```

:   Not active in default, only if TMC2130_SERVICE_CODES_M910_M918 is
    defined in source code.

#### M917: Set motor standstill current reduction {#m917_set_motor_standstill_current_reduction}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{yes|1.20+}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   **X,Y,Z,E** Percentage of normal current to use when the motor is
    standing still or moving slowly, default 100

Example
:   M917 X70 Y70 Z80 E70:70

Some motor drivers (e.g. TMC2660) allow higher motor currents to be used
while the motor is moving than when it is at standstill. This command
sets the percentage of the current set by M906 that is to be used when
the motor is stationary but not idle, or moving very slowly.

Standstill current reduction is not the same as idle current reduction.
The standstill current must be high enough to produce accurate motion at
low speeds; whereas the idle current (set using the I parameter in the
M906 command) needs only to be high enough to hold the motor position
sufficiently so that when the current is restored to normal, the
position is the same as it was before the current was reduced to idle.

#### M917: Set TMC2130 PWM amplitude offset (pwm_ampl) {#m917_set_tmc2130_pwm_amplitude_offset_pwm_ampl}

```{=mediawiki}
{{Firmware Support | prusa={{yes}} }}
```

:   Not active in default, only if TMC2130_SERVICE_CODES_M910_M918 is
    defined in source code.

#### M918: Configure direct-connect display {#m918_configure_direct_connect_display}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{yes|1.21+}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
This command is used to tell RepRapFirmware about a directly-connected
dumb LCD or similar display.

Parameters
:   **P** Directly-connected display type: 0 = none (default), 1 =
    128x64 pixel mono graphics display using ST7920 controller, 2 =
    128x64 mono display using ST7567 controller
:   **E** The number of pulses generated by the rotary encoder per
    detent. Typical values are 2 and 4. Negative values (e.g. -2 and -4)
    reverse the encoder direction.
:   **F** (optional, supported in RRF 2.03 and later) SPI clock
    frequency in Hz, default 2000000 (i.e. 2MHz)
:   **C** (optional, supported in RRF 3.2 and later) Display contrast,
    in range 0 to 100. Only used with ST7567-based displays.
    ST7920-based displays usually have a contrast potentiometer instead.
:   **R** (optional, supported in RRF 3.2 and later) Display resistor
    ratio, in range 1 to 7. Only used with ST7567-based displays. The
    default value of 6 is suitable for the Fysetc Mini 12864 display.
    Some other displays need 3.

Example
:   M918 P1 E2

#### M918: Set TMC2130 PWM amplitude gradient (pwm_grad) {#m918_set_tmc2130_pwm_amplitude_gradient_pwm_grad}

```{=mediawiki}
{{Firmware Support | marlin={{no}} | reprapfirmware={{no}} | klipper={{no}} | prusa={{yes}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | druid={{no}} | mk4duo={{no}} | makerbot={{no}} | grbl={{no}} | sprinter={{no}} | bfb={{no}} | fived={{no}} | machinekit={{no}} | redeem={{no}} | teacup={{no}} | yaskawa={{no}} }}
```

:   Not active in default, only if TMC2130_SERVICE_CODES_M910_M918 is
    defined in source code.

#### M919: TMC Chopper Time {#m919_tmc_chopper_time}

```{=mediawiki}
{{Firmware Support | marlin={{yes}} | reprapfirmware={{no}} | klipper={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | druid={{no}} | mk4duo={{no}} | makerbot={{no}} | grbl={{no}} | sprinter={{no}} | bfb={{no}} | fived={{no}} | machinekit={{no}} | redeem={{no}} | teacup={{no}} | yaskawa={{no}} }}
```
**(Does not apply to STANDALONE stepper drivers.)**

Set or report Chopper Times for all Trinamic stepper drivers. Refer to
Marlin configurations, the TMCStepper library, and Trinamic datasheets
for information on how these values work.

Send `M919` with no parameters report Chopper Times for all axes.

Usage
:   `M919 [O``<off-time>`{=html}`] [S``<start>`{=html}`] [P``<end>`{=html}`] [I``<index>`{=html}`] [T``<eindex>`{=html}`] [XYZ...]`

<!-- -->

Parameters
:   `X Y Z A B C U V W` Flags for all axis steppers that will be set
:   `I[index]` Zero-based index for multi-stepper axes (I0 for X1, Y1 ;
    I1 for X2, Y2 ; etc.). Omit to apply to all axis steppers.
:   `T[index]` Zero-based extruder/tool index. Omit for all extruders.
:   `O` Time-off value (1..15)
:   `S` Hysteresis Start (1..8)
:   `P` Hysteresis End (-3..12)

#### M920: TMC Homing Current {#m920_tmc_homing_current}

```{=mediawiki}
{{Firmware Support | marlin={{yes|2.1.3}} | reprapfirmware={{no}} | klipper={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | druid={{no}} | mk4duo={{no}} | makerbot={{no}} | grbl={{no}} | sprinter={{no}} | bfb={{no}} | fived={{no}} | machinekit={{no}} | redeem={{no}} | teacup={{no}} | yaskawa={{no}} }}
```
**(Does not apply to STANDALONE stepper drivers.)**

Set or report the firmware Homing Current settings for all Trinamic
stepper drivers. All values are in milliamps (mA). Homing Current should
be adjusted in conjunction with StallGuard Threshold and Homing Speed to
achieve reliable sensorless homing. Refer to Marlin example
configurations to find suitable starting values for your hardware.

Send `M920` with no parameters report the Homing Current for all axes.

Usage
:   `M920 [I``<index>`{=html}`] [T``<index>`{=html}`] [X``<current>`{=html}`] [Y``<current>`{=html}`] [Z``<current>`{=html}`] [A``<current>`{=html}`] [B``<current>`{=html}`] [C``<current>`{=html}`] [U``<current>`{=html}`] [V``<current>`{=html}`] [W``<current>`{=html}`]`

<!-- -->

Parameters
:   `X[current]` Current in mA to set for X stepper driver(s)
:   `Y[current]` Current in mA to set for Y stepper driver(s)
:   `Z[current]` Current in mA to set for Z stepper driver(s)
:   `...ABCUVW...` And the same for any other axes...
:   `I[index]` Zero-based index for multi-stepper axes (I0 for X1, Y1 ;
    I1 for X2, Y2 ; etc.). Omit to apply to all axis steppers.

#### M928: Start SD logging {#m928_start_sd_logging}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{yes}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Example

`M928 filename.g`

Stop SD logging with `M29`.

#### M929: Start/stop event logging to SD card {#m929_startstop_event_logging_to_sd_card}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{yes}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{yes|1.20+}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   **P\"filename\"** The name of the file to log to. Only used if the
    S1 parameter is used. A default filename will be used if this
    parameter is missing.
:   **Sn** S1 = start logging, S0 = stop logging

Example
:   M929 P\"eventlog.txt\" S1 ; start logging to file eventlog.txt
:   M929 S0 ; stop logging

When event logging is enabled, important events such as power up,
start/finish printing, most error messages and (if possible) power down
will be logged to the SD card. Each log entry is a single line of text,
starting with the date and time if available, or the elapsed time since
power up if not. If the log file already exists, new log entries will be
appended to the existing file.

#### M950: Create heater, fan or GPIO/servo device {#m950_create_heater_fan_or_gpioservo_device}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{yes|3.0+}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   **Dn** SD card slot number (RRF 3.4 on Duet 3 MB6HC only - the only
    value supported is 1)
:   **Enn** LED strip number (RRF 3.5 and later)
:   **Fnn** Fan number
:   **Hnn** Heater number
:   **Jnn** GP input number
:   **Pnn or Snn** GPIO or Servo number (the only difference is the
    default PWM frequency)
:   **Rnn** Spindle number \*RRF 3.3 and later)
:   **C\"name\"** Pin name(s) and optional inversion status. Pin name
    \"nil\" frees up the pin. A leading \'!\' character inverts the
    output. A leading \'\^\' character enables the pullup resistor. The
    \'\^\' and \'!\' characters may be placed in either order.
:   **Qnn** (optional) For fans and heaters: PWM frequency in Hz. For
    LED strips: clock frequency in Hz.
:   **Tnn** Temperature sensor number, required when creating a heater;
    or LED strip type when creating an LED port
:   **Kaaa:bbb:ccc** (optional, for spindles only, RRF 3.5 and later)
    Optional PWM values (0..1) for spindle control (max \[aaa\] - or -
    min, max [2](aaa:bbb) - or - min, max, idle [3](aaa:bbb:ccc))

<!-- -->

Examples
:   M950 H1 C\"out1\" Q100 T1 ; create heater 1 using temperature sensor
    1
:   M950 H2 C\"nil\" ; disable heater 2 and free up the associated pin
:   M950 H2 C\"1.out0\" T2 ; create heater 2 using pin out0 on expansion
    board 1 and temperature sensor 2
:   M950 F3 C\"heater2\" Q100 ; Fan 3 is connected to heater 2 pin, PWM
    at 100Hz
:   M950 P0 C\"exp.heater3\" ; create GPIO port 0 attached to heater 3
    pin on expansion connector
:   M950 F2 C\"!fan2+\^pb6\" ; Fan 2 uses the Fan2 output, but we are
    using a PWM fan so the output needs to be inverted, also we are
    using PB6 as a tacho input with pullup resistor enabled
:   M950 D1 C\"spi.cs0+spi.cs2\" ; on Duet 3 MB6HC support external SD
    card using pins spi.cs0 and spi.cs2 for the CS and Card Detect pins
    respectively

M950 is used to create heaters, fans, LED strip ports and GP in and out
ports and to assign pins to them. Each M950 command assigns a pin or
pins to a single device. So every M950 command must have exactly one of
the D, E, F, H, J, P or S parameters.

If a M950 command has C and/or Q parameters, then the pin allocation
and/or frequency of any existing device will be changed accordingly.
Otherwise, the current configuration will be reported.

When using M950 to create a heater, you must first use M308 to define a
temperature sensor to control that heater, and specify its number in the
T parameter of the M950 command.

#### M951: Set height following mode parameters {#m951_set_height_following_mode_parameters}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{yes|3.0+}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters:
:   **Snn or Hnn** Sensor number
:   **Pnn.n** Proportional factor, in mm per sensor unit
:   **Inn.n** Integral factor, in mm per sensor unit per second
:   **Dnn.n** Derivative factor, in mm per rate of change of sensor
    units (change in sensor unit per second)
:   **Fnn.n** (optional) Sample and correction frequency (Hz), default
    5Hz
:   **Znn.n:nn.n** Minimum and maximum permitted Z values

Height following mode allows the Z position of the tool to be controlled
by a PID controller using feedback from a sensor. See also M594.

If commanding the motors to increase Z causes the sensor value to
increase, then all of P, I and D must be positive. If commanding the
motors to increase Z causes the sensor value to decrease, then all of P,
I and D must be negative.

#### M952: Set CAN expansion board address and/or normal data rate {#m952_set_can_expansion_board_address_andor_normal_data_rate}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{yes|3.0+}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   **Bn** Existing CAN address of expansion board to be changed, 1 to
    125.
:   **An** New CAN address of that expansion board, 1 to 125.
:   **Sn.n** Requested bit rate in Kbits/second (1K = 1000)
:   **T0.n** Fraction of the bit time between the bit start and the
    sample point (optional)
:   **J0.n** Maximum jump time as a fraction of the bit time (optional)

Example
:   M952 B120 A11 ; change the CAN address of expansion board 101 to 11
:   M952 B11 S500 ; change the CAN bit rate or expansion board 11 to
    500kbps

Some CAN-connected expansion boards are too small to carry address
selection switches. Such boards default to a standard address, which can
be changed using this command.

This command can also be used to change the normal data rate, for
example if the printer has CAN bus cables that are too long to support
the standard data rate (1Mbits/sec in RepRapFirmware). All boards in the
system on the same CAN bus must use the same CAN data rate. The
procedure for changing the data rate is:

- Use M952 to change the data rate on all the expansion boards, one at a
  time. After changing the data rate on each expansion board, you will
  no longer be able to communicate with it, and you may need to power it
  down or disconnect it from the CAN bus to prevent it interfering with
  subsequent CAN communications.
- Change the data rate of the main board last. Then the main board
  should be able to communicate with all the expansion boards again.

#### M953: Set CAN-FD bus fast data rate {#m953_set_can_fd_bus_fast_data_rate}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{yes|3.0+}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   **Sn.n** Requested bit rate in Kbits/second (1K = 1000). Ignored if
    it is lower than the bit rate for the negotiation phase.
:   **T0.n** Fraction of the bit time between the bit start and the
    sample point (optional)
:   **J0.n** Maximum jump time as a fraction of the bit time (optional)
:   **Caa:bb** Transceiver delay compensation offset and minimum, in
    nanoseconds (optional)

Example
:   M953 S4000 T0.6 J0.2

This command allows the bandwidth of the CAN bus to be optimised, by
increasing the data rate during transmission of CAN-FD data packets
using the BRS (bit rate switch) feature. The maximum speed supported by
CAN-FD is 8Mbits/sec but the practical limit depends on the cable
length, cable quality, number of devices on the bus and CAN interface
hardware used. The rate specified will be rounded down to the nearest
achievable rate.

The optional C parameter allows fine-tuning of the transmitter delay
compensation. The first parameter is the offset added to the measured
transmitter delay. The optional second value, which must be greater than
the first, is the minimum delay compensation applied. Glitches seen by
the receiver while the transceiver delay is being measured will be
ignored if they would result in a transceiver delay compensation lower
than this value. When CAN is implemented on Microchip SAME5x and SAMC21
processors, these values are converted from nanoseconds into time quanta
and stored in the TDCO and TDCF fields of the transceiver delay
compensation register.

#### M954: Configure as CAN expansion board {#m954_configure_as_can_expansion_board}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{yes|3.3+}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   **Ann** CAN address to use (required)

This command is used to reconfigure the board it is executed on as a
CAN-connected expansion board. It would typically be the only command in
the config.g file. When it is executed, the board changes its CAN
address to the one specified in the A parameter, stops sending CAN time
sync messages, and responds to requests received via CAN just like a
regular expansion board. A few GCode commands can still be executed
locally for diagnostic purposes, for example M111 and M122.

#### M955: Configure Accelerometer {#m955_configure_accelerometer}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{yes|3.4+}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters (provisional)
:   **Pnn** or **Pbb.nn** Accelerometer to use (required)
:   **Inn** Accelerometer orientation
:   **Snnn** Sample rate (Hz)
:   **Rnn** Resolution (bits), typically 8, 10 or 12

This command configures an accelerometer.

The P parameter selects which accelerometer to use and is mandatory. To
use an accelerometer on a CAN-connected expansion board, use the form
**P***board-address*.*device-number* for example **P22.0**.

If none of the other parameters are provided, the current configuration
of the specified accelerometer is reported. Otherwise the configuration
of that accelerometer is adjusted according to the I, S, and R
parameters. These configuration settings persist until they are changed.

The I (orientation) parameter tells the firmware which of the 24
possible orientations the accelerometer chip is in relative to the
printer axes. It is expressed as a 2-digit number. The first digit
specifies which machine direction the Z axis of the accelerometer chip
(usually the top face of the chip) faces, as follows: 0 = +X, 1 = +Y, 2
= +Z, 4 = -X, 5 = -Y, 6 = -Z. The second digit expresses which direction
the X axis of the accelerometer chip faces, using the same code. If the
accelerometer chip axes line up with the machine axis, the orientation
is 20. This is the default orientation if no orientation has been
specified.

The S and R parameters control how the accelerometer is programmed. The
R parameter is ignored unless the S parameter is also provided. If S is
provided but R is missing, a default resolution is used. The sensor
resolution will be adjusted to be no greater than the value of the R
parameter (or the minimum supported resolution if greater), then the
sensor sampling rate will be adjusted to a value supported at that
resolution that is close to the S parameter. The actual rate and
resolution selected can be found by using M955 with just the P
parameter.

#### M956: Collect accelerometer data and write to file {#m956_collect_accelerometer_data_and_write_to_file}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{yes|3.4+}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   **Pnn** or **Pbb.nn** Accelerometer to use (required)
:   **Snnn** Number of samples to collect (required)
:   **X** and/or **Y** and/or **Z** Machine axes to collect data for. If
    no axes are specified, data is collected for all three axes.
:   **An** (required) 0 = activate immediately, 1 = activate just before
    the start of the next move, 2 = activate just before the start of
    the deceleration segment of the next move
:   **Kn** (optional, default 0) Skip the specified number of moves
    before activating (use with A1 or A2)

This command causes the specified number of accelerometer samples to be
collected and saved to a .csv file on the SD card.

The P parameter selects which accelerometer to use and is mandatory. To
use an accelerometer on a CAN-connected expansion board, use the form
**P***board-address*.*device-number* for example **P22.0**.

#### M957: Raise event {#m957_raise_event}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{yes|3.4+}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   **E\"type\"** Event type name
:   **Dnn** Device number to which the event relates, optionally
    including the CAN address of the board concerned
:   **Pnn** (optional) additional data about the event (unsigned
    integer)
:   **Bnn** (optional) CAN address that the event should appear to
    originate from
:   **S\"text\"** (optional) Short text string to be appended to the
    event message

This command is used to raise an event internally as if the event had
actually occurred, and execute any related handler macro for that event.
Its main use is to test event handler macros.

The event type names are firmware-dependent. In RepRapFirmware they are:
heater_fault, driver_error, filament_error, driver_warning, driver_stall
and mcu_temperature_warning.

The meaning of the device number depends on the event type. For a driver
error it is the local driver number. For a heater fault it is the heater
number. For a filament error it is the extruder number.

The meaning of the optional additional parameter also depends on the
event type. For example, for a driver error it is the driver status.

#### M958: Excite harmonic vibration {#m958_excite_harmonic_vibration}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters (provisional)
:   **X** or **Y** or **Z** Machine axis
:   **Fnnn** Frequency (Hz)
:   **Annn** Acceleration (mm/s^2^)
:   **Snnn** Duration (s)

#### M970: Enable/Disable Phase Stepping {#m970_enabledisable_phase_stepping}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{yes}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | reprapfirmware={{yes}} | makerbot={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `Xn` 0 = disable, 1 = enable
:   `Yn` 0 = disable, 1 = enable
:   `{Axis letter}n` (RRF) 0 = disable, 1 = enable

#### M970.1: Configure Phase Stepping Velocity Constant {#m970.1_configure_phase_stepping_velocity_constant}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | reprapfirmware={{yes}} | makerbot={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `{Axis letter}nnn`(RRF 3.6 onwards) velocity constant

Configure the velocity constant used to scale the motor current in phase
stepping.

#### M970.2: Configure Phase Stepping Acceleration Constant {#m970.2_configure_phase_stepping_acceleration_constant}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | reprapfirmware={{yes}} | makerbot={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `{Axis letter}nnn`(RRF 3.6 onwards) acceleration constant

Configure the acceleration constant used to scale the motor current in
phase stepping.

#### M972: Retrieve Current Correction {#m972_retrieve_current_correction}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{yes}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | reprapfirmware={{no}} | makerbot={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
Outputs the current correction table in format: \``<axis>`{=html},
`<direction>`{=html}, `<index>`{=html}, `<mag>`{=html}, `<pha>`{=html}\`
per line. Multiple axes can be specified.

#### M973: Set Single Entry in Current Correction Table {#m973_set_single_entry_in_current_correction_table}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{yes}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | reprapfirmware={{no}} | makerbot={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   **String argument in format: `<X/Y>`{=html}`<F/B>`{=html}\<list of
    mag,phase pairs separated by space\>**

#### M974: Measure Print Head Resonance {#m974_measure_print_head_resonance}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{yes}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | reprapfirmware={{no}} | makerbot={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   **X/Y** choose motor to use
:   **F** motion speed in rev/sec
:   **R** number of revolutions

Outputs raw accelerometer sample `<seq>`{=html}, `<X>`{=html},
`<Y>`{=html}, `<Z>`{=html} per line and real sampling frequency of the
accelerometer as \"sample freq: `<freq>`{=html}\".

#### M975: Measure Dwarf Accelerometer Sampling Frequency {#m975_measure_dwarf_accelerometer_sampling_frequency}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{yes}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | reprapfirmware={{no}} | makerbot={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```
Outputs sampling frequency of the accelerometer as \"sample freq:
`<freq>`{=html}\".

#### M976: Measure Print Head Resonance {#m976_measure_print_head_resonance}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{yes}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | reprapfirmware={{no}} | makerbot={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   **X/Y** choose motor to use
:   **F** motion speed in rev/sec
:   **R** number of revolutions

Outputs frequency response

#### M977: Calibrate Motor {#m977_calibrate_motor}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{yes}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | reprapfirmware={{no}} | makerbot={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   **X/Y** choose motor to use

Calibrates given motor and sets the newly found compensation.

#### M995: Calibrate Touch Screen {#m995_calibrate_touch_screen}

```{=mediawiki}
{{Firmware Support | grbl={{no}} | fived={{no}} | teacup={{no}} | makerbot={{no}} | redeem={{no}} | sprinter={{no}} | marlin={{yes|2.0.6+}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | reprapfirmware={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | mk4duo={{no}} | klipper={{no}} | yaskawa={{no}} }}
```
#### M997: Perform in-application firmware update {#m997_perform_in_application_firmware_update}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes|2.0.0+}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | reprapfirmware={{yes}} | makerbot={{no}} | redeem={{no}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Parameters
:   `Snnn` Firmware module number(s), default 0
:   `Bnnn` Expansion board address, default 0 (i.e. main controller
    board)

Example

`M997 S0:1 ; update firmware modules 0 and 1 on the main controller board`\
`M997 B3 ; update firmware module 0 on the expansion board with address 3`

This command triggers a firmware update if the necessary files are
present on the SD card. In RepRapFirmware on the Duet series, module
numbers are as follows:

0 - main firmware. The firmware filename depends on the controller
electronics, e.g.sys/RepRapFirmware.bin (Duet 06/085),
sys/Duet2CombinedFirmware (Duet WiFi/Ethernet),
sys/DuetMaestroFirmware.bin (Duet Maestro). File sys/iap.bin (Duet),
sys/iap4e.bin (Duet WiFi/Ethernet) or sys/iap4s.bin (Duet Maestro) must
also be present.

1 - WiFi module firmware, filename sys/DuetWiFiServer.bin

2 - Reserved (on Duet WiFi running RepRapFirmware 1.18 and earlier, was
web server file system)

3 - Duet WiFi main boards: put the WiFi module into bootloader mode so
that firmware can be uploaded directly via its serial port. Duet 3
expansion boards: update the bootloader (RepRapFirmware 3.2 and later).

4 - Updates the firmware on an attached PanelDue v3 or later touch
screen (supported in RRF 3.2 and later)

In marlin, `M997` will trigger a firmware update after the update file
has been uploaded to the SD card, on the following platforms: LPC176x,
STM32, STM32F1

#### M998: Request resend of line {#m998_request_resend_of_line}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{no}} | bfb={{no}} | machinekit={{no}} | reprapfirmware={{yes}} }}
```

Parameters
:   `Pnnn` Line number

Example

`M998 P34`

Request a resend of line 34. In some implementations the input-handling
code overwrites the incoming G Code with this when it detects, for
example, a checksum error. Then it leaves it up to the G-code
interpreter to request the resend.

#### M999: Restart after being stopped by error {#m999_restart_after_being_stopped_by_error}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{yes}} | prusa={{no}} | buddy={{no}} | repetier={{no}} | smoothie={{yes}} | reprapfirmware={{yes}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{no}} | mk4duo={{yes}} | yaskawa={{no}} }}
```

Parameters
:   *This command can be used without any additional parameters.*
:   `Pnnn` Reset flags^1^
:   `Bnnn` CAN address of the board to reset (RRF only)^2^

Example

`M999`

Restarts the firmware using a software reset.

Notes

^1^The dc42 fork of RepRapFirmware not only resets the board but also
puts the board into firmware upload mode if parameter PERASE is present.
^2^Starting from RRF 3.3 this parameter may be set to -1 to reboot the
attached SBC (DuetPi + SBC)

## Other commands {#other_commands}

#### G: List all G-codes {#g_list_all_g_codes}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | smoothie={{no}} | repetier={{no}} | reprapfirmware={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{yes}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Example

`G`

Print a list of all implemented G-codes in the firmware with description
to the host.\
(Note: this has been implemented in
[Redeem](Redeem "Redeem"){.wikilink}, and so is only a proposal.)

#### M: List all M-codes {#m_list_all_m_codes}

```{=mediawiki}
{{Firmware Support | fived={{no}} | teacup={{no}} | sprinter={{no}} | marlin={{no}} | prusa={{no}} | buddy={{no}} | smoothie={{no}} | repetier={{no}} | reprapfirmware={{no}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{yes}} | mk4duo={{no}} | yaskawa={{no}} }}
```

Example

`M`

Print a list of all implemented M-codes in the firmware with description
to the host.\
(Note: this has been implemented in
[Redeem](Redeem "Redeem"){.wikilink}, and so is only a proposition)

#### T: Select Tool {#t_select_tool}

```{=mediawiki}
{{Firmware Support | fived={{yes}} | teacup={{yes}} | sprinter={{no}} | marlin={{yes}} | prusa={{yes}} | buddy={{no}} | repetier={{yes}} | smoothie={{yes}} | reprapfirmware={{yes}} | bfb={{no}} | grbl={{no}} | makerbot={{no}} | machinekit={{no}} | redeem={{yes}} | mk4duo={{yes}} | yaskawa={{yes}} }}
```

Parameters
:   *This command can be used without any additional parameters.*
:   `Pnnn`: Bitmap of all the macros to be run (only RRF 1.17b or later)
:   Tool number

Example

`T1`

Select tool (or in older implementations extruder) number 1 to build
with.

The sequence followed is:

1.  Set the current tool to its standby temperatures specified by `G10`
    (see above),
2.  Set the new tool to its operating temperatures specified by `G10`
    and wait for **all** temperatures to stabilise,
3.  Apply any X, Y, Z offset for the new tool specified by `G10`,
4.  Use the new tool.

Selecting a non-existent tool (100, say) just does Step 1 above^1^. That
is to say it leaves all tools in their standby state. You can, of
course, use the `G10` command beforehand to set that standby temperature
to anything you like.

Note that you may wish to move to a parking position *before* executing
a T command in order to allow the new extruder to reach temperature
while not in contact with the print. It is acceptable for the firmware
to apply a small offset \[by convention (-1mm x tool-number) in Y\] to
the current position when the above sequence is entered to allow
temperature changes to take effect just away from the parking position.
Any such offset must, of course, be undone when the procedure finishes.

If the Z value changes in the offsets and the tool moves up, then the Z
move is made before the X and Y moves. If Z moves down, X and Y are done
first.

Some firmware (Such as Prusa i3 Printers with MMU) also support the `Tx`
(recommended) and `T?`(depricated)^2^ commands to prompt the user to
select a tool (or a filament in the case of the MultiMaterial Unit) on
the printer\'s menu. Then the `Tc` command actually loads the selected
filament.

Some implementations (e.g. RepRapFirmware) allow you to specify
tool-change G Code macros^3^. There are normally three specified (any of
which can contain no commands if desired) that execute in this order:

1.  Actions to do with the old tool before it is released - macro name:
    `tfreeN.g` where N is the tool number;
2.  (Old tool is released);
3.  Actions to do with the new tool before it is selected - macro name:
    `tpreN.g` where N is the tool number;
4.  (New tool is selected); and
5.  Actions to do with the new tool after it is selected - macro name:
    `tpostN.g` where N is the tool number.

With such implementations there is no wait for temperature
stabilisation. That can be achieved by an `M116` in any of the macros,
of course. However be aware that recent RepRapFirmware versions does NOT
run any tool change macros if the axes are not homed.

After a reset tools will not start heating until they are selected. You
can either put them all at their standby temperature by selecting them
in turn, or leave them off so they only come on if/when you first use
them. The `M0`, `M1`, and `M112` commands turn them all off. You can, of
course, turn them all off with the `M1` command, then turn some back on
again. Don\'t forget also to turn on the heated bed (if any) if you use
that trick.

Tool numbering may start at 0 or 1, depending on the implementation.
Some implementations (those that use the `M563` command to define tools)
allow the user to specify tool numbers, so with them you can have tools
17, 99 and 203 if you want. Negative numbers are not allowed.

Notes

^1^ For RepRapFirmware, selecting a non-existent tool also removes any
X/Y/Z offset applied for the old tool.

^2^ `T?` was the original form of the command, but it was changed to
`Tx` when it was realized that the question mark character caused
problems when printing through octoprint. This change was implemented in
Prusa firmware 3.5.0.

^3^ Under special circumstances, the execution of those macro files may
not be desired. RepRapFirmware 1.17b or later supports an optional `P`
parameter to specify which macros shall be run. If absent then all the
above macros will be run. Otherwise pass a bitmap of all the macros to
be executed. The bitmap of this value consists of tfree=1, tpre=2 and
tpost=4.

#### D: Debug codes {#d_debug_codes}

```{=mediawiki}
{{Firmware Support | prusa={{yes}}  }}
```
NOTE: These D codes are not compatible with the Gcode spec ( NIST Gcode
spec, initially written for CNC, which Reprap initially messed up, after
what the CNC side of Reprap has spent years trying to get Reprap back to
respecting it ), and will make life hell for those building machines
that do more than just 3D printing, or controllers that support this, as
well as possibly cause other issues. I see this is from Prusa, and
I know these guys are really cool about Open-Source, so I\'m sure they
care a lot about respecting standards and other projects as well, so
I\'m certain they\'ll fix this as soon as they see there is an issue.
Thankfully this is very easy to fix, just change from D1 to Mxxx D1,
where you find a Mxxx Gcode that is currently free and start using it.
In Gcode, only M, G and T are keywords, D is a parameter, you can\'t
make it a keyword without messing everything up. I\'m sure for your
subset of using Gcode, that\'s probably just fine, but it\'s not for the
rest of us, and the whole point of adding things to this page, is for
others to use it if they want/can/need, and the way it currently is (
breaking a standard ), this can\'t be used by others. Links:

- <https://en.wikipedia.org/wiki/G-code>
- <https://www.nist.gov/publications/nist-rs274ngc-interpreter-version-3>

This note by: \-- wolf.arthur@gmail.com

Debug codes are not active by defalut and must be defined in source
code.

##### D-1: Endless Loop {#d_1_endless_loop}

```{=mediawiki}
{{Firmware Support | prusa={{yes}}  }}
```

:   *\-\--*

##### D0: Reset {#d0_reset}

```{=mediawiki}
{{Firmware Support | prusa={{yes}}  }}
```

:   *This command will reset the board*
:   `B`: Bootloader

##### D1: Clear EEPROM and RESET {#d1_clear_eeprom_and_reset}

```{=mediawiki}
{{Firmware Support | prusa={{yes}}  }}
```

:   *This command will clear the EEPROM and reset the board*

##### D2: Read/Write RAM {#d2_readwrite_ram}

```{=mediawiki}
{{Firmware Support | prusa={{yes}}  }}
```

Parameters
:   *This command can be used without any additional parameters. It will
    read the entire RAM.*
:   `Annnn`: Address (x0000-x1fff)
:   `Cnnnn`: Count (1-8192)
:   `Xnnnn`: Data (hex)

<!-- -->

Notes
:   The hex address needs to be lowercase without the 0 before the x
:   Count is decimal
:   The hex data needs to be lowercase

##### D3: Read/Write EEPROM {#d3_readwrite_eeprom}

```{=mediawiki}
{{Firmware Support | prusa={{yes}}  }}
```

Parameters
:   *This command can be used without any additional parameters. It will
    read the entire EEPROM.*
:   `Annnn`: Address (x0000-x0fff)
:   `Cnnnn`: Count (1-4096)
:   `Xnnnn`: Data (hex)

<!-- -->

Notes
:   The hex address needs to be lowercase without the 0 before the x
:   Count is decimal
:   The hex data needs to be lowercase

##### D4: Read/Write PIN {#d4_readwrite_pin}

```{=mediawiki}
{{Firmware Support | prusa={{yes}}  }}
```

:   *To read the digital value of a pin you need only to define the pin
    number.*

Parameters
:   `Pnnn`: Pin (0-255)
:   `Fn`: Function in/out (0/1)
:   `Vn`: Value (0/1)

##### D5: Read/Write FLASH {#d5_readwrite_flash}

```{=mediawiki}
{{Firmware Support | prusa={{yes}}  }}
```

Parameters
:   *This command can be used without any additional parameters. It will
    read the 1kb FLASH.*
:   `Annnn`: Address (x00000-x3ffff)
:   `Cnnnn`: Count (1-8192)
:   `Xnnnn`: Data (hex)
:   `E`: Erase

<!-- -->

Notes
:   The hex address needs to be lowercase without the 0 before the x
:   Count is decimal
:   The hex data needs to be lowercase

##### D6: Read/Write external FLASH {#d6_readwrite_external_flash}

```{=mediawiki}
{{Firmware Support | prusa={{yes}}  }}
```

:   Reserved

##### D7: Read/Write Bootloader {#d7_readwrite_bootloader}

```{=mediawiki}
{{Firmware Support | prusa={{yes}}  }}
```

:   Reserved

##### D8: Read/Write PINDA {#d8_readwrite_pinda}

```{=mediawiki}
{{Firmware Support | prusa={{yes}}  }}
```

Parameters
:   `?`: Read PINDA temperature shift values
:   `!`: Reset PINDA temperature shift values to default
:   `Pnnn`: Pinda temperature \[C\]
:   `Znnnn`: Z Offset \[mm\]

##### D9: Read/Write ADC {#d9_readwrite_adc}

```{=mediawiki}
{{Firmware Support | prusa={{yes}}  }}
```

Parameters
:   `I(index)`: ADC channel index
:   `I0`: Heater 0 temperature
:   `I1`: Heater 1 temperature
:   `I2`: Bed temperature
:   `I3`: PINDA temperature
:   `I4`: PWR voltage
:   `I5`: Ambient temperature
:   `I6`: BED voltage
:   `V`: Value to be written as simulated

===== D10: Set XYZ calibration = OK =====
`{{Firmware Support | prusa={{yes}}  }}`{=mediawiki}

##### D12: Time {#d12_time}

```{=mediawiki}
{{Firmware Support | prusa={{yes}}  }}
```

:   *Writes current time in the log file.*

##### D20: Generate an offline crash dump {#d20_generate_an_offline_crash_dump}

```{=mediawiki}
{{Firmware Support | prusa={{yes}}  }}
```

:   *Generate a crash dump for later retrival.*

<!-- -->

Usage
:   `D20 [E]`

<!-- -->

Parameters
:   `E`: Perform an emergency crash dump (resets the printer).

<!-- -->

Notes
:   A crash dump can be later recovered with D21, or cleared with D22.
:   An emergency crash dump includes register data, but will cause the
    printer to reset after the dump is completed.

##### D21: Print crash dump to serial {#d21_print_crash_dump_to_serial}

```{=mediawiki}
{{Firmware Support | prusa={{yes}}  }}
```

:   *Output the complete crash dump (if present) to the serial.*

<!-- -->

Usage
:   `D21`

<!-- -->

Notes
:   The starting address can vary between builds, but it\'s always at
    the beginning of the data section.

##### D22: Clear crash dump state {#d22_clear_crash_dump_state}

```{=mediawiki}
{{Firmware Support | prusa={{yes}}  }}
```

:   *Clear an existing internal crash dump.*

<!-- -->

Usage
:   `D22`

##### D23: Request emergency dump on serial {#d23_request_emergency_dump_on_serial}

```{=mediawiki}
{{Firmware Support | prusa={{yes}}  }}
```

:   *On boards without offline dump support, request online dumps to the
    serial port on firmware faults.*
:   *When online dumps are enabled, the FW will dump memory on the
    serial before resetting.*

<!-- -->

Usage
:   `D23 [E] [R]`

<!-- -->

Parameters
:   `E`: Perform an emergency crash dump (resets the printer).
:   `R`: Disable online dumps.

##### D80: Bed check {#d80_bed_check}

```{=mediawiki}
{{Firmware Support | prusa={{yes}}  }}
```

:   *This command will log data to SD card file \"mesh.txt\".*

<!-- -->

Parameters
:   `E`: Dimension X (default 40)
:   `F`: Dimension Y (default 40)
:   `G`: Points X (default 40)
:   `H`: Points Y (default 40)
:   `I`: Offset X (default 74)
:   `J`: Offset Y (default 34)

##### D81: Bed analysis {#d81_bed_analysis}

```{=mediawiki}
{{Firmware Support | prusa={{yes}}  }}
```

:   *This command will log data to SD card file \"wldsd.txt\".*

<!-- -->

Parameters
:   `E`: Dimension X (default 40)
:   `F`: Dimension Y (default 40)
:   `G`: Points X (default 40)
:   `H`: Points Y (default 40)
:   `I`: Offset X (default 74)
:   `J`: Offset Y (default 34)

##### D106: Print measured fan speed for different pwm values {#d106_print_measured_fan_speed_for_different_pwm_values}

```{=mediawiki}
{{Firmware Support | prusa={{yes}}  }}
```
##### D2130: Trinamic stepper controller {#d2130_trinamic_stepper_controller}

```{=mediawiki}
{{Firmware Support | prusa={{yes}}  }}
```

:   Reserved

##### D9125: PAT9125 filament sensor {#d9125_pat9125_filament_sensor}

```{=mediawiki}
{{Firmware Support | prusa={{yes}}  }}
```

:   *This command can be used without any additional parameters. It will
    read the PAT9125 values.*

Parameters
:   `?`: Print values
:   `!`: Print values
:   `R`: Resolution. Not active in code
:   `X`: X values
:   `Y`: Y values
:   `L`: Activate filament sensor log

## Proposed EEPROM configuration codes {#proposed_eeprom_configuration_codes}

**Background:** Every 3D printer has parameters that need to be
persistent but also easily tunable, such as extrusion steps-per-mm and
various planner values. Some of these parameters are hardcoded in
firmware so that a user has to modify, recompile, and re-flash the
firmware for certain adjustments, while others can be modified with an
M-code and stored to the EEPROM or other persistent storage.

**Current implementations:**

:   [Marlin](Marlin "Marlin"){.wikilink} and
    [Sprinter](Sprinter "Sprinter"){.wikilink} use G-codes `M500`-`M503`
    to save, load, reset, and report the settings mirrored in EEPROM.
    Note that the `M503` command reports settings that may not have been
    saved to EEPROM yet.

<!-- -->

:   [Teacup](Teacup "Teacup"){.wikilink} uses G-codes `M130`-`M136` to
    set, read, and save PID values.

<!-- -->

:   [Repetier
    Firmware](Repetier_Firmware "Repetier Firmware"){.wikilink} uses
    `M206` to set a stored value (using an ID number) and `M205` to
    report settings.

<!-- -->

:   [RepRapFirmware](RepRapFirmware "RepRapFirmware"){.wikilink} uses
    the `config-override.g` file on the SD card for settings storage.
    `M500` saves some values to that file, `M501` re-loads settings from
    this file, and `M502` loads the \"factory settings\" values from
    `config.g`, ignoring `config-override.g`.

*Please see the RFC [M-codes for EEPROM
config](M-codes_for_EEPROM_config "M-codes for EEPROM config"){.wikilink}
proposed by [AlexRa](User:AlexRa "AlexRa"){.wikilink} in March of 2011.
There is currently no working implementation of the proposed commands.*

## Replies from the RepRap machine to the host computer {#replies_from_the_reprap_machine_to_the_host_computer}

All communication is in printable ASCII characters.

Messages sent back to the host computer are terminated by a newline.

The basic protocol responses look like this:

**xx \[line number to resend\] \[T:93.2 B:22.9\] \[C: X:9.2 Y:125.4
Z:3.7 E:1902.5\] \[Some debugging or other information may be here\]**

`xx` can be one of:

- `ok` - The RepRap machine is ready to receive the next line from the
  host.
- `rs` or `Resend` - There was a communication error and the RepRap
  machine is requesting a resend of the line in question. The line is
  specified either as `N``<linenumber>`{=html} or
  `N:``<linenumber>`{=html}. Examples: `Resend: 123`, `Resend: N123`,
  `rs:123`
- `!!` or `Error:` or `fatal:` (Repetier Firmware) - There was an error.
  Common communication errors such as
  `checksum mismatch, Last Line: ``<number>`{=html} or `Wrong checksum`,
  `No Checksum with line number, Last Line: ``<number>`{=html} or
  `Missing checksum`,
  `Line Number is not Last Line Number+1, Last Line: ``<number>`{=html}
  or `expected line ``<number1>`{=html}` got ``<number2>`{=html} are
  recoverable and should immediately be followed by a resend. Other
  non-fatal errors commonly include
  `Unknown command: "``<command>`{=html}`"` and several SD related
  errors such as `<code>`{=html}Cannot open subdir
  <dir>

  `</code>`{=html}, `SD init fail`, `volume.init failed`,
  `openRoot failed`, `workDir open failed`,
  `open failed, File: ``<name>`{=html}, `error writing to file`,
  `<code>`{=html}Cannot enter subdir:

  <dir>

  `</code>`{=html} and `SD read error`. Any other errors indicate a
  hardware fault that will make the RepRap machine shut down immediately
  after it has sent this message. They should be considered fatal by
  hosts.
- `wait` - The RepRap machine\'s command buffers are empty and it is
  waiting for the next line from the host.
- `busy:``<reason>`{=html} - The RepRap machine is busy for some reason
  and currently cannot receive or process commands through the serial
  interface from a connected host. Possible reasons are: \`processing\`
  (the RepRap machine is busy with processing some lengthy command, like
  homing, heatup or auto leveling), `paused for user` (the RepRap
  machine is paused and awaiting an action by the user via its built in
  controller unit, e.g. clicking the button), `paused for input` (the
  RepRap machine is paused and waiting for input from the user via its
  built in controller unit, e.g. selecting a menu option). Examples:
  `busy: processing`, `busy: paused for user`.

The **T:** and **B:** values are the temperature of the
currently-selected extruder and the bed respectively, and are only sent
in response to `M105`. If such temperatures don\'t exist (for example
for an extruder that works at room temperature and doesn\'t have a
sensor) then a value below absolute zero (-273^o^C) is returned.

**C:** means that coordinates follow. Those are the **X: Y:** etc
values. These are only sent in response to `M114` and `M117`.

The RepRap machine may also send lines that look like this:

**// This is some debugging or other information on a line on its own.
It may be sent at any time.**

Such lines will always be preceded by **//**.

The most common response is simply:

`ok`

When the machine boots up it sends the string

`start`

once to the host before sending anything else. This should not be
replaced or augmented by version numbers and the like. `M115` (see
above) requests those.

Originally, every line sent by RepRap to the host computer except the
start line was supposed to have a two-character prefix (one of `ok`,
`rs`, `!!` or `//`). The machine should never send a line without such a
prefix. These days, firmwares generally do not adhere to this rule and
thus it should be considered obsolete.

### Example of a communication error with resend request {#example_of_a_communication_error_with_resend_request}

`>>>` are lines sent from the host to the RepRap machine, `<<<` are
lines sent from the RepRap machine to the host.

` >>> N66555 G1 X131.338 Y133.349 E0.0091*91`\
` <<< ok`\
` >>> N66556 G1 X131.574 Y133.428 E0.0046*42`\
` <<< Error:checksum mismatch, Last Line: 66555`\
` <<< Resend: 66556`\
` <<< ok`\
` >>> N66556 G1 X131.574 Y133.428 E0.0046*92`\
` <<< ok`

### Action commands {#action_commands}

The current versions of Pronterface and OctoPrint can interpret special
commands sent by the firmware of the form:

`//action:``<command>`{=html}

Other hosts simply ignore or echo this output from the firmware.

The available Host Action Commands are:

- `start`: Tell the host to start the currently selected print job.
  (OctoPrint 1.5.0+)
- `pause`: Tell the host to pause the print job.
- `resume`: Tell the host to resume the print job.
- `disconnect`: Tell the host to disconnect from the printer.
- `cancel`: Tell the host to abort the current job.
- `out_of_filament T``<extruder_id>`{=html}: Tell the host that an
  extruder\'s filament is out or jammed. Host should issue a pause and
  can offer better help to the user. For backwards-compatibility it
  should be followed by the `pause` action.
- `paused`: Tell the host that a printer-controlled print job was
  paused. (OctoPrint 1.3.9+)
- `resumed`: Tell the host that a printer-controlled print job was
  resumed. (OctoPrint 1.3.9+)
- `probe_rewipe`: Display a \"`G29` Probing Retrying\" alert. (Lulzbot
  Cura 3.6+)
- `probe_failed`: Cancel the print job and display a \"`G29` Probing
  Failed\" alert. (Lulzbot Cura 3.6+)
- `sd_inserted`: The SD card was inserted. Hosts should update internal
  state as needed. (OctoPrint 1.6.0+)
- `sd_ejected`: The SD card was ejected. Hosts should update internal
  state as needed. (OctoPrint 1.6.0+)
- `sd_updated`: The SD card was updated. Hosts should update internal
  state as needed. (OctoPrint 1.6.0+)

Action commands can also be sent by the firmware to have the host show
alerts and prompts for user feedback. The following commands are
supported by OctoPrint 1.3.9 or later with the \"Action Command Prompt
support\" plugin enabled.

- `prompt_begin ``<message>`{=html}: Start a user prompt dialog that
  displays `<message>`{=html} to the user.
- `prompt_choice ``<text>`{=html}: Define a dialog choice with the
  associated `<text>`{=html}.
- `prompt_button ``<text>`{=html}: Same as `prompt_choice`.
- `prompt_show`: Tell the host to prompt the user with the defined
  dialog.
- `prompt_end`: Tell the host to close the dialog (e.g., the choice was
  made from the printer\'s own UI).

After showing a user dialog the host should wait for feedback and send
the user\'s selection back to the firmware with `M876 Snnn` as described
in
[G-Code#M876:\_Dialog_handling](G-Code#M876:_Dialog_handling "G-Code#M876:_Dialog_handling"){.wikilink}.
On connection (or whenever the functionality is enabled in the host) the
host can tell the firmware that it supports host dialogs by sending
`M876 P1`.

For more detailed examples of `prompt_*` action command dialogs, see
[OctoPrint\'s
documentation](http://docs.octoprint.org/en/master/bundledplugins/action_command_prompt.html).

### Further notes {#further_notes}

RepRapFirmware responds to some commands with a reply string in JSON
format, terminated by a newline. This allows later firmware revisions to
include additional information without confusing clients (e.g. PanelDue)
that do not expect it, and to make responses self-describing so that the
client will not be confused if responses are delayed or lost. The
commands affected are:

- `M105 S2` (now deprecated in favor of `M408` and `M409`)
- `M105 S3` (now deprecated in favor of `M408` and `M409`)
- `M20 S2`
- `M36`
- `M408`
- `M409`

It is also possible to generate GCODE by using ChatGPT prompts such as
following source [additive
blog](https://addithive.com/2023/03/20/generating-gcode-for-3d-printing-with-chat-gpt-4/):

\"write the gcode of 10cm \* 10cm \* 10cm cube with 50% infill for an
open source reprap design 3d printer\"

## Proposal for sending multiple lines of G-code {#proposal_for_sending_multiple_lines_of_g_code}

So far, this is a proposal, open for discussion.

#### Problem to solve {#problem_to_solve}

When using Marlin firmware or emulating Marlin, each line of G-code sent
from the host to the controller is answered with an `ok` before the next
line can be sent without locking communications up. This slows down
communication and limits the number of commands-per-second that can be
sent to the control board, and the USB stack on the host and the serial
interface driver on the Arduino also add their own latencies (up to 10
milliseconds). This is not a problem for other controller electronics
using native USB such as the Duet, because the standard serial-over-USB
drivers provide flow control, so the host software can be configured not
to wait for the `ok`.

For more details on this proposal, some suggested solutions and
comments, please see
[GCODE_buffer_multiline_proposal](GCODE_buffer_multiline_proposal "GCODE_buffer_multiline_proposal"){.wikilink}

## Alternatives to G-code {#alternatives_to_g_code}

:   *Main article: [Firmware/Alternative#alternatives to
    G-code](Firmware/Alternative#alternatives_to_G-code "Firmware/Alternative#alternatives to G-code"){.wikilink}*

Several people have suggested using STEP-NC or some other control
language; or perhaps designing a completely new control language.

[ ](Category:G-code " "){.wikilink}
[Category:Firmware](Category:Firmware "Category:Firmware"){.wikilink}
[Category:Software](Category:Software "Category:Software"){.wikilink}
[Category:Reference](Category:Reference "Category:Reference"){.wikilink}
