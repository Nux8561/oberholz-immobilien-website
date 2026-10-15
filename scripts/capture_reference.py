"""Referenz-Screenshots des Originals: python3 scripts/capture_reference.py [viewport-namen…] [--full-only]"""
import asyncio, sys
from capture_common import capture
names = [a for a in sys.argv[1:] if not a.startswith('--')] or None
asyncio.run(capture("original", names, positions='--full-only' not in sys.argv))
