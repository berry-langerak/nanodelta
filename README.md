# Nanodelta
Nanodelta is a simple package to asynchronously run deltas on an SQLite
database. It currently strongly depends on aiosqlite. 

## Installation

`pip install nanodelta`

## Use guide

### Creating a delta file

First, you create a delta file in pure SQL and store it into a directory of
your choice. Make sure the filename starts with digits followed by a dash, 
so that nanodelta can determine if something is or isn't newer.

Next, create a run file like the one below. Once you run this file, a deltas
table will be created if it isn't there already, and all deltas that aren't
executed will be executed.

```python
import sys
import logging
import asyncio

import nanodelta import DeltaFile, DeltaLog, DeltaRunner
import aiosqlite

async def run_deltas():
    try:
        db = await aiosqlite.connect('databasename.db')
        db.row_factory = aiosqlite.Row

        log = await DeltaLog.create(db)
        runner = DeltaRunner(db, log)
        finder = DeltaFinder("your/path/here")
        
        latest = await log.get_latest()
        deltas = await finder.find_newer(latest)

        if len(deltas) == 0:
            logging.info("No new deltas found")

        for delta in deltas.values():
            logging.info("Running delta " + delta.get_name())
            await runner.run(delta)

        await db.close()
    finally:
        await db.close()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

asyncio.run(run_deltas())
```