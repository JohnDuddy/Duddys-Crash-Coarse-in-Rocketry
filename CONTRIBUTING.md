# Contributing

Contributions are welcome when they improve technical correctness, evidence quality, pedagogy, accessibility, reproducibility, or maintainability.

## Technical Content Standard

Every technical change should identify:

1. The claim being added or changed.
2. The system boundary, frame, units, assumptions, and validity limits.
3. At least one authoritative primary source.
4. Verification evidence, including limiting cases or independent calculations.
5. Validation evidence when the model is used to represent physical behavior.
6. Uncertainty or model-form limitations that affect interpretation.
7. Safety or misuse implications.

## Code Changes

1. Create a focused branch.
2. Keep interactive laboratories explicitly labeled as screening models.
3. Add or update automated tests.
4. Run `python -m unittest discover -s tests -v`.
5. Describe technical risk and unresolved limitations in the pull request.

Do not add NASA marks, imply agency endorsement, or present this application as flight-certified software.
