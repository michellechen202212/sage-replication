"""Validate the frozen benchmark and public replication-package structure."""
from __future__ import annotations

import csv
import re
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = {
    "implementation_first/run_01": ROOT / "generation/implementation_first/run_01",
    "implementation_first/run_02": ROOT / "generation/implementation_first/run_02",
    "semantic_first/run_01": ROOT / "generation/semantic_first/run_01",
    "semantic_first/run_02": ROOT / "generation/semantic_first/run_02",
}
REVIEWS = {
    "implementation_first/run_01": ROOT / "results/implementation_first_run_01_review.md",
    "implementation_first/run_02": ROOT / "results/implementation_first_run_02_review.md",
    "semantic_first/run_01": ROOT / "results/semantic_first_run_01_review.md",
    "semantic_first/run_02": ROOT / "results/semantic_first_run_02_review.md",
}


def scalar(db: sqlite3.Connection, sql: str) -> int:
    return db.execute(sql).fetchone()[0]


def validate_fixture(schema: Path, seed: Path) -> None:
    db = sqlite3.connect(":memory:")
    db.executescript(schema.read_text(encoding="utf-8"))
    db.executescript(seed.read_text(encoding="utf-8"))
    checks = {
        "duplicate order_number": ("SELECT COUNT(*) FROM commerce_order WHERE order_number='ORD-7788'", 2),
        "distinct order_id": ("SELECT COUNT(DISTINCT order_id) FROM commerce_order WHERE order_number='ORD-7788'", 2),
        "same-SKU lines": ("SELECT COUNT(*) FROM order_line WHERE order_id='O1001' AND sku='SKU-A'", 2),
        "L2 fulfillments": ("SELECT COUNT(*) FROM fulfillment_event WHERE order_line_id='L2'", 2),
        "P1 events": ("SELECT COUNT(*) FROM payment_event WHERE payment_id='P1'", 5),
        "AUTH cents": ("SELECT SUM(amount_cents) FROM payment_event WHERE payment_id='P1' AND event_type='AUTH'", 24000),
        "CAPTURE cents": ("SELECT SUM(amount_cents) FROM payment_event WHERE payment_id='P1' AND event_type='CAPTURE'", 12000),
        "REFUND cents": ("SELECT SUM(amount_cents) FROM payment_event WHERE payment_id='P1' AND event_type='REFUND'", 3000),
        "R1 items": ("SELECT COUNT(*) FROM receipt_item_occurrence WHERE receipt_id='R1'", 3),
        "R1 tenders": ("SELECT COUNT(*) FROM tender_leg WHERE receipt_id='R1'", 3),
        "repeated SKU": ("SELECT COUNT(*) FROM receipt_item_occurrence WHERE receipt_id='R1' AND sku='SKU-A'", 2),
        "repeated VISA": ("SELECT COUNT(*) FROM tender_leg WHERE receipt_id='R1' AND tender_type='VISA'", 2),
    }
    for label, (sql, expected) in checks.items():
        assert scalar(db, sql) == expected, label
    tables = {row[0] for row in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert not any("return" in table.lower() and "refund" in table.lower() for table in tables)
    db.close()


def review_scores(path: Path) -> tuple[int, list[str]]:
    text = path.read_text(encoding="utf-8")
    rows = re.findall(r"^\| (T\d{2}) \| (PASS|FAIL|UNDETERMINED) \|", text, re.MULTILINE)
    assert [item[0] for item in rows] == [f"T{i:02d}" for i in range(1, 21)], f"bad IDs in {path.name}"
    assert not any(status == "UNDETERMINED" for _, status in rows), f"undetermined status in {path.name}"
    return sum(status == "PASS" for _, status in rows), [item for item, status in rows if status == "FAIL"]


def main() -> None:
    required = [ROOT / name for name in ("README.md", "LICENSE", ".gitignore")]
    required += [ROOT / "benchmark" / name for name in ("DOMAIN_CONTRACT.md", "TEST_REQUIREMENTS.md", "schema.sql", "seed.sql")]
    required += [ROOT / "review" / name for name in ("DOMAIN_CONTRACT_REVIEWER.md", "REVIEW_INSTRUCTIONS.md", "SCORING_RUBRIC.md")]
    required += list(RUNS.values()) + list(REVIEWS.values()) + [ROOT / "results/summary.csv"]
    assert all(path.exists() for path in required), "required package path missing"
    validate_fixture(ROOT / "benchmark/schema.sql", ROOT / "benchmark/seed.sql")
    for run in RUNS.values():
        validate_fixture(run / "schema.sql", run / "seed.sql")
    rubric = (ROOT / "review/SCORING_RUBRIC.md").read_text(encoding="utf-8")
    assert re.findall(r"^\| (T\d{2}) \|", rubric, re.MULTILINE) == [f"T{i:02d}" for i in range(1, 21)]
    assert all(not (run / "DOMAIN_CONTRACT.md").exists() for label, run in RUNS.items() if label.startswith("implementation"))
    assert all((run / "DOMAIN_CONTRACT.md").exists() for label, run in RUNS.items() if label.startswith("semantic"))
    observed = {}
    for label, path in REVIEWS.items():
        passed, failed_ids = review_scores(path)
        expected = ["T10", "T19"] if label.startswith("implementation") else []
        assert failed_ids == expected, f"unexpected failures in {path.name}"
        observed[label] = (passed, failed_ids)
    with (ROOT / "results/summary.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 4
    for row in rows:
        label = f"{row['condition'].replace('-', '_')}/{row['run']}"
        passed, failed_ids = observed[label]
        assert int(row["semantic_invariants_passed"]) == passed
        assert row["failed_invariants"] == ";".join(failed_ids)
        assert float(row["sipr"]) == passed / 20
    print("PASS: structure, fixtures, rubric, contracts, score sheets, and summary")


if __name__ == "__main__":
    main()
