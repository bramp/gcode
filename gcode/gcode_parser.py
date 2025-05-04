import re
from typing import List, Optional, TextIO

from gcode.gcode_command import GcodeCommand
from gcode.gcode_validator_rules import default_validator

class GCodeParser:
    def __init__(self, validator=None):
        """
        Initialize the GCodeParser with a validator. If no validator is provided, use the default_validator.

        Args:
            validator (callable, optional): A validator function to validate G-code commands. Defaults to default_validator.
        """
        self.validator = validator or default_validator

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
        if not line or line.startswith(';'):  # Ignore empty lines and comments
            return None

        # Match the command (e.g., G1, M104, M569.2)
        match = re.match(r'([A-Za-z])(\d+(?:\.\d+)?)', line)
        if not match:
            raise ValueError(f"Invalid G-code command: {line}")

        command_type, command_number = match.groups()
        command_type = command_type.upper()

        # Extract fields starting after the command
        fields = {}
        for field, value in re.findall(r'(?<![A-Za-z])([A-Z])([-+]?[0-9]*\.?[0-9]+)', line[len(match.group(0)):]):
            if field in fields:
                raise ValueError(f"Duplicate field '{field}'")
            if value == '':
                # If the field is present but has no value, treat it as a flag
                fields[field] = True
            # TODO Check if value is string
            elif '.' in value:
                fields[field] = float(value)
            else:
                fields[field] = int(value)

        command = GcodeCommand(command=f"{command_type}{command_number}", fields=fields)
        try:
            self.validator.validate(command)
        # Catch all error, and re-raise it with the command for better debugging
        except Exception as e:
            raise ValueError(f"'{command}': {e}") from e

        return command

    def parse_stream(self, stream: TextIO, to_list: bool = False):
        """
        Parse a stream of G-code line by line.

        Args:
            stream (TextIO): A text stream (e.g., file-like object or StringIO) to parse.

        Yields:
            GcodeCommand: Parsed G-code command objects one at a time if to_list is False.

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

    def parse_stream_to_list(self, stream: TextIO) -> List[GcodeCommand]:
        """
        Parse a stream of G-code and return a list of GcodeCommand objects.

        Args:
            stream (TextIO): A text stream (e.g., file-like object or StringIO) to parse.

        Returns:
            List[GcodeCommand]: A list of parsed G-code command objects.

        Raises:
            ValueError: If a line contains an invalid command or unknown fields.
        """
        return list(self.parse_stream(stream))

    def parse_file(self, file_path: str):
        """
        Parse a G-code file line by line in a streaming manner.

        Args:
            file_path (str): The path to the G-code file to parse.

        Yields:
            GcodeCommand: Parsed G-code command objects one at a time.

        Raises:
            ValueError: If a line contains an invalid command or unknown fields.
        """
        with open(file_path, 'r') as file:
            yield from self.parse_stream(file)

    def parse_file_to_list(self, file_path: str) -> List[GcodeCommand]:
        """
        Parse a G-code file and return a list of GcodeCommand objects.

        Args:
            file_path (str): The path to the G-code file to parse.

        Returns:
            List[GcodeCommand]: A list of parsed G-code command objects.

        Raises:
            ValueError: If a line contains an invalid command or unknown fields.
        """
        return list(self.parse_file(file_path))

