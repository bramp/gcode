from gcode.gcode_command import GcodeCommand

class GCodeValidator:
    class _GCodeRule:
        """
        Represents a validation rule for a G-code command.

        Attributes:
            required (dict): A dictionary of required fields and their expected types.
                            Example: {"X": float, "Y": (float, int)}
            optional (dict): A dictionary of optional fields and their expected types.
                            Example: {"Z": float, "E": float, "F": int}
            custom_rule (callable): A custom validation function for additional rules specific
                                   to the command. The function should accept a `GcodeCommand`
                                   object and raise a `ValueError` if validation fails.
        """
        def __init__(self, required: dict, optional: dict, custom_rule=None):
            self.required = required
            self.optional = optional
            self.custom_rule = custom_rule

    def __init__(self):
        self.rules = {}

    def register_rule(self, command: str, required: dict, optional: dict, custom_rule=None):
        """
        Registers a validation rule for a G-code command.

        Args:
            command (str): The G-code command (e.g., G0, G1).
            required (dict): Dictionary of required fields and their types.
            optional (dict): Dictionary of optional fields and their types.
            custom_rule (callable, optional): Custom validation function.
        """
        if command in self.rules:
            raise ValueError(f"Rule for command '{command}' already exists")

        if not isinstance(command, str):
            raise TypeError(f"Command {command} must be a string")
        if not isinstance(required, dict):
            raise TypeError(f"Required fields {required} must be a dictionary")
        if not isinstance(optional, dict):
            raise TypeError(f"Optional fields {optional} must be a dictionary")
        if custom_rule is not None and not callable(custom_rule):
            raise TypeError(f"Custom rule {custom_rule} must be a callable")

        # Ensure that required and optional fields don't overlap
        for field in required:
            if field in optional:
                raise ValueError(f"Field '{field}' cannot be both required and optional")

        self.rules[command] = self._GCodeRule(required, optional, custom_rule)

    def validate(self, command: GcodeCommand):
        """
        Validates a G-code command against its registered rule.

        Args:
            command (GcodeCommand): The G-code command to validate.

        Raises:
            ValueError: If validation fails.
        """
        rule = self.rules.get(command.command)
        if not rule:
            raise ValueError(f"{command.command} is an unsupported command")

        # Check required fields and their types
        for field, expected_type in rule.required.items():
            if field not in command.fields:
                raise ValueError(f"{command.command} is missing required field: {field}")

            value = command.fields[field]
            if not self._is_valid_type(value, expected_type):
                raise ValueError(f"{command.command} field {field} must be of type {self._type_name(expected_type)} found {value}")

        # Check optional fields and their types
        for field, value in command.fields.items():
            if field in rule.optional:
                expected_type = rule.optional[field]
                if not self._is_valid_type(value, expected_type):
                    raise ValueError(f"{command.command} field {field} must be of type {self._type_name(expected_type)} found {value}")

            elif field not in rule.required:
                raise ValueError(f"{command.command} has unsupported field: {field}")

        # Apply custom rule if provided
        if rule.custom_rule:
            rule.custom_rule(command)

    def _is_valid_type(self, value, expected_type):
        """
        Checks if a value matches the expected type.

        Args:
            value: The value to check.
            expected_type: The expected type or a tuple of expected types.

        Returns:
            bool: True if the value matches the expected type, False otherwise.
        """
        return isinstance(value, expected_type)

    def _type_name(self, expected_type):
        """
        Returns a human-readable name for the expected type.

        Args:
            expected_type: The expected type or a tuple of types.

        Returns:
            str: A human-readable name for the type.
        """
        if isinstance(expected_type, tuple):
            return " or ".join(t.__name__ for t in expected_type)
        return expected_type.__name__

            
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

          
class NoValidator:
    def validate(self, command: GcodeCommand):
        """
        A validator that allows all commands without any validation.

        Args:
            command: The G-code command to validate.
        """
        pass

no_validator = NoValidator()