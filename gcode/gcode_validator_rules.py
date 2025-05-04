# Registering G-code commands
# See https://reprap.org/wiki/G-code
# See https://help.prusa3d.com/article/buddy-firmware-specific-g-code-commands_633112

from gcode.gcode_command import GcodeCommand
from gcode.gcode_validator import GCodeValidator

# The G-code validator instance prefers the Prusa Buddy firmware rules.
validator = GCodeValidator()
default_validator = validator

# A number type that is either float or int.
num = (float, int)

# A flag type, that sometimes can have a value, that we should ignore.
flag_ignore_value = (bool, num)

def require_fields(*field_names: str):
    """Returns a validator function that ensures the specified fields are present."""
    def validator(command):
        missing = [f for f in field_names if f not in command.fields]
        if missing:
            raise ValueError(f"{command.command} is missing required field(s): {', '.join(missing)}")
    return validator

def require_at_least_one(command: GcodeCommand):
    """
    Checks at least one of the field is present in the command.

    Args:
        command (GcodeCommand): The GcodeCommand instance to check.

    Returns:
        bool: True if at least one required field is present, otherwise raises ValueError.
    """
    if len(command.fields) == 0:
        raise ValueError(f"{command.command} requires at least one of the fields, but none were provided.")

    return True

def arc_move_rule(command: GcodeCommand):
    """Ensure either I/J or R is present for G2 and G3"""
    if not ("I" in command.fields and "J" in command.fields) and "R" not in command.fields:
        raise ValueError(f"{command.command} requires either I and J fields or an R field.")
          
# Helper function to validate percentage values (0-100)
def validate_percentage(*field_names: str):
    """Returns a validator function that ensures fields are percentages between 0 and 100."""
    def validator(command):
        for field_name in field_names:
            if field_name in command.fields:
                if command.fields[field_name] < 0 or command.fields[field_name] > 100:
                    raise ValueError(f"{command.command} {field_name} must be between 0 and 100.")
    return validator

# Helper function to ensure fields are mutually exclusive
def mutually_exclusive(*field_names: str):
    """Returns a validator function that ensures only one of the specified fields is present."""
    def validator(command):
        present_fields = [f for f in field_names if f in command.fields]
        if len(present_fields) > 1:
            raise ValueError(f"{command.command} fields {', '.join(present_fields)} are mutually exclusive.")
    return validator

# Helper function to validate binary values (0 or 1)
def validate_binary(*field_names: str):
    """Returns a validator function that ensures fields are either 0 or 1."""
    def validator(command):
        for field in field_names:
            if field in command.fields and command.fields[field] not in [0, 1]:
                raise ValueError(f"{command.command} field {field} must be either 0 or 1.")
    return validator

# Helper function to validate tool change parameters
def validate_tool_change_params(command: GcodeCommand):
    """Validates tool change parameters have correct values."""
    validate_binary("S", "M", "D")(command)
    if "L" in command.fields and command.fields["L"] not in [0, 1, 2]:
        raise ValueError(f"{command.command} L must be 0, 1, or 2")

# List of all rules, keep the list sorted by command for easier maintenance.

# G0/G1: Move
validator.register_rule("G0", {
    "X": num, # X coordinate (mm)
    "Y": num, # Y coordinate (mm)
    "Z": num, # Z coordinate (mm)
    "E": num, # Extruder position (mm)
    "F": num, # Feedrate (mm/min)
    "S": bool # Flag parameter
}, custom_rule=require_at_least_one)

validator.register_rule("G1", {
    "X": num, # X coordinate (mm)
    "Y": num, # Y coordinate (mm)
    "Z": num, # Z coordinate (mm)
    "E": num, # Extruder position (mm)
    "F": num, # Feedrate (mm/min)
    "S": bool # Flag parameter
}, custom_rule=require_at_least_one)

# G2: Controlled Arc Move (Clockwise)
validator.register_rule("G2", {
    "Z": num, # Z coordinate (mm)
    "E": num, # Extruder position (mm)
    "F": num, # Feedrate (mm/min)
    "R": num, # Radius (mm)
    "K": num  # K parameter
}, custom_rule=arc_move_rule)

# G3: Controlled Arc Move (Counter-Clockwise)
validator.register_rule("G3", {
    "Z": num, # Z coordinate (mm)
    "E": num, # Extruder position (mm)
    "F": num, # Feedrate (mm/min)
    "R": num, # Radius (mm)
    "K": num  # K parameter
}, custom_rule=arc_move_rule)

# G4: Dwell
validator.register_rule("G4", {
    "P": int, # Time in milliseconds
    "S": int  # Time in seconds
})

# G10: Retract
validator.register_rule("G10", {
    "S": int # Tool number
})

# G11: Unretract
validator.register_rule("G11", {
    "S": int # Tool number
})

# G20: Set Units to Inches
validator.register_rule("G20", {})

# G21: Set Units to Millimeters
validator.register_rule("G21", {})

# G22: Firmware Retract
validator.register_rule("G22", {})

# G23: Firmware Recover
validator.register_rule("G23", {})

# G26: Mesh Validation Pattern
validator.register_rule("G26", {
    "X": bool, # X axis
    "Y": bool, # Y axis
    "Z": bool, # Z axis
    "P": int,  # Pattern
    "S": int,  # Size
    "T": int,  # Type
    "E": float # Extruder
}, custom_rule=require_fields("X", "Y", "Z"))

# G27: Park Toolhead
validator.register_rule("G27", {
    "X": bool, # X axis
    "Y": bool, # Y axis
    "Z": bool, # Z axis
    "P": int # Position
}, custom_rule=require_fields("X", "Y", "Z"))

# G28: Move to Origin (Home)
validator.register_rule("G28", {
    "X": flag_ignore_value, # Home X axis
    "Y": flag_ignore_value, # Home Y axis
    "Z": flag_ignore_value, # Home Z axis
    "I": bool, # Imprecise: do not perform precise refinement
    "L": bool, # Force leveling state ON (if possible)
    "N": bool, # No-change mode (do not change any motion setting such as feedrate)
    "O": bool, # Home only if the position is not known and trusted
    "P": bool, # Do not check print sheet presence
    "R": float, # <linear> Raise by n mm/inches before homing
    "S": bool, # Simulated homing only in MARLIN_DEV_MODE
    "W": bool, # Suppress mesh bed leveling if `X`, `Y` or `Z` are not provided
    "C": bool  # Calibrate X and Y origin (home) - Only on MK3/s
})

# G29: Unified Bed Leveling
# This is a complex command that supports a lot of different features.
# See https://github.com/prusa3d/Prusa-Firmware-Buddy/blob/818d812f954802903ea0ff39bf44376fb0b35dd2/lib/Marlin/Marlin/src/gcode/bedlevel/ubl/G29.cpp
validator.register_rule("G29", {
    "A": bool,  # Activate UBL
    "P": num,   # Phase
    "B": bool,  # Business Card mode
    "C": bool,  # Continue with the closest mesh point
    "D": bool,  # Disable UBL
    "E": bool,  # Edit the mesh values
    "F": num,   # Fade Height
    "H": num,   # Height Value
    "I": bool,  # Invalidate a mesh point
    "J": int,   # Grid Size
    "K": bool,  # Kompare Mesh Values
    "L": bool,  # Load Mesh
    "M": bool,  # Manual Edit
    "N": bool,  # Next Mesh Point
    "O": bool,  # Fine Tune (Offset) Mesh
    "Q": bool,  # Query Mesh
    "R": bool,  # Restore Mesh
    "S": bool,  # Save Mesh
    "T": bool,  # Three Point Probe
    "U": bool,  # Unlevel the Bed
    "V": int,   # Version and Info
    "W": int,   # Requires UBL_DEVEL_DEBUGGING. What? What is my Mesh?
    "X": num,   # X Coordinate
    "Y": num,   # Y Coordinate
    "Z": num    # Z Offset
})

# G30: Single Z-Probe
validator.register_rule("G30", {
    "X": float, # X coordinate
    "Y": float, # Y coordinate
    "Z": float, # Z coordinate
    "P": int,   # Probe number
    "S": int    # Probe type
})

# G31: Set or Report Current Probe Status
validator.register_rule("G31", {
    "X": float, # X coordinate
    "Y": float, # Y coordinate
    "Z": float, # Z coordinate
    "P": int    # Probe number
})

# G32: Probe Z and Calibrate Bed
validator.register_rule("G32", {
    "S": int # Start calibration
})

# G33: Delta Auto Calibration
validator.register_rule("G33", {
    "P": int, # Pattern
    "S": int  # Size
})

# G34: Set Delta Height
validator.register_rule("G34", {
    "P": int, # Position
    "S": int  # Size
})

# G35: Tramming Assistant
validator.register_rule("G35", {
    "P": bool, # Pattern
    "S": bool  # Size
})

# G36: Mesh Bed Leveling
validator.register_rule("G36", {
    "P": bool, # Pattern
    "S": bool  # Size
})

# G37: Probe Z and Save Mesh
validator.register_rule("G37", {
    "P": bool, # Pattern
    "S": bool  # Size
})

# G38: Probe Target
validator.register_rule("G38", {
    "X": bool, # X axis
    "Y": bool, # Y axis
    "Z": bool, # Z axis
    "P": bool, # Pattern
    "S": bool  # Size
}, custom_rule=require_fields("X", "Y", "Z"))

# G39: Probe Bed and Save Mesh
validator.register_rule("G39", {
    "P": bool, # Pattern
    "S": bool  # Size
})

# G40: Cancel Tool Offset
validator.register_rule("G40", {})

# G80: Cancel Current Motion Mode
validator.register_rule("G80", {})

# G90: Set to Absolute Positioning
validator.register_rule("G90", {})

# G92: Set Position
validator.register_rule("G92", {
    "X": num, # X position
    "Y": num, # Y position
    "Z": num, # Z position
    "E": num  # Extruder position
})

# M0: Stop or Unconditional stop
validator.register_rule("M0", {})

# M17: Enable Steppers
validator.register_rule("M17", {
    "X": bool, # Enable X stepper
    "Y": bool, # Enable Y stepper
    "Z": bool, # Enable Z stepper
    "E": bool, # Enable E stepper
    "I": bool, # Enable I stepper
    "J": bool, # Enable J stepper
    "K": bool, # Enable K stepper
    "U": bool, # Enable U stepper
    "V": bool, # Enable V stepper
    "W": bool  # Enable W stepper
})

# M18: Disable all stepper motors
validator.register_rule("M18", {})

# M20: List SD card
validator.register_rule("M20", {})

# M23: Select SD file
validator.register_rule("M23", {})

# M24: Start/resume SD print
validator.register_rule("M24", {})

# M25: Pause SD print
validator.register_rule("M25", {
    "U": bool # Unload filament when paused
})

# M27: Report SD print status
validator.register_rule("M27", {})

# M28: Begin write to SD card
validator.register_rule("M28", {})

# M29: Stop writing to SD card
validator.register_rule("M29", {})

# M30: Delete a file on the SD card
validator.register_rule("M30", {})

# M31: Output time since last M109 or SD card start to serial
validator.register_rule("M31", {})

# M32: Select file and start SD print
validator.register_rule("M32", {})

# M42: Switch I/O pin
validator.register_rule("M42", {})

# M46: Show the assigned IP address
validator.register_rule("M46", {})

# M50: Selftest
validator.register_rule("M50", {
    "X": bool, # X axis test
    "Y": bool, # Y axis test
    "Z": bool, # Z axis test
    "F": bool, # Fan test
    "H": bool  # Heater test
})

# M73: Set/Get build percentage
validator.register_rule("M73", {
    "P": num, # Percent finished
    "R": num, # Time remaining
    "T": num, # Time to pause
    "Q": num, # Percent in silent mode
    "S": num, # Time remaining in silent mode (minutes)
    "C": num, # Time to change/pause/user interaction in normal mode (minutes)
    "D": num  # Time to change/pause/user interaction in silent mode (minutes)
})

# M74: Set weight on print bed
validator.register_rule("M74", {
    "W": num # Set the total mass in grams of everything that is currently sitting on the bed.
})

# M75: Start print timer
validator.register_rule("M75", {})

# M76: Pause print timer
validator.register_rule("M76", {})

# M77: Stop print job timer
validator.register_rule("M77", {})

# M80: ATX Power On
validator.register_rule("M80", {
    "S": bool # Report the current state and exit
})

# M81: ATX Power Off
validator.register_rule("M81", {})

# M82: Set Extruder to Absolute Mode
validator.register_rule("M82", {})

# M83: Set Extruder to Relative Mode
validator.register_rule("M83", {})

# M84: Stop Idle Hold
validator.register_rule("M84", {
    "S": bool # Stop idle hold
})

# M92: Set axis_steps_per_unit
validator.register_rule("M92", {
    "X": num, # Steps per unit for X axis
    "Y": num, # Steps per unit for Y axis
    "Z": num, # Steps per unit for Z axis
    "E": num  # Steps per unit for extruder
})

# M104: Set Extruder Temperature
validator.register_rule("M104", {
    "T": num, # Tool number
    "S": num  # Target temperature
}, custom_rule=require_fields("S"))

# M106: Turn Fan On
validator.register_rule("M106", {
    "S": num, # Fan speed (0-255)
    "P": num  # Fan number
})

# M107: Turn Fan Off
validator.register_rule("M107", {})

# M109: Set Extruder Temperature and Wait
validator.register_rule("M109", {
    "S": num, # Set extruder temperature
    "R": num, # Set extruder temperature (Parameters S and R are treated identically.) # TODO we could normalise this
    "T": num, # Tool number (RepRapFirmware and Klipper), optional
    "B": num, # Set max. extruder temperature, while S is min. temperature. Not active in default, only if AUTOTEMP is defined in source code.
})

# M114: Get Current Position
validator.register_rule("M114", {})

# M115: Get Firmware Version and Capabilities
validator.register_rule("M115", {
    "V": bool, # Report current installed firmware version
    "U": num # Firmware version provided by G-code to be compared to current one. # TODO this is actually a string
}, custom_rule=require_at_least_one)

# M140: Set Bed Temperature (Fast)
validator.register_rule("M140", {
    "S": num, # Target temperature
    "R": num, # Standby temperature
    "T": num, # Tool number
}, custom_rule=require_fields("S"))

# M142: Set Cooler Temperature (Fast)
validator.register_rule("M142", {
    "S": num,  # Target temperature
    "T": int,  # Tool number
    "R": num   # Standby temperature
})

# M155: Automatically send temperatures
validator.register_rule("M155", {})

# M190: Wait for bed temperature to reach target temp
validator.register_rule("M190", {
    "S": num, # Set bed temperature and wait
    "R": num  # Set bed temperature and wait (Parameters S and R are treated identically.)  # TODO we could normalise this
})

# M200: Set filament diameter
validator.register_rule("M200", {})

# M201: Set Maximum Acceleration
validator.register_rule("M201", {
    "X": num, # Acceleration for X axis in units/s^2
    "Y": num, # Acceleration for Y axis in units/s^2
    "Z": num, # Acceleration for Z axis in units/s^2
    "E": num  # Acceleration for the active extruder in units/s^2
})

# M203: Set Maximum Feedrate
validator.register_rule("M203", {
    "X": num, # Maximum feedrate for X axis in mm/min
    "Y": num, # Maximum feedrate for Y axis in mm/min
    "Z": num, # Maximum feedrate for Z axis in mm/min
    "E": num  # Maximum feedrate for extruder drives in mm/min
})

# M204: Set Default Acceleration
validator.register_rule("M204", {
    "S": num, # Print and travel acceleration (mm/s^2)
    "P": num, # Print acceleration (mm/s^2)
    "T": num, # Travel acceleration (mm/s^2)
    "R": num  # Retract acceleration (mm/s^2)
})

# M205: Advanced Settings
validator.register_rule("M205", {
    "S": num, # Minimum feedrate for print moves (unit/s)
    "T": num, # Minimum feedrate for travel moves (units/s)
    "B": num, # Minimum segment time (us)
    "X": num, # Maximum X jerk (units/s)
    "Y": num, # Maximum Y jerk (units/s)
    "Z": num, # Maximum Z jerk (units/s)
    "E": num  # Maximum E jerk (units/s)
})

# M206: Offset axes
validator.register_rule("M206", {})

# M211: Enable, Disable, and/or Report software endstops
validator.register_rule("M211", {})

# M217: Toolchange Parameters
validator.register_rule("M217", {
    "S": num, # Swap length (mm)
    "E": num, # Purge length (mm)
    "P": num, # Prime speed (mm/min)
    "R": num, # Retract speed (mm/min)
    "X": num, # Park X position (mm)
    "Y": num, # Park Y position (mm)
    "Z": num  # Z Raise (mm)
})

# M220: Set speed factor override percentage
validator.register_rule("M220", {
    "S": num # Feedrate Percentage
}, custom_rule=validate_percentage("S"))

# M221: Set extrusion percentage
validator.register_rule("M221", {
    "T": num, # Tool number
    "S": num  # Extrusion rate Percentage
}, custom_rule=validate_percentage("S"))

# M301: Set PID parameters
validator.register_rule("M301", {
    "P": num, # Proportional
    "I": num, # Integral
    "D": num, # Derivative
    "C": num, # Cycle time
    "L": num, # Min power
    "O": num, # Bias
    "F": num, # PWM frequency
    "T": num  # Tool number
})

# M302: Allow cold extrudes
validator.register_rule("M302", {
    "S": num, # Minimum extrude temperature
    "P": int  # Enable (1) or disable (0) cold extrusion
}, custom_rule=validate_binary("P"))

# M402: Deploy Probe
validator.register_rule("M402", {})

# M403: Set Filament Type
validator.register_rule("M403", {
    "E": num, # Extruder number
    "F": num, # Filament type
    "S": num  # Filament diameter in mm
})

