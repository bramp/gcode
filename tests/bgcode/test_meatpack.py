"""Tests for the MeatPack compression algorithm.

This module contains tests for both the compression and decompression
functionality of the MeatPack algorithm. It tests:
1. Basic compression and decompression
2. Space omission
3. Comment removal
4. Case handling
5. Edge cases and error conditions
"""

import pytest  # type: ignore
from gcode_file.bgcode.meatpack import MeatPacker, MeatUnpacker, compress, decompress


def test_basic_compression():
    """Test basic compression and decompression."""
    # Test with simple G-code
    gcode = "G1 X100 Y200"
    compressed = compress(gcode)
    decompressed = decompress(compressed)
    assert decompressed.decode("ascii") == gcode


def test_original_example():
    """Test the original example from the OctoPrint README."""
    gcode = "G1 X113.214 Y91.45 E1.3154\n"

    compressed1 = compress(gcode)
    assert compressed1 == (
        b"\xff\xff\xfb"  # _ENABLE_PACKING
        b"\x1d\xeb\x11\xa3\x12\xb4\x9fY\xa1T\xfbE\xa1\x13E\xcc"
        b"\xff\xff\xf9"  # _RESET_ALL
    )

    compressed2 = compress(gcode, omit_spaces=True)
    assert compressed2 == (
        b"\xff\xff\xfb"  # _ENABLE_PACKING
        b"\xff\xff\xf7"  # _ENABLE_NO_SPACE
        b"\x1d\x1e1*A\x9fY\xa1T\x1b:Q\xc4"
        b"\xff\xff\xf9"  # _RESET_ALL
    )

    decompressed1 = decompress(compressed1)
    assert decompressed1.decode("ascii").rstrip() == gcode.rstrip()

    decompressed2 = decompress(compressed2)
    assert decompressed2.decode("ascii").rstrip() == "G1X113.214Y91.45E1.3154"


def test_space_omission():
    """Test compression with space omission."""
    gcode = "G1 X100 Y200"
    compressed = compress(gcode, omit_spaces=True)
    decompressed = decompress(compressed)
    assert decompressed.decode("ascii") == "G1X100Y200"


def test_comment_removal():
    """Test compression with comment removal."""
    gcode = "G1 X100 Y200 ; This is a comment"
    compressed = compress(gcode, omit_comments=True)
    decompressed = decompress(compressed)
    assert decompressed.decode("ascii").rstrip() == "G1 X100 Y200"


def test_case_handling():
    """Test case handling in compression."""
    # Test with lowercase
    gcode = "g1 x100 y200"
    compressed = compress(gcode, uppercase=True)
    decompressed = decompress(compressed)
    assert decompressed.decode("ascii") == "G1 X100 y200"

    # Test with mixed case
    gcode = "G1 x100 Y200"
    compressed = compress(gcode, uppercase=True)
    decompressed = decompress(compressed)
    assert decompressed.decode("ascii") == "G1 X100 Y200"

    # Test with uppercase disabled
    gcode = "g1 x100 y200"
    compressed = compress(gcode, uppercase=False)
    decompressed = decompress(compressed)
    assert decompressed.decode("ascii") == "g1 x100 y200"


def test_combined_options():
    """Test compression with multiple options enabled."""
    gcode = "g1 x100 y200 ; Comment"
    compressed = compress(gcode, omit_spaces=True, omit_comments=True)
    decompressed = decompress(compressed)
    assert decompressed.decode("ascii") == "G1X100y200"


def test_edge_cases():
    """Test edge cases and special characters."""
    # Test with empty string
    gcode = ""
    compressed = compress(gcode)
    decompressed = decompress(compressed)
    assert decompressed.decode("ascii") == ""

    # Test with only comments
    gcode = "; Comment only"
    compressed = compress(gcode, omit_comments=True)
    decompressed = decompress(compressed)
    assert decompressed.decode("ascii") == ""

    # Test with only spaces
    gcode = "   "
    compressed = compress(gcode, omit_spaces=True)
    decompressed = decompress(compressed)
    assert decompressed.decode("ascii") == ""


def test_error_conditions():
    """Test error conditions and invalid inputs."""
    # Test with None
    with pytest.raises(TypeError):
        compress(None)

    # Test with invalid type
    with pytest.raises(TypeError):
        compress(123)

    # Test with invalid bytes
    with pytest.raises(TypeError):
        decompress("not bytes")


def test_multiple_operations():
    """Test multiple compression/decompression operations with the same instance."""
    # Test multiple compressions with same settings
    packer = MeatPacker()
    gcode1 = "G1 X100"
    gcode2 = "G2 Y200"
    compressed1 = packer.compress(gcode1)
    compressed2 = packer.compress(gcode2)
    assert compressed1 != compressed2

    # Test multiple decompressions
    unpacker = MeatUnpacker()
    decompressed1 = unpacker.decompress(compressed1)
    decompressed2 = unpacker.decompress(compressed2)
    assert decompressed1.decode("ascii").rstrip() == gcode1
    assert decompressed2.decode("ascii").rstrip() == gcode2

    # Test multiple compressions with different settings
    packer1 = MeatPacker(omit_spaces=True)
    packer2 = MeatPacker(omit_comments=True)
    compressed1 = packer1.compress(gcode1)
    compressed2 = packer2.compress(gcode1)
    assert compressed1 != compressed2
