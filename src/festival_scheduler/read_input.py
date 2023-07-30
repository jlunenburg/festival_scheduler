import argparse
from .types import Show


def get_shows() -> list[Show]:
    """
    Returns the shows to be scheduled from the input file as a list of Shows
    :return:
    """
    filename = get_filename_from_args()
    shows = read_input(filename)
    return shows


def get_filename_from_args() -> str:
    """
    Gets the filename by parsing the provided arguments
    :return:
    """
    parser = argparse.ArgumentParser(description="Creates a festival schedule")
    parser.add_argument('filename', help='file containing the data to create a schedule for')
    args = parser.parse_args()
    return args.filename


class ParseError(Exception):
    pass


def read_input(filename: str) -> list[Show]:
    """
    Reads and parses the file

    :param filename:
    :return:
    """
    result = []
    with open(filename, "r") as f:
        while True:
            line = f.readline()
            if line:
                try:
                    result.append(parse_line(line))
                except ParseError:
                    print(f"Cannot parse {line}, skipping")
                    continue
            else:
                break
    return result


def parse_line(line: str) -> Show:
    """
    Parses a line and returns a Show object

    :param line:
    :return:
    :raises: ParseError
    """
    words = line.split()
    try:
        result = Show(words[0], int(words[1]), int(words[2]))
    except Exception:
        raise ParseError(f"Cannot parse '{line}'")
    return result
