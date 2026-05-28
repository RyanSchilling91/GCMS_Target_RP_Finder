# FAILURE_CATALOG

## Purpose of this document
Record important failures so they become reusable engineering memory instead of being forgotten.

---

## How to use this file
Before changing risky behavior:
1. Check whether the failure pattern already exists here.
2. If it does, treat it as a regression landmine.
3. If it does not, add a new entry once root cause is understood.

---

## Project-specific known failures / near-failures

### Session-state key drift can break rehydration subtly
#### Symptom
Saved runs reload with missing/odd editor state or mismatched pair/label artifacts after app changes.

#### Root cause
Session snapshots rely on many UI-adjacent keys and compatibility assumptions across versions.

#### Detection gap
Existing tests do not currently cover full snapshot round-trip across app versions.

#### Prevention rule
Add snapshot fixture tests, schema/app version metadata, and explicit compatibility checks before restore.

### Pairing can become stale after categorization edits
#### Symptom
Labels or downstream data no longer reflect the latest category assignments.

#### Root cause
Pairing artifacts are derived from categorize output and must be rebuilt when source changes.

#### Detection gap
Manual checks catch most cases, but automated regression around re-categorize + relabel transitions is limited.

#### Prevention rule
Enforce rebuild triggers and add integration tests for recategorize->relabel->results transitions.

### Bad raw rows can poison Sample Set Manager rebuilds mid-batch
#### Symptom
One frustrating or unusable instrument row in the middle of a batch forces every later Sample Set Manager rematch to drift, because rebuild consumes the bad row instead of skipping it.

#### Root cause
The upload preview initially had no operator-controlled drop flag on raw rows, and the first implementation bound the drop checkbox directly to a rerunning editor so each click could snap the page back to the top before the operator finished selecting multiple rows.

#### Detection gap
The workflow supported excluding Sample Set Manager lines, but not excluding a bad raw row from the rematch path while keeping the original uploaded table visible for audit; later, the first row-drop UI did not have a buffered save step to prevent per-click reruns from interrupting multi-row edits. A follow-on regression reintroduced a duplicate `raw_preview_editor` render path plus stray standalone `main` text in `Upload & Match`, which let unsaved checkbox changes leak directly into `raw_df` before the explicit save boundary.

#### Prevention rule
Allow operators to mark raw rows as dropped in the upload preview, keep exactly one buffered raw-preview editor behind an explicit save action, persist that working-state flag only when `Save raw row drops` is clicked, remove any duplicate render path or stray merge residue from the section, and cover rematch behavior with tests that verify multiple saved drop edits are what Sample Set Manager rebuild consumes.

### Explicit draft-save checkpoints can drift away from the authoritative working snapshot
#### Symptom
A draft appears saved in the local cache, but reopening the run from home routes to the wrong page because `working.duckdb` never received the latest Sample Set Manager, upload/match, or raw-row-drop edits.

#### Root cause
Some workflow save points only updated `st.session_state` plus the convenience cache, while the authoritative shared-storage resume snapshot was only written by sidebar run actions. Upstream edits such as Sample Set Manager changes or raw-row-drop saves could also leave stale downstream match/results artifacts in the durable snapshot.

An additional regression path allowed the Upload & Match screen to treat the same still-selected upload as a fresh parse signal on rerun, which could overwrite already-saved raw-row drop flags and rematch state with a clean raw import.

#### Detection gap
Existing reopen tests covered home routing against saved snapshots, but not the intermediate draft save points that should survive closing and reopening from home.

#### Prevention rule
Use one shared helper for durable working-state persistence at every explicit draft-save checkpoint, treat `save_state()` as cache-only, clear downstream derived artifacts when upstream draft inputs change, write both raw-row-drop saves and rebuild-match actions back to `working.duckdb`, and keep reopen-routing regression coverage for Sample Set Manager save, upload/match save, raw-row-drop save, and rebuild-match save paths.

Guard upload parsing with an idempotent “new file” boundary so reruns/navigation cannot silently overwrite the last saved `raw_df` + drop-flag state before an explicit new upload action.

