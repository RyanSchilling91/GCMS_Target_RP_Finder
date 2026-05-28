\# ADR-0005 - Use Password-Only Admin Challenges as a Near-Term Protected-Action Bootstrap



\## Status

\- Accepted



\## Decision

For the current hardening phase, protected admin actions use a password-only challenge rather than separately managed in-app admin usernames or enterprise identity.



The acting person is still recorded from the workstation identity already captured by the application. The password challenge is an additional control for protected actions, not the sole source of attribution.



A bootstrap fallback credential is intentionally retained during the near-term phase so protected actions do not become unrecoverable in restricted/offline environments. Additional admin passwords may be added through the governed admin path and stored only as salted password hashes.



This ADR is a near-term operational exception, not a long-term target security model.



\## Context

The project currently operates in a constrained environment without a reliable enterprise identity provider and without a mature account lifecycle for distinct in-app admin users.



At the same time, certain actions must remain governed and recoverable, including:

\- force unlock

\- criteria governance

\- controlled reopen from published evidence

\- other protected administrative workflow actions



The project cannot safely leave those actions unguarded, but it also cannot assume a fully managed identity solution yet. A practical bootstrap mechanism is therefore needed so the workflow remains operable while stronger identity options remain unavailable.



\## Alternatives considered

\- Require unique named admin accounts now:

&#x20; - Rejected because the current environment does not yet support a manageable provisioning, reset, and recovery lifecycle.



\- Keep only environment-variable-backed credentials:

&#x20; - Rejected because that makes credential recovery and governed administration too brittle for real operations.



\- Allow protected actions with no credential challenge:

&#x20; - Rejected because it weakens control, auditability, and trust in governed actions.



\- Delay protected actions until stronger auth exists:

&#x20; - Rejected because the workflow must remain usable in the current environment.



\## Why chosen

This approach keeps protected admin actions available in the current environment without pretending the project already has a complete long-term identity model.



It preserves a recoverable near-term control path, supports offline/restricted deployment, and allows the workflow to function while stronger authentication approaches remain deferred.



Just as importantly, it keeps this decision explicitly temporary and reviewable rather than letting an emergency workaround become an unspoken permanent standard.



\## Consequences

\- Easier:

&#x20; - Protected actions remain available in restricted/offline operation.

&#x20; - The team is not blocked on enterprise identity before continuing hardening work.

&#x20; - Recovery remains possible if supplemental passwords are lost.



\- Harder:

&#x20; - Security remains based on a shared secret model rather than fully individualized credential attribution.

&#x20; - This decision must be carefully documented as temporary so it does not quietly harden into a permanent norm.



\- Requires:

&#x20; - Workstation identity must still be captured as the acting user context.

&#x20; - Protected actions must log actor, reason, and governed action path.

&#x20; - Supplemental stored passwords must be hashed rather than recoverable in plaintext.

&#x20; - The bootstrap credential policy must be treated as local to this project and deployment phase, not as a reusable default for future projects.



\- Important limitation:

&#x20; - This ADR does not claim that password-only shared-secret control is the desired long-term security posture. It exists to keep the governed workflow operational until stronger identity controls are available.



\## Review trigger

Revisit this ADR if any of the following become true:

\- enterprise identity or centrally managed secrets become available

\- the app gains a practical lifecycle for individually attributable admin accounts

\- governance requirements tighten beyond what a shared-secret bootstrap model can reasonably support

\- the project exits the hardening/bootstrap phase and is preparing for a more production-grade security posture

