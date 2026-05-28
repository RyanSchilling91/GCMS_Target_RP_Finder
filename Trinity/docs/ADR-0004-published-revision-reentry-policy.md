# ADR-0004 - Keep Published Revisions Immutable and Re-enter Workflow by Creating a New Working Revision

## Status
- Accepted

## Decision
Treat every published revision as immutable evidence. If a published run must be revised or reloaded, an admin/project lead may authenticate, record a reason, and create a new working revision derived from the published package. The original published revision is never edited in place.

## Context
The operating environment expects regulated data reloads and revisions even after publish. At the same time, published outputs, summary reports, and signoff logs must remain defensible and historically stable. The system therefore needs both immutable evidence and controlled re-entry into workflow.

## Alternatives considered
- Edit published artifacts in place: rejected because it destroys auditability and evidence integrity.
- Forbid all post-publish revisions: rejected because it conflicts with real government workflow.
- Keep only one mutable working folder with no revision lineage: rejected because it obscures what was published and what changed later.

## Why chosen
This preserves the audit story while allowing practical operational corrections and reprocessing.

## Consequences
- Easier: defensible archive, clear lineage, safe rework pattern.
- Harder: requires revision lineage metadata, admin credential challenge, and reopen audit events.
- Publish package must include approved snapshot, CSV/XLSX outputs, summary report, signature/signoff log, and manifest.
- Reopen action must copy from published evidence into a new working revision and record the source revision.

## Review trigger
Revisit if operational policy changes to require central approval services, enterprise identity enforcement, or different publish-package contents.
