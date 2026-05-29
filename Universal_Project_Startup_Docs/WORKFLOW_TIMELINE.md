# WORKFLOW_TIMELINE

## Purpose of this document
Describe the real workflow chronologically from folder selection through export, including human actions, system actions, review points, persistence points, and edge cases.

---

## Guided fill status
- Status: Complete
- Last reviewed by: Project owner + AI
- Source of truth: `BOOTSTRAP_QUESTIONNAIRE_APP.md`

---

## Workflow summary

The workflow begins when a user selects a `.b` batch folder. The system traverses the folder hierarchy, parses `target.rp` files within each `.d` sample folder, surfaces a summary of results and any issues, and waits for the user to confirm before committing anything to Trinity. Once confirmed, the data is persisted as a versioned batch entry. The user can repeat this process for additional batches over time, building up a queryable database. At any point, the user can export a filtered or full-DB extract to Excel or CSV.

---

## Timeline

| Step | Actor | Action | Data touched | System response | State impact | Notes |
|---:|---|---|---|---|---|---|
| 1 | Human | Browse or type a `.b` folder path | Folder path input | App accepts path, validates it exists and is a `.b` folder | — | Supports local paths and UNC/network paths |
| 2 | System | Traverse `.b` folder to find all `.d` subfolders | File system | Builds list of `.d` folders found at the top level of `.b` | Working — scan job begins | Skips non-`.d` entries silently |
| 3 | System | For each `.d` folder, locate `target.rp` subfolder | File system | Records found/missing status per `.d` | Working — per-sample status tracked | Missing `target.rp` is flagged, not a hard stop |
| 4 | System | Parse each `target.rp` found | target.rp file contents | Extracts compound number, compound name, U-Del comment field for each compound | Working — parsed compound records held in memory | U-Del variants: `U-Delete`, `U-Del`, `UDEL` |
| 5 | System | Compute U-Del detection counts | Parsed compound records | Counts U-Del hits per compound across samples in this batch | Derived — computed, not yet persisted | This is a derived summary value |
| 6 | System | Build scan summary / preview | All parse results + flags | Displays: samples found, compounds extracted, U-Del count summary, list of any flagged `.d` folders (missing `target.rp` or parse error) | Working — summary displayed, nothing committed yet | User can see everything before confirming |
| 7 | Human | Review summary; acknowledge any flags | Summary display | — | — | User can cancel here with no DB impact |
| 8 | Human | Confirm commit | User action | App proceeds to persist data to Trinity | — | If user cancels, nothing is written |
| 9 | System | Check if this `.b` already exists in Trinity DB | Trinity DB | If exists: create new versioned entry. If new: create first version entry. | Evidence — new version committed | Never overwrites existing version |
| 10 | System | Persist batch, samples, and compounds to Trinity | Parsed data | Writes batch record, all sample records, all compound instance records to SQLite via Trinity | Evidence — frozen after commit | Data is immutable after this point |
| 11 | Human | (Later) Open export panel | — | App shows batch list with checkboxes and full-DB export option | — | Can happen at any time after at least one committed batch exists |
| 12 | Human | Select batch filter or choose full-DB export | Batch selection | — | — | User controls scope of export |
| 13 | System | Generate `.xlsx` and/or `.csv` | Trinity DB query | Queries selected batches, formats output, writes export file | Derived — ephemeral export artifact | Not stored in DB; download and done |

---

## Review and approval points

| Point | Reviewer / actor | What is reviewed | What can still change | What freezes after approval |
|---|---|---|---|---|
| Pre-commit summary (Step 6–7) | Lab analyst / operator | Sample count, compound count, U-Del detection summary, flagged .d folders | User can cancel — nothing is committed | N/A (cancel = no change) |
| Commit confirmation (Step 8) | Lab analyst / operator | Final confirmation to write to DB | Nothing — commit is the freeze point | All batch, sample, and compound data becomes immutable |

---

## Handoff points

- **Analyst → Export consumer (manager/stakeholder):** Analyst generates `.xlsx` or `.csv` and distributes it manually. Stakeholders never touch the app.

---

## Freeze / archive points

- **After commit confirmation (Step 10):** All batch, sample, and compound records written to Trinity are immutable. No in-place editing after this point.
- **Re-scan = new version:** If the same `.b` folder is re-scanned, a new versioned entry is created. The prior version is retained and hidden by default; accessible via history view.
- **Exports are not freeze points:** Export files are ephemeral. Generating a new export does not modify or freeze any DB state.

---

## Edge cases and alternate paths

### Missing `target.rp` in a `.d` folder
- System flags the `.d` folder in the summary as "target.rp not found"
- Scan continues on remaining `.d` folders
- User sees the flag in the pre-commit summary
- User can acknowledge and still commit the rest of the data
- The flagged `.d` is recorded with parse status = `missing_target_rp`

### Parse failure on a `target.rp` file
- System flags the `.d` folder in the summary as "parse error" with detail
- Scan continues on remaining `.d` folders
- Partial parse data (if any) is not committed — the sample is flagged as failed
- User can acknowledge and commit the successfully parsed samples

### Re-scan of an existing batch
- System detects that the `.b` folder name already exists in Trinity
- Creates a new versioned entry (version N+1)
- Prior versions are preserved and hidden by default
- History view exposes prior versions on demand

### User cancels at summary screen
- No data is written to Trinity
- Scan results are discarded from memory
- No version entry is created

### Network path unavailable
- System reports path not found or not accessible
- No scan begins
- User is prompted to check the path and retry

### Simultaneous scans by two users
- Both scans can proceed independently (different `.b` folders)
- On commit, SQLite write-lock ensures only one write transaction completes at a time
- The second write queues and completes after the first — no data loss, no corruption

### Export with no batches selected
- App disables or grays the export button until at least one batch is selected (or full-DB is chosen)

---

## Notes for the agent
- The pre-commit summary is a required step — do not skip it or make it bypassable.
- Parse failures and missing `target.rp` are flaggable conditions, not hard stops. The scan must continue and report.
- Do not write anything to Trinity until the user explicitly confirms the commit.
- Versioning is non-negotiable — never overwrite an existing batch entry in place.
- Export generation must query Trinity — do not re-parse the file system at export time.