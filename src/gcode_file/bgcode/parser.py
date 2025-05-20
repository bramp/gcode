import io
import struct
from typing import List, BinaryIO, Iterator, Dict, Optional
from dataclasses import dataclass
from enum import IntEnum
import zlib
from abc import ABC
from gcode_file.bgcode.meatpack import decompress
from gcode_file.gcode.basic_parser import BasicGCodeParser
import heatshrink2
from gcode_file.gcode.command import GcodeCommand


class BlockType(IntEnum):
    FILE_METADATA = 0
    GCODE = 1
    SLICER_METADATA = 2
    PRINTER_METADATA = 3
    PRINT_METADATA = 4
    THUMBNAIL = 5

    def __str__(self) -> str:
        return f"{self.__class__.__name__}.{self.name}"


class CompressionType(IntEnum):
    NONE = 0
    DEFLATE = 1
    HEATSHRINK_11_4 = 2
    HEATSHRINK_12_4 = 3

    def __str__(self) -> str:
        return f"{self.__class__.__name__}.{self.name}"


class ChecksumType(IntEnum):
    NONE = 0
    CRC32 = 1

    def __str__(self) -> str:
        return f"{self.__class__.__name__}.{self.name}"


class EncodingType(IntEnum):
    INI = 0

    def __str__(self) -> str:
        return f"{self.__class__.__name__}.{self.name}"


class ThumbnailFormat(IntEnum):
    PNG = 0
    JPG = 1
    QOI = 2

    def __str__(self) -> str:
        return f"{self.__class__.__name__}.{self.name}"


class GCodeEncoding(IntEnum):
    NONE = 0
    MEATPACK = 1
    MEATPACK_COMMENTS = 2

    def __str__(self) -> str:
        return f"{self.__class__.__name__}.{self.name}"


@dataclass
class FileHeader:
    magic: bytes  # Should be b"GCDE"
    version: int
    checksum_type: ChecksumType

    def __str__(self) -> str:
        return (
            "FileHeader("
            f"magic={self.magic}, version={self.version}, "
            f"checksum_type={self.checksum_type}"
            ")"
        )


@dataclass
class BlockHeader:
    parent: FileHeader
    type: BlockType
    compression: CompressionType
    uncompressed_size: int
    compressed_size: int

    def __str__(self) -> str:
        return (
            "BlockHeader("
            f"type={self.type}, "
            f"compression={self.compression}, "
            f"uncompressed_size={self.uncompressed_size}, "
            f"compressed_size={self.compressed_size}"
            ")"
        )

    @property
    def is_metadata(self) -> bool:
        """Returns True if the block is a metadata block."""
        return self.type in (
            BlockType.FILE_METADATA,
            BlockType.PRINTER_METADATA,
            BlockType.PRINT_METADATA,
            BlockType.SLICER_METADATA,
        )


class Block(ABC):
    """Base class for all block types."""

    def __init__(self, header: BlockHeader):
        self.header = header

    @property
    def type(self) -> BlockType:
        return self.header.type

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(type={self.type})"


@dataclass
class GCodeParameter:
    encoding: GCodeEncoding

    def __str__(self) -> str:
        return f"GCodeParameter(encoding={self.encoding})"


class GCodeBlock(Block):
    """Represents a G-code block."""

    def __init__(
        self, header: BlockHeader, parameters: GCodeParameter, raw_data: bytes
    ):
        super().__init__(header)
        self.parameters = parameters
        self.raw_data = raw_data

    def data(self) -> str:
        """Returns the G-code data as a string, decompressing if necessary."""

        if self.parameters.encoding == GCodeEncoding.NONE:
            return self.raw_data.decode("utf-8")

        if (
            self.parameters.encoding == GCodeEncoding.MEATPACK
            or self.parameters.encoding == GCodeEncoding.MEATPACK_COMMENTS
        ):
            return decompress(self.raw_data).decode("utf-8")

        raise ValueError(f"Unsupported encoding {self.parameters.encoding}")

    def commands(self) -> List[GcodeCommand]:
        """
        Parse the G-code data and return a list of GcodeCommand objects.

        Returns:
            List[GcodeCommand]: A list of parsed GcodeCommand objects.
        """
        return BasicGCodeParser().parse_stream(self.data())

    def __str__(self) -> str:
        if self.parameters.encoding == GCodeEncoding.NONE:
            # Show first few lines of G-code
            lines = self.raw_data.decode("utf-8", errors="replace").splitlines()[:3]
            preview = "\n".join(lines)
            if len(lines) == 3:
                preview += "\n..."
            return (
                f"{self.__class__.__name__}("
                f"size={len(self.raw_data)} bytes, "
                f"encoding={self.parameters.encoding}, "
                f"preview=\n{preview})"
            )

        return (
            f"{self.__class__.__name__}("
            f"size={len(self.raw_data)} bytes, "
            f"encoding={self.parameters.encoding})"
        )


