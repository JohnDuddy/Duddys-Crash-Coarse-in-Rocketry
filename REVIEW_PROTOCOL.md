# Independent Technical Review Protocol

## Purpose

This protocol enables a qualified aerospace specialist to evaluate the exact public build of **Duddy's Crash Coarse in Rocketry** without implying prior endorsement.

## Reviewer Record

Record:

- Reviewer name and relevant technical specialties
- Date
- Git commit SHA or release tag
- Operating system, browser, and Python version
- Modules and laboratories sampled in depth

## Required Review Threads

1. Technical correctness: equations, units, signs, frames, and assumptions.
2. Depth: graduate derivation, research methods, uncertainty, and open questions.
3. Model discipline: fidelity, convergence, validity, and model-form discrepancy.
4. Source traceability: authoritative support and correct interpretation.
5. Simulation integrity: conservation, limits, and response to parameter changes.
6. Pedagogy: conceptual progression without hiding mathematical difficulty.
7. Safety: non-operational framing and correct regulatory context.
8. Reproducibility: installation, tests, configuration, and rerun capability.
9. Original contribution: value beyond a curated reading list.
10. Funding readiness: technical risk, evidence gaps, roadmap, and maintainability.

## Severity

- **Blocker**: Materially wrong or unsafe; invalidates funding or public technical claims.
- **High**: Likely to mislead a serious learner or expert reviewer.
- **Medium**: Important incompleteness, ambiguity, or weak evidence.
- **Low**: Local clarity, usability, or maintainability issue.

## Completion

A review is complete only when findings cite the exact module, seminar, equation, simulation behavior, source, or code path. Export the JSON record from `/review`, then preserve it with the reviewed commit or release.
