# RETROSPECTIVE

## Purpose of this document
Capture what worked, what failed, and what should become standard practice after each meaningful phase or incident.

---

## How to use this file
Update this file when:
- a phase completes
- a major defect reveals a process weakness
- a repeated pattern suggests a better standard
- the team learns something that should carry into future projects

---

## Entry: 2026-03 Documentation hardening pass (in-place modernization)

### What worked
- The existing app already enforces a practical workflow with explicit categorize, label, audit, and results stages.
- Helper-module decomposition preserved maintainability despite ongoing changes.
- Save-and-resume behavior delivered immediate operational value over spreadsheets.

### What failed
- Planning documents lagged implementation, making design intent implicit.
- Reviewer/signoff and lock-management behavior were not formalized.
- Test strategy and quality gates were too generic for production-adjacent use.

### What to standardize
- Keep docs synchronized with workflow changes in the same PR.
- Treat persistence/concurrency/signoff as first-class architecture surfaces, not UI details.
- Require artifact/version compatibility checks before persistence changes ship.

### What rule should be added or modified in AGENTS.md
- For active projects, require periodic “docs re-baselining” against current app behavior before major enhancements.
- Require explicit ADR updates when persistence or collaboration semantics change.

---

## Entry: 2026-03 App import smoke and home-routing release gate

### What worked
- The docs-first pass already identified deterministic home routing and release-gate import integrity as quality requirements, so the needed guardrails were straightforward to encode in tests/scripts.
- A dedicated release-gate import smoke check catches syntax/import regressions in the app entry points before helper-heavy workflow tests run.

### What failed
- The main app entry modules carried unresolved merge leftovers, which meant helper tests could still appear healthier than the actual app startup path.
- Home-routing behavior had unit coverage, but not a single integrated check that exercised new/draft/review/published launch paths together.

### What to standardize
- Treat app-entry imports as a first-class release gate, not just an incidental side effect of other tests.
- Keep at least one integrated home-routing check that covers new, draft, reviewable, and published launch actions together.

### What rule should be added or modified in AGENTS.md
- Require release-hardening changes that affect app startup or home routing to include an explicit app-import smoke check plus a combined home-action routing test.

---

## Entry: 2026-03 Test collection hardening

### What worked
- The stdlib-only workflow tests were already separated from the dependency-heavy publish workflow tests.
- Running plain `pytest` in a minimal environment exposed collection fragility quickly.

### What failed
- Some tests imported optional dependencies directly at module import time, causing collection failure instead of a controlled skip.
- The suite depended on environment-specific package import behavior rather than bootstrapping the repo path explicitly.

### What to standardize
- Treat plain `pytest` collection in a minimal environment as a required smoke check.
- Centralize any test bootstrap needed for local package imports in `tests/conftest.py`.
- Use `pytest.importorskip(...)` for optional dependency-backed tests at module scope.

### What rule should be added or modified in AGENTS.md
- Require dependency-backed tests to skip cleanly when optional packages are absent, rather than failing collection.

---

## Entry: 2026-03 Release-hardening workflow fixtures and regression coverage

### What worked
- Converting workflow expectations into representative fixtures made publish/reopen and review-independence behavior much easier to reason about.
- Adding service-level workflow actions reduced dependence on UI-only state transitions for review, approval, and rework paths.
- Artifact validation checks provided a clean seam for testing damaged publish packages and safe reopen failures.

### What failed
- The docs tree had unresolved merge-conflict artifacts, which undermined the docs-first workflow until cleaned up.
- Earlier publish/reopen coverage was too optimistic and did not stress missing manifest fields, bad override requests, or damaged artifact packages.

### What to standardize
- Treat docs integrity issues (including merge markers) as blocking defects for docs-first implementation work.
- Keep representative workflow fixtures for happy path, pairing warnings, stale locks, self-review rejection, and damaged publish artifacts.
- Validate protected-action prerequisites at service boundaries, not only in UI handlers.

### What rule should be added or modified in AGENTS.md
- Require docs conflict-marker cleanup before relying on planning docs for implementation work.
- Require publish/reopen hardening work to include damaged-artifact and invalid-override regression coverage.

---

## Entry: 2026-03 Governed criteria and admin-password hardening

