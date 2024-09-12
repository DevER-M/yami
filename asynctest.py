import sys
from spotdl import Spotdl
import asyncio

spotdl = Spotdl("5f573c9620494bae87890c0f08a60293", "212476d9b0f3472eaa762d90b19b0ba8")

async def spotdl_download(q):
    result = spotdl.search([q])[0]
    try:
        await asyncio.create_task(spotdl.download(result))
    except Exception as e:
        print(f"Error: {e}")
    sys.stdout.flush()

async def main():
        q = input("search song: ")
        task = asyncio.create_task(spotdl_download(q))
        await task
        

asyncio.run(main())