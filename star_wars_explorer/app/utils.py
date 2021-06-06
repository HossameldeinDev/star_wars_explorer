from datetime import datetime
from pathlib import Path

time_stamp = datetime.today().strftime("%Y-%m-%d")
data_path = Path(__file__).parent / ".." / "data"
