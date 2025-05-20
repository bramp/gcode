import re
from typing import Iterator, Optional, TextIO

from gcode_file.gcode.command import GcodeCommand
from gcode_file.gcode.validator_rules import default_validator


class BasicGCodeParser:
    def __init__(self, validator=None, strict_mode: bool = True):
        """
        Initialize the BasicGCodeParser with a validator. If no validator is provided, use the default_validator.

        Args:
            validator (callable, optional): A validator function to validate G-code commands. Defaults to default_validator.
            strict_mode (bool, optional): If True, validation errors will raise ValueError. If False, validation errors
                                        will be stored in the command's error field. Defaults to True.
        """
        self.validator = validator or default_validator
        self.strict_mode = strict_mode

    def parse_line(self, line: str) -> Optional[GcodeCommand]:
        """
        Parse a single line of G-code and optionally validate it.

        Args:
            line (str): A single line of G-code to parse.
            validate (bool): Whether to validate the parsed command.

        Returns:
            Optional[GcodeCommand]: An instance of GcodeCommand containing the parsed command and fields,
                                     or None if the line is empty or a comment.

        Raises:
            ValueError: If the line contains an invalid command or unknown fields.
        """
        line = line.strip()
        if not line:
            return None

        # Split the line into command and comment parts
        # TODO There is a bug here, due to Strings may contain ;
        parts = line.split(';', 1)
        command_part = parts[0].strip()
        comment = parts[1].strip() if len(parts) > 1 else None

        if not command_part:
            return GcodeCommand(command="", fields={}, comment=comment)

        # Match the command (e.g., G1, M104, M569.2)
        match = re.match(r'([A-Za-z])(\d+(?:\.\d+)?)', command_part)
        if not match:
            raise ValueError(f"Invalid G-code command: {command_part}")

        command_type, command_number = match.groups()
        command_type = command_type.upper()

        fields_part = command_part[len(match.group(0)):]

        # Extract fields starting after the command
        fields = {}
        for field, value in re.findall(r'(?<![A-Za-z])([A-Z])([-+]?[0-9]*\.?[0-9]+|"[^"]*")', fields_part):
            if field in fields:
                raise ValueError(f"Duplicate field '{field}'")
            if value == '':
                # If the field is present but has no value, treat it as a flag
                fields[field] = True
            elif value.startswith('"') and value.endswith('"'):
                # Handle string values
                fields[field] = value[1:-1]  # Remove quotes
            elif '.' in value:
                fields[field] = float(value)
            else:
                fields[field] = int(value)

        command = GcodeCommand(command=f"{command_type}{command_number}",
                               fields=fields, comment=comment)
        try:
            self.validator.validate(command)
        # Catch all error, and re-raise it with the command for better debugging
        except Exception as e:
            if self.strict_mode:
                raise ValueError(f"'{command}': {e}") from e
            command.error = str(e)

        return command

    def parse_stream(self, stream: TextIO) -> Iterator[GcodeCommand]:
        """
        Parse a stream of G-code line by line.

        Args:
            stream (TextIO): A text stream (e.g., file-like object or StringIO) to parse.

        Yields:
            GcodeCommand: Parsed G-code command objects one at a time.

        Raises:
            ValueError: If a line contains an invalid command or unknown fields.
        """
        for line_number, line in enumerate(stream, start=1):
            try:
                command = self.parse_line(line)
                if command:
                    yield command
            except Exception as e:
                raise ValueError(f"Error on line {line_number}: {e}") from e
