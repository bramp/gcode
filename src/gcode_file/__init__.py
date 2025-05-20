"""
G-Code and Binary G-Code parser library.

This library provides tools for parsing and validating both standard G-Code files
and Binary G-Code (BGCode) files used by modern 3D printers. It supports:

- Basic G-Code parsing and command extraction
- G-Code validation with configurable rules
- Binary G-Code (BGCode) parsing with support for:
  - Multiple compression types (None, Deflate, Heatshrink)
  - Various G-code encodings (MeatPack)
  - Metadata blocks (file, printer, print, slicer)
  - Thumbnail extraction
"""

# Basic G-Code Parser Components
from .gcode.basic_parser import BasicGCodeParser  # Low-level G-Code parsing
from .gcode.parser import GCodeParser  # High-level G-Code parsing
from .gcode.command import (
    GcodeCommand,
    ThumbnailCommand,
)  # G-Code command representation

# G-Code Validation Components
from .gcode.validator import GCodeValidator  # G-Code validation engine

# Binary G-Code (BGCode) Components
from .bgcode.parser import (
    # Core parser
    BasicBGCodeParser,
    # Enums
    BlockType,  # Types of blocks in BGCode files
    CompressionType,  # Supported compression methods
    ChecksumType,  # Supported checksum methods
    EncodingType,  # Metadata encoding types
    ThumbnailFormat,  # Supported thumbnail formats
    GCodeEncoding,  # G-Code encoding methods
    # Headers and Parameters
    FileHeader,  # BGCode file header
    BlockHeader,  # Block header information
    GCodeParameter,  # G-Code block parameters
    ThumbnailParameter,  # Thumbnail block parameters
    # Block Types
    Block,  # Base block class
    MetadataBlock,  # Base metadata block
    FileMetadataBlock,  # File metadata
    GCodeBlock,  # G-Code content
    PrinterMetadataBlock,  # Printer settings
    PrintMetadataBlock,  # Print settings
    SlicerMetadataBlock,  # Slicer settings
    ThumbnailBlock,  # Thumbnail image
)

__version__ = "0.1.0"

__all__ = [
    # Basic G-Code Parser
    "BasicGCodeParser",  # Low-level G-Code parsing
    "GCodeParser",  # High-level G-Code parsing
    "GcodeCommand",  # G-Code command representation
    "ThumbnailCommand",  # Thumbnail command representation
    # Validator
    "GCodeValidator",  # G-Code validation engine
    "GCodeValidatorRules",  # Validation rule definitions
    # Binary G-Code Parser
    "BasicBGCodeParser",  # Core BGCode parser
    "BlockType",  # Types of blocks in BGCode files
    "CompressionType",  # Supported compression methods
    "ChecksumType",  # Supported checksum methods
    "EncodingType",  # Metadata encoding types
    "ThumbnailFormat",  # Supported thumbnail formats
    "GCodeEncoding",  # G-Code encoding methods
    "FileHeader",  # BGCode file header
    "BlockHeader",  # Block header information
    "Block",  # Base block class
    "MetadataBlock",  # Base metadata block
    "FileMetadataBlock",  # File metadata
    "GCodeParameter",  # G-Code block parameters
    "GCodeBlock",  # G-Code content
    "PrinterMetadataBlock",  # Printer settings
    "PrintMetadataBlock",  # Print settings
    "SlicerMetadataBlock",  # Slicer settings
    "ThumbnailParameter",  # Thumbnail block parameters
    "ThumbnailBlock",  # Thumbnail image
]
