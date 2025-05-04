Warning: This is a work in progress.

# G-code Parser

This project is designed to parse G-code files, which are used to control CNC machines and 3D printers. The goal is to provide a simple and efficient way to read and interpret G-code commands.

## Project Structure

```
gcode-parser
├── src
│   ├── __init__.py
│   └── parser.py
├── tests
│   ├── __init__.py
│   └── test_parser.py
├── requirements.txt
├── setup.py
└── README.md
```

## Installation

To install the required dependencies, run:

```
pip install -r requirements.txt
```

## Usage

To use the G-code parser, import the necessary functions or classes from the `parser` module in the `src` directory.

Example:

```python
from src.parser import parse_gcode

# Your code to parse G-code files
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an
issue for any suggestions or improvements.

### Running Tests

```shell
python -m unittest discover tests
```

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
