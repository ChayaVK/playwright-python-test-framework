"""Reads test data files from the data folder."""
import csv
import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"


def read_json(file_name: str):
    with open(DATA / file_name, encoding="utf-8") as f:
        return json.load(f)


def read_csv(file_name: str) -> list[dict[str, str]]:
    """Each row becomes a dict keyed by the header row. Quoted values with commas work too."""
    with open(DATA / file_name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))
