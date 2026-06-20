# CI Pipeline Comparison Baseline

This project now includes equivalent CI definitions for:

- GitHub Actions: `.github/workflows/ci.yml`
- GitLab CI/CD: `.gitlab-ci.yml`
- Bitbucket Pipelines: `bitbucket-pipelines.yml`

## Functional Scope (kept equivalent)

Each provider runs the same two checks:

1. Frontend validation
   - Install dependencies (`npm ci`)
   - Lint (`npm run lint`)
   - Build (`npm run build`)
2. Backend validation
   - Install dependencies (`pip install -r requirements.txt` + `pytest`)
   - Run tests (`pytest app/tests -q`)

## Runtime Baseline

- Node.js: `22`
- Python: `3.11`
- Backend test env:
  - `DATABASE_URL=postgresql+psycopg://postgres:postgres@<host>:5432/notes_test`
  - `SECRET_KEY=ci-secret-key`
  - `ACCESS_TOKEN_EXPIRE_MINUTES=30`

## Branch and PR/MR Behavior

- GitHub Actions:
  - Runs on `push` and `pull_request` for any branch via `branches: ["**"]`.
- GitLab CI/CD:
  - Runs on branch pushes and merge request pipelines through `workflow: rules`.
  - Tag pipelines are intentionally excluded in this baseline.
- Bitbucket Pipelines:
  - Runs on all branch pushes and all pull requests via `branches: "**"` and `pull-requests: "**"`.

## Platform Limitations and Applied Adjustments

1. Trigger model differences
   - Providers do not share identical event semantics.
   - Adjustment applied: each file uses the native trigger model while preserving equivalent branch and PR/MR coverage.

2. Cache behavior is provider-specific
   - Cache performance and invalidation logic differ by platform.
   - Adjustment applied: provider-native caching is configured for npm and pip where available.

3. Secret management differs by platform
   - Secret injection UX and scoping vary.
   - Adjustment applied: only non-sensitive CI defaults are committed; production secrets should be set in each provider UI.

4. Service container networking differs by provider
   - Hostname conventions are not identical across GitHub, GitLab, and Bitbucket.
   - Adjustment applied:
     - GitHub Actions uses `localhost` for the mapped Postgres port.
     - GitLab CI/CD uses service alias hostname `postgres`.
     - Bitbucket Pipelines uses `127.0.0.1` for service access.

## Next Extension (optional)

If you want a deeper benchmark, add the same extra stages on all three providers:

- Security scan (dependency and SAST)
- Test coverage upload
- Build artifact upload
- Deployment preview stage
