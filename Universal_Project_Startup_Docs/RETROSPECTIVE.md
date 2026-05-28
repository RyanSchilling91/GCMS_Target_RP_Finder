# Retrospective

## Purpose
Capture what worked, what failed, and what should become standard practice after each meaningful phase or incident.

This is how the documentation kit evolves into a living methodology.

## When to update
Update after:
- phase completion
- major defect
- architecture correction
- production incident
- repeated friction pattern
- project closeout

## Entry template

### Retrospective title / phase
#### What worked
- 

#### What failed
- 

#### What to standardize
- 

#### What rule should be added or modified in AGENTS.md
- 

#### What should be generalized back into the universal docs kit
- 

---

## Seed lessons to preserve

### Documentation-first development reduced drift
#### What worked
Reading docs before touching code reduced AI hallucination, scope drift, and architecture mismatch.
#### What to standardize
`INDEX.md` is always the agent entrypoint.

### Workflow modeling prevented false simplicity
#### What worked
Forcing intake → edit → derive → review → freeze/archive timelines exposed hidden states early.
#### What to standardize
No feature implementation before workflow timeline exists.

### State classification prevented corrupted truth
#### What worked
Separating working, derived, and evidence state prevented stale calculations from becoming source truth.
#### What to standardize
No persistence design before state classification.

### Thin UI preserved portability
#### What worked
Keeping business rules outside UI files made apps easier to test, debug, and migrate.
#### What to standardize
UI is a renderer, not the system core.

### Architecture selection must stay project-specific
#### What failed
Prior successful stacks can become accidental defaults.
#### What to standardize
Compare plausible options before selecting UI, persistence, deployment, auth/session, and concurrency.

### Failure documentation is part of the fix
#### What worked
Capturing symptom, root cause, detection gap, and prevention rule made later debugging faster.
#### What to standardize
Bug fixes are incomplete until failure memory and regression coverage are addressed.
