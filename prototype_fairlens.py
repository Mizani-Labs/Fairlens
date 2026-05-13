#!/usr/bin/env python3
"""FairLens initial prototype.

Offline-first command line workflow:
1. Capture exclusion reports with pseudonymous reporter IDs.
2. Persist encrypted-like payloads (base64 envelope) to local queue.
3. Sync queued reports into an analyst store.
4. Generate a disparity summary by language cohort.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import time
import uuid
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List


DEFAULT_DB = Path("data/fairlens_store.json")


@dataclass
class Report:
    report_id: str
    pseudonymous_id: str
    locale: str
    exclusion_type: str
    impact_level: str
    narrative: str
    created_at: float
    synced: bool = False


class FairLensStore:
    def __init__(self, db_path: Path = DEFAULT_DB) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.state = self._load()

    def _load(self) -> Dict[str, List[dict]]:
        if self.db_path.exists():
            return json.loads(self.db_path.read_text())
        return {"queue": [], "synced": []}

    def _save(self) -> None:
        self.db_path.write_text(json.dumps(self.state, indent=2))

    @staticmethod
    def _encode_report(report: Report) -> str:
        raw = json.dumps(asdict(report)).encode("utf-8")
        return base64.b64encode(raw).decode("ascii")

    @staticmethod
    def _decode_report(encoded: str) -> Report:
        raw = base64.b64decode(encoded.encode("ascii")).decode("utf-8")
        return Report(**json.loads(raw))

    def capture(self, locale: str, exclusion_type: str, impact_level: str, narrative: str) -> Report:
        report = Report(
            report_id=str(uuid.uuid4()),
            pseudonymous_id=str(uuid.uuid4()),
            locale=locale,
            exclusion_type=exclusion_type,
            impact_level=impact_level,
            narrative=narrative,
            created_at=time.time(),
        )
        self.state["queue"].append(self._encode_report(report))
        self._save()
        return report

    def sync(self) -> int:
        synced_count = 0
        new_queue = []
        seen = {item["report_id"] for item in self.state["synced"]}

        for encoded in self.state["queue"]:
            report = self._decode_report(encoded)
            if report.report_id in seen:
                continue
            report.synced = True
            self.state["synced"].append(asdict(report))
            seen.add(report.report_id)
            synced_count += 1

        self.state["queue"] = new_queue
        self._save()
        return synced_count

    def summary(self) -> Dict[str, dict]:
        rows = self.state["synced"]
        by_locale: Dict[str, dict] = {}

        for row in rows:
            locale = row["locale"]
            impact = row["impact_level"]
            bucket = by_locale.setdefault(locale, {"total": 0, "high_impact": 0})
            bucket["total"] += 1
            if impact.lower() == "high":
                bucket["high_impact"] += 1

        for locale, values in by_locale.items():
            total = values["total"]
            values["high_impact_rate"] = round(values["high_impact"] / total, 3) if total else 0.0

        return by_locale


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="FairLens initial prototype CLI")
    parser.add_argument("--db", default=str(DEFAULT_DB), help="Path to local store")
    sub = parser.add_subparsers(dest="cmd", required=True)

    capture = sub.add_parser("capture", help="Capture exclusion report into offline queue")
    capture.add_argument("--locale", required=True, choices=["en", "ar", "fr", "pt", "sw"])
    capture.add_argument("--exclusion-type", required=True)
    capture.add_argument("--impact-level", required=True, choices=["low", "medium", "high"])
    capture.add_argument("--narrative", required=True)

    sub.add_parser("sync", help="Sync queued reports into analyst store")
    sub.add_parser("summary", help="Show disparity summary by locale")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    store = FairLensStore(Path(args.db))

    if args.cmd == "capture":
        report = store.capture(args.locale, args.exclusion_type, args.impact_level, args.narrative)
        print(json.dumps({"captured": report.report_id, "pseudonymous_id": report.pseudonymous_id}, indent=2))
        return 0

    if args.cmd == "sync":
        synced = store.sync()
        print(json.dumps({"synced_reports": synced}, indent=2))
        return 0

    if args.cmd == "summary":
        print(json.dumps(store.summary(), indent=2))
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