### Shared-storage collaboration can deadlock on stale run ownership (target risk)
#### Symptom
Users are blocked from continuing a run because previous ownership/lock was not cleared.

#### Root cause
No fully formalized lock lifecycle (heartbeat, timeout, override, audit) yet.

#### Detection gap
Current implementation has save/resume but no full lock-manager test harness.

#### Prevention rule
Implement explicit lock metadata + timeout + controlled override, and test stale lock recovery paths.

### Publish/reopen control paths can accept incomplete metadata or damaged artifact packages
#### Symptom
Publish or reopen appears to succeed until a later step discovers missing manifest fields, missing files, or a bad protected-action request.

#### Root cause
Protected workflow actions depended on loosely validated manifest/package state and did not consistently reject missing reason fields before mutating workflow state.

#### Detection gap
Earlier tests covered happy-path publish/reopen flows but not damaged metadata, missing artifacts, or invalid override requests.

#### Prevention rule
Validate required manifest metadata before publish, validate published artifact packages before reopen, require non-empty admin-override reasons, and keep regression fixtures for damaged packages.

### Governed criteria and protected admin access can drift away from real operational needs
#### Symptom
The admin criteria UI lacks a threshold that operators rely on in review, or protected admin actions depend on credentials that users cannot realistically manage or recover.

#### Root cause
Governed criteria and near-term admin-auth assumptions were only partially modeled, so the UI exposed some controls without a complete rule set or a maintainable credential workflow.

#### Detection gap
The original implementation focused on existing thresholds and a single environment-backed credential, but did not verify whether all operator-facing criteria and recovery paths were truly governed from inside the app.

#### Prevention rule
Model governed criteria and protected-action credential management explicitly in docs and tests before extending the admin UI, and add regression coverage for newly governed thresholds and admin-password recovery behavior.

### Merge-conflict artifacts can ship into code and docs
#### Symptom
The app fails at import or rerun time with syntax or indentation errors, and docs-first guidance becomes unreliable because planning files contain stray branch-marker text.

#### Root cause
Merge-conflict artifacts or branch-label lines were committed without an integrity check covering both Python sources and Markdown docs.

#### Detection gap
Existing checks did not scan the repository for conflict markers or arbitrary `codex/*` branch-label residue before release, so the breakage surfaced only at runtime.

Recent example: unresolved `codex/...`, `=======`, and `main` merge text in `nutrients_app/App.py` and `nutrients_app/helpers/run_ui.py` broke app import/rerun with an `IndentationError` before the workflow router could render.

#### Prevention rule
Add a repository smoke check that scans tracked code/docs for conflict-marker artifacts and any standalone `codex/*` branch-label residue, including `<<<<<<<`, `=======`, `>>>>>>>`, and bare `codex/...` lines, and treat any match as a release-blocking defect.

### Test collection can fail before business rules run
#### Symptom
`pytest` fails during collection with import errors instead of skipping dependency-backed tests or loading the local package correctly.

#### Root cause
The test suite assumed optional runtime dependencies were always installed and relied on environment-specific import path behavior for the repo package.

#### Detection gap
Prior checks used narrower commands and did not exercise plain `pytest` collection in a minimal environment.

#### Prevention rule
Keep a shared test bootstrap that adds the repo root to `sys.path`, use `pytest.importorskip(...)` in tests that require optional dependencies such as `pandas` or `duckdb`, run an explicit app-entry import smoke check for `nutrients_app.App` plus `nutrients_app.helpers.run_ui` before dependency-backed helper tests, and treat collection failures in routing/progress home-router tests as release-blocking defects.

---

### Post-run metadata capture can force the workflow into a fragile order
#### Symptom
Operators must wait until after instrument upload to categorize and label samples, which makes missed injections, exclusions, and metadata corrections harder to manage and increases the chance of mismatching planned samples to instrument rows.

#### Root cause
The earlier workflow introduced editable metadata after raw upload, even though the operational truth starts with a planned sample set prepared before the run.

