# Business Requirements Document — sas-ci360-solutions

| | |
| --- | --- |
| Document | BRD-CI360SOLUTIONS-1.0 |
| Owner | Nelson Grey LLC |
| Scope | Layer 3 of the CI360 Connect toolkit: identity-bridge and reporting orchestration |
| Basis | Adapted from the CI360 Connect BRD/TRD/DD (v1.1, 2026-09-20), scoped to this repository |
| Related | [sas-ci360-sdk BRD](https://github.com/mnelson3/sas-ci360-sdk/blob/main/docs/BRD.md) (Layers 1–2, this repo's foundation) |

## 1. Executive summary

`sas-ci360-solutions` is the reference orchestration layer built on top of `sas-ci360-sdk`'s client packages — specifically, the identity-bridge cycle: upload a chain file to CI360, pull the resulting import-request-job status, and email a status/support distribution list with the outcome. It runs as a Windows Service or a Linux systemd daemon, polling on a configurable interval.

## 2. Business context

An implementer who needs more than a single API call — an actual scheduled, unattended business process composed from several API calls — needs a worked example of how the individual clients compose together, not just documentation of each one in isolation. This repository is that example: it demonstrates composing `sol-data` (Marketing Data API: import-request-jobs, file-transfer-location, tables) with `api-core`'s `Communication` (email) and `Reporter` (JSON audit trail) primitives into a real, schedulable business process.

It was rebuilt during the 2026-09-20 monorepo consolidation, replacing an earlier `automation-engine` generation (archived) that duplicated Connection/Security/Reporter logic instead of depending on `api-core`.

## 3. Goals & objectives

| ID | Objective | Primary metric |
| --- | --- | --- |
| BG-1 | Provide a working, runnable reference implementation of identity-bridge synchronization. | End-to-end cycle runnable from a fresh clone |
| BG-2 | Run unattended, on a schedule, as a real OS service (Windows and Linux). | Both service wrappers present and tested |
| BG-3 | Every operation verifiable without a live tenant or SMTP server. | 95% line coverage on `src/` (achieved 2026-09-20) |
| BG-4 | No dead or broken code left in the tree pretending to be a feature. | 0 unimportable modules (2 were found and removed — see TRD.md) |

## 4. Stakeholders

- **Implementation engineer** deploying identity-bridge automation for a real client tenant.
- **Operations / on-call** — the audience for `logs/service.log` and the status/support email distribution lists this process sends to.

## 5. Scope

### In scope
The identity-bridge cycle: chain-file upload, import-request-job status polling, status/support email notification, JSON audit reporting. The Windows Service and Linux systemd wrappers that run it unattended. The `Standard` configuration class every module in this repository depends on.

### Explicitly out of scope
- Content-delivery and Plan API orchestration — unfinished, broken stub modules for both existed in this repository previously (`content/`, `planning/`) and were removed 2026-09-20 rather than fixed or kept, since neither could even be imported and neither was referenced by any functional requirement. See `docs/DDD.md` for the full history if either is picked back up.
- The Plan connector framework itself — that's `sas-ci360-plan-connector`, a separate repository.
- Anything not related to the identity-bridge use case.

## 6. Business requirements

| ID | Requirement | Priority |
| --- | --- | --- |
| BR-1 | The identity-bridge cycle must be runnable end-to-end as a reference for composing individual API clients into a real business process. | P1 |
| BR-2 | Configuration must fail safely (fallback defaults, never a crash) when no `config/config.ini` is present. | P1 |
| BR-3 | A dropped chain file must be moved out of the watched location immediately, not after the cycle completes, so a new file can be dropped mid-cycle. | P2 |
| BR-4 | Code that can't even be imported must not be left in the source tree implying a working feature. | P1 (real finding, see TRD.md) |

## 7. Success metrics

Same categories as the parent SDK — see [sas-ci360-sdk/docs/BRD.md](https://github.com/mnelson3/sas-ci360-sdk/blob/main/docs/BRD.md) §7 — applied to this repository's own scope: time-to-first-cycle, test signal quality, CI health, and (new for this repo) 0 unimportable modules.

## 8. Assumptions & constraints

- CI360 processes an import request job asynchronously in the background after upload; `CI360Main` does not block waiting for that job to finish — the cadence decision (how often to poll) belongs to whatever schedules calls into it.
- Depends on `sasci360soldata` (`sol-data`) and `sasci360apicore` (`api-core`) from `sas-ci360-sdk`, pulled via a pinned VCS reference to that public repository.

## 9. Licensing

Nelson Grey LLC Community License 1.0 — see [LICENSE](../LICENSE).
