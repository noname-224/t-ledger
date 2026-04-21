import asyncio
import logging
import sys

from t_ledger.containers import Container
from t_ledger.presentation.telegram.bootstrap import run_bot


async def main() -> None:
    container = Container()
    container.wire(packages=["t_ledger.presentation.telegram.handlers"])

    await run_bot()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
