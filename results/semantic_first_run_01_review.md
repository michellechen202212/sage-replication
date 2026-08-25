# Blind review: semantic_first/run_01

RUBRIC FILES VERIFIED

| ID | Status | Concise evidence note |
|---|---|---|
| T01 | PASS | Order interfaces retain `order_id` identity. |
| T02 | PASS | Both duplicate-reference orders remain independently addressable. |
| T03 | PASS | L1 and L2 retain separate identities and values. |
| T04 | PASS | Split fulfillment facts remain distinct without duplicating line value. |
| T05 | PASS | Both authorization attempts remain visible with event identity. |
| T06 | PASS | AUTH is excluded from paid/captured economic totals. |
| T07 | PASS | Both capture events remain separately traceable. |
| T08 | PASS | Gross posted capture reconciles to 120.00. |
| T09 | PASS | E5 remains a distinct posted 30.00 refund. |
| T10 | PASS | No incorrectly typed net metric is exposed; payment facts state their grouping semantics. |
| T11 | PASS | All three receipt-item occurrences remain traceable. |
| T12 | PASS | All three tender-leg occurrences remain traceable. |
| T13 | PASS | Repeated VISA legs retain separate source IDs. |
| T14 | PASS | Items and tenders remain separate bounded collections. |
| T15 | PASS | Receipt total remains non-additive at receipt grain. |
| T16 | PASS | Timeline uses the corresponding business-event timestamps. |
| T17 | PASS | Compact output declares one source fact occurrence per row. |
| T18 | PASS | Amounts are contextualized by fact type and currency. |
| T19 | PASS | Derived totals state source selection, grouping, operation, and currency. |
| T20 | PASS | No absent allocation or causal relationship is invented. |

## Totals

- Passes: 20
- Failures: 0
- Undetermined: 0
- SIPR: 1.00 (100%)
- Defect classes: none.
- Review notes: Corrected canonical blind review beginning `RUBRIC FILES VERIFIED`; the earlier invalid missing-materials review is not included.
- Generated test result: 5/5 passed.
