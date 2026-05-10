"""
Smoke test -- verify both scripts parse without runtime errors and that the
overall structure is sound. Does not actually pull data (that requires
network and FRED key); only imports the modules to confirm syntax.
"""

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def _check(name: str, path: Path) -> None:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Could not load {path}")
    mod = importlib.util.module_from_spec(spec)
    # We don't execute main() -- only ensure the module compiles.
    code = path.read_text()
    compile(code, str(path), "exec")
    print(f"  OK  {name} ({path.name}, {len(code)} bytes)")


print("Smoke test: parsing pipeline modules...")
_check("data_pipeline", ROOT / "data_pipeline.py")
_check("analysis", ROOT / "analysis.py")
print("All modules compile cleanly.")
