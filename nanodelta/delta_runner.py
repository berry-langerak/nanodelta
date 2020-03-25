import aiosqlite

from .delta_file import DeltaFile
from .delta_log import DeltaLog

class DeltaRunner:
    log: DeltaLog
    connection: aiosqlite.Connection

    def __init__(self, connection: aiosqlite.Connection, delta_log: DeltaLog):
        self.connection = connection
        self.delta_log = delta_log

    async def run(self, delta: DeltaFile):
        script = await delta.get_script()
        delta_number = delta.get_delta_number()
        delta_name = delta.get_name()

        await self.connection.executescript(script)
        await self.delta_log.add_log(delta_number, delta_name)
