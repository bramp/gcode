Warning: This is a work in progress.

# Gcode-file

Python library for parsing G-Code, Binary G-Code files, and related metadata (thumbnails, slicer settings, etc

## Installation

```bash
pip install gcode-file
```

## Usage

### Command Line

The package includes a command-line tool to inspect gcode / bgcode files:

```bash
bgcode path/to/your/file.bgcode
```

This will print a summary of the file's contents, including metadata, G-code preview, and thumbnail information.

### Python API

```python
from bgcode.bgcode_parser import BasicBGCodeParser

# Parse a file
parser = BasicBGCodeParser()
blocks = parser.parse_file_to_list("path/to/your/file.bgcode")

# Iterate through blocks
for block in blocks:
    if block.type == BlockType.GCODE:
        # Access G-code content
        gcode_text = block.data()
    elif block.type == BlockType.FILE_METADATA:
        # Access metadata
        metadata = block.data
```

## Features

- Parses all BGCode block types:
  - File metadata
  - G-code
  - Slicer metadata
  - Printer metadata
  - Print metadata
  - Thumbnails
- Supports multiple compression types:
  - None
  - Deflate
  - Heatshrink (11/4 and 12/4)
- Supports multiple G-code encodings:
  - None
  - MeatPack
  - MeatPack with comments

## Development

```

# Setup venv
python3 -m venv venv

# Activate venv
source venv/bin/activate

# Install tools
pip install --upgrade pytest build twine

# Install dependencies
pip install -r requirements.txt

# Install editable version
pip install -e .


# Run tests
pytest tests/

# Publish Packages
python3 -m build
python3 -m twine upload --repository testpypi dist/*

python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps gcode
```

## License

```
BSD 3-Clause License

Copyright (c) 2025, Andrew Brampton

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```
