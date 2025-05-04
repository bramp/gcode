from typing import Any, Dict


class GcodeCommand:
    """
    Represents a parsed G-code command.

    Attributes:
        command (str): The G-code command (e.g., G1, M104).
        fields (Dict[str, Any]): The fields associated with the command. The
        values may be one of int, float, str, or bool.
    """
    def __init__(self, command: str, fields: Dict[str, Any]):
        self.command = command
        self.fields = fields

    def _field_repr(self, key: str, value: Any) -> str:
        """
        Return a string representation of a field in valid G-code notation.

        Args:
            key (str): The field key (e.g., 'X', 'Y', 'Z').
            value (Any): The field value (int, float, str, or bool).

        Returns:
            str: The field as a string in valid G-code format.
        """
        if isinstance(value, bool):
            # If the flag is false, we treat it as being unset.
            return f"{key}{int(value)}" if value else ""

        if isinstance(value, (int, float)):
            return f"{key}{value}"

        if isinstance(value, str):
            raise NotImplementedError("String fields are not yet supported.")

        return ValueError(f"Unsupported field type: {type(value)} for key: {key}")

    def __repr__(self):
        """
        Return a string representation of the G-code command in valid G-code notation.

        Returns:
            str: The G-code command as a string in valid G-code format.
        """
        params_str = " ".join(self._field_repr(key, value) for key, value in self.fields.items())
        return f"{self.command} {params_str}".strip()