@dataclass
class MetadataBlock(Block):
    """Base class for all metadata blocks."""

    header: BlockHeader
    encoding: EncodingType
    data: Dict[str, str]

    def __str__(self) -> str:
        items = [f"{k}={v}" for k, v in self.data.items()]
        return f"{self.__class__.__name__}({', '.join(items)})"


@dataclass
class FileMetadataBlock(MetadataBlock):
    """Represents a file metadata block."""

    pass


@dataclass
class PrinterMetadataBlock(MetadataBlock):
    """Represents a printer metadata block."""

    pass


@dataclass
class PrintMetadataBlock(MetadataBlock):
    """Represents a print metadata block."""

    pass


@dataclass
class SlicerMetadataBlock(MetadataBlock):
    """Represents a slicer metadata block."""

    pass


@dataclass
class ThumbnailParameter:
    format: ThumbnailFormat
    width: int
    height: int

    def __str__(self) -> str:
        return (
            "Thumbnail("
            f"format={self.format}, "
            f"width={self.width}, height={self.height})"
            ")"
        )


@dataclass
class ThumbnailBlock(Block):
    """Represents a thumbnail block."""

    header: BlockHeader
    parameters: ThumbnailParameter
    data: bytes

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"{self.parameters}, "
            f"size={len(self.data)} bytes"
            ")"
        )


