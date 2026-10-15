# Aquilonny test automation framework

[![Tests](https://github.com/AliceManenok/aquilonny-test-framework/actions/workflows/tests.yml/badge.svg)](https://github.com/AliceManenok/aquilonny-test-framework/actions/workflows/tests.yml)
· [Latest test reports](https://alicemanenok.github.io/aquilonny-test-framework/)

## Overview

A test automation framework for a lease-processing platform: a user uploads a PDF lease,
OCR and an LLM extract its fields, and the user reviews the result. The platform is not
built yet, so the example tests run against public demo apps: **Restful-Booker** (API),
**Sauce Demo** and **The Internet** (UI). The framework itself carries over unchanged.

**Stack:** Python 3.13 · pytest · httpx + pydantic (API) · Playwright (UI) ·
pydantic-settings (config) · Faker (test data) · ruff + pre-commit (code quality) ·
GitHub Actions + GitHub Pages (CI and reports).

## Quick start

```powershell
git clone https://github.com/AliceManenok/aquilonny-test-framework.git
cd aquilonny-test-framework
python -m venv .venv
.venv\Scripts\Activate.ps1                # Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements.txt
python -m playwright install chromium
python -m pre_commit install              # ruff runs before every commit
copy .env.example .env                    # then fill in API_USERNAME and API_PASSWORD
```

The Restful-Booker login is the public one from its API docs; Sauce Demo accounts are in
`test_data/users.json`.

| Run | Command |
| --- | --- |
| everything | `python -m pytest` |
| API and settings tests | `python -m pytest -m "not ui"` |
| UI tests, 4 workers | `python -m pytest -m ui -n 4` |
| smoke only | `python -m pytest -m smoke` |
| watch the browser | `python -m pytest -m ui --headed --slowmo 500` |
| another environment | `$env:TEST_ENV = "dev"; python -m pytest` (needs `config/dev.env`) |
| HTML report | add `--html=reports/report.html --self-contained-html` |
| trace of a failed UI test | `python -m playwright show-trace test-results/<test>/trace.zip` |

Use `python -m ...` rather than bare `pytest` or `playwright`: Windows Application Control
can block the unsigned `.exe` launchers in `.venv\Scripts`.

## Project structure

```
config/              demo.env (public demo targets), dev.env.example (platform template)
framework/
  config.py          Settings: typed settings per TEST_ENV, secrets from .env or env vars
  api/clients/       BaseApiClient (URL, timeout, logging) → BookingClient (one method per endpoint)
  api/models/        strict pydantic models = the API contract
  ui/pages/          BasePage (abstract) → LoginPage, InventoryPage, UploadPage
  ui/components/     HeaderComponent, shared by pages through composition
  utils/             data_factory.build_booking(), polling.wait_until()
tests/
  conftest.py        settings fixture, quiet library loggers
  api/               API fixtures (clients, token, bookings with cleanup) and tests
  ui/                page fixtures, test data fixtures and tests
test_data/           users.json, files/sample_lease.pdf
.github/workflows/   tests.yml: lint → API ‖ UI → publish reports
```

## Adding tests

- **API:** add a method to a client (or a new client inheriting `BaseApiClient`), a model in
  `framework/api/models/`, then a test in `tests/api/` that gets data from `build_booking()`
  or a fixture and validates responses with the model.
- **UI:** add a page object inheriting `BasePage` (`path`, locators in `__init__`,
  `expect_loaded()`, user actions), a fixture in `tests/ui/conftest.py`, then a test in
  `tests/ui/`.
- **Conventions:** names say what is checked (`test_update_booking_without_token_is_forbidden`);
  every file has an `api` or `ui` marker, `smoke` only for critical and fast checks;
  Arrange / Act / Assert; asserts live in tests, not in clients or pages; no `sleep` —
  `expect(...)` in UI, `wait_until(...)` for async processes; each test owns its data and
  cleans it up through a `yield` fixture; locators: test id → role and name → CSS → XPath.

## Architecture decisions

| Decision | Why |
| --- | --- |
| Layers: tests → framework → config | tests describe scenarios; URLs, locators and auth change in one place |
| Settings via pydantic-settings and `TEST_ENV` | one typed source, fails fast on a missing value; env vars override files, so CI injects secrets |
| API client returns raw responses | tests own every assert, negative ones (403, 404) included |
| Strict models, extra fields forbidden | one call checks the whole contract; `"150"` instead of `150` is a bug |
| Faker data factory with overrides | a test states only what matters to it; unique data allows parallel runs |
| Function-scoped data with `yield` cleanup; separate clients with and without a token | no shared mutable state, tests are order-independent |
| Playwright + Page Object Model | auto-waiting, traces, network mocking; layout changes are fixed in page objects |
| `wait_until` instead of `sleep` | waits exactly as long as needed and fails with the last value seen |
| ruff + pre-commit + lint in CI; pinned versions | the same checks locally and on the server; reproducible environments |

## CI & reports

`.github/workflows/tests.yml` runs on every push and pull request to `main`, every night,
and by hand ("Run workflow", suite `all` or `smoke`):

```
lint (pre-commit) → api-tests ‖ ui-tests → publish-report (main only)
```

- HTML and JUnit reports are uploaded as artifacts on every run; a results summary is shown
  on the run page; traces and screenshots are uploaded only when a UI test fails.
- The latest reports of `main` are published to
  [GitHub Pages](https://alicemanenok.github.io/aquilonny-test-framework/).
- `API_USERNAME` and `API_PASSWORD` come from GitHub Secrets as environment variables.
- Parallel runs with `-n auto`; `--reruns 1` in CI only, and reruns are visible in reports.

## Test strategy: where tests run

- **Every pull request:** lint, unit and contract checks, API smoke tests — minutes, blocks the merge.
- **After a deploy to a test environment:** end-to-end flows on real services (upload → processing → review).
- **Nightly:** full regression, all browsers, LLM accuracy on the golden dataset.

Where a test runs is decided by its folder and markers, so tests are not rewritten per pipeline.

## Testing async document processing

- Upload returns `202 Accepted`; the test polls the document status with `wait_until`
  (timeout = processing SLA + margin) until `ready_for_review` or `failed`.
- Only valid state transitions are allowed, and every document reaches a final state.
- Error paths: invalid files, size limits, OCR/LLM timeouts and 429 with retries,
  duplicate uploads, concurrent uploads, access to another tenant's document.
- Most of the pipeline is tested with fake OCR and LLM for speed and determinism; a small set
  runs against real Azure services.

## Testing LLM extraction accuracy

- Every response is validated against a strict schema (pydantic), on every run.
- Accuracy is measured on a versioned golden dataset of labeled leases: precision, recall
  and F1 per field, hallucinations and misses, share of documents with all critical fields right.
- Comparison depends on the field type: exact after normalization for dates and amounts,
  fuzzy for names and addresses, semantic or LLM-as-judge for free text.
- OCR errors are separated from LLM errors (CER/WER); stability is checked with repeated runs
  at temperature 0; prompt injection inside a lease must not change the result.
- Thresholds act as a quality gate on nightly runs and on every model or prompt change;
  user corrections in production extend the golden dataset.

## Traceability & quality gates (Azure DevOps)

- User story → requirement-based suite in Azure Test Plans → test cases linked to these tests.
- The pipeline publishes JUnit XML with `PublishTestResults`; results land in Test Runs per story.
- Exit criteria: all smoke tests green and the pass rate above the agreed threshold; part of the
  Definition of Done and enforced by branch policies.
- Moving to Azure Pipelines changes only the pipeline file: same commands, secrets from a
  variable group or Key Vault as environment variables.

## What's next

- A lock file for transitive dependencies (pip-tools or uv) and mypy for static type checks.
- Split `Settings` into API and UI parts if UI tests stop needing the API login.
- Contract tests from the platform's OpenAPI spec; an LLM evaluation suite in `tests/llm_eval/`.
- Cache Playwright browsers in CI; an `azure-pipelines.yml` once an Azure DevOps project exists.