#### Detection gap
The app had the needed pieces (sample typing, metadata entry, exclusions, pairing audits) but they were separated into a later step order that was never modeled against the real lab preparation sequence.

#### Prevention rule
Model pre-run sample planning explicitly with a Sample Set Manager, then match uploaded instrument rows against that plan and test exclusion/missed-injection behavior as part of the main workflow.


### UI/runtime helpers can drift from persisted starter-state and identity contracts
#### Symptom
The Sample Set Manager can reopen with only a single legacy starter row instead of the documented 10 starter lines, and the admin criteria page can crash with an `AttributeError` when UI code expects `IdentityContext.user`.

#### Root cause
The UI trusted older cached Sample Set Manager seed state and an outdated identity attribute name without a compatibility shim or regression coverage for either path.

#### Detection gap
The repo had tests for the 10-line seed helper and admin services, but not for rehydrating a legacy single-row starter state or for backward-compatible `IdentityContext` access used by UI call sites.

#### Prevention rule
Add compatibility helpers/tests for legacy starter-state rehydration and identity accessors whenever saved UI state or shared helper dataclasses are reused across screens.

### Home review queue can advertise self-review as available work
#### Symptom
The `Runs Ready for Review` home-screen queue can show a run authored by the current user as if it were claimable review work, even though the open/claim path rejects self-review.

#### Root cause
The home-screen queue filtered `Ready for Review` runs by status only and did not apply the same `can_review_run(...)` reviewer-independence rule enforced later by `_try_open_run(...)`.

#### Detection gap
Workflow tests covered service-level self-review rejection, but not home-screen queue presentation for self-authored review candidates.

#### Prevention rule
Build the actionable `Runs Ready for Review` queue from the same reviewer-eligibility helper used by claim/open paths, exclude self-authored runs from that actionable section, and add regression coverage for manifests where `primary_user == current user`.

### Run home summary and open-route landing can drift apart for the same draft snapshot
#### Symptom
The home screen can tell the user to resume at one workflow step while opening the same run lands on a different page.

#### Root cause
Home summary labels and open-route destinations were derived in separate helpers with overlapping draft-state inference instead of sharing one workflow-progress helper.

#### Detection gap
Existing tests asserted summary behavior and route behavior independently, but not that both surfaces stayed aligned for the same persisted snapshot.

#### Prevention rule
Use `determine_run_progress()` as the single source of truth for landing page, step label, percent complete, and blocking reason, keep a regression test that compares home summary output with route destination for one snapshot, and treat routing/progress test collection failures as release blockers because the home screen is the primary workflow router.

### Published runs can reopen on the editable review/results page instead of a read-only evidence viewer
#### Symptom
Opening a run from `Published Runs` lands on `Review & Results`, which makes immutable evidence look like a draft/review workspace and hides the dedicated published artifact context.

#### Root cause
The home/router logic treated `Published` like other late-stage statuses and mapped it to the same final workflow page instead of a distinct published evidence surface.

#### Detection gap
Routing/progress tests covered review-stage landing, but did not enforce a dedicated published page constant and read-only viewer expectation end to end.

#### Prevention rule
Route `Published` runs to a dedicated published evidence page constant, keep reopen controls separate from draft/review editing actions, and keep regression tests aligned with the published-viewer landing rule.

### Persisted Streamlit action-widget keys can crash run reopen or rerun
#### Symptom
Opening or rerendering a saved run fails with `streamlit.errors.StreamlitValueAssignmentNotAllowedError`, citing action-widget keys such as `run_save_draft`.

#### Root cause
Transient keyed action widgets from the run sidebar and home actions were treated as restorable state by one or more persistence paths. The run working-snapshot serializer originally persisted them, and the older general session-cache filter could still restore `run_*` / `open_*` trigger keys into `st.session_state` before Streamlit recreated the widgets.

#### Detection gap
Snapshot round-trip coverage verified dataframes and metadata, but did not include explicit keyed button state across both persistence layers or assert that trigger-only widget keys were excluded from the legacy cache as well as run snapshots.

