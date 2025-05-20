from dataclasses import dataclass
from enum import IntEnum


class ThumbnailFormat(IntEnum):
    PNG = 0
    JPG = 1
    QOI = 2

    def __str__(self) -> str:
        return f"{self.__class__.__name__}.{self.name}"


@dataclass
class Thumbnail:
    """
    Represents a thumbnail image with metadata and raw image data.

    Attributes:
        format (ThumbnailFormat): The format of the thumbnail image (e.g., PNG, JPG, QOI).
        width (int): The width of the thumbnail image in pixels.
        height (int): The height of the thumbnail image in pixels.
        data (bytes): The compressed image data of the thumbnail.
    """

    format: ThumbnailFormat
    width: int
    height: int
    data: bytes

    def __str__(self) -> str:
        return (
            "Thumbnail("
            f"format={self.format}, "
            f"width={self.width}, height={self.height}), "
            f"size={len(self.data)} bytes"
            ")"
        )
