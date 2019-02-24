from core import Bam
import asyncio

"""RUN THIS FILE TO START THE BOT"""

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Bam.run())