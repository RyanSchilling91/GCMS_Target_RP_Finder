# PROJECT_BRIEF

## Purpose of this document
Define the business purpose, users, scope boundaries, operating constraints, and success conditions for the app.

---

## Guided fill status
- Status: Complete
- Last reviewed by: Project owner + AI
- Source of truth: `BOOTSTRAP_QUESTIONNAIRE_APP.md`

---

## Problem being solved

Lab analysts are required to locate and record compound U-Delete / U-Del / UDEL codes from instrument output files spread across thousands of sample folders per batch run. There is no automated tooling for this today. The analyst must manually navigate a `.b` batch folder, open each `.d` sample subfolder, find the `target.rp` instrument file inside it, and transcribe the relevant compound code data into a spreadsheet by hand.

A single batch can contain hundreds of `.d` sample folders. Each folder contains multiple compounds. The manual process is:
- **Slow** — opening hundreds to thousands of files takes hours per batch
- **Error-prone** — hand transcription introduces missed entries and code mismatches
- **Inconsistent** — no standard format for the resulting lists
- **Not queryable** — each manual export is a one-off artifact with no persistent database behind it

This tool solves that problem by automating the entire scan and extraction process, persisting the results to a structured database, and making the data available for selective, repeatable export — so the analyst never has to open files by hand again.

---

## Intended users and roles

| Role | What they do | Permissions / boundaries | Success for this role |
|---|---|---|---|
| Lab analyst / operator | Runs scans, reviews parse summaries, confirms commits, triggers exports | Full app access — scan, review, confirm, export | Scans a batch in minutes instead of hours; exports a clean, accurate Excel/CSV file |
| Manager / stakeholder | Consumes exported Excel or CSV files | No app access — export consumers only | Receives a reliable, consistently formatted compound report without requesting manual effort |

---

## Objective / version purpose

Version 1 must deliver:
1. A folder scan engine that walks a `.b` → `.d` → `target.rp` hierarchy and extracts compound number, compound name, and U-Del comment field (variants: `U-Delete`, `U-Del`, `UDEL`) from each sample
2. A pre-commit summary/preview screen that flags any missing `target.rp` folders or parse failures before data is written to the database
3. Persistent storage of all parsed data in Trinity (SQLite backend) organized by batch, sample, and compound
4. Versioned re-scan behavior — re-scanning an existing batch creates a new version without overwriting prior data
5. Batch-filterable export to `.xlsx` and `.csv`, plus a full-DB export option

---

## Non-goals (out of scope for v1)

- User authentication or login system — app is open to all local users
- Support for any file format other than `target.rp`
- Manual editing of parsed compound data after commit
- External integrations (LIMS, cloud storage, network sync services)
- Audit trail for export actions — exports are ephemeral
- Compound data correction UI — re-scan is the correction mechanism

---

## Operational constraints

- **Deployment:** Local desktop or server application — no cloud dependency
- **File access:** Must support both local file paths and network paths (UNC / mapped drives)
- **Backend:** Trinity SQLite + FastAPI — imported as a Python library, not called over HTTP
- **Concurrency:** Light — a few users may scan different `.b` folders simultaneously; simultaneous writes to SQLite require write-lock or queue strategy
- **No internet required:** Fully self-contained; no external API calls at runtime
- **No auth:** No login, no role enforcement at the application layer in v1
- **Data size:** Small-to-medium — a few hundred `.d` folders per batch; no performance scaling concern in v1

---

## Success criteria

| Criterion | How measured / observed | Required for v1? |
|---|---|---|
| All .d samples and compounds from a known .b folder appear correctly in Trinity DB after scan | Manual DB inspection against known folder contents | Yes |
| U-Delete / U-Del / UDEL code variants captured with zero false positives or misses | Compare app output to manually-identified codes from same folder | Yes |
| Missing target.rp folders flagged in summary before commit | Test with a batch that has one .d folder missing its target.rp | Yes |
| Re-scan creates new version without overwriting prior data | Re-scan same .b twice; verify both versions exist in history | Yes |
| Export batch filter produces correct scoped output | Export single batch; verify only that batch's data appears in file | Yes |
| Excel/CSV output matches a manually-built reference sheet | Side-by-side comparison with analyst-constructed reference | Yes |
| Lab user runs app against real batch data and confirms output | User acceptance test with production-representative data | Yes |

---

## Domain shape / system direction

Core real-world objects:
- **Batch** (`.b` folder) — the top-level run unit
- **Sample** (`.d` folder) — one instrument acquisition within a batch
- **Compound** — a chemical entity identified within a sample, with an associated U-Del code
- **Scan version** — a timestamped snapshot of a batch scan; multiple versions can exist for the same batch

Likely future expansion (not in v1):
- Additional compound code types beyond U-Del variants
- Support for additional instrument file formats
- Reporting dashboards or batch comparison views
- Role-based access if the user base grows

---

## Notes for the agent
- Trinity is the persistence layer — it is imported as a library, not deployed as a separate service.
- Do not model the export as a persistent artifact. It is generated on demand and discarded.
- The scan engine and the UI are separate concerns. Business logic (parsing, versioning, validation) must not live in UI files.
- Re-scan behavior must create a new version — never silently overwrite.
- Treat missing `target.rp` as a flaggable condition, not a hard stop.