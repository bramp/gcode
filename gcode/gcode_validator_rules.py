# Registering G-code commands
# See https://reprap.org/wiki/G-code
# See https://help.prusa3d.com/article/buddy-firmware-specific-g-code-commands_633112

from gcode.gcode_validator import GCodeValidator, arc_move_rule, require_at_least_one

# The G-code validator instance prefers the Prusa Buddy firmware rules.
validator = GCodeValidator()
default_validator = validator

# A number type that is either float or int.
num = (float, int) # TODO maybe change this to a union int | float.

# List of all rules, keep the list sorted by command for easier maintenance.

# G0/G1: Move
validator.register_rule("G0", {}, {
    "X": num, # X coordinate (mm)
    "Y": num, # Y coordinate (mm)
    "Z": num, # Z coordinate (mm)
    "E": num, # Extruder position (mm)
    "F": num, # Feedrate (mm/min)
    "S": bool # Flag parameter
}, custom_rule=require_at_least_one)

validator.register_rule("G1", {}, {
    "X": num, # X coordinate (mm)
    "Y": num, # Y coordinate (mm)
    "Z": num, # Z coordinate (mm)
    "E": num, # Extruder position (mm)
    "F": num, # Feedrate (mm/min)
    "S": bool # Flag parameter
}, custom_rule=require_at_least_one)

# G2: Controlled Arc Move (Clockwise)
validator.register_rule("G2", {}, {
    "Z": num, # Z coordinate (mm)
    "E": num, # Extruder position (mm)
    "F": num, # Feedrate (mm/min)
    "R": num, # Radius (mm)
    "K": num  # K parameter
}, custom_rule=arc_move_rule)

# G3: Controlled Arc Move (Counter-Clockwise)
validator.register_rule("G3", {}, {
    "Z": num, # Z coordinate (mm)
    "E": num, # Extruder position (mm)
    "F": num, # Feedrate (mm/min)
    "R": num, # Radius (mm)
    "K": num  # K parameter
}, custom_rule=arc_move_rule)

# G4: Dwell
validator.register_rule("G4", {}, {
    "P": int, # Time in milliseconds
    "S": int  # Time in seconds
})

# G10: Retract
validator.register_rule("G10", {}, {
    "S": int # Tool number
})

# G11: Unretract
validator.register_rule("G11", {}, {
    "S": int # Tool number
})

# G28: Move to Origin (Home)
validator.register_rule("G28", {}, {
    "X": bool, # Home X axis
    "Y": bool, # Home Y axis
    "Z": bool, # Home Z axis
    "I": bool, # Home I axis
    "L": bool, # Home L axis
    "N": bool, # Home N axis
    "O": bool, # Home O axis
    "P": bool, # Home P axis
    "R": float, # Home R axis
    "S": bool, # Home S axis
    "W": bool, # Home W axis
    "C": bool  # Home C axis
})

# G29: Detailed Z-Probe
validator.register_rule("G29", {}, {
    "S": int, # Start mesh bed leveling
    "P": int  # Probe points
})

# G20: Set Units to Inches
validator.register_rule("G20", {}, {})

# G21: Set Units to Millimeters
validator.register_rule("G21", {}, {})

# G22: Firmware Retract
validator.register_rule("G22", {}, {})

# G23: Firmware Recover
validator.register_rule("G23", {}, {})

# G26: Mesh Validation Pattern
validator.register_rule("G26", {
    "X": bool, # X axis
    "Y": bool, # Y axis
    "Z": bool  # Z axis
}, {
    "P": int,  # Pattern
    "S": int,  # Size
    "T": int,  # Type
    "E": float # Extruder
})

# G27: Park Toolhead
validator.register_rule("G27", {
    "X": bool, # X axis
    "Y": bool, # Y axis
    "Z": bool  # Z axis
}, {
    "P": int # Position
})

# G30: Single Z-Probe
validator.register_rule("G30", {}, {
    "X": float, # X coordinate
    "Y": float, # Y coordinate
    "Z": float, # Z coordinate
    "P": int,   # Probe number
    "S": int    # Probe type
})

# G31: Set or Report Current Probe Status
validator.register_rule("G31", {}, {
    "X": float, # X coordinate
    "Y": float, # Y coordinate
    "Z": float, # Z coordinate
    "P": int    # Probe number
})

