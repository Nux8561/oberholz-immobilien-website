"""Screenshots der lokalen Version (npm run dev muss laufen): python3 scripts/capture_local.py [viewport-namen…] [--full-only]"""
import asyncio, sys
from capture_common import capture
names = [a for a in sys.argv[1:] if not a.startswith('--')] or None
asyncio.run(capture("local", names, positions='--full-only' not in sys.argv))
