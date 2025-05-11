
import argparse

from src.basic_parser import GCodeParser

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="Parse and print G-code file commands line by line.")
    arg_parser.add_argument("file", help="Path to the G-code file to parse.")
    args = arg_parser.parse_args()

    parser = GCodeParser()
    parser.parse_file(args.file)