import os
import pytest  # type: ignore
from io import StringIO
from gcode_file import BasicGCodeParser


@pytest.fixture
def fixtures_dir() -> str:
    """Return the path to the fixtures directory."""
    return os.path.join(os.path.dirname(__file__), "..", "fixtures")


def test_parse_line_valid_command():
    parser = BasicGCodeParser()
    line = "G1 X10.5 Y20.3 Z-5.0 F1500"
    result = parser.parse_line(line)
    assert result is not None
    assert result.command == "G1"
    assert result.fields == {"X": 10.5, "Y": 20.3, "Z": -5.0, "F": 1500}
    assert result.error is None


def test_parse_line_invalid_command():
    parser = BasicGCodeParser()
    line = "G999 X10"
    with pytest.raises(ValueError):
        parser.parse_line(line)


def test_parse_line_comment():
    """Test parsing a line that is just a comment."""
    parser = BasicGCodeParser()
    line = "; This is a comment"
    result = parser.parse_line(line)
    assert result is not None
    assert result.command == ""
    assert result.fields == {}
    assert result.comment == "This is a comment"
    assert str(result) == " ;This is a comment"


def test_parse_line_with_comment():
    """Test parsing a line with both a command and a comment."""
    parser = BasicGCodeParser()
    line = "G1 X10 Y20 ; Move to position"
    result = parser.parse_line(line)
    assert result is not None
    assert result.command == "G1"
    assert result.fields == {"X": 10, "Y": 20}
    assert result.comment == "Move to position"
    assert str(result) == "G1 X10 Y20 ;Move to position"


def test_parse_line_with_multiple_comments():
    """Test parsing a line with multiple semicolons."""
    parser = BasicGCodeParser()
    line = "G1 X10 ; First comment ; Second comment"
    result = parser.parse_line(line)
    assert result is not None
    assert result.command == "G1"
    assert result.fields == {"X": 10}
    assert result.comment == "First comment ; Second comment"
    assert str(result) == "G1 X10 ;First comment ; Second comment"


def test_parse_stream_with_comments():
    """Test parsing a stream with multiple lines including comments."""
    parser = BasicGCodeParser()
    gcode = """G1 X10 Y20 ; First move
; Comment line
G1 Z30 ; Second move
"""
    stream = StringIO(gcode)
    commands = list(parser.parse_stream(stream))

    assert len(commands) == 3

    assert commands[0].command == "G1"
    assert commands[0].fields == {"X": 10, "Y": 20}
    assert commands[0].comment == "First move"

    assert commands[1].command == ""
    assert commands[1].fields == {}
    assert commands[1].comment == "Comment line"

    assert commands[2].command == "G1"
    assert commands[2].fields == {"Z": 30}
    assert commands[2].comment == "Second move"


def test_parse_line_unknown_field():
    parser = BasicGCodeParser()
    line = "G1 X10.5 Y20.3 Q5.0"
    with pytest.raises(ValueError):
        parser.parse_line(line)


def test_parse_line_non_strict_mode():
    parser = BasicGCodeParser(strict_mode=False)
    line = "G999 X10"  # Invalid command
    result = parser.parse_line(line)
    assert result is not None
    assert result.command == "G999"
    assert result.fields == {"X": 10}
    assert result.error is not None
    assert "unsupported command" in result.error.lower()


def _test_single_file(parser: BasicGCodeParser, file_path: str):
    try:
        found = 0
        for command in parser.parse_file(file_path):
            if command.error:
                # We accept empty g1 commands, due to bugs in PrusaSlicer.
                # For example: https://github.com/prusa3d/PrusaSlicer/issues/7714
                if command.command == "G1" and command.error == "G1 requires at least one of the fields, but none were provided.":
                    continue

                pytest.fail(f"Failed to parse {file_path}: {command.error}")
            found += 1

        assert found > 0, f"No commands parsed in {file_path}"

    except Exception as e:
        pytest.fail(f"Failed to parse {file_path}: {e}")


def test_parse_all_fixtures(fixtures_dir):
    parser = BasicGCodeParser(strict_mode=False)

    for filename in os.listdir(fixtures_dir):
        if filename.endswith(".gcode"):
            file_path = os.path.join(fixtures_dir, filename)
            _test_single_file(parser, file_path)
