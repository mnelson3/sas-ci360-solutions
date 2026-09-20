# Detailed Design Document — sas-ci360-solutions

| | |
| --- | --- |
| Document | DDD-CI360SOLUTIONS-1.0 |
| Owner | Nelson Grey LLC |

## Architecture overview

Layer 3 of the CI360 Connect toolkit — see [sas-ci360-sdk/docs/DDD.md](https://github.com/mnelson3/sas-ci360-sdk/blob/main/docs/DDD.md) for the full 4-layer picture. This repository composes Layer 2 clients (`sol-data`) and Layer 1 primitives (`api-core`'s `Communication`, `Reporter`) into a scheduled business process; it does not reimplement HTTP, auth, or retry logic itself.

```
Service Layer (UnixService.py / SASCI360Service.py)
        │  poll interval, sigterm/stop-event handling
        ▼
CI360Main (main.py)
        │  run_identity_bridge_cycle() / check_and_run() / run_support_check()
        ▼
identity_data/  (Upload, CreateReports, SendStatusMessage, SendSupportMessage)
        │
        ▼
sol-data client (sas-ci360-sdk)  +  api-core Communication / Reporter
```

## `CI360Main` — dependency injection over patching

Every collaborator (`standard`, `upload`, `create_reports`, `send_status`, `send_support`) is accepted as a constructor keyword argument, defaulting to a real instance if not given:

```python
def __init__(self, **kwargs):
    self.standard = kwargs.get("standard") or Standard(mode=self.mode)
    self.upload = kwargs.get("upload") or UploadIdentityBridgeData(mode=self.mode, standard=self.standard)
    ...
```

This is why `tests/TestMain.py` never needs to patch module internals — it constructs `CI360Main` with `MagicMock()` collaborators directly. Every test file added or extended in this repository during 2026-09-20's testing pass follows the same principle: prefer real objects and explicit dependency injection over patching, and reach for `unittest.mock.patch` only where a real dependency (pywin32, a live tenant, SMTP) genuinely can't be constructed in a test environment.

## The removed content/planning modules

Both `content/__init__.py` and `planning/__init__.py` did `from sasci360solutions.main import Main` — a class that stopped existing when `main.py` was rewritten to `CI360Main` during this repository's own identity-bridge rebuild. Neither module could be imported at all; `Content.__init__` did nothing but print a value, and `Planning.__init__` made a live, untested network call (`self.root.get_root()`) in its constructor. Neither was referenced anywhere else in `src/` or `tests/`, and neither was named in any functional requirement in this document or its predecessor. Confirmed with the repository owner and removed 2026-09-20 (`git rm`) rather than fixed or kept — fixing them would have meant guessing at unfinished intent (a real content-delivery/Plan integration, or an abandoned exploration) that nothing in the codebase or history settled either way.

## `SASCI360Service` — testing a Windows-only module elsewhere

`SASCI360Service.py` imports `servicemanager`, `win32event`, `win32service`, `win32serviceutil` at module level — real dependencies of the deployed Windows service, genuinely unavailable outside Windows (including this repository's own CI, `ubuntu-latest`). `tests/TestSASCI360Service.py` registers minimal fake modules for all four directly in `sys.modules` before importing the real module:

```python
def _install_fake_module(dotted_name):
    if dotted_name in sys.modules:
        return sys.modules[dotted_name]
    module = types.ModuleType(dotted_name)
    sys.modules[dotted_name] = module
    if "." in dotted_name:
        parent_name, attr = dotted_name.rsplit(".", 1)
        parent = _install_fake_module(parent_name)
        setattr(parent, attr, module)
    return module
```

This is the same technique `sol-identity` (in `sas-ci360-sdk`) established for its own uninstalled private dependency, generalized here to a whole namespace package (`win32.win32event`, `win32.lib.win32serviceutil`) rather than a single module. `SvcStop`, `SvcDoRun`, and `main`'s poll loop are all exercised this way, with `win32event.CreateEvent`/`WaitForSingleObject`/`SetEvent` patched per-test to control the fake event/stop-signal behavior.

## `UnixService` — testing the poll loop

`run()` imports `CI360Main` lazily (inside the method, not at module level) so it can be swapped via `sys.modules` injection per test; `got_sigterm()` and `time.sleep` are patched directly to make the poll loop terminate deterministically after a fixed number of iterations instead of running forever.

## `Standard` — testing config fallback deterministically

`Standard` computes its config-file path from a module-level `root_path` set at import time. Tests monkeypatch that variable to point at an empty `tmp_path` per test, so the fallback-default behavior (NFR-6-equivalent, see TRD.md) is exercised deterministically regardless of whether the machine running the tests happens to have a real `config/config.ini` checked out locally — the only way to test "no config file present" reliably without that risk.

## CI/CD pipeline

Same four-gate GitHub Actions workflow as `sas-ci360-sdk`, plus local `pre-commit` hooks (black, isort, flake8, mypy, bandit) that run on every commit — see `README.md` §Code Quality Tools.
