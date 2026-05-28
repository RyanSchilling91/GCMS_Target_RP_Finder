# State Classification

## Purpose
Separate data into working state, derived state, and evidence state.

This prevents duplicated truth, stale persisted calculations, and silent corruption of archival records.

## Guided fill status
- Status: [Complete / Present but weak / Missing]
- Last reviewed by:
- Last updated:

## Working state
Editable state used during normal workflow.

| Name | Why working state | Who can edit | Where it persists | When it stops being editable |
|---|---|---|---|---|
|  |  |  |  |  |

## Derived state
Recomputable outputs.

| Name | Source inputs | Persist or recompute? | Why persisting is safe/unsafe | Stale-state risk |
|---|---|---|---|---|
|  |  |  |  |  |

## Evidence state
Frozen, publishable, signed, archived, or defensible records.

| Name | Freeze trigger | Created by | Superseded/versioned? | Integrity expectations |
|---|---|---|---|---|
|  |  |  |  |  |

## Persistence boundary summary
What survives each event?

| Event | Working state | Derived state | Evidence state | Notes |
|---|---|---|---|---|
| User refresh/reload |  |  |  |  |
| App restart |  |  |  |  |
| Reprocessing/recalculation |  |  |  |  |
| Publication/archive |  |  |  |  |
| Restore from backup |  |  |  |  |

## Overwrite and recovery rules
Describe what may be overwritten, versioned, retried, superseded, or reconstructed.

Fill in:

## Notes for the agent
- Challenge permanent storage of recomputable data.
- Verify that evidence state cannot be silently overwritten.
- If working and evidence state are mixed, flag it as a design risk.