#### Prevention rule
Exclude action-widget keys and prefixes from every persistence path, aggressively clear them during startup/rehydration, and keep regression tests that prove keyed sidebar/home buttons such as `run_save_draft` and `open_*` are not restored from saved state.

### Step 1 sidebar saves can serialize stale Sample Set Manager rows
#### Symptom
Editing the Step 1 Sample Set Manager and then clicking `Save Draft` or `Save & Close` can write the previously saved/default rows into `working.duckdb` instead of the rows currently visible in the editor, so reopen restores stale Step 1 values.

#### Root cause
The Step 1 editor could diverge from the authoritative `sample_set_table_data` snapshot source, and sidebar save actions persisted the run without first reconciling the current editor state back into that durable working-state table.

#### Detection gap
Existing persistence tests covered explicit Step 1 saves and downstream rebuild checkpoints, but not the workflow where the user edits Step 1 and immediately uses sidebar draft-save actions.

#### Prevention rule
Keep the Step 1 editor synchronized with `sample_set_table_data` before any sidebar save serializes the run, and keep reopen regressions proving sidebar `Save Draft`/`Save & Close` restore the current edited Step 1 rows while starter-table seeding does not overwrite restored Sample Set Manager data.

### Active Step 1 navigation can silently drop current Sample Set Manager edits
#### Symptom
An analyst can lose Step 1 work in one of two ways: previously, away/back navigation could restore stale/default rows instead of the committed Sample Set Manager; later, an over-corrective rerun-time sync caused the table to jump/reset while the analyst was still entering multiple values before pressing `Save Sample Set Manager`.

#### Root cause
The real contract is an explicit commit boundary: the data editor must remain stable while the analyst fills out multiple cells, and only the `Save Sample Set Manager` action should synchronize those rows into committed working state. Both failure modes came from violating one side of that contract—either never committing the submitted editor rows, or committing/reacting to in-progress editor rows on every rerun. A later variant also trusted the immediate `st.data_editor(...)` return payload during save; for selectbox/checkbox edits that payload can lag one rerun behind the keyed editor buffer, so the newest non-text choice was overwritten by stale data.

#### Detection gap
Regression coverage did not simultaneously test both halves of the Step 1 contract: stable multi-cell entry before save, and correct committed-state reuse after save/navigation/reopen.

#### Prevention rule
Keep Step 1 behind an explicit `Save Sample Set Manager` commit boundary: no rerun-time sync of in-progress editor rows, no autosave-on-edit, and regressions that prove users can enter multiple values stably before save while later pages/reopens use only the last committed Sample Set Manager table. On save, commit from the keyed editor session value (for example `sample_set_table_editor`) rather than relying on a potentially one-rerun-stale return value.

### Home/router click actions can be overwritten by stale widget state on the next rerun
#### Symptom
Home-screen `Open` and run-sidebar actions such as `Save & Close`, `Submit for Review`, and `Publish Revision` can appear to ignore the first click and require repeated rapid clicks before the routed page or workflow status visibly changes.

#### Root cause
Those actions previously mutated or cleared `st.session_state` after the related widgets had already been instantiated in the same rerun. The resulting route/status change was then vulnerable to being overwritten by the still-stale sidebar radio/widget state on the next rerun.

#### Detection gap
The test suite covered route selection helpers and service-level workflow actions independently, but it did not simulate a stale `__router_radio__` selection immediately after a requested route change.

#### Prevention rule
Queue home/sidebar actions through widget callbacks before the page renders, carry a durable route-intent key across reruns, bound any forced reroute sync to a single retry per intent, and keep a regression test proving the requested page wins even if the radio reports the prior selection for one rerun.

### Snapshot null semantics and draft routing can drift across resume
#### Symptom
Saved draft reopen behavior can fail determinism checks because Sample Set Manager booleans treat `NaN` as truthy, concentration fields reopen as `"nan"` instead of `"N/A"`, optional pair/sample fields drift between `None`, `NaN`, and `<NA>`, or review-open routing uses stale session values instead of the freshly loaded snapshot/manifest.

