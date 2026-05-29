# Trinity

Trinity is a **reusable, plug-and-play Python backend package** providing
governed workflow lifecycle management, run persistence, lock control, review
and audit services, and immutable evidence packaging.

Trinity is not an application. It is a pure Python service/domain/persistence
library. It has no routes, no UI, and no entry point of its own. Any host
application that needs governed run lifecycle management imports and calls Trinity.

---

## What Trinity provides

- Run lifecycle management (create, open, lock, transition, publish, reopen)
- Working revision persistence with version-aware save/resume and rehydration
- Planned sample set, raw upload, exclusion, and match domain services
- Review claim, approval, rework, and audit event services
- Immutable evidence package assembly and publish validation
- Lock management, stale-lock recovery, and admin override services
- Criteria configuration access and provenance tracking

## What Trinity does not provide

- HTTP routes or API endpoints
- HTML rendering or any frontend
- Session management or authentication token handling
- Any awareness of the web framework used by its callers
- An application entry point or launcher

The host repository owns all of that. Trinity is a dependency of that
application, not an application itself.

---

## How Trinity is used

A host repo imports Trinity as a Python package and calls its service functions
from route handlers or service scripts. All caller context — actor identity,
action reason, workstation ID — is passed explicitly into Trinity's service API.
Trinity never infers caller identity from environment or session state.

Example mental model:

```
host_repo/
├── app/
│   ├── routes/        ← FastAPI route handlers — call Trinity services
│   ├── scripts/       ← service scripts — call Trinity services
│   └── ...
└── trinity/           ← this package
    ├── services/      ← workflow, lock, review, publish service modules
    ├── persistence/   ← file-backed storage, rehydration, schema versioning
    ├── domain/        ← run, revision, sample set, audit domain models
    └── docs/          ← this documentation set
```

---

## Core package rules

1. Trinity modules never import a web framework (FastAPI, Flask, Streamlit, etc.).
2. Trinity modules never read from HTTP request state or session objects.
3. All caller context is passed as explicit function parameters.
4. Trinity service functions return plain Python objects — not HTTP responses.
5. Every Trinity module is importable and testable with plain `pytest` and no
   running server.

Any violation of these rules is a boundary defect that must be fixed before merge.

---

## Workflow Trinity governs

1. Create or open a run
2. Complete the planned sample set
3. Save working truth
4. Upload instrument/raw data
5. Save governed exclusions or row-drop decisions
6. Rebuild and audit downstream matches/calculations
7. Continue draft work or submit for review
8. Independent reviewer claims and reviews the run
9. Approved runs are published into an immutable evidence package
10. Published evidence can re-enter workflow only through a new working revision —
    never by editing the published artifact in place

---

## Documentation

Start at `docs/INDEX.md`. Read before changing anything.

The docs govern the package contract. If code and docs disagree, surface the
conflict before writing more code.