# M486: Set Object Name
validator.register_rule("M486", {
    "T": num,  # Total number of objects
    "S": num,  # Object index (0-based, negative for non-objects like purge towers)
    "A": str,  # Object name (RepRapFirmware)
    "P": num,  # Cancel object with index
    "U": num,  # Un-cancel object with index
    "C": bool  # Cancel current object
})

# M552: Set IP Address
validator.register_rule("M552", {
    "P": str, # IP address
    "S": bool # Enable/disable network
})

# M555: Set Bounding Box
validator.register_rule("M555", {
    "X": num, # Minimum X coordinate
    "Y": num, # Minimum Y coordinate of model
    "W": num, # X size of model (max - min X coordinate)
    "H": num  # Y size of model (max - min Y coordinate)
})

# M569: Enable StealthChop
validator.register_rule("M569", {
    "S": int,  # Enable or disable StealthChop (1 or 0)
    "X": bool, # Target X axis
    "Y": bool, # Target Y axis
    "Z": bool, # Target Z axis
    "E": bool  # Target extruder
}, custom_rule=lambda command: "S" not in command.fields or command.fields["S"] in [0, 1])

# M572: Set or report extruder pressure advance
validator.register_rule("M572", {
    "D": int,  # Extruder number
    "S": num,  # Pressure advance value (0.0 to 1.0 seconds, 0 disables)
    "W": num   # Time range for velocity calculation (0.0 to 0.2 seconds, default 0.04)
})

# M701: Load Filament
validator.register_rule("M701", {
    "T": num, # Tool number
    "Z": num, # Z lift height
    "L": num  # Load length
})

# M702: Unload Filament
validator.register_rule("M702", {
    "T": num, # Tool number
    "Z": num, # Z lift height
    "U": num  # Unload length
})

# M862.1: Check nozzle diameter
validator.register_rule("M862.1", {
    "P": num, # Nozzle diameter in mm (typically 0.25, 0.40 or 0.60)
    "Q": bool, # Current nozzle diameter
    "T": num,  # Tool number
    "A": int, # Abrasive resistent / hardened nozzle
    "F": int, # High-Flow nozzle
}, custom_rule=[
    mutually_exclusive("P", "Q"),
    validate_binary("A", "F")
])

# M862.3: Check Model ID
validator.register_rule("M862.3", {
    "P": num, # Model ID
    "T": num  # Tool number
})

# M862.4: Check Firmware Version
validator.register_rule("M862.4", {
    "P": num, # Firmware version
    "T": num  # Tool number
})

# M862.5: Check G-code level
validator.register_rule("M862.5", {
    "P": int, # Gcode level
    "Q": num  # Current Gcode level
})

# M862.6: Check Firmware Version
validator.register_rule("M862.6", {
    "P": str, # Firmware version
    "T": num  # Tool number
})

# M900: Linear Advance
validator.register_rule("M900", {
    "K": num, # Linear advance factor
    "T": num  # Tool number
})

# M907: Set Motor Current
validator.register_rule("M907", {
    "X": num, # X motor current in mA
    "Y": num, # Y motor current in mA
    "Z": num, # Z motor current in mA
    "E": num, # E motor current in mA
    "I": num, # I motor current in mA
    "J": num, # J motor current in mA
    "K": num, # K motor current in mA
    "U": num, # U motor current in mA
    "V": num, # V motor current in mA
    "W": num, # W motor current in mA
    "A": num, # All motor current in mA
    "B": num, # Second extruder current in mA
    "C": num, # Third extruder current in mA
    "D": num  # Fourth extruder current in mA
})

# T0, T1, T2, T3, T4: Select Tool
for t in range(5):
    # T{t}: Select Tool {t}}
    validator.register_rule(f"T{t}", {
        "F": num,  # Feedrate (mm/min)
        "S": int,  # Don't move the tool in XY after change (0 or 1)
        "M": int,  # Use tool mapping (default is yes) (0 or 1)
        "L": int,  # Z Lift settings: 0=no lift, 1=lift by max MBL diff, 2=full lift(default)
        "D": int   # Return in Z after lift: 0=do not return, 1=normal return
    }, custom_rule=validate_tool_change_params)

# P0, P1, P2, P3, P4: Tool park
for t in range(5):
    # P{t}: Tool park {t}}
    validator.register_rule(f"P{t}", {
        "F": num,  # Feedrate (mm/min)
        "S": int,  # Don't move the tool in XY after change (0 or 1)
        "M": int,  # Use tool mapping (default is yes) (0 or 1)
        "L": int,  # Z Lift settings: 0=no lift, 1=lift by max MBL diff, 2=full lift(default)
        "D": int   # Return in Z after lift: 0=do not return, 1=normal return
    }, custom_rule=validate_tool_change_params)