# G32: Probe Z and Calibrate Bed
validator.register_rule("G32", {}, {
    "S": int # Start calibration
})

# G33: Delta Auto Calibration
validator.register_rule("G33", {}, {
    "P": int, # Pattern
    "S": int  # Size
})

# G34: Set Delta Height
validator.register_rule("G34", {}, {
    "P": int, # Position
    "S": int  # Size
})

# G35: Tramming Assistant
validator.register_rule("G35", {}, {
    "P": bool, # Pattern
    "S": bool  # Size
})

# G36: Mesh Bed Leveling
validator.register_rule("G36", {}, {
    "P": bool, # Pattern
    "S": bool  # Size
})

# G37: Probe Z and Save Mesh
validator.register_rule("G37", {}, {
    "P": bool, # Pattern
    "S": bool  # Size
})

# G38: Probe Target
validator.register_rule("G38", {
    "X": bool, # X axis
    "Y": bool, # Y axis
    "Z": bool  # Z axis
}, {
    "P": bool, # Pattern
    "S": bool  # Size
})

# G39: Probe Bed and Save Mesh
validator.register_rule("G39", {}, {
    "P": bool, # Pattern
    "S": bool  # Size
})

# G40: Cancel Tool Offset
validator.register_rule("G40", {}, {})

# G90: Set to Absolute Positioning
validator.register_rule("G90", {}, {})

# G92: Set Position
validator.register_rule("G92", {}, {
    "X": bool, # X position
    "Y": bool, # Y position
    "Z": bool, # Z position
    "E": bool  # Extruder position
})

# M73: Set Print Progress
validator.register_rule("M73", {}, {
    "P": num, # Percent in normal mode
    "R": num, # Time remaining in normal mode (minutes)
    "T": num, # Time to pause
    "Q": num, # Percent in silent mode
    "S": num, # Time remaining in silent mode (minutes)
    "C": num, # Time to change/pause/user interaction in normal mode (minutes)
    "D": num  # Time to change/pause/user interaction in silent mode (minutes)
})

# M82: Set Extruder to Absolute Mode
validator.register_rule("M82", {}, {})

# M84: Stop Idle Hold
validator.register_rule("M84", {}, {
    "S": bool # Stop idle hold
})

# M104: Set Extruder Temperature
validator.register_rule("M104", {
    "S": bool # Target temperature
}, {
    "T": bool # Tool number
})

# M106: Turn Fan On
validator.register_rule("M106", {
    "S": bool # Fan speed
}, {
    "P": bool # Fan number
})

# M107: Turn Fan Off
validator.register_rule("M107", {}, {})

# M109: Set Extruder Temperature and Wait
validator.register_rule("M109", {
    "S": bool # Target temperature
}, {
    "T": bool # Tool number
})

# M201: Set Maximum Acceleration
validator.register_rule("M201", {}, {
    "X": num, # Acceleration for X axis in units/s^2
    "Y": num, # Acceleration for Y axis in units/s^2
    "Z": num, # Acceleration for Z axis in units/s^2
    "E": num  # Acceleration for the active extruder in units/s^2
})

# M203: Set Maximum Feedrate
validator.register_rule("M203", {}, {
    "X": num, # Maximum feedrate for X axis in mm/min
    "Y": num, # Maximum feedrate for Y axis in mm/min
    "Z": num, # Maximum feedrate for Z axis in mm/min
    "E": num  # Maximum feedrate for extruder drives in mm/min
})

# M204: Set Default Acceleration
validator.register_rule("M204", {}, {
    "P": num, # Acceleration for printing moves in units/s^2
    "T": num, # Acceleration for travel moves in units/s^2
    "R": num  # Acceleration for retract moves in units/s^2
})

# M205: Advanced Settings
validator.register_rule("M205", {}, {
    "X": num, # Maximum XY jerk
    "Z": num, # Maximum Z jerk
    "E": num, # Maximum E jerk
    "B": num, # Minimum segment time
    "S": num, # Minimum planner speed
    "T": num  # Travel minimum planner speed
})

# M569: Set Motor Direction and Enable
validator.register_rule("M569", {}, {
    "S": bool, # Enable/disable motor
    "T": bool, # Tool number
    "E": bool  # Extruder number
})

