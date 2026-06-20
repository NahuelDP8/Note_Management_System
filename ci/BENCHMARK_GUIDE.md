# CI Benchmark Guide (GitHub vs GitLab vs Bitbucket)

## Objective

Measure comparable CI performance across providers using the same project tasks.

## What is measured

Each provider records a CSV artifact with task durations (seconds):

- `frontend_npm_ci`
- `frontend_lint`
- `frontend_build`
- `backend_pip_install`
- `backend_pytest_install`
- `backend_pytest`

## Artifact locations

- GitHub Actions:
  - `github-frontend-benchmark`
  - `github-backend-benchmark`
- GitLab CI/CD:
  - Job artifacts from `frontend_validate` and `backend_tests`
- Bitbucket Pipelines:
  - Step artifacts from frontend/backend steps

## Recommended benchmark protocol

1. Use dedicated branches per provider to avoid interference.
2. Run at least 10 pipelines per provider.
3. Separate analysis into:
   - Cold cache runs (first run after cache clear)
   - Warm cache runs (subsequent runs)
4. Compare:
   - Median duration per metric
   - P90 duration per metric
   - Failure rate (%)
   - Queue/wait time (from provider UI)

## Important limitations

1. Hosted runner hardware differs across providers.
2. Queue policies and regional capacity differ by time of day.
3. Cache internals are provider-specific and not fully equivalent.
4. Network path to package registries is provider-dependent.

Because of these constraints, prioritize median and P90 trends over single-run results.

## Local validation note

Local execution uses your own environment and is not directly comparable to hosted runners.
For local test execution with conda, use:

```bash
conda run -n <your_env_name> pytest app/tests -q
```
