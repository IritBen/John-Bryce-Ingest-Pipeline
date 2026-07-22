"""Tasks 2 and 3 — get rows out of a file, and turn them into trips."""
from __future__ import annotations

from pathlib import Path
from typing import Iterator
from datetime import datetime
import json

from trip_ingest.errors import MissingField, BadTimestamp, NegativeDistance
from trip_ingest.model import RawRow ,Trip


def read_drop(path: Path) -> Iterator[RawRow]:
    """Yield one raw JSON object per line of a `.jsonl` drop.

    Task 2. A drop is a night's trips: it does not fit in memory, and on a bad night it does not fit
    on the machine. Nothing that reads it may hold more than one line at a time.
    """
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                yield json.loads(line)

def mandatory_field(raw: dict, field: str) -> any:
    value = raw.get(field)
    if value is None:
        raise MissingField(f"{field} as missing")
    return value

def check_timestamp(raw: dict, started_at: str) -> datetime:
    value = raw.get("started_at")
    if value is None or not isinstance(value, str) or value == "":
        raise BadTimestamp(f"{started_at} is not a datetime")
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        raise BadTimestamp(f"{started_at} is not a datetime")
    return value


def parse_row(raw: dict) -> Trip:
    trip_id = mandatory_field(raw, "trip_id")
    station_id = mandatory_field(raw, "station_id")
    distance_m = mandatory_field(raw, "distance_m")
    started_at = check_timestamp(raw, "started_at")
    if distance_m < 0:
        raise NegativeDistance(f"distance_m is not a positive distance: {distance_m}")
    return Trip(trip_id=str(trip_id), station_id=str(station_id), distance_m=int(distance_m), started_at=(started_at))
#pydentic - (reading and writing files)
#
