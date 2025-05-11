import io
import pytest # type: ignore
from gcode_file import GCodeParser, ThumbnailCommand

@pytest.fixture
def parser():
    """Create a parser instance for testing."""
    return GCodeParser()

def test_thumbnail_without_format(parser: GCodeParser):
    """Test parsing a thumbnail without a specified format."""
    stream = io.StringIO("""; thumbnail begin 16x16 956
        ; iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAACk0lEQVR4AVWS60/TUBjG+2cYgwEdA0
        ; VgMnQMx2Xd1q27tLu0XbuuHUPjlaDBaIwENGQY75dEUNSoJERjvMcPGmM0EfWD/lOPfd9YCB+e9PS8
        ; z+8577kI8XgcoiiyEokEK5lMsgoVCiRJ4n+/7vuJFXwglUqxyJzJZFAsFpHP55FOp6EoCo+p5v
        ; v8QIEmyUQQiVYtl8uY0URMFCVks1nIsoyaKsMsqzwmHzHECvRDk7lcjsFSqYSzRhIrWi9euPvx6cQI
        ; fk8fZM0Z4+yhjvwggUBVVWEYBrdN42tuCjNjHViu9G7ApPlqnGEKobMhVtA0bQMmUQc3JiS8aoTx5W
        ; hkS8BTJ4K7DRHzThZGSWFOqFarnOanUuCcmcCqFcKTaj8eV/vwwNsObWlR7sIlqZO/z9woZutZCAS6
        ; loGpundwtopWQ8Z1YwinRtpxUQoyQGPS52PDWJ8exbvJCNbsAVw2hiHcd0fxvhnGh+YgXrsDuKPuwU
        ; O9l4HndghfvW3MJgOYjrXj1+kx/D0Tx5+ZcTwy+mGnYxCWnRi+HR/C+skoXjr72LxU3ssBb7xzoPmr
        ; uW5cSAQY/j4Vw1yqEy0lBL1cgnDbjGKtFmLjlWw3t7yQDnLA2/8BrUwQS5U+3FJ7cDjSholoAGalCF
        ; 3XIay4MfzwTGRcNftxr9TDaslBfJwcxM+pYdxUduPQgTbUw9thi2FYWhl0+HwLk4qII0M7vHvfifPi
        ; Lix4q7W8ThY9LWS6cE4MoBraBn2wA1YugVqtBsuyNgOoDUPzri+fgaHI0HMp6LLI0qQR6NIoaqUCms
        ; 0mHMfZEsBb8B+SaZpcsG17Q/V6neWPG40Gf8lLDLECPR5KokQq+EEkWs1fkUQ1P4wCiP0Hjx3/1QGw
        ; q6gAAAAASUVORK5CYII=
        ; thumbnail end
    """)

    commands = list(parser.parse_stream(stream))
    assert len(commands) == 1

    thumbnail = commands[0]
    assert isinstance(thumbnail, ThumbnailCommand)

    assert thumbnail.format == "PNG"
    assert thumbnail.width == 16
    assert thumbnail.height == 16
    assert thumbnail.size == 956

    # TODO Test the content is the expected PNG data

def test_thumbnail_with_format(parser: GCodeParser):
    """Test parsing a thumbnail without a specified format."""
    stream = io.StringIO("""; thumbnail_QOI begin 16x16 500
        ; cW9pZgAAABAAAAAQBAD/ZmZmAMP/NDQ0/8D+Y2NjhoiViH+iiJyIpYhAo4g6wgH+ZGRkk4gIBBM1Fx
        ; MmsIi2iDrAAcACiIgXExc1IsAEu4gglYg6AbyIrogENRMXEwT+iFUg/k5OTrmIIIyIlYgB/mlpaTuQ
        ; iA8EJqWIBBP+lWEtEQIaDyK8iDHAPBo8MRY8uYj+mmcym4j+RUVFwDz+jVolJhMXIqWIpIj+XkIm/p
        ; RhLBEzJQCiiDwPKTUXMQQTC76I/nBUODM8AP5dQSX+jVklLaWICyYiJv6KViIlAqaIGTTAODwapIgL
        ; FhMmIhkgAi3AB6aIf52IBxoDNP6KVyIpM6SICv5EREQ8wP5cQCQWp4iiiD8wAzADPi8pIjwePAcLFg
        ; 6miMA7MD4dMS08DwspCyXAA6eIBjdAGjEAMQs4GgslFqSIPwMOKKOIADEACw8aFiUHIcADDiEOKBMA
        ; LQAaCykSMAPAPxIdLDcAAAAAAAAAAQ==
        ; thumbnail_QOI end
    """)

    commands = list(parser.parse_stream(stream))
    assert len(commands) == 1

    thumbnail = commands[0]
    assert isinstance(thumbnail, ThumbnailCommand)

    assert thumbnail.format == "QOI"
    assert thumbnail.width == 16
    assert thumbnail.height == 16
    assert thumbnail.size == 500

# def test_missing_end():
#     """Test handling of missing thumbnail end marker."""
#     stream = io.StringIO("""; thumbnail begin 16x16 956
#     """)
# 
#     with pytest.raises(ValueError):
#         parser.parse_stream(stream)

