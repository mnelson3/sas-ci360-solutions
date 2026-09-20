# Implementer Guide — sas-ci360-solutions

This guide is about *deploying and extending* the identity-bridge service. For contributing to this codebase itself (dev environment setup, code quality tools, writing tests), see the "Developer/Implementation Guide" section in [`README.md`](README.md). For requirements and design rationale, see [`docs/`](docs/).

## 1. What this actually does

One cycle, on a schedule:

1. Check a watched drop location for a chain file.
2. If present: move it out immediately, upload it to CI360 via a signed URL, poll the resulting import-request-job, email a status distribution list with success/failure.
3. If absent: send a "no chain file processed today" status update instead of contacting CI360 at all.

There's a second, independent check (`run_support_check`) for a manually dropped support/change file, meant to run on its own (weekly) cadence, emailing it to SAS Technical Support.

Nothing here blocks waiting for CI360 to finish processing the import request — that happens asynchronously on CI360's side. The polling cadence is a property of *how often you schedule this process*, not of any code in this repository.

## 2. Configure before you run anything

```bash
cp config/config.ini.example config/config.ini
```

Edit the `[IDENTITIES]` section with your real `identity_bridge_table_id`, `secret_key`, `tenant_id`; `[PATHS]` with your real `export_path`/`export_post_path` (where chain files get dropped); `[EMAIL]` with a real SMTP server and status/support distribution lists. Everything has a fallback default so a missing file doesn't crash — but every default is an obviously-fake placeholder (`"changeme"`, `noreply@example.com`), not something that will work against a real tenant. See `docs/TRD.md` §5 for the full field list.

## 3. Run it once, manually, before scheduling it

```python
from sasci360solutions.main import CI360Main

app = CI360Main(mode="test")   # or "development" / "production" - see Standard's mode handling
app.check_and_run()
```

This is the same thing the service wrappers call in a loop. Running it once by hand first, against a `test`-mode tenant, is the fastest way to confirm your `config.ini` is actually correct before trusting a scheduled service to run it unattended.

## 4. Deploy as a service

**Linux (systemd)**:
```bash
sudo cp src/sas_ci360_solutions.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now sas_ci360_solutions
```
Or run it directly: `python src/UnixService.py start` (see `src/UnixService.py`'s `__main__` block for `start`/`stop`/`status`).

**Windows**:
```bash
python src/SASCI360Service.py install
python src/SASCI360Service.py start
```

Both wrappers poll every 300 seconds (`UnixService.POLL_INTERVAL_SECONDS`; `SASCI360Service.main`'s `WaitForSingleObject(..., 300000)`) by default. Change the constant/literal directly if you need a different cadence — there's no config-file knob for it currently.

## 5. Extending this to a new use case

This repository is meant to be read as a worked example of composing `sas-ci360-sdk` clients, not just used as-is. If you're building a different scheduled orchestration (say, a Digital Assets sync job instead of identity-bridge):

- Follow `CI360Main`'s dependency-injection pattern: accept every collaborator as a constructor kwarg with a real default, so your orchestration class is testable the same way `TestMain.py` tests this one — no patching module internals.
- Compose Layer 2 clients (`sol-data`, or whichever `sas-ci360-sdk` package fits), don't reimplement their HTTP or auth logic.
- Use `api-core`'s `Reporter`/`Communication` for audit persistence and notification, the same way `identity_data/` does, rather than writing your own.
- If it needs to run unattended, copy `UnixService.py`/`SASCI360Service.py`'s shape rather than writing OS-service integration from scratch.

**Two modules that used to live here — `content/` and `planning/` — were unfinished stubs for exactly this kind of extension** (Digital Assets and Plan API orchestration, respectively) and were removed 2026-09-20 because both were broken (see `docs/DDD.md`). If you're picking either use case back up, treat it as a fresh implementation following the pattern above, not as a fix to the removed code — neither ever had a working `run()` method or a test.

## 6. Common pitfalls

- **Don't assume `check_and_run()` blocks until CI360 finishes processing.** It doesn't, by design — see §1.
- **Don't skip the fallback-default warning.** A `config.ini` with `secret_key = changeme` will construct a client just fine and fail loudly on the first real API call, not at startup — check your config before trusting the service is actually configured, not just that it started.
- **Don't run this against production without testing in `mode="test"` first.** `Standard(mode=...)` exists precisely so you can point every environment-sensitive field (secret, tenant, path) at a test tenant during development.
