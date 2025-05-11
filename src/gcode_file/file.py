from typing import List, Union
from gcode_file.gcode.parser import GCodeParser
from gcode_file.bgcode.parser import BasicBGCodeParser, ThumbnailBlock, GCodeBlock, SlicerMetadataBlock

class FileBase:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def get_thumbnail_data(self) -> List[ThumbnailBlock]:
        raise NotImplementedError("This method should be implemented by subclasses.")

    def get_gcode_commands(self) -> List[str]:
        raise NotImplementedError("This method should be implemented by subclasses.")

    def get_slicer_settings(self) -> List[SlicerMetadataBlock]:
        raise NotImplementedError("This method should be implemented by subclasses.")

class BGFile(FileBase):
    def __init__(self, file_path: str):
        super().__init__(file_path)
        self.parser = BasicBGCodeParser()

    def get_thumbnail_data(self) -> List[ThumbnailBlock]:
        blocks = self.parser.parse_file_to_list(self.file_path)
        return [block for block in blocks if isinstance(block, ThumbnailBlock)]

    def get_gcode_commands(self) -> List[str]:
        blocks = self.parser.parse_file_to_list(self.file_path)
        return [block.data() for block in blocks if isinstance(block, GCodeBlock)]

    def get_slicer_settings(self) -> List[SlicerMetadataBlock]:
        blocks = self.parser.parse_file_to_list(self.file_path)
        return [block for block in blocks if isinstance(block, SlicerMetadataBlock)]

class GFile(FileBase):
    def __init__(self, file_path: str):
        super().__init__(file_path)
        self.parser = GCodeParser()

    def get_thumbnail_data(self) -> List[ThumbnailBlock]:
        return []  # GCode files do not have thumbnail data

    def get_gcode_commands(self) -> List[str]:
        return [command.command for command in self.parser.parse_file(self.file_path)]

    def get_slicer_settings(self) -> List[SlicerMetadataBlock]:
        return []  # GCode files do not have slicer settings

def File(file_path: str) -> Union[BGFile, GFile]:
    if file_path.endswith('.bgcode'):
        return BGFile(file_path)
    else:
        return GFile(file_path)