from typing import Iterator, TextIO
import re

from gcode_file.gcode.basic_parser import BasicGCodeParser
from gcode_file.gcode.command import (
    GcodeCommand,
    PrusaSlicerConfigCommand,
    ThumbnailCommand,
)


class GCodeParser(BasicGCodeParser):
    """
    A higher-level G-code parser that extends BasicGCodeParser and provides
    additional processing to extract additional information that slicers
    place into comments.
    """

    def __init__(self, validator=None, strict_mode: bool = True):
        super().__init__(validator=validator, strict_mode=strict_mode)

    def parse_stream(self, stream: TextIO) -> Iterator[GcodeCommand]:
        """
        Parse a stream of G-code line by line and yield each command.

        Args:
            stream (TextIO): A text stream to parse line by line.

        Yields:
            GcodeCommand: Processed G-code commands.
        """
        commands = super().parse_stream(stream)
        try:
            while True:
                command = next(commands)
                # Match "; thumbnail_{format} begin" lines
                if command.comment and re.match(
                    r"thumbnail(?:_\w+)?\s+begin", command.comment
                ):
                    yield ThumbnailCommand.from_stream(command, commands)
                elif command.comment == "; prusaslicer_config = begin":
                    yield PrusaSlicerConfigCommand.from_stream(command, commands)
                else:
                    yield command

        except StopIteration:
            pass
