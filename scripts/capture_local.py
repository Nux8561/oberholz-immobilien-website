"""Capture screenshots from the local reconstruction."""
import runpy
import sys
from pathlib import Path

sys.argv = [sys.argv[0], "local"]
runpy.run_path(str(Path(__file__).with_name("capture_screenshots.py")), run_name="__main__")
