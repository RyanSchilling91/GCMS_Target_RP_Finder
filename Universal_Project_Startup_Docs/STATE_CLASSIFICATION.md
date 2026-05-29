# STATE_CLASSIFICATION

## Purpose of this document
Define what kind of state each piece of data is — working, derived, or evidence — and establish the rules that govern mutability, persistence, and protection.

This prevents the most common architectural failure: derived data casually promoted to canonical truth, or evidence silently overwritten.

---

## Guided fill status
- Status: Complete
- Last reviewed by: Project owner + AI
- Source of truth: `BOOTSTRAP_QUESTIONNAIRE_APP.md`, `DATA_MODEL.md`

---

## State categories

### Working state
Temporary, mutable data that exists before a user confirms a commit. Lives in memory only. Discarded if the user cancels. Never written to Trinity until the user explicitly confirms.

### Derived state
Values computed from committed working or evidence state. Not stored as canonical truth. May be cached for display performance, but must always be reconstructable from source records. Stale derived state must never be allowed to masquerade as source truth.

### Evidence state
Immutable records committed to Trinity after user confirmation. Never edited in place. A new version (re-scan) is the only mechanism to supersede evidence state.

---

## Classification table

| Data | State type | Mutable? | Persisted? | Notes |
|---|---|---|---|---|
| Folder path entered by user | Working | Yes | No | Discarded if user cancels or closes without scanning |
| In-progress scan job (traversal, parse operations) | Working | Yes | No | Lives in memory; discarded on cancel or error |
| Parsed batch / sample / compound records (pre-confirm) | Working | Yes (cancel discards) | No | Held in memory until user confirms commit |
| Pre-commit summary data (sample count, flag list) | Working | No (read-only display) | No | Displayed to user; discarded after confirm or cancel |
| U-Del detection count (pre-commit) | Derived | — | No | Computed from working parse results for display in summary |
| Batch record (post-commit) | Evidence | No | Yes — Trinity | Immutable after commit |
| ScanVersion record (post-commit) | Evidence | No | Yes — Trinity | Immutable after commit; `is_latest` flag is the only system-managed field that changes |
| Sample record (post-commit) | Evidence | No | Yes — Trinity | Immutable after commit; `parse_status` frozen |
| Compound record (post-commit) | Evidence | No | Yes — Trinity | Immutable after commit |
| CompoundInstance record (post-commit) | Evidence | No | Yes — Trinity | Immutable after commit; `udel_comment` and `is_udel` frozen |
| U-Del detection count (post-commit) | Derived | — | No | Computed at query time from CompoundInstance records; never stored as a field |
| Export file (.xlsx / .csv) | Derived | — | No | Generated on demand from Trinity query; ephemeral; not stored in DB |
| Scan history (old versions) | Evidence | No | Yes — Trinity | Retained permanently; hidden by default; surfaced via history view |

---

## Mutability rules

### What can be changed before commit
- The folder path can be changed at any time before scan begins
- The user can cancel the scan at any point before confirming commit — nothing is written

### What can never be changed after commit
- Batch record fields (batch_name, batch_id, first_scanned_at)
- ScanVersion fields (version_number, scan_path, scanned_at, sample_count, flagged_sample_count)
- Sample fields (sample_folder_name, parse_status, parse_error_detail)
- Compound fields (compound_number, compound_name)
- CompoundInstance fields (udel_comment, is_udel)

### The one system-managed exception
- `ScanVersion.is_latest` is updated to `False` when a new version is created for the same batch — this is a system bookkeeping field, not a user-visible data field, and is the only post-commit write to an existing evidence record

### How to correct committed data
- Re-scan the `.b` folder — this creates a new `ScanVersion` with fresh parse results
- The prior version is retained in history
- There is no UI mechanism to edit committed records directly

---

## Derived state rules

### U-Del detection count
- **Source:** `CompoundInstance` records where `is_udel = True`
- **Computed at:** Pre-commit summary display AND post-commit batch overview display AND export generation
- **Never stored as:** A field on `Batch`, `ScanVersion`, or `Compound`
- **Rule:** If the count and the CompoundInstance records ever disagree, the CompoundInstance records are truth

### Export files
- **Source:** Trinity DB query filtered by user-selected batches
- **Not stored:** Export is generated, downloaded, and discarded
- **No audit trail in v1:** No record of when or what was exported is maintained
- **Rule:** Generating an export never modifies any DB state

---

## Versioning behavior

When a `.b` folder is re-scanned and the user confirms:
1. A new `ScanVersion` is created (version N+1) with a new scan timestamp
2. The prior `ScanVersion` has `is_latest` set to `False`
3. All prior `Sample` and `CompoundInstance` records remain untouched
4. The new scan's samples and compound instances are written as entirely new records linked to the new `ScanVersion`
5. History view shows all versions; default view shows only the latest

---

## Forbidden state transitions

| Forbidden transition | Why |
|---|---|
| In-place update of any committed evidence record | Destroys audit trail; breaks versioning contract |
| Deleting a ScanVersion | Old versions must be retained for history |
| Storing U-Del count as a DB field | Derived data must not become canonical truth |
| Writing export file to DB | Exports are ephemeral by design |
| Promoting working-state parse results to DB without user confirmation | Pre-confirm data must never be silently committed |
| Re-using a Compound record from a prior scan with updated fields | Compound is a shared immutable entity; field changes require a new record or schema migration |

---

## Notes for the agent
- If working state and evidence state are ever confused (e.g. pre-confirm data is persisted), treat that as a critical defect.
- Derived data must always be recomputable from source. If a query to recompute U-Del count produces a different result than a cached value, the query result is correct.
- The `is_latest` field is the only legitimate post-commit write to an evidence record. All other post-commit writes are forbidden.
- Do not add a "last exported" field or export log without explicit project owner sign-off — it is out of scope for v1.