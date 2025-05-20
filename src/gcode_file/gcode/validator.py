from gcode_file.gcode.command import GcodeCommand


class GCodeValidator:
    class _GCodeRule:
        """
        Represents a validation rule for a G-code command.

        Attributes:
            fields (dict): A dictionary of fields and their expected types.
                          Example: {"Z": float, "E": float, "F": int}
            custom_rules (list): A list of custom validation functions for additional rules specific
                               to the command. Each function should accept a `GcodeCommand`
                               object and raise a `ValueError` if validation fails.
        """

        def __init__(self, fields: dict, custom_rules=None):
            self.fields = fields
            self.custom_rules = custom_rules or []

    def __init__(self):
        self.rules = {}

    def register_rule(self, command: str, fields: dict, custom_rule=None):
        """
        Registers a validation rule for a G-code command.

        Args:
            command (str): The G-code command (e.g., G0, G1).
            fields (dict): Dictionary of fields and their types.
            custom_rule (callable or list[callable], optional): Custom validation function(s).
        """
        if command in self.rules:
            raise ValueError(f"Rule for command '{command}' already exists")

        if not isinstance(command, str):
            raise TypeError(f"Command {command} must be a string")
        if not isinstance(fields, dict):
            raise TypeError(f"Fields {fields} must be a dictionary")

        # Convert single rule to list if needed
        custom_rules = []
        if custom_rule is not None:
            if callable(custom_rule):
                custom_rules = [custom_rule]
            elif isinstance(custom_rule, list):
                for rule in custom_rule:
                    if not callable(rule):
                        raise TypeError(f"Custom rule {rule} must be a callable")
                custom_rules = custom_rule
            else:
                raise TypeError(
                    f"Custom rule {custom_rule} must be a callable or list of callables"
                )

        self.rules[command] = self._GCodeRule(fields, custom_rules)

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

        # Check fields and their types
        for field, value in command.fields.items():
            if field in rule.fields:
                expected_type = rule.fields[field]
                if not self._is_valid_type(value, expected_type):
                    raise ValueError(
                        f"{command.command} field {field} must be of type {self._type_name(expected_type)} found {value}"
                    )

            elif field not in rule.fields:
                raise ValueError(f"{command.command} has unsupported field: {field}")

        # Apply custom rules if provided
        for custom_rule in rule.custom_rules:
            custom_rule(command)

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


class NoValidator:
    def validate(self, command: GcodeCommand):
        """
        A validator that allows all commands without any validation.

        Args:
            command: The G-code command to validate.
        """
        pass


no_validator = NoValidator()
