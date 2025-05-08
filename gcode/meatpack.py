"""MeatPack compression algorithm for G-code.

This module implements the MeatPack compression algorithm, which is specifically
designed for compressing G-code files. The algorithm uses a 4-bit encoding scheme
for common G-code characters to achieve efficient compression.

The MeatPack algorithm is particularly useful for:
- Reducing the size of G-code files for storage
- Speeding up G-code transmission to 3D printers
- Compressing G-code for embedded systems with limited memory

Example usage:
    >>> from meatpacking import compress, decompress
    
    # Compress a G-code string
    >>> gcode = "G1 X100 Y200"
    >>> compressed = compress(gcode)
    
    # Decompress the data
    >>> decompressed = decompress(compressed)
    >>> print(decompressed.decode('ascii'))
    'G1 X100 Y200'
    
    # Using the classes directly
    >>> from meatpacking import MeatPacker, MeatUnpacker
    >>> packer = MeatPacker()
    >>> compressed = packer.compress(gcode)
    >>> unpacker = MeatUnpacker()
    >>> decompressed = unpacker.decompress(compressed)

The compression algorithm works by:
1. Using 4-bit codes for common G-code characters (0-9, ., E, \\n, G, X)
2. Packing two characters into one byte when possible
3. Using signal codes for characters that can't be packed
4. Supporting command sequences for controlling compression state

Note: The algorithm is case-insensitive for G, E, and X characters.

Related:
* https://github.com/scottmudge/OctoPrint-MeatPack/blob/master/OctoPrint_MeatPack/meatpack.py
* https://github.com/prusa3d/libbgcode/blob/main/src/LibBGCode/binarize/meatpack.cpp
* https://github.com/jamesgopsill/meatpack/
* https://purisa.me/blog/meat-pack-algorithm/
"""


from typing import Union

# Command bytes for controlling the compression state
_ENABLE_PACKING   = 0xFB  # Enable 4-bit packing mode
_DISABLE_PACKING  = 0xFA  # Disable 4-bit packing mode
_RESET_ALL        = 0xF9  # Reset all settings to defaults
_QUERY_CONFIG     = 0xF8  # Query current configuration
_ENABLE_NO_SPACE  = 0xF7  # Signal that spaces will be omitted (so 'E' will be handled as a normal character)
_DISABLE_NO_SPACE = 0xF6  # Signal that spaces will be included (so 'E' will be handled as a special character)

# Signal code for unpacked characters
_SIGNAL_CODE = 0x0F  # Indicates the following byte is an unpacked character

# Base lookup table for common G-code characters (4-bit codes)
_CHAR_TO_CODE = {
    '0': 0x00, '1': 0x01, '2': 0x02, '3': 0x03, '4': 0x04,
    '5': 0x05, '6': 0x06, '7': 0x07, '8': 0x08, '9': 0x09,
    '.': 0x0A, ' ': 0x0B, 'E': 0x0B, '\n': 0x0C, 'G': 0x0D, 'X': 0x0E
}

# Reverse lookup table for converting codes back to characters
_CODE_TO_CHAR = {v: k for k, v in _CHAR_TO_CODE.items()}

class GCodeCharIterator:
    """Iterator for G-code characters that handles filtering based on settings.
    
    This class provides a clean interface for iterating over G-code characters
    while handling comment removal, space omission, and case conversion.
    """
    
    def __init__(self, data: Union[str, bytes], omit_spaces: bool = False, 
                 omit_comments: bool = False, uppercase: bool = True):
        """Initialize the iterator.
        
        Args:
            data: Input data as string or bytes
            omit_spaces: If True, spaces will be skipped
            omit_comments: If True, comments will be skipped
            uppercase: If True, G, X, and E characters will be converted to uppercase
        """
        if isinstance(data, str):
            data = data.encode('ascii')
        self._data = data
        self._omit_spaces = omit_spaces
        self._omit_comments = omit_comments
        self._uppercase = uppercase
        self._pos = 0
    
    def __iter__(self):
        """Return self as an iterator."""
        return self
    
    def __next__(self) -> str:
        """Get the next character from the input, applying filters.
        
        Returns:
            The next character as a string.
            
        Raises:
            StopIteration: When there are no more characters to process.
        """
        while self._pos < len(self._data):
            char = chr(self._data[self._pos])
            self._pos += 1
            
            # Skip comments if enabled
            if self._omit_comments and char == ';':
                while self._pos < len(self._data) and self._data[self._pos] != ord('\n'):
                    self._pos += 1
                continue
            
            # Skip spaces if enabled
            if self._omit_spaces and char in (' ', '\t'):
                continue
            
            # Convert case if enabled
            if self._uppercase and char in ('egx' if self._omit_spaces else 'gx'):
                char = char.upper()
            
            return char
        
        raise StopIteration

