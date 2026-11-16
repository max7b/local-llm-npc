from pathlib import Path

# Define BASEDIR for the Project
BASEDIR = Path(__file__).parents[2]

DATA_DIR = BASEDIR / "data"

PATH_STORED_CONVERSATIONS = f"{DATA_DIR}/conversations/"
