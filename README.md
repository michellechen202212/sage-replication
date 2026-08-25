# Code Generation Is Not Model Generation

## Semantic Contracts for Reliable AI-Assisted Data Engineering

This repository is an anonymized replication package for **SAGE — Semantic Assurance for Generated Engineering**. The study asks whether AI-generated data-engineering implementations that pass their generated tests also preserve the meaning, identity, grain, lineage, and aggregation behavior of the underlying data model—and whether providing an explicit semantic contract improves that preservation.

## Experimental design

The study compares two conditions:

- **Implementation-first:** the model receives the implementation task, schema, fixtures, and test requirements without an explicit domain contract.
- **Semantic-first:** the model receives the same kind of implementation materials plus an explicit semantic contract before implementation.

The benchmark is fully synthetic. Its deliberately difficult cases include duplicate human-readable references, repeated SKUs, split fulfillments, multiple authorization and capture events, refunds, repeated tender types, independent receipt-item and tender grains, and absent relationships that must not be invented. No production data are used.

Semantic integrity is evaluated with 20 invariants (T01–T20) in [`review/SCORING_RUBRIC.md`](review/SCORING_RUBRIC.md). The **Semantic Integrity Preservation Rate (SIPR)** is:

```text
SIPR = semantic invariants passed / 20
```

## Hard-benchmark results

| Condition | Run | Generated tests | Semantic invariants | SIPR |
|---|---|---:|---:|---:|
| Implementation-first | run_01 | 4/4 passed | 18/20 | 90% |
| Implementation-first | run_02 | 4/4 passed | 18/20 | 90% |
| Semantic-first | run_01 | 5/5 passed | 20/20 | 100% |
| Semantic-first | run_02 | 5/5 passed | 20/20 | 100% |

Both implementation-first runs failed the same invariants:

- **T10:** any exposed net metric must equal 90.00 and be explicitly typed as gross posted captures minus posted refunds, with currency and grouping semantics.
- **T19:** derived amounts must retain reproducible source identity and aggregation lineage, including the operation, grouping, source selection, and currency rule.

Passing generated tests therefore did not guarantee full semantic preservation in these runs. These results are exploratory observations from a small synthetic benchmark, not population-level effect estimates, and no claim of statistical significance is made.

## Repository structure

- [`benchmark/`](benchmark/) — shared synthetic schema, seed data, domain contract, and test requirements.
- [`generation/implementation_first/`](generation/implementation_first/) — two frozen implementation-first runs.
- [`generation/semantic_first/`](generation/semantic_first/) — two frozen semantic-first runs.
- [`review/`](review/) — blind-review instructions, reviewer contract, and the 20-invariant scoring rubric.
- [`results/`](results/) — machine-readable summary and four frozen blind-review score sheets.
- [`scripts/validate.py`](scripts/validate.py) — package validation utility retained with the replication materials.

Validate the package structure, synthetic fixtures, rubric IDs, contract placement, score sheets, and summary agreement from the repository root:

```bash
python scripts/validate.py
```

## Run the generated tests

Python 3 is required. From the repository root, run each frozen implementation’s tests in its own directory:

```bash
cd generation/implementation_first/run_01
python -m unittest -v

cd ../run_02
python -m unittest -v

cd ../../semantic_first/run_01
python -m unittest discover -s tests -v

cd ../run_02
python -m unittest -v
```

The commands intentionally run the tests shipped with each generated implementation. Semantic validation is a separate review step: follow [`review/REVIEW_INSTRUCTIONS.md`](review/REVIEW_INSTRUCTIONS.md), apply all T01–T20 criteria in [`review/SCORING_RUBRIC.md`](review/SCORING_RUBRIC.md), and record `SIPR = passes / 20`.

## Inspect and reproduce the frozen implementations

Each directory under [`generation/`](generation/) contains its archived prompt, schema, seed fixture, test requirements, implementation source, generated tests, and run-specific usage documentation. To inspect a run, enter its directory and read `README.md`; execute its documented service or command-line entry point there so relative schema and fixture paths resolve correctly. To reproduce a condition, use that run’s `PROMPT.md`, `schema.sql`, `seed.sql`, and `TEST_REQUIREMENTS.md`; for semantic-first runs, also use the archived `DOMAIN_CONTRACT.md`. Keep regenerated outputs separate from these frozen directories so the archived evidence remains unchanged.

## Privacy and scope

This public package contains no proprietary source code, production data, employer-specific schemas, internal identifiers, screenshots, tickets, or organizational information. It also contains no identifying external project context.
