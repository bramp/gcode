import base64
import io
import re
from typing import Any, Dict, Generator, Optional

# TODO Refactor GcodeCommand to be a base class for GcodeCommand and GcodeComment, GcodeInvalidCommand, and other types


class GcodeCommand:
    """
    Represents a parsed G-code command.

    Attributes:
        command (str): The G-code command (e.g., G1, M104).
        fields (Dict[str, Any]): The fields associated with the command. The
        values may be one of int, float, str, or bool.
        error (str, optional): If present, contains a validation error message.
        comment (str, optional): If present, contains the comment from the line.
    """

    def __init__(
        self,
        command: str,
        fields: Dict[str, Any],
        comment: Optional[str] = None,
        error: Optional[str] = None,
    ):
        self.command = command
        self.fields = fields
        self.comment = comment
        self.error = error

    def _field_repr(self, key: str, value: Any) -> str:
        """
        Return a string representation of a field in valid G-code notation.

        Args:
            key (str): The field key (e.g., 'X', 'Y', 'Z').
            value (Any): The field value (int, float, str, or bool).

        Returns:
            str: The field as a string in valid G-code format.
        """
        if isinstance(value, bool):
            # If the flag is false, we treat it as being unset.
            return f"{key}{int(value)}" if value else ""

        if isinstance(value, (int, float)):
            return f"{key}{value}"

        if isinstance(value, str):
            raise NotImplementedError("String fields are not yet supported.")

        return ValueError(f"Unsupported field type: {type(value)} for key: {key}")

    def __repr__(self):
        """
        Return a string representation of the G-code command in valid G-code notation.

        Returns:
            str: The G-code command as a string in valid G-code format.
        """
        params_str = " ".join(
            self._field_repr(key, value) for key, value in self.fields.items()
        )
        result = f"{self.command} {params_str}".strip()
        if self.comment:
            result = f"{result} ;{self.comment}"
        return result


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
    def from_stream(
        start: GcodeCommand, stream: Generator[GcodeCommand, Any, None]
    ) -> "ThumbnailCommand":
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
                return ThumbnailCommand(
                    output_stream.getvalue(), format or "PNG", width, height, size
                )

            output_stream.write(base64.b64decode(command.comment + "=="))

        raise ValueError("Did not find thumbnail block end")


class PrusaSlicerConfigCommand:
    """A special command that represents a PrusaSlicer config block in G-code."""

    def __init__(self, config: dict):
        self.config = config

    @staticmethod
    def from_stream(
        stream: Generator[GcodeCommand, Any, None],
    ) -> "PrusaSlicerConfigCommand":
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

            key, value = PrusaSlicerConfigCommand.parse_config_line(command.comment)
            config[key] = value

        raise ValueError("Did not find end of prusaslicer_config block")

    @staticmethod
    def parse_config_line(comment: str):
        """Parse a prusaslicer_config comment into a dictionary."""
        # Split the comment into key-value pairs, e.g
        #   arc_fitting = emit_center
        #   before_layer_gcode = ;BEFORE_LAYER_CHANGE\nG92 E0.0\n;[layer_z]\n\n
        key, value = comment.split(" = ")
        return key, value
