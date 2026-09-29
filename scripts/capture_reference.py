"""Capture reference screenshots from the public homepage."""
import runpy
import sys
from pathlib import Path

sys.argv = [sys.argv[0], "original"]
runpy.run_path(str(Path(__file__).with_name("capture_screenshots.py")), run_name="__main__")
