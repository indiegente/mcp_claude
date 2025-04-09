#!/usr/bin/env python3
import asyncio
from src.core import SetupOrchestrator
from src.utils import Logger

async def main():
    logger = Logger()
    try:
        orchestrator = SetupOrchestrator()
        await orchestrator.setup()
    except Exception as e:
        logger.error(f"Setup failed: {str(e)}")
        return 1
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code) 