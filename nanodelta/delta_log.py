import aiofiles
import aiosqlite

class DeltaLog:
    connection: aiosqlite.Connection = None

    _install_script: str = """
    REATE TABLE delta (
        delta_number TEXT PRIMARY KEY,
        delta_name TEXT NOT NULL,
        executed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );"""

    @classmethod
    async def create(cls, connection: aiosqlite.Connection):
        self = DeltaLog()
        self.connection  = connection

        if (not await self.is_installed()):
            await self.install()
        
        return self

    async def install(self):
        await self.connection.executescript(self._install_script)

        return True

    async def is_installed(self) -> bool:
        query = "SELECT COUNT(1) AS installed FROM sqlite_master WHERE name='delta' AND type='table'"
        cursor = await self.connection.execute(query)
        row = await cursor.fetchone()

        return row['installed'] > 0

    async def get_latest(self) -> int:
        cursor = await self.connection.execute('SELECT MAX(delta_number) as max_delta FROM delta')
        (delta_number, ) = await cursor.fetchone()

        if delta_number is None:
            return 0
        
        return int(delta_number)

    async def add_log(self, delta_number: int, delta_name: str):
        parameters = {'number': delta_number, 'name': delta_name}
        query = 'INSERT INTO delta (delta_number, delta_name) VALUES (:number, :name)'

        await self.connection.execute(query, parameters)
        await self.connection.commit()