#### Root cause
Working-state normalization relied on plain Python truthiness and default pandas/DuckDB round-trips instead of canonicalizing missing values on save/load. The home open path also trusted ambient `st.session_state` after loading rather than explicitly applying the loaded snapshot/manifold state before routing.

#### Detection gap
The suite had targeted resume/routing tests, but the implementation still left gaps between pandas missing-value behavior, snapshot rehydration, and `_try_open_run(...)`'s test seam.

#### Prevention rule
Canonicalize working-state missing values during normalization and snapshot restore, keep explicit regression coverage for `None`/`NaN`/`<NA>` stability, and ensure `_try_open_run(...)` routes from the freshly loaded snapshot plus refreshed manifest rather than stale session leftovers.

### Duplicate LIMS ID creation can silently overwrite an existing run
#### Symptom
Choosing `Start New Dataset` with a LIMS ID that already exists can rewrite the existing run's top-level manifest and working snapshot instead of directing the operator back to the saved run.

#### Root cause
Run creation trusted the target folder name alone and always wrote a fresh draft manifest/snapshot, even when the run directory already contained a valid `manifest.json` for that LIMS ID.

#### Detection gap
Existing run-creation tests covered the happy path and lock flow, but not repeated creation attempts against an existing draft or published run folder.

#### Prevention rule
Treat a valid existing `manifest.json` as authoritative for that LIMS ID, reject duplicate creation attempts with a clear home-screen recovery message, and keep regression tests that prove existing manifest/snapshot files remain untouched for draft and published runs.

#### Current status
Guarded in the service/persistence create path: duplicate `Start New Dataset` now returns an explicit recovery/open result for the existing run identity and preserves draft + published artifacts. Regression coverage lives in `tests/test_duplicate_identity_guard.py`.

### Review-open routing can crash after claiming a review run
#### Symptom
Opening a `Ready for Review` run from home, or reopening an `In Review` run as the assigned reviewer, can crash before navigation completes and the success notice may fail while formatting the run id.

#### Root cause
The home open handler treated `claim_review(...)` as if it returned only a manifest, even though the service returns `(updated_manifest, lock_info)`. That raw tuple was passed into the router and later indexed like a dict when building the open notice.

#### Detection gap
Routing tests covered review destinations and workflow-service tests covered review claim semantics, but there was no `_try_open_run(...)` regression test that exercised the home open path for both first-claim and same-reviewer resume flows.

#### Prevention rule
Destructure review-claim service returns before routing, refresh session-state manifest/status from the updated manifest after snapshot load, and keep regression tests that open both `Ready for Review` and `In Review` runs through `_try_open_run(...)`.

## Seed lessons from prior successful use of this framework

### Parent/child state changes can fail when related records are still active
#### Symptom
A seemingly valid update or deactivation can fail because dependent child records still reference the parent.

#### Root cause
The workflow updated parent state directly without first handling dependent records in a safe order.

#### Detection gap
Tests covered the happy path but not live-state scenarios with active linked children.

#### Prevention rule
When mutating or disabling parent records, test and document dependency handling order explicitly.

### Version markers can lie if actual schema or required objects are not verified
#### Symptom
The system appears upgraded on paper but fails because the real storage shape does not match the recorded version.

#### Root cause
Startup trusted metadata/version markers without validating required structures.

#### Detection gap
Migration checks covered nominal version movement but not inconsistent persisted state.

#### Prevention rule
Verify both version markers and required structural objects before declaring the system ready.

### Derived truth can become stale when persisted casually
#### Symptom
Outputs look plausible but no longer reflect the current source state.

#### Root cause
Data that should have been derived/recomputed was stored as if it were source truth.

#### Detection gap
The planning docs did not clearly classify working, derived, and evidence state early enough.

#### Prevention rule
Use `STATE_CLASSIFICATION.md` before persistence design and challenge permanent storage of recomputable values.
