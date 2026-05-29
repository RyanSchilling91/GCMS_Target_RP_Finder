# DATA_MODEL

## Purpose of this document
Define the core entities, ownership boundaries, identifiers, required fields, allowed states, relationships, and forbidden states that make the system's data deterministic.

---

## Guided fill status
- Status: Complete
- Last reviewed by: Project owner + AI
- Source of truth: `BOOTSTRAP_QUESTIONNAIRE_APP.md`

---

## Modeling principles

### 1. The batch is the top-level identity anchor
A `Batch` record is the durable identity for a `.b` folder scan. All samples and compounds belong to a batch. Batch identity is the folder name — not a system-generated UUID — because the folder name is the real-world business key that users refer to.

### 2. Versioning is first-class, not an afterthought
Re-scanning a `.b` folder creates a new `ScanVersion`. The `Batch` record is the durable anchor; a `ScanVersion` is one snapshot of it. Old versions are never deleted — they are hidden by default and surfaced via history.

### 3. Compounds are shared entities
The same compound (by number and name) appears across many samples and many batches. Compounds are not owned by a single sample. A `CompoundInstance` is the join record that ties a specific compound to a specific sample within a specific scan version.

### 4. U-Del detection count is derived
The count of U-Del hits per compound per batch is computed from `CompoundInstance` records at query/display time. It is not stored as a canonical field on any entity.

### 5. Exports are not entities
Export files are ephemeral artifacts generated on demand. They are not modeled in the data layer.

---

## Core entities

---

### 1. Batch

#### What it is
The durable identity anchor for a `.b` folder. One `Batch` record exists per unique `.b` folder name, regardless of how many times it has been scanned.

#### Identifier
- `batch_name` — the `.b` folder name (e.g. `Run001.b`) — **business key, human-readable, unique**

#### Fields
| Field | Type | Required | Owner | Changes over time? |
|---|---|---|---|---|
| `batch_name` | string | Yes | System (from folder name) | No |
| `batch_id` | integer / UUID | Yes | System (auto-generated) | No |
| `first_scanned_at` | timestamp | Yes | System | No |
| `latest_version_number` | integer | Yes | System | Yes — increments on re-scan |

#### Allowed states
- Active (has at least one committed scan version)

#### Must never happen
- Two `Batch` records with the same `batch_name`
- `batch_name` modified after creation

---

### 2. ScanVersion

#### What it is
One versioned snapshot of a batch scan. Created each time a user confirms a scan of a `.b` folder. Multiple `ScanVersion` records can exist for the same `Batch`.

#### Identifier
- `batch_id` + `version_number` — composite key

#### Fields
| Field | Type | Required | Owner | Changes over time? |
|---|---|---|---|---|
| `scan_version_id` | integer / UUID | Yes | System | No |
| `batch_id` | FK → Batch | Yes | System | No |
| `version_number` | integer | Yes | System (auto-increment per batch) | No |
| `scan_path` | string | Yes | System (from user input) | No |
| `scanned_at` | timestamp | Yes | System | No |
| `sample_count` | integer | Yes | System (derived at scan time) | No |
| `flagged_sample_count` | integer | Yes | System (derived at scan time) | No |
| `is_latest` | boolean | Yes | System | Yes — set to false when superseded |

#### Allowed states
- Latest (most recent version for this batch)
- Historical (superseded by a newer version — hidden by default)

#### Must never happen
- Modifying a committed `ScanVersion` record
- Deleting a `ScanVersion` record
- Two `ScanVersion` records with the same `batch_id` + `version_number`

---

### 3. Sample

#### What it is
One `.d` folder found during a scan. Belongs to exactly one `ScanVersion`.

#### Identifier
- `scan_version_id` + `sample_folder_name` — composite key
- `sample_folder_name` is the `.d` folder name (e.g. `20192950103.d`) — timestamp-structured, unique within a scan

#### Fields
| Field | Type | Required | Owner | Changes over time? |
|---|---|---|---|---|
| `sample_id` | integer / UUID | Yes | System | No |
| `scan_version_id` | FK → ScanVersion | Yes | System | No |
| `sample_folder_name` | string | Yes | System (from folder name) | No |
| `parse_status` | enum | Yes | System | No (set at parse time, immutable after commit) |
| `parse_error_detail` | string | No | System | No |

#### Parse status values
- `success` — `target.rp` found and parsed without error
- `missing_target_rp` — `target.rp` folder not found in this `.d`
- `parse_error` — `target.rp` found but could not be parsed (with detail)

#### Must never happen
- A `Sample` with no parent `ScanVersion`
- Modifying `parse_status` after commit

---

### 4. Compound

#### What it is
A chemical entity identified in instrument data. Shared across samples and batches — not owned by any single sample.

#### Identifier
- `compound_number` — the instrument-assigned number (unique identifier)

#### Fields
| Field | Type | Required | Owner | Changes over time? |
|---|---|---|---|---|
| `compound_id` | integer / UUID | Yes | System | No |
| `compound_number` | string | Yes | System (from target.rp) | No |
| `compound_name` | string | Yes | System (from target.rp) | No |

#### Must never happen
- Two `Compound` records with the same `compound_number`
- `compound_name` or `compound_number` edited after creation

---

### 5. CompoundInstance

#### What it is
The join record tying a specific compound to a specific sample within a specific scan version. One `CompoundInstance` per compound per sample. This is where the U-Del comment field value lives.

#### Identifier
- `sample_id` + `compound_id` — composite key

#### Fields
| Field | Type | Required | Owner | Changes over time? |
|---|---|---|---|---|
| `compound_instance_id` | integer / UUID | Yes | System | No |
| `sample_id` | FK → Sample | Yes | System | No |
| `compound_id` | FK → Compound | Yes | System | No |
| `udel_comment` | string / null | No | System (from target.rp) | No |
| `is_udel` | boolean | Yes | System (derived at parse time) | No |

#### `udel_comment` values
- `U-Delete`
- `U-Del`
- `UDEL`
- null (compound present but no U-Del comment)

#### `is_udel` derivation rule
`is_udel = True` if `udel_comment` is any of: `U-Delete`, `U-Del`, `UDEL` (case-insensitive match recommended)

#### Must never happen
- Two `CompoundInstance` records with the same `sample_id` + `compound_id`
- `udel_comment` or `is_udel` modified after commit

---

## Derived values (not stored as entities)

### U-Del detection count
- **What it is:** Count of `CompoundInstance` records where `is_udel = True` for a given compound within a given batch version
- **Where it lives:** Computed at query time from `CompoundInstance` records
- **Used in:** Pre-commit summary display, batch overview display, export summary row
- **Must never happen:** Storing this count as a canonical field on `Batch`, `ScanVersion`, or `Compound`

---

## Entity relationship summary

```
Batch (1)
  └── ScanVersion (many — one per scan)
        └── Sample (many — one per .d folder)
              └── CompoundInstance (many — one per compound found)
                    └── Compound (shared — same compound referenced across many instances)
```

---

## Notes for the agent
- `Batch` and `ScanVersion` are separate identities — do not collapse them into one record.
- `Compound` is a shared entity — do not create duplicate compound records for the same `compound_number`.
- `CompoundInstance` is the source of truth for U-Del code values — not `Compound`.
- All committed records are immutable — no update paths after commit, only new version creation.
- U-Del detection counts are always derived — never store them as canonical fields.