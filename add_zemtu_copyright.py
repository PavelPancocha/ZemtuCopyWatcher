"""
   Zemtu Carsharing Application
   Copyright (C) 2023 Zemtu OG
"""

import sys
import re
from datetime import datetime


class ZemtuCopyrightUpdater:
    COPYRIGHT_MESSAGE: str = \
'''\
"""
   Zemtu Carsharing Application
   Copyright (C) {current_year} Zemtu OG
"""\
'''

    def __init__(self, filename: str):
        self.filename: str = filename
        self.current_year: int = datetime.now().year

    def update_copyright(self):
        original_content: str = self._read_file()
        updated_content: str = self._process_content(original_content)
        if original_content != updated_content:
            self._write_file(updated_content)

    def _read_file(self) -> str:
        with open(self.filename, "r", newline="", encoding="utf8") as f_read:
            return f_read.read()

    def _write_file(self, content: str) -> None:
        with open(self.filename, "w", newline="", encoding="utf8") as f_write:
            f_write.write(content)

    def _process_content(self, content: str) -> str:
        copyright_found = re.search(r"Copyright \(C\) (\d{4})(?:-(\d{4}))? Zemtu OG", content)

        if copyright_found:
            content = self._update_existing_copyright(content, copyright_found)
        else:
            content = self._add_new_copyright(content)

        return content

    def _update_existing_copyright(self, content: str, copyright_found: re.Match) -> str:
        start_year: str = copyright_found.group(1)
        end_year: str = copyright_found.group(2) or start_year

        if int(end_year) < self.current_year:
            new_copyright: str = f"Copyright (C) {start_year}-{self.current_year} Zemtu OG"
            content = content.replace(copyright_found.group(0), new_copyright)

        copyright_end: int = content.find('"""', copyright_found.end())
        if copyright_end != -1 and content[copyright_end + 3 : copyright_end + 5] != "\n\n":
            content = content[: copyright_end + 3] + "\n" + content[copyright_end + 3 :]

        return content

    def _add_new_copyright(self, content: str) -> str:
        copyright_message = self.COPYRIGHT_MESSAGE.format(current_year=self.current_year)
        separator: str = "\n" if not content.startswith("\n") else ""
        return copyright_message + separator + "\n" + content


if __name__ == "__main__":
    updater = ZemtuCopyrightUpdater(filename=sys.argv[1])
    updater.update_copyright()
