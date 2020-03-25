import os
import re
import aiofiles

class DeltaFile:
    delta_number: int
    filename: str
    path: str

    def __init__(self, filename: str, path: str):
        self.delta_number = self._find_delta_number(filename)
        self.filename = filename
        self.path = path

    def get_delta_number(self) -> int:
        return self.delta_number

    def get_name(self) -> str:
        return self.filename

    async def get_script(self):
        filename = os.path.join(self.path, self.filename)
        async with aiofiles.open(filename, 'r') as file_handle:
            return await file_handle.read()

    def _find_delta_number(self, filename: str) -> int:
        match = re.match(r'^(\d+)-.*$', filename)
        if not match:
            raise ValueError("Filenames must start with a numeric value")

        return int(match.group(1))