### What worked
- Treating the admin criteria page as governed configuration made it straightforward to identify which thresholds already flow into review and publish behavior.
- Using workstation identity for the audit actor fits the restricted deployment model better than asking users to invent an in-app admin username that is not otherwise managed.

### What failed
- The initial governed-criteria model did not include every operator-facing threshold, including the TPC raw Fb range used during review.
- The first protected-action implementation assumed a manageable admin username/password pair without giving operators an in-app way to maintain or recover the password set.

### What to standardize
- When a threshold appears in review or QA decisions, model it in `CriteriaConfig` before exposing the admin page as the source of truth.
- For restricted/offline deployments, document the bootstrap admin credential path and the supplemental-password lifecycle before wiring the UI.

### What rule should be added or modified in AGENTS.md
- Require protected-action UX changes to document how credentials are provisioned, recovered, and audited before implementation.

---

## Entry: 2026-03 Sample Set Manager workflow reorder

### What worked
- The existing categorize, label, and audit pieces were modular enough to be recomposed around a pre-run Sample Set Manager.
- Converting planned metadata into a deterministic upload/match step kept downstream calculations unchanged.

### What failed
- The old workflow captured key metadata too late relative to the real lab process.
- Missed-injection handling depended on post-upload edits instead of being first-class planning state.

### What to standardize
- When a workflow begins with a planned run sheet, model that planning artifact directly rather than treating it as post-ingest cleanup.
- Keep match logic deterministic and documented whenever planning rows are paired to later uploads.

### What rule should be added or modified in AGENTS.md
- For workflow tools that transform uploaded data, require explicit documentation of any pre-run planning artifact and the row-matching strategy before UI sequencing changes ship.

---

## Entry: 2026-03 Workflow-progress single-source-of-truth hardening

### What worked
- The existing `RunProgress` helper already provided a natural seam for centralizing landing-page and resume-step decisions.
- Adding one snapshot-based regression test made it easy to lock summary and routing behavior together.

### What failed
- Home summary labels and open-route destinations drifted because draft progress was inferred in multiple helpers.
- The duplication made it easy for one path to treat a run as “resume at review/results” while another reopened it on an earlier audit page.

### What to standardize
- Keep workflow-progress derivation in one helper that returns both the human step label and the machine route destination.
- When a home/dashboard surface summarizes workflow progress, test it against the actual open/run route for the same persisted snapshot.

### What rule should be added or modified in AGENTS.md
- Require any new workflow-resume surface to reuse the shared progress helper instead of re-deriving step state locally.

---

## Entry: 2026-03 Routing/progress collection release blocker

### What worked
- The docs-first pass and existing routing/progress helpers made it straightforward to identify that the home-router release gate was blocked by collection-time merge artifacts rather than by the workflow assertions themselves.
- The routing tests already modeled draft, review, and published destinations closely enough that cleaning the conflicts restored useful release coverage quickly.

### What failed
- A conflicted routing/progress test module was able to break collection before the home-router release checks could actually execute.
- Router helper conflicts drifted alongside the test conflict, so the release signal failed before the primary workflow router could be validated end to end.

### What to standardize
- Treat routing/progress test collection as part of the release gate, not just the assertions that would have run after collection.
- Keep published-run routing expectations synchronized across run-progress, run-routes, and integration tests whenever the home router changes.

### What rule should be added or modified in AGENTS.md
- Require release-hardening changes that affect the home router to include a conflict-marker scan plus a routing/progress collection smoke check before broader workflow tests run.

## Entry: 2026-03 Merge-artifact cleanup and Streamlit width migration

### What worked
- The docs-first pass exposed the same merge-artifact pattern in both planning docs and Python/test files before deeper debugging continued.
- Replacing deprecated Streamlit `use_container_width` calls with explicit `width="stretch"` preserved the existing full-width layout while removing future-removal warnings.

### What failed
- The repo had no release smoke check for merge-conflict residue, allowing branch-label text to ship into executable modules.
- UI deprecation warnings accumulated across several screens because compatibility maintenance was not part of routine cleanup.
- The original branch-label scan was too narrow, so a different `codex/*` residue string could still break imports even after earlier cleanup work.

### What to standardize
- Run a repository-wide conflict-marker scan as part of bug-fix validation and before packaging the app.
- Match any standalone `codex/*` branch-label residue in that scan instead of relying on a short allow/block list of specific branch names.
- Treat framework deprecation warnings as backlog items to clear before the removal date when the replacement is low risk.

