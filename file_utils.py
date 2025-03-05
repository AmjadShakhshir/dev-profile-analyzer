import orjson
from pathlib import Path

def read_json_file(file_path: Path) -> dict:
    """Loads a JSON file efficiently using orjson."""
    try:
        with open(file_path, "r") as f:
            return orjson.loads(f.read())
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return {}
