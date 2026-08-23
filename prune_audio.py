#!/usr/bin/env python3
"""Prune tracked brief audio outside the rolling 60-day live window."""

from __future__ import annotations

import argparse
from datetime import date, datetime, timedelta
from pathlib import Path
import re
import subprocess


RETENTION_DAYS = 60
AUDIO_PATTERN = re.compile(r"^audio/(\d{4}-\d{2}-\d{2})\.mp3$")


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Remove tracked brief audio older than the rolling 60-day window."
    )
    parser.add_argument(
        "--as-of",
        type=lambda value: datetime.strptime(value, "%Y-%m-%d").date(),
        default=date.today(),
        metavar="YYYY-MM-DD",
        help="reference date (default: today)",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="remove candidates from HEAD; without this flag the command is a dry run",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    script_dir = Path(__file__).resolve().parent
    repo = Path(git(script_dir, "rev-parse", "--show-toplevel").strip())
    cutoff = args.as_of - timedelta(days=RETENTION_DAYS)

    tracked = git(repo, "ls-tree", "-r", "--name-only", "HEAD", "--", "audio")
    candidates: list[str] = []
    for path in tracked.splitlines():
        match = AUDIO_PATTERN.fullmatch(path)
        if not match:
            continue
        brief_date = datetime.strptime(match.group(1), "%Y-%m-%d").date()
        if brief_date < cutoff:
            candidates.append(path)

    mode = "APPLY" if args.apply else "DRY-RUN"
    print(
        f"[{mode}] as-of={args.as_of.isoformat()} "
        f"retention={RETENTION_DAYS}d cutoff={cutoff.isoformat()}"
    )

    if not candidates:
        print("No tracked audio is outside the live window.")
        return

    for path in candidates:
        print(f"prune {path}")

    if not args.apply:
        print("Re-run with --apply after reviewing the list.")
        return

    for path in candidates:
        git(repo, "rm", "--cached", "--sparse", "--", path)
        local_file = repo / path
        if local_file.exists():
            local_file.unlink()

    print(f"Pruned {len(candidates)} tracked audio file(s).")


if __name__ == "__main__":
    main()
