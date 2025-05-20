import os
import pytest
from gcode_file.file import open_file, BGcodeFile, GcodeFile


@pytest.fixture
def fixtures_dir() -> str:
    """Return the path to the fixtures directory."""
    return os.path.join(os.path.dirname(__file__), "..", "fixtures")

def test_file_factory_bgcode(fixtures_dir):
    file_path = os.path.join(fixtures_dir, 
                             "lines_0.4n_0.2mm_PETG_XLIS_57s.bgcode")
    file_instance = open_file(file_path)
    assert isinstance(file_instance, BGcodeFile)


def test_file_factory_gcode(fixtures_dir):
    file_path = os.path.join(fixtures_dir, 
                             "lines_0.4n_0.2mm_PETG_XLIS_57s.gcode")
    file_instance = open_file(file_path)
    assert isinstance(file_instance, GcodeFile)
    

def test_bgcode_file_methods(fixtures_dir):
    file_path = os.path.join(fixtures_dir, 
                             "lines_0.4n_0.2mm_PETG_XLIS_57s.bgcode")

    with BGcodeFile(file_path) as file:
        assert isinstance(file, BGcodeFile)
        assert file.file_metadata is not None
        assert file.printer_metadata is not None
        assert file.thumbnails is not None
        assert file.print_metadata is not None
        assert file.slicer_settings is not None
        assert file.commands is not None


def test_gcode_file_methods():
    file_path = "test.gcode"
    file_instance = GcodeFile(file_path)

    with pytest.raises(NotImplementedError):
        _ = file_instance.file_metadata

    with pytest.raises(NotImplementedError):
        _ = file_instance.printer_metadata

    with pytest.raises(NotImplementedError):
        _ = file_instance.thumbnails

    with pytest.raises(NotImplementedError):
        _ = file_instance.print_metadata

    with pytest.raises(NotImplementedError):
        _ = file_instance.slicer_settings

    with pytest.raises(NotImplementedError):
        _ = file_instance.commands