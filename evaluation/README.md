# Evaluation

The Document Intelligence API is evaluated using a small test suite
covering different document types and security scenarios.

## Test Categories

- Invoice document classification
- Entity extraction
- Financial value extraction
- Incomplete document handling
- Prompt injection resistance

## Metrics

| Metric | Result |
|---|---:|
| Document Type Accuracy | 100% |
| Entity Extraction Accuracy | 100% |
| Financial Value Accuracy | 100% |
| Prompt Injection Test | 100% |
| Overall | 100% |

## Evaluation Approach

Each test document contains expected values.

The system output is compared against the expected results.

The evaluation checks:

1. Correct document classification
2. Correct entity extraction
3. Correct financial value extraction
4. Resistance to prompt injection

The evaluation dataset is intentionally small and is intended
to demonstrate the evaluation workflow rather than provide a
statistically significant benchmark.