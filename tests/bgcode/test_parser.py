import os
import pytest # type: ignore
import struct
from io import BytesIO
from gcode_file import BasicBGCodeParser, CompressionType, ChecksumType, GCodeBlock

def create_test_bgcode(blocks=None):
    """Helper function to create a test bgcode file in memory."""
    if blocks is None:
        blocks = []

    # Create file header
    header = bytearray()
    header.extend(b"GCDE")  # Magic number
    header.extend(struct.pack("<I", 1))  # Version 1
    header.extend(struct.pack("<H", ChecksumType.NONE))  # No checksum

    # Create blocks
    data = bytearray(header)
    for block_type, content in blocks:
        # Block header
        data.extend(struct.pack("<H", block_type))  # Block type
        data.extend(struct.pack("<H", CompressionType.NONE))  # No compression
        data.extend(struct.pack("<I", len(content)))  # Uncompressed size
        # Block data
        data.extend(content)

    return BytesIO(data)

@pytest.fixture
def parser():
    """Create a parser instance for testing."""
    return BasicBGCodeParser()

def test_parse_real_files(parser: BasicBGCodeParser):
    """Test parsing real bgcode files from fixtures."""
    # Test files to check
    test_files = [
        "lines_0.4n_0.2mm_PETG_XLIS_57s.bgcode",
        "BonkersBenchy_PLA_8m.bgcode",
        "BenchyRules_PLA_14m.bgcode",
        "3DBenchy (5 Colours)_0.4n_0.2mm_PETG,PETG,PETG,PETG,PETG_XLIS_2h34m.bgcode"
    ]
    
    for filename in test_files:
        filepath = os.path.join("tests", "fixtures", filename)
        blocks = list()

        for block in parser.parse_file(filepath):
            blocks.append(block)
        
        # Basic validation
        assert len(blocks) > 0, f"No blocks found in {filename}"
        
        # Check that we have at least one G-code block
        gcode_blocks = [b for b in blocks if isinstance(b, GCodeBlock)]
        assert len(gcode_blocks) > 0, f"No G-code blocks found in {filename}"

        # Check that the G-code content is not empty
        for block in gcode_blocks:
            print(block.data())
            assert len(block.data()) > 0, f"Empty G-code data in {filename}"
