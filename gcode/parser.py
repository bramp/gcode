import base64
import io
from typing import Any, Generator, List, Optional, TextIO
import re

from gcode.basic_parser import BasicGCodeParser
from gcode.command import GcodeCommand


class ThumbnailCommand:
    """A special command that represents a thumbnail block in G-code."""
    def __init__(self, content: bytes, format: str, width: int, height: int, size: int):
        """
        Initialize a ThumbnailCommand with the given parameters.

        Args:
            content (bytes): The raw bytes of the thumbnail image data
            format (str): The format of the thumbnail (e.g., "QOI", "PNG")
            width (int): The width of the thumbnail in pixels
            height (int): The height of the thumbnail in pixels
            size (int): The size of the base64 encodedthumbnail in bytes
        """
        self.content = content
        self.format = format
        self.width = width
        self.height = height
        self.size = size

    # TODO Improve error handling in here. If the base64 fails, or another error, it doesn't fit the erros the rest of the library returns
    @staticmethod
    def from_stream(start: GcodeCommand, stream: Generator[GcodeCommand, Any, None]) -> 'ThumbnailCommand':
        """
        Create a ThumbnailCommand by consuming a thumbnail block from the stream.

        This method reads commands from the stream until it finds a "thumbnail end" comment,
        collecting all the thumbnail content in between. It expects all commands in the
        thumbnail block to be comments.

        Args:
            start (GcodeCommand): The command that started the thumbnail block (with "thumbnail begin")
            stream (Generator[GcodeCommand, Any, None]): The stream of G-code commands to consume from

        Returns:
            ThumbnailCommand: A single command containing all the thumbnail content

        Raises:
            ValueError: If a non-comment command is encountered before finding "thumbnail end"
        """
        # Parse the start line, e.g "thumbnail_QOI begin 16x16 500" or "thumbnail begin 16x16 500"
        pattern = r"thumbnail(?:_(\w+))?\s+begin\s+(\d+)x(\d+)\s+(\d+)"
        match = re.match(pattern, start.comment)
        if not match:
            raise ValueError(f"Invalid thumbnail start format: {start.comment}")

        format = match.group(1)
        width = int(match.group(2))
        height = int(match.group(3))
        size = int(match.group(4))

        output_stream = io.BytesIO()

        end = f"thumbnail{'_' + format if format else ''} end"

        for command in stream:
            if command.command or not command.comment:
                raise ValueError("Thumbnail block not correctly ended")

            if command.comment.startswith(end):
                # TODO We can be strict/paranoid here, and check a few things
                # * Is the output_stream actually the format, width, and height we expect?
                return ThumbnailCommand(output_stream.getvalue(), format or "PNG", width, height, size)

            output_stream.write( base64.b64decode(command.comment + "==") )
        
        raise ValueError("Did not find thumbnail block end")


class PrusaSlicerConfigCommand:
    """A special command that represents a PrusaSlicer config block in G-code."""
    def __init__(self, config: dict):
        self.config = config

    @staticmethod
    def from_stream(stream: Generator[GcodeCommand, Any, None]) -> 'PrusaSlicerConfigCommand':
        """
        Create a PrusaSlicerConfigCommand by consuming a prusaslicer_config block from the stream.
        """
        config = {}

        for command in stream:
            if command.command or not command.comment:
                raise ValueError("prusaslicer_config block not correctly ended")

            if command.comment == "prusaslicer_config = end":
                # TODO We can be strict/paranoid here, and check a few things
                # * Is the output_stream actually the format, width, and height we expect?
                return PrusaSlicerConfigCommand(config)

            key, value = parse_config_line(command.comment)
            config[key] = value
        raise ValueError("Did not find end of prusaslicer_config block")

    def parse_config_line(comment: str):
        """Parse a prusaslicer_config comment into a dictionary."""
        # Split the comment into key-value pairs, e.g
        #   arc_fitting = emit_center
        #   before_layer_gcode = ;BEFORE_LAYER_CHANGE\nG92 E0.0\n;[layer_z]\n\n
        key, value = comment.split(' = ')
        return key, value


class GCodeParser(BasicGCodeParser):
    """
    A higher-level G-code parser that extends BasicGCodeParser and provides 
    additional processing to extract additional information that slicers 
    place into comments.
    """
    def __init__(self, validator=None, strict_mode: bool = True):
        super().__init__(validator=validator, strict_mode=strict_mode)

    def parse_stream(self, stream: TextIO):
        """
        Parse a stream of G-code line by line and yeld each command.

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
                if command.comment and re.match(r"thumbnail(?:_\w+)?\s+begin", command.comment):
                    yield ThumbnailCommand.from_stream(command, commands)
                elif command.comment == "; prusaslicer_config = begin":
                    yield PrusaSlicerConfigCommand.from_stream(command, commands)
                else:
                    yield command

        except StopIteration:
            pass
