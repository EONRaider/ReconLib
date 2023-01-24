from pathlib import Path
from random import randrange
from typing import TextIO


def _get_random_line(fd: TextIO, line_num: int = None) -> str:
    """
    Get a random line from a file

    :param fd: File descriptor pointing to a file containing lines of
        text
    :param line_num: Number of a line to select in the file. Defaults to
        a random line if None
    :return: A string containing a line selected from the file
    """
    line = line_num
    for i, aline in enumerate(fd, start=1):
        if randrange(i) == 0:  # random int [0..i)
            line = aline
    return line.strip()


def random_user_agent(file_path: [str, Path] = None) -> str:
    """
    Get a random user-agent from a text file

    :param file_path: Path to a file containing line-separated
        user-agent strings
    :return: A string containing a randomly selected user-agent from the
        file
    """
    if file_path is None:
        file_path = Path(__file__).parent.absolute().joinpath("user-agents-list.txt")
    with open(file_path) as file:
        return _get_random_line(file)
