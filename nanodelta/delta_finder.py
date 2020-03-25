import os
from .delta_file import DeltaFile

class DeltaFinder:
    path: str = None

    def __init__(self, path):
        self.path = path

    async def find_newer(self, latest: int) -> dict: 
        deltas = await self.find_deltas()
        to_be_executed = {}

        for key in sorted(deltas.keys()):
            delta_number = deltas[key].get_delta_number()
            if (delta_number > latest):
                to_be_executed[delta_number] = deltas[key]
        
        return to_be_executed

    async def find_deltas(self):
        deltas = {}
        for file in os.listdir(self.path):
            delta = DeltaFile(file, self.path)

            deltas[delta.get_delta_number()] = delta

        return deltas