class MeatPacker:
    """MeatPack compression algorithm for G-code.
    
    This class implements the compression part of the MeatPack algorithm which is
    specifically designed for compressing G-code files. It uses a 4-bit encoding
    scheme for common G-code characters to achieve compression.
    
    The class can be used in two ways:
    1. Instance-based usage for multiple operations:
        >>> packer = MeatPacker()
        >>> compressed = packer.compress("G1 X100")
    
    2. Using the module-level functions for one-off operations:
        >>> from meatpacking import compress
        >>> compressed = compress("G1 X100")
    """
    
    def __init__(self, omit_spaces: bool = False, omit_comments: bool = False, uppercase: bool = True):
        """Initialize a new MeatPacker instance.
        
        Args:
            omit_spaces: If True, spaces between commands will be omitted in the
                        compressed output. This makes the algorithm lossy. Defaults to False.
            omit_comments: If True, G-code comments (lines starting with ;) will
                          be removed before compression. This makes the algorithm lossy. Defaults to False.
            uppercase: If True, converts G, X, and E (when omit_spaces is False)
                      characters to uppercase before compression. This leads to better compression, 
                      but makes the algorithm lossy. Defaults to True.
        """
        self._buffer = bytearray()
        self._omit_spaces = omit_spaces
        self._omit_comments = omit_comments
        self._uppercase = uppercase
    
    def _char_to_code(self, char: str) -> int | None:
        """Convert a character to its 4-bit code."""
        if char == ' ' and self._omit_spaces:
            return None
        if char == 'E' and not self._omit_spaces:
            return None
        return _CHAR_TO_CODE.get(char)
    
    def _pack_data(self, data: bytes):
        """Pack input data into compressed format using the MeatPack algorithm.
        
        Processes data in pairs, packing characters into single bytes when possible.
        Uses GCodeCharIterator to handle filtering and case conversion.
        
        Args:
            data: ASCII-encoded G-code bytes to compress.
        
        Note: Modifies _buffer directly. Clear buffer before calling if needed.
        """
        # Create iterator for processing characters
        iterator = GCodeCharIterator(data, self._omit_spaces, self._omit_comments, self._uppercase)
        
        while True:
            # Get two characters
            c1 = next(iterator, None)
            if c1 is None:
                break

            c2 = next(iterator, "\n")
            
            # Check if both characters can be packed
            p1 = self._char_to_code(c1)
            p2 = self._char_to_code(c2)
            
            if p1 is not None and p2 is not None:
                # Pack both characters into one byte
                packed = p1 | (p2 << 4)
                self._buffer.append(packed)
            elif p1 is not None:
                # First character can be packed, second cannot
                self._buffer.append(p1 | (_SIGNAL_CODE << 4))
                self._buffer.append(ord(c2))
            elif p2 is not None:
                # Second character can be packed, first cannot
                self._buffer.append(_SIGNAL_CODE | (p2 << 4))
                self._buffer.append(ord(c1))
            else:
                # Neither character can be packed
                self._buffer.append(_SIGNAL_CODE | (_SIGNAL_CODE << 4))
                self._buffer.append(ord(c1))
                self._buffer.append(ord(c2))
        
    
    def compress(self, data: Union[str, bytes]) -> bytes:
        """Compress the input data using MeatPack algorithm.
        
        This method compresses G-code data by:
        1. Converting common characters to 4-bit codes
        2. Packing two characters into one byte when possible
        3. Using signal codes for characters that can't be packed
        4. Adding appropriate command sequences
        
        Args:
            data: Input data as string or bytes. If string, it will be encoded
                 as ASCII before compression.
        
        Returns:
            Compressed data as bytes. The output includes command sequences
            to enable packing at the start and reset at the end.
        
        Raises:
            TypeError: If the input is neither string nor bytes
        
        Example:
            >>> packer = MeatPacker()
            >>> compressed = packer.compress("G1 X100 Y200")
            >>> len(compressed) < len("G1 X100 Y200".encode('ascii'))
            True
        """
        if not isinstance(data, (str, bytes)):
            raise TypeError(f"Input data must be string or bytes, got {type(data).__name__}")
        
        self._buffer.clear()

        # Add enable packing command
        self._buffer.extend([0xFF, 0xFF, _ENABLE_PACKING])

        # Signal if spaces will be omitted
        if self._omit_spaces:
            self._buffer.extend([0xFF, 0xFF, _ENABLE_NO_SPACE])

        self._pack_data(data)

        # Add reset command at the end
        self._buffer.extend([0xFF, 0xFF, _RESET_ALL])
        return bytes(self._buffer)


