# Technical Requirements Document — sas-ci360-solutions

| | |
| --- | --- |
| Document | TRD-CI360SOLUTIONS-1.0 |
| Owner | Nelson Grey LLC |

## 1. Overview & traceability

| BRD | TRD | Relationship |
| --- | --- | --- |
| `CI360SOLUTIONS-BR-1` | `CI360SOLUTIONS-FR-1` | Runnable end-to-end cycle → `CI360Main.run_identity_bridge_cycle` / `check_and_run`. |
| `CI360SOLUTIONS-BR-2` | `CI360SOLUTIONS-NFR-1` | Safe config fallback → `Standard`'s `_by_mode` and per-field fallback defaults. |
| `CI360SOLUTIONS-BR-4` | `CI360SOLUTIONS-NFR-2` | No unimportable modules → `content/`/`planning/` removed. |

## 2. Functional requirements

| ID | Requirement | Class / method |
| --- | --- | --- |
| `CI360SOLUTIONS-FR-1` | Run one identity-bridge cycle: upload a chain file (or send a no-op status if none given), pull the import-request-job report, email the outcome. | `CI360Main.run_identity_bridge_cycle(file_name=None)` |
| `CI360SOLUTIONS-FR-2` | Check the configured drop location for a new chain file; if present, move it out immediately and run a full cycle for it; if not, run the no-op status cycle. | `CI360Main.check_and_run()` |
| `CI360SOLUTIONS-FR-3` | Independent weekly check: if a manually dropped change file is present, email it to SAS Technical Support. | `CI360Main.run_support_check()` |
| `CI360SOLUTIONS-FR-4` | Upload a chain file to CI360 via `sol-data`'s file-transfer-location signed-URL flow. | `identity_data.UploadIdentityBridgeData.run()` |
| `CI360SOLUTIONS-FR-5` | Pull the import-request-job report for the identity-bridge table and build a status summary. | `identity_data.CreateIdentityBridgeReports.run()` |
| `CI360SOLUTIONS-FR-6` | Email the status distribution list with the cycle's outcome. | `identity_data.SendIdentityBridgeStatusMessage.run()` |
| `CI360SOLUTIONS-FR-7` | Email SAS Technical Support with a manually dropped support/change file. | `identity_data.SendIdentityBridgeSupportMessage.run()` |
| `CI360SOLUTIONS-FR-8` | Run the cycle unattended, on a poll interval, as a Windows Service or Linux systemd daemon. | `SASCI360Service`, `UnixService` |

## 3. Non-functional requirements

| ID | Category | Requirement | Status (2026-09-20) |
| --- | --- | --- | --- |
| `CI360SOLUTIONS-NFR-1` | Configurability | `Standard` must provide safe fallback defaults for every config field when no `config/config.ini` is present, and select dev/test/production variants from comma-separated `_arr` values. | Verified: `docs/TRD.md`'s parent repo `CI360SOLUTIONS-NFR-6` equivalent; `standard.py` at 100% line coverage as of 2026-09-20 (was 48%, and had no dedicated test file at all before then). |
| `CI360SOLUTIONS-NFR-2` | Maintainability | No module in this repository may be unimportable — dead code implying a working feature is worse than no code. | **Real finding**: `content/__init__.py` and `planning/__init__.py` both imported a `Main` class that no longer existed after `main.py` was rewritten to `CI360Main` during this repository's own identity-bridge rebuild — neither could even be imported. Removed 2026-09-20 (confirmed with the repository owner) rather than fixed or left flagged, since neither was referenced anywhere else and neither's original intent (finished feature vs. abandoned exploration) survived to make that call otherwise. |
| `CI360SOLUTIONS-NFR-3` | Testability | `SASCI360Service` (Windows) must be testable even though pywin32 is genuinely unavailable outside Windows. | **Fixed**: stubbed `win32event`/`win32service`/`win32serviceutil`/`servicemanager` via `sys.modules` injection — the same convention `sol-identity` (in `sas-ci360-sdk`) established for an uninstalled private dependency. 0% → 98% coverage (everything but the `__main__` guard). |
| `CI360SOLUTIONS-NFR-4` | Testability | `UnixService` (Linux) must be directly testable, not just importable. | **Fixed**: 0% → 62% (everything but the `__main__` CLI dispatcher — `start`/`stop`/`status`). |

## 4. Integration requirements

Depends on `sasci360soldata` (Marketing Data API) and `sasci360apicore` (auth, email, JSON reporting) from `sas-ci360-sdk`, installed via a pinned VCS reference to that public repository (`sasci360soldata @ git+https://github.com/mnelson3/sas-ci360-sdk.git@main#subdirectory=packages/sol-data`, similarly for `sasci360apicore`).

## 5. Data requirements

`Standard` reads `config/config.ini` (see `config/config.ini.example`), sections `[EMAIL]`, `[FILES]`, `[IDENTITIES]`, `[PATHS]`, `[SETTINGS]`. Every field has a fallback default; `host`/`secret_key`/`tenant_id`-equivalent identity fields fall back to `"changeme"` rather than a real-looking placeholder, so a misconfiguration is visibly broken rather than silently wrong.

## 6. Technology stack

Python 3.8+, `sasci360soldata`/`sasci360apicore` (from `sas-ci360-sdk`), `service` (Unix daemon framework), `pywin32` (Windows service framework, platform-gated in `requirements.txt` via `sys_platform == "win32"`), `python-daemon`, `python-dateutil`.

## 7. Environments

`Standard(mode="development"|"test"|"production")` selects dev/test/production variants of any config field that has a corresponding `_arr` (comma-separated) value; fields without an `_arr` value use the same bare value regardless of mode.

## 8. Dependency policy

Same `CI360SOLUTIONS-NFR-8` pattern as `sas-ci360-sdk` — a dependency is declared only if the code that declares it actually imports it. `pywin32` is platform-gated so it's never required outside Windows.

## 9. Testing strategy

Unit tests inject fakes via constructor keyword arguments (`standard`, `client`, `reporter`, `communication`) rather than patching module internals — see `README.md` §Writing Tests for the pattern. `src/` overall: 95% line coverage, 82 tests, as of 2026-09-20 (was 65% before this session's testing pass).

Live-tenant / UAT coverage is not yet implemented for this repository — see [sas-ci360-sdk/UAT.md](https://github.com/mnelson3/sas-ci360-sdk/blob/main/UAT.md) §What's covered, which names this repository as follow-up work rather than silently omitted.

## 10. CI/CD requirements

Same four-gate workflow as `sas-ci360-sdk` — flake8, mypy, pytest with coverage, clean-environment install — plus `pre-commit` hooks (black, isort, flake8, mypy, bandit) enforced locally before a commit lands.