### What rule should be added or modified in AGENTS.md
- Require a conflict-marker scan and targeted framework-deprecation cleanup whenever a runtime failure or release-hardening pass touches shared UI or workflow files.

---

## Entry: 2026-03 Streamlit action-widget snapshot hardening

### What worked
- The run snapshot layer already had a reserved-key filter, so the fix stayed localized to persistence rather than spreading Streamlit-specific guards through the UI.
- A small snapshot round-trip regression test was enough to lock the failure down without needing a full interactive Streamlit harness.

### What failed
- Keyed action widgets in the run sidebar and home router were treated like durable workflow state and got written into working snapshots.
- Rehydration tests focused on scientific/workflow data and missed Streamlit’s rule that button values cannot be assigned through `st.session_state`.

### What to standardize
- Treat keyed action widgets (`st.button`, submit buttons, and similar trigger-only controls) as ephemeral UI state that must never enter persisted run snapshots.
- Add snapshot-level regression coverage whenever new keyed widgets are introduced on resumable workflow surfaces.

### What rule should be added or modified in AGENTS.md
- Require persistence filters and regression coverage for any new keyed Streamlit trigger widget that appears on a save/resume workflow surface.

## Entry: 2026-03 Step 1 active-navigation persistence repair

### What worked
- The Step 1 workflow already had a single authoritative table key (`sample_set_table_data`), so the repair stayed localized to keeping the editor synchronized with that working-state object.
- Existing save/reopen regressions made it straightforward to add a narrower navigation-away-and-back regression without redesigning the workflow.

### What failed
- Step 1 regressions initially focused on persistence edge cases without also protecting the intended explicit-commit editing model for the Sample Set Manager chart itself.
- An over-correction blurred the line between in-progress editor state and committed Sample Set Manager state, causing rerun-time chart instability before the save button was pressed.

### What to standardize
- For explicit-commit workflow tables, test realistic multi-cell entry before save so rerun behavior cannot destabilize the chart while the analyst is still typing.
- Separately test the committed-state boundary: later workflow steps and reopen paths must use only the last committed Sample Set Manager table, not in-progress editor state.

### What rule should be added or modified in AGENTS.md
- Require workflow regressions for any resumable editor page to cover navigation away and back without relying only on explicit save-button paths.

---

## Entry: 2026-03 Duplicate run-creation guard

### What worked
- The file-backed run model already treated `manifest.json` as the durable run identity surface, so duplicate detection could key off the existing manifest before any rewrite occurred.
- Home-screen messaging provided a natural place to direct operators back to the correct draft or published queue.

### What failed
- Starting a new dataset reused the run folder path without first checking whether a valid manifest already existed for that LIMS ID.
- The duplicate-creation path lacked regression coverage for published runs, where overwrite risk is especially dangerous.

### What to standardize
- Treat valid run manifests as authoritative identity claims for a LIMS ID before creating any new draft folder content.
- Add duplicate-creation regression coverage for both mutable drafts and immutable published runs.

### What rule should be added or modified in AGENTS.md
- Require run-creation changes to test duplicate-ID rejection and preservation of any pre-existing manifest/snapshot artifacts.

---

## Seed lessons from prior successful use of this framework

### What worked
- Reading the docs before touching code reduced drift and improved alignment.
- Forcing workflow timeline and data model decisions before feature work reduced rework.
- Keeping UI thin and business logic outside UI files improved maintainability and portability.
- Recording irreversible decisions in ADRs reduced repeated stack churn.
- Treating failure documentation as part of the fix improved long-term stability.

### What failed
- Letting proven prior patterns quietly become defaults can bias new projects toward the wrong stack.
- Tests that only cover clean or happy-path scenarios miss real-world persisted-state and dependency failures.
- Architecture recommendations can drift when assumptions are not logged explicitly.

### What to standardize
- Add a dedicated architecture-selection step before ADRs.
- Distinguish universal method rules from stack-specific recommendations.
- Require more realistic fixtures around sessions, dependencies, migration state, and live-record conditions.
- Treat missing planning docs as blocking conditions for architecture work.

### What rule should be added or modified in AGENTS.md
- Require explicit comparison of plausible stack options before committing to a UI or persistence choice.
- Require the agent to call out when a recommendation is based on prior success rather than current project requirements.
