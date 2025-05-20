import io
import itertools
import os
from typing import BinaryIO, Iterable, List, Union
from gcode_file.gcode.command import GcodeCommand
from gcode_file.gcode.parser import GCodeParser
from gcode_file.bgcode.parser import (
    BasicBGCodeParser,
    FileMetadataBlock,
    PrintMetadataBlock,
    PrinterMetadataBlock,
    SlicerMetadataBlock,
    ThumbnailBlock,
    GCodeBlock,
    is_bgcode_file,
)
from gcode_file.types import Thumbnail


class GcodeFileBase:
    @property
    def file_metadata(self) -> dict:
        """Generic metadata, such as producer (software), etc."""
        raise NotImplementedError("This method should be implemented by subclasses.")

    @property
    def printer_metadata(self) -> dict:
        """Metadata consumed by printer, such as printer model, nozzle diameter etc."""
        raise NotImplementedError("This method should be implemented by subclasses.")

    @property
    def thumbnails(self) -> List[Thumbnail]:
        """Image data for thumbnail."""
        raise NotImplementedError("This method should be implemented by subclasses.")

    @property
    def print_metadata(self) -> dict:
        """Print metadata, such as print time or material consumed, etc.."""
        raise NotImplementedError("This method should be implemented by subclasses.")

    @property
    def slicer_settings(self) -> dict:
        """Metadata produced and consumed by the software generating the G-code file."""
        raise NotImplementedError("This method should be implemented by subclasses.")

    @property
    def commands(self) -> List[str]:
        """G-code commands."""
        raise NotImplementedError("This method should be implemented by subclasses.")


class BGcodeFile(GcodeFileBase):
    def __init__(self, file: Union[BinaryIO, str]):
        """
        Initialize a BGcodeFile instance.

        Args:
            file (BinaryIO | str): file can be a path to a file (a string), a file-like object or a path-like object.

        Raises:
            TypeError: If the provided file is neither a string/path nor a file-like object.
        """

        if isinstance(file, (str, bytes, os.PathLike)):
            self.file = open(file, "rb")
            self.file_owned = True
        elif hasattr(file, "read"):
            self.file = file
            self.file_owned = False
        else:
            raise TypeError("filename must be a str or bytes object, or a file")

        # Read the entire file into memory. In future we may want to
        # implement a streaming/seeking parser.
        self.parser = BasicBGCodeParser()
        self.blocks = self.parser.parse_stream(self.file)

    def __enter__(self):
        """
        Enter the runtime context related to this object.

        Returns:
            BGcodeFile: The instance itself.
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit the runtime context related to this object.

        Closes the file if it is owned by this instance.

        Args:
            exc_type (type): The exception type.
            exc_value (Exception): The exception value.
            traceback (Traceback): The traceback object.
        """
        if self.file and self.file_owned:
            self.file.close()
            self.file = None

    @property
    def file_metadata(self) -> dict:
        """Generic metadata, such as producer (software), etc."""
        return {
            key: value
            for block in self.blocks
            if isinstance(block, FileMetadataBlock)
            for key, value in block.data.items()
        }

    @property
    def printer_metadata(self) -> dict:
        """Metadata consumed by printer, such as printer model, nozzle diameter
        etc."""

        return {
            key: value
            for block in self.blocks
            if isinstance(block, PrinterMetadataBlock)
            for key, value in block.data.items()
        }

    @property
    def print_metadata(self) -> dict:
        """Print metadata, such as print time or material consumed, etc.."""
        return {
            key: value
            for block in self.blocks
            if isinstance(block, PrintMetadataBlock)
            for key, value in block.data.items()
        }

    @property
    def slicer_settings(self) -> dict:
        """Metadata produced and consumed by the software generating the G-code file."""
        return {
            key: value
            for block in self.blocks
            if isinstance(block, SlicerMetadataBlock)
            for key, value in block.data.items()
        }

    @property
    def thumbnails(self) -> List[Thumbnail]:
        """Image data for thumbnail."""
        return [
            Thumbnail(
                format=block.parameters.format,
                width=block.parameters.width,
                height=block.parameters.height,
                data=block.image_data,
            )
            for block in self.blocks
            if isinstance(block, ThumbnailBlock)
        ]

    @property
    def commands(self) -> Iterable[GcodeCommand]:
        """G-code commands."""
        gcode_blocks = [block for block in self.blocks if isinstance(block, GCodeBlock)]
        # TODO I'm not sure why there are multiple GCodeBlocks
        # in a single file. For now, we merge them.
        return itertools.chain.from_iterable(block.commands for block in gcode_blocks)


class GcodeFile(GcodeFileBase):
    def __init__(self, file_path: str):
        self.parser = GCodeParser()

    @property
    def file_metadata(self) -> dict:
        """Generic metadata, such as producer (software), etc."""
        raise NotImplementedError("This method should be implemented by subclasses.")

    @property
    def printer_metadata(self) -> dict:
        """Metadata consumed by printer, such as printer model, nozzle diameter etc."""
        raise NotImplementedError("This method should be implemented by subclasses.")

    @property
    def thumbnails(self) -> List[Thumbnail]:
        """Image data for thumbnail."""
        raise NotImplementedError("This method should be implemented by subclasses.")

    @property
    def print_metadata(self) -> dict:
        """Print metadata, such as print time or material consumed, etc.."""
        raise NotImplementedError("This method should be implemented by subclasses.")

    @property
    def slicer_settings(self) -> dict:
        """Metadata produced and consumed by the software generating the G-code file."""
        raise NotImplementedError("This method should be implemented by subclasses.")

    @property
    def commands(self) -> List[str]:
        """G-code commands."""
        raise NotImplementedError("This method should be implemented by subclasses.")


def open_file(file_path: str) -> GcodeFileBase:
    with open(file_path, "rb") as stream:
        return open_stream(stream)


def open_stream(stream: BinaryIO) -> GcodeFileBase:
    # Wrap in a BufferedReader, so is_bgcode_file can read the first
    # few bytes, and seek back.
    stream = io.BufferedReader(stream)

    if is_bgcode_file(stream):
        return BGcodeFile(stream)
    else:
        return GcodeFile(stream)
