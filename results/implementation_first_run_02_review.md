# Blind review: implementation_first/run_02

| ID | Status | Concise evidence note |
|---|---|---|
| T01 | PASS | Order interfaces and projections retain `order_id`. |
| T02 | PASS | O1001 and O1002 remain separate despite duplicate `ORD-7788`. |
| T03 | PASS | L1 and L2 remain distinct same-SKU occurrences. |
| T04 | PASS | F2 and F3 remain separate under L2 without repeating line value as event value. |
| T05 | PASS | E1 and E2 authorization attempts remain visible. |
| T06 | PASS | AUTH is excluded from posted capture/refund facts. |
| T07 | PASS | E3 and E4 remain separate capture events. |
| T08 | PASS | Posted captures reconcile to 120.00. |
| T09 | PASS | E5 remains a distinct posted 30.00 refund. |
| T10 | FAIL | Exposed net metric lacked the rubric-required explicit semantic definition/grouping rule. |
| T11 | PASS | I1, I2, and I3 remain distinct item occurrences. |
| T12 | PASS | T1, T2, and T3 remain distinct tender legs. |
| T13 | PASS | Repeated VISA legs T1 and T2 remain distinct. |
| T14 | PASS | Item and tender collections remain separate; no cross-product is exposed. |
| T15 | PASS | Receipt total remains on the receipt parent. |
| T16 | PASS | Business-event timestamps remain distinct from persistence timestamps. |
| T17 | PASS | Projection records declare source record type and identity. |
| T18 | PASS | Monetary values remain contextualized by their source fact. |
| T19 | FAIL | Derived totals lacked explicit source and aggregation lineage; currency handling was unsafe/hardcoded. |
| T20 | PASS | No unsupported allocation or causal relationship is asserted. |

## Totals

- Passes: 18
- Failures: 2
- Undetermined: 0
- SIPR: 0.90 (90%)
- Defect classes: explicit semantic definition/grouping; aggregation/source lineage and currency handling.
- Review notes: Frozen blind-review outcome; failure pattern preserved exactly. Evidence notes do not claim more than the recorded review outcome.
- Generated test result: 4/4 passed.
