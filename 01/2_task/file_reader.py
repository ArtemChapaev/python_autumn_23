import re
import io


def file_reader(filename, words: list) -> str:
    if not isinstance(filename, str) and not isinstance(filename, io.TextIOBase):
        raise TypeError("filename must be str or io.TextIOBase")

    if not isinstance(words, list):
        raise TypeError("words must be list")

    # we delete word if it's equal ""
    words_with_spaces = [" " + w + " " for w in words if w]

    with open(filename, "r", encoding="UTF-8") if isinstance(filename, str) else filename as file:

        for line in file:
            line = re.match(r"[^\n\r]*", line).group(0)
            line_with_spaces = " " + line + " "
            line_with_spaces.lower()

            found_words = [w for w in words_with_spaces
                           if w in line_with_spaces]
            if found_words:
                yield line
