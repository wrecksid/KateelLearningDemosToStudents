# Backwards-compatible shim. The real validator has been moved to Utils/rmp_validator.py
# This script will execute the one in Utils/ to preserve existing usage patterns.
import runpy
import sys
from pathlib import Path

new_path = Path(__file__).resolve().parent / 'Utils' / 'rmp_validator.py'
if new_path.exists():
    runpy.run_path(str(new_path), run_name='__main__')
else:
    print("Moved: Please run 'uv run python Utils/rmp_validator.py <file.rmp>'")
    sys.exit(1)
