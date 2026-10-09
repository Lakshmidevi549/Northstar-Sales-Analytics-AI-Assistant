"""Step 1: create/reload the demo SQLite database by running seed.py."""
import runpy
from pathlib import Path

project_folder = Path(__file__).resolve().parent
print("Creating the sample SQL database...")
runpy.run_path(str(project_folder / "seed.py"), run_name="__main__")
