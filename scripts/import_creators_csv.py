from __future__ import annotations

import argparse
import csv

from bootstrap import bootstrap

bootstrap()

from app.services.creator_discovery import import_creator_candidate


def import_csv(path: str) -> list:
    creators = []
    with open(path, newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            creators.append(import_creator_candidate(row))
    return creators


def main() -> None:
    parser = argparse.ArgumentParser(description="Import creator candidates from CSV.")
    parser.add_argument("csv_path")
    args = parser.parse_args()
    creators = import_csv(args.csv_path)
    print(f"Imported {len(creators)} creators into local JSON storage.")


if __name__ == "__main__":
    main()