class MeatUnpacker:
    """MeatPack decompression algorithm for G-code.
    
    This class implements the decompression part of the MeatPack algorithm which is
    specifically designed for decompressing G-code files. It handles the 4-bit
    encoded characters and command sequences to restore the original G-code.
    
    The class can be used in two ways:
    1. Instance-based usage for multiple operations:
        >>> unpacker = MeatUnpacker()
        >>> decompressed = unpacker.decompress(compressed)
    
    2. Using the module-level functions for one-off operations:
        >>> from meatpacking import decompress
        >>> decompressed = decompress(compressed)
    """
    
    def __init__(self):
        """Initialize a new MeatUnpacker instance."""
        self._buffer = bytearray()
        self._packing = False
        self._omit_spaces = False
    
    def _code_to_char(self, code: int, omit_spaces: bool = False) -> str:
        """Convert a 4-bit code to its character."""
        if code == 0x0B:
            return 'E' if omit_spaces else ' '
        return _CODE_TO_CHAR.get(code)
    
    def decompress(self, data: bytes) -> bytes:
        """Decompress MeatPack compressed data.
        
        This method decompresses data that was compressed using the MeatPack
        algorithm. It handles:
        1. Command sequences for enabling/disabling packing
        2. 4-bit packed characters
        3. Signal codes for unpacked characters
        4. Case-insensitive handling of G, E, and X characters
        
        Args:
            data: Compressed data as bytes. Must be valid MeatPack compressed
                 data including command sequences.
        
        Returns:
            Decompressed data as bytes. The output will be ASCII-encoded
            G-code if the input was compressed from ASCII G-code.
        
        Example:
            >>> unpacker = MeatUnpacker()
            >>> compressed = packer.compress("G1 X100")
            >>> decompressed = unpacker.decompress(compressed)
            >>> print(decompressed.decode('ascii'))
            'G1 X100'
        """
        result = bytearray()
        i = 0
        
        while i < len(data):
            # Check for command sequence
            if i + 2 < len(data) and data[i] == 0xFF and data[i + 1] == 0xFF:
                cmd = data[i + 2]
                if cmd == _ENABLE_PACKING:
                    self._packing = True
                elif cmd == _DISABLE_PACKING:
                    self._packing = False
                elif cmd == _RESET_ALL:
                    self._packing = False
                    self._omit_spaces = False
                elif cmd == _ENABLE_NO_SPACE:
                    self._omit_spaces = True
                elif cmd == _DISABLE_NO_SPACE:
                    self._omit_spaces = False
                i += 3
                continue
            
            if not self._packing:
                result.append(data[i])
                i += 1
                continue
            
            # Process packed byte
            packed = data[i]
            i += 1
            
            # Extract the two 4-bit codes
            code1 = packed & 0x0F
            code2 = (packed >> 4) & 0x0F
            
            # Handle first character
            if code1 == _SIGNAL_CODE:
                if i < len(data):
                    result.append(data[i])
                    i += 1
            else:
                if (char := self._code_to_char(code1, self._omit_spaces)) is not None:
                    result.append(ord(char))
            
            # Handle second character
            if code2 == _SIGNAL_CODE:
                if i < len(data):
                    result.append(data[i])
                    i += 1
            else:
                if (char := self._code_to_char(code2, self._omit_spaces)) is not None:
                    result.append(ord(char))
        
        return bytes(result)


def compress(data: Union[str, bytes], omit_spaces: bool = False, omit_comments: bool = False, uppercase: bool = True) -> bytes:
    """Compress data using MeatPack algorithm.
    
    This is a convenience function that creates a MeatPacker instance and
    compresses the input data. It's useful for one-off compression operations.
    
    Args:
        data: Input data as string or bytes. If string, it will be encoded
              as ASCII before compression.
        omit_spaces: If True, spaces between commands will be omitted in the
                    compressed output. Defaults to False.
        omit_comments: If True, G-code comments (lines starting with ;) will
                      be removed before compression. Defaults to False.
        uppercase: If True, converts G, X, and E (when omit_spaces is False)
                  characters to uppercase before compression. This ensures
                  consistent handling of case-insensitive G-code commands.
                  Defaults to True.
    
    Returns:
        Compressed data as bytes.
    
    Example:
        >>> compressed = compress("G1 X100 Y200 ; Comment", omit_spaces=True, omit_comments=True)
        >>> decompressed = decompress(compressed)
        >>> print(decompressed.decode('ascii'))
        'G1X100Y200'
    """
    packer = MeatPacker(omit_spaces=omit_spaces, omit_comments=omit_comments, uppercase=uppercase)
    return packer.compress(data)


def decompress(data: bytes) -> bytes:
    """Decompress MeatPack compressed data.
    
    This is a convenience function that creates a MeatUnpacker instance and
    decompresses the input data. It's useful for one-off decompression operations.
    
    Args:
        data: Compressed data as bytes. Must be valid MeatPack compressed
              data including command sequences.
    
    Returns:
        Decompressed data as bytes.
    
    Example:
        >>> compressed = compress("G1 X100 Y200")
        >>> decompressed = decompress(compressed)
        >>> print(decompressed.decode('ascii'))
        'G1 X100 Y200'
    """
    unpacker = MeatUnpacker()
    return unpacker.decompress(data) 