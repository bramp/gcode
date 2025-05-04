import unittest

from gcode.gcode_parser import GCodeParser

class TestGCodeParser(unittest.TestCase):
    def setUp(self):
        from gcode.gcode_parser import GCodeParser
        self.parser = GCodeParser()

    def test_parse_line_valid_command(self):
        line = "G1 X10.5 Y20.3 Z-5.0 F1500"
        result = self.parser.parse_line(line)
        self.assertIsNotNone(result)
        self.assertEqual(result.command, "G1")
        self.assertEqual(result.fields, {"X": 10.5, "Y": 20.3, "Z": -5.0, "F": 1500})
        self.assertIsNone(result.error)

    def test_parse_line_invalid_command(self):
        line = "G999 X10"
        with self.assertRaises(ValueError):
            self.parser.parse_line(line)

    def test_parse_line_comment(self):
        line = "; This is a comment"
        result = self.parser.parse_line(line)
        self.assertIsNone(result)

    def test_parse_line_unknown_field(self):
        line = "G1 X10.5 Y20.3 Q5.0"
        with self.assertRaises(ValueError):
            self.parser.parse_line(line)

    def test_parse_line_non_strict_mode(self):
        parser = GCodeParser(strict_mode=False)
        line = "G999 X10"  # Invalid command
        result = parser.parse_line(line)
        self.assertIsNotNone(result)
        self.assertEqual(result.command, "G999")
        self.assertEqual(result.fields, {"X": 10})
        self.assertIsNotNone(result.error)
        self.assertIn("unsupported command", result.error.lower())

    def test_parse_file(self):
        self.parser.parse_file("fixtures/simple.gcode")

class TestGCodeParserOnAllFixtures(unittest.TestCase):
    def setUp(self):
        from gcode.gcode_parser import GCodeParser
        self.parser = GCodeParser(strict_mode=False)

    def test_parse_all_fixtures(self):
        import os

        fixtures_dir = os.path.join(os.path.dirname(__file__), "fixtures")
        for filename in os.listdir(fixtures_dir):
            if filename.endswith(".gcode"):
                file_path = os.path.join(fixtures_dir, filename)
                with self.subTest(fixture=filename):
                    try:
                        found = 0;
                        for command in self.parser.parse_file(file_path):
                            if command.error:
                                # We accept empty g1 commands, due to bugs in PrusaSlicer
                                # e.g https://github.com/prusa3d/PrusaSlicer/issues/7714
                                if command.command == "G1" and command.error == "G1 requires at least one of the fields, but none were provided.":
                                    continue

                                self.fail(f"Failed to parse {filename}: {command.error}")
                            found += 1

                        self.assertGreater(found, 0, f"No commands parsed in {filename}")

                    except Exception as e:
                        self.fail(f"Failed to parse {filename}: {e}")


if __name__ == '__main__':
    unittest.main()