Bootstrap Questionnaire — AI-Guided Project Intake
Project: Batch File Scraper & U-Del Compound Database App (Trinity-Backed)

Guided Fill Status

Status: COMPLETE — All 7 Phases
Completed by: Project owner + AI guided intake
Trinity role: Plug-and-play SQLite/FastAPI backend (library/storage layer only)
This questionnaire covers the full application layer built on top of Trinity


PHASE 1 — Project Purpose
Target: PROJECT_BRIEF.md
Status: COMPLETE
What problem are we solving?
Lab analysts must manually open thousands of .d sample folders to locate and record compound U-Delete/U-Del/UDEL codes. This is slow, error-prone, and produces hand-built lists that are inconsistent and hard to audit. The app automates the entire scrape — scanning folder hierarchies, parsing target instrument files, and building a structured, queryable database — so that no user ever has to open files by hand again.
Who are the primary users?

Lab analysts / operators — use the app directly to run scans, review summaries, and trigger exports
Managers and other stakeholders — consume Excel/CSV exports only; never interact with the app directly

What do users do today without this tool?
They manually navigate folder hierarchies, open individual instrument files, and transcribe compound codes into spreadsheets by hand. With potentially thousands of .d folders per batch, this is prohibitively slow and introduces transcription errors.
What is painful, slow, risky, or inconsistent today?

Opening thousands of files manually
Building compound lists by hand with no consistency guarantee
No persistent database — each export is a one-off effort
No way to selectively query or filter historical batch data

What is out of scope for version 1?

User authentication / login system (app is open to all local users)
Any file format other than target.rp
External integrations (LIMS, cloud, network sync)
Compound data editing after import

What would prove this project worked?

A known .b folder is scanned and all .d samples and their compounds appear correctly in the Trinity DB
U-Delete / U-Del / UDEL codes are captured with zero false positives or misses
An Excel export matches a manually-built reference sheet


PHASE 2 — Workflow Reality
Target: WORKFLOW_TIMELINE.md
Status: COMPLETE
Step-by-step operational sequence:

User initiates a scan — user manually types or browses to a .b folder path (local or network)
App traverses the folder — scans for all upper-level .d subfolders within the .b
App locates target.rp — within each .d folder, app finds the target.rp folder
App parses target.rp — extracts compound number, compound name, and U-Del comment field (variants: U-Delete, U-Del, UDEL)
App flags parse issues — any .d folder missing a target.rp, or any file that fails to parse, is flagged in the summary; scanning continues on other folders
User reviews summary/preview — scan results are shown before any data is committed; user acknowledges any flags
User confirms commit — user confirms and data is persisted to Trinity (batch → sample → compound hierarchy)
Versioning on re-scan — if the .b batch already exists in the DB, a new versioned entry is created; old versions are preserved and hidden by default but accessible via history view
DB accumulates over time — user can scan different .b folders on separate occasions; all data accumulates in Trinity
User triggers export — at any time, user opens export panel, selects specific batches to include OR chooses full DB export, and generates .xlsx or .csv file
Export is ephemeral — exported file is a download-and-done action; not stored in the DB

Human vs. system actions:
StepActorBrowse/type folder pathHumanFolder traversal and .d discoverySystemtarget.rp location and parsingSystemFlag missing/failed foldersSystemReview summary and confirmHumanDB commit and versioningSystemSelect export range and trigger exportHumanGenerate .xlsx / .csvSystem

PHASE 3 — Data Model / Truth Layer
Target: DATA_MODEL.md
Status: COMPLETE
Core entities:
1. Batch

Identifier: .b folder name (e.g. Run001.b)
Fields: folder name, full folder path, scan timestamp, scan version number
Owner: system (created at scan time)
Notes: Multiple scan versions can exist per batch; each re-scan creates a new version

2. Sample

Identifier: .d folder name (e.g. 20192950103.d) — timestamp-structured, unique enough without parent batch, but stored with parent batch reference
Fields: folder name, parent batch reference, parse status (success / flagged)
Owner: system (created at scan time)

3. Compound

Identifier: compound number + compound name (shared across samples/batches)
Fields: compound number, compound name, U-Del comment field value (U-Delete / U-Del / UDEL)
Owner: system (extracted from target.rp)
Notes: Same compound appears across many samples and batches; compound records are shared, not owned by a single sample

4. Compound Instance (Sample ↔ Compound join)

Identifier: sample reference + compound reference
Fields: U-Del comment value for this specific instance
Owner: system

5. U-Del Detection Count (Derived)

Not stored as a raw field — computed at parse time from compound instance data
Represents: count of U-Del hits per compound per batch / per sample
Displayed in: summary view and batch overview; not persisted as canonical truth

6. Scan Version

Identifier: batch reference + version number + scan timestamp
Fields: batch reference, version number, scan timestamp, commit status
Owner: system
Behavior: Old versions hidden by default; accessible via history view

Forbidden states:

A compound instance with no parent sample
A sample with no parent batch
An in-place overwrite of a previously committed batch version


PHASE 4 — State Classification
Target: STATE_CLASSIFICATION.md
Status: COMPLETE
Working state (mutable before confirm)

Scan results in preview/summary — editable only in the sense that the user can cancel before commit
Pending scan job (in-flight parse operations)

Evidence state (immutable after confirm)

All committed batch, sample, and compound data in Trinity
Once the user confirms a scan, all parsed records are frozen — never edited by users
Re-scan is the only mechanism to update a batch's data (creates a new version, does not overwrite)

Derived state (computed, not stored as canonical truth)

U-Del detection count per batch / per compound
Export files (.xlsx / .csv) — ephemeral, generated on demand, never stored in DB

Versioning behavior:

Re-scanning a .b folder creates a new versioned entry
Old versions are retained and hidden by default
History view exposes old versions explicitly when requested
No silent overwrites — ever

Export behavior:

Ephemeral: generated on demand, no audit trail required in v1
User selects batch filter or full DB export before generation


PHASE 5 — Integration Points
Target: INTEGRATIONS.md
Status: COMPLETE
File system access

Must support both local paths and network paths (UNC paths, mapped drives)
App is deployed as a local desktop/server tool
No cloud file access in v1

Trinity integration

Interface: Trinity is imported as a Python library — direct SQLite access via Trinity's internal API
Transport: No HTTP/REST calls to Trinity; Trinity is a local storage and persistence layer
Frontend: FastAPI + HTML for the local UI
Role: Trinity provides the DB schema, persistence, and query interface; the app provides the scan engine and UI logic on top

Export

Formats: .xlsx and .csv both supported
Library: openpyxl (xlsx) + csv stdlib or pandas (csv)
Format standard: Formatted output — headers, readable column widths; matches what stakeholders expect to receive

External integrations

None in v1 — fully self-contained local system


PHASE 6 — Unknowns & Risks
Target: UNKNOWNS.md
Status: COMPLETE
Resolved / Low risk:
ItemStatusNotestarget.rp file format✅ KnownSample files available; structure confirmedScale per batch✅ LowFew hundred .d folders max; no performance concernTrinity interface✅ KnownSQLite + FastAPI; direct library integrationExport format✅ Decidedxlsx + csv both supported
Open / Flagged risks:
ItemRisk LevelNotesSQLite concurrent writes⚠️ MildMultiple users scanning simultaneously could cause write contention; need write-lock or scan queue strategy in Trinity integration layerNetwork path reliability⚠️ MinorUNC/mapped drive behavior on target OS needs a test pass; timeout and path error handling must be implemented

PHASE 7 — Verification Criteria
Target: VERIFICATION.md
Status: COMPLETE
Primary end-to-end verification test:

DB build test: Run a known .b folder through the app; verify all .d samples and their compounds appear correctly in Trinity DB
Code accuracy test: Confirm all U-Delete / U-Del / UDEL variants are captured with zero false positives or misses across the known test set
Export accuracy test: Generate Excel output and verify it matches a manually-built reference sheet

Must-pass edge cases before v1 is shippable:

 Missing target.rp folder in a .d is flagged in the summary UI (not silently skipped)
 Re-scan of an existing .b folder creates a new versioned entry without overwriting old data
 Export batch filter correctly limits output to only selected batches

Sign-off process:

Internal dev test — developer runs all primary tests and edge cases against real sample data
User acceptance — lab user runs the app against their actual batch folders and confirms output matches expectations before v1 is called done


Final Readiness Summary
This bootstrap is complete and ready to generate:

 PROJECT_BRIEF.md
 WORKFLOW_TIMELINE.md
 DATA_MODEL.md
 STATE_CLASSIFICATION.md
 INTEGRATIONS.md
 UNKNOWNS.md
 VERIFICATION.md

Do not begin coding until planning documents above are drafted and reviewed.