class BasicBGCodeParser:
    def __init__(self):
        """
        Initialize the BasicBGCodeParser.
        """
        pass

    def _parse_metadata_parameters(
        self, file: BinaryIO, header: BlockHeader
    ) -> EncodingType:
        """
        Parse metadata block parameters from a binary file.

        Args:
            file (BinaryIO): A binary file stream to parse.
            header (BlockHeader): The block's header.

        Returns:
            EncodingType: The encoding type used for the metadata.

        Raises:
            ValueError: If the block parameters are invalid.
        """
        assert header.is_metadata

        encoding = EncodingType(struct.unpack("<H", file.read(2))[0])
        if encoding != EncodingType.INI:
            raise ValueError(f"Unsupported encoding type: {encoding}")

        return encoding

    def _parse_thumbnail_parameters(
        self, file: BinaryIO, header: BlockHeader
    ) -> ThumbnailParameter:
        """
        Parse thumbnail block parameters from a binary file.

        Args:
            file (BinaryIO): A binary file stream to parse.
            header (BlockHeader): The block's header.

        Returns:
            ThumbnailParameter: The thumbnail parameters.

        Raises:
            ValueError: If the block parameters are invalid.
        """
        assert header.type == BlockType.THUMBNAIL
        format, width, height = struct.unpack("<HHH", file.read(6))
        return ThumbnailParameter(
            format=ThumbnailFormat(format), width=width, height=height
        )

    def _parse_gcode_parameters(
        self, file: BinaryIO, header: BlockHeader
    ) -> GCodeParameter:
        """
        Parse G-code block parameters from a binary file.

        Args:
            file (BinaryIO): A binary file stream to parse.
            header (BlockHeader): The block's header.

        Returns:
            GCodeParameter: The G-code parameters.

        Raises:
            ValueError: If the block parameters are invalid.
        """
        assert header.type == BlockType.GCODE
        encoding = struct.unpack("<H", file.read(2))[0]
        return GCodeParameter(encoding=GCodeEncoding(encoding))

    def _parse_metadata(self, data: bytes, encoding: EncodingType) -> Dict[str, str]:
        """
        Parse metadata content based on the encoding type.

        Args:
            data (bytes): The metadata content.
            encoding (EncodingType): The encoding type.

        Returns:
            Dict[str, str]: The parsed metadata as key-value pairs.

        Raises:
            ValueError: If the metadata cannot be parsed.
        """
        if encoding == EncodingType.INI:
            text = data.decode("utf-8")
            result = {}
            for line in text.splitlines():
                line = line.strip()
                if not line or line.startswith(";"):  # Skip empty lines and comments
                    continue
                try:
                    key, value = line.split("=", 1)
                    result[key.strip()] = value.strip()
                except ValueError:
                    raise ValueError(f"Invalid metadata line: {line}")
            return result

        raise ValueError(f"Unsupported encoding type: {encoding}")

    def _read_block(self, file: BinaryIO, header: BlockHeader) -> bytes:
        """
        Read and uncompress a block's data from a binary file.

        Args:
            file (BinaryIO): A binary file stream to parse.
            header (BlockHeader): The block's header.

        Returns:
            bytes: The block's data, decompressed if necessary.

        Raises:
            ValueError: If the block data is invalid or decompression fails.
        """
        data = file.read(header.compressed_size)
        if len(data) != header.compressed_size:
            raise ValueError("Invalid block data: too short")

        if header.parent.checksum_type == ChecksumType.CRC32:
            checksum = struct.unpack("<I", file.read(4))[0]
            # TODO: Implement CRC32 verification

        if header.compression == CompressionType.NONE:
            return data

        if header.compression == CompressionType.DEFLATE:
            return zlib.decompress(data)

        if header.compression == CompressionType.HEATSHRINK_11_4:
            return heatshrink2.decompress(data, window_sz2=11, lookahead_sz2=4)

        if header.compression == CompressionType.HEATSHRINK_12_4:
            return heatshrink2.decompress(data, window_sz2=12, lookahead_sz2=4)

        raise ValueError(f"Unsupported block compression type: {header.compression}")

    def parse_stream(self, stream: BinaryIO) -> Iterator[Block]:
        """
        Parse a stream of bgcode blocks.

        Args:
            stream (BinaryIO): A binary stream to parse.

        Yields:
            Block: The parsed block.

        Raises:
            ValueError: If the stream contains invalid data.
        """
        if not isinstance(stream, io.IOBase):
            raise AttributeError(
                "stream is not a IOBase object, " f"it is a {type(stream)}"
            )
        if not stream.readable():
            raise AttributeError("stream is not readable")

        try:
            file_header = self._parse_file_header(stream)

            while True:
                block = self._parse_block(stream, file_header)
                if block is None:
                    break
                yield block

        except Exception as e:
            raise ValueError(f"Error parsing bgcode: {e}") from e

    def _parse_file_header(self, file: BinaryIO) -> FileHeader:
        """
        Parse the file header from a binary file.

        Args:
            file (BinaryIO): A binary file stream to parse.

        Returns:
            FileHeader: The parsed file header.

        Raises:
            ValueError: If the file header is invalid.
        """
        header_data = file.read(10)
        if len(header_data) != 10:
            raise ValueError("Invalid file header: too short")

        magic = header_data[:4]
        if magic != b"GCDE":
            raise ValueError(f"Invalid magic number: {magic}")

        version = struct.unpack("<I", header_data[4:8])[0]
        if version != 1:
            raise ValueError(f"Unsupported version: {version}")

        checksum_type = ChecksumType(struct.unpack("<H", header_data[8:10])[0])
        if checksum_type not in (ChecksumType.NONE, ChecksumType.CRC32):
            raise ValueError(f"Unsupported checksum type: {checksum_type}")

        return FileHeader(magic=magic, version=version, checksum_type=checksum_type)

    def _parse_block(
        self, stream: BinaryIO, file_header: FileHeader
    ) -> Optional[Block]:
        block_header = self._parse_block_header(stream, file_header)
        if block_header is None:
            # Reached the end of the file
            return None

        # Parse block parameters if needed
        if block_header.is_metadata:
            encoding = self._parse_metadata_parameters(stream, block_header)
            data = self._read_block(stream, block_header)
            metadata = self._parse_metadata(data, encoding)

            if block_header.type == BlockType.FILE_METADATA:
                return FileMetadataBlock(block_header, encoding, metadata)

            if block_header.type == BlockType.PRINTER_METADATA:
                return PrinterMetadataBlock(block_header, encoding, metadata)

            if block_header.type == BlockType.PRINT_METADATA:
                return PrintMetadataBlock(block_header, encoding, metadata)

            if block_header.type == BlockType.SLICER_METADATA:
                return SlicerMetadataBlock(block_header, encoding, metadata)

        if block_header.type == BlockType.GCODE:
            parameters = self._parse_gcode_parameters(stream, block_header)
            data = self._read_block(stream, block_header)
            return GCodeBlock(block_header, parameters, data)

        if block_header.type == BlockType.THUMBNAIL:
            parameters = self._parse_thumbnail_parameters(stream, block_header)
            data = self._read_block(stream, block_header)
            return ThumbnailBlock(block_header, parameters, data)

        raise ValueError(f"Unsupported metadata block type: {block_header.type}")

    def _parse_block_header(self, file: BinaryIO, parent: FileHeader) -> BlockHeader:
        """
        Parse a block header from a binary file.

        Args:
            file (BinaryIO): A binary file stream to parse.
            parent (FileHeader): The parent file header.

        Returns:
            BlockHeader: The parsed block header.

        Raises:
            ValueError: If the block header is invalid.
        """
        type_compression = file.read(4)
        if len(type_compression) == 0:
            # Readed the end of the file
            return None

        if len(type_compression) != 4:
            raise ValueError(
                f"Invalid block header: too short. Expected 4 bytes, got {len(type_compression)} bytes"
            )

        block_type = BlockType(struct.unpack("<H", type_compression[:2])[0])
        compression = CompressionType(struct.unpack("<H", type_compression[2:4])[0])

        uncompressed_size = struct.unpack("<I", file.read(4))[0]
        if compression == CompressionType.NONE:
            compressed_size = uncompressed_size
        else:
            compressed_size = struct.unpack("<I", file.read(4))[0]

        return BlockHeader(
            parent=parent,
            type=block_type,
            compression=compression,
            uncompressed_size=uncompressed_size,
            compressed_size=compressed_size,
        )


def is_bgcode_file(stream: BinaryIO) -> bool:
    """
    Checks if the given stream is a BGCode file by reading the first four bytes.

    Args:
        stream (BinaryIO): The stream to check.

    Returns:
        bool: True if the file starts with 'GCDE', False otherwise.
    """
    # Save the current position
    current_position = stream.tell()

    # Read the first four bytes
    magic = stream.read(4)

    # Restore the original position
    stream.seek(current_position)

    return magic == b"GCDE"


def main():
    """
    Prints a summary of the BGCode file, block by block.
    """
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="Parse and summarize a BGCode file")
    parser.add_argument("file", help="Path to the BGCode file to parse")
    args = parser.parse_args()

    try:
        bgcode_parser = BasicBGCodeParser()
        blocks = bgcode_parser.parse_file_to_list(args.file)

        print(f"\nBGCode File Summary: {args.file}")
        print("=" * 50)

        for i, block in enumerate(blocks, 1):
            print(f"\nBlock {i}:")
            print(f"Type: {block.type}")
            print(f"Compression: {block.header.compression}")
            print(f"Size: {block.header.uncompressed_size} bytes (uncompressed)")

            if isinstance(block, MetadataBlock):
                print("Metadata:")
                for key, value in block.data.items():
                    print(f"  {key}: {value}")

            elif isinstance(block, GCodeBlock):
                print(f"Encoding: {block.parameters.encoding}")
                print("Preview:")
                lines = block.data().splitlines()[:3]
                for line in lines:
                    print(f"  {line}")
                if len(lines) == 3:
                    print("  ...")

            elif isinstance(block, ThumbnailBlock):
                print(f"Format: {block.parameters.format}")
                print(f"Dimensions: {block.parameters.width}x{block.parameters.height}")
                print(f"Size: {len(block.data)} bytes")

            print("-" * 30)

        print(f"\nTotal blocks: {len(blocks)}")

    except Exception as e:
        print(f"Error parsing BGCode file: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
