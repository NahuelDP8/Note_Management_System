# CI Benchmark Guide (GitHub vs GitLab vs Bitbucket)

## Objective

Measure comparable CI performance across providers using the same project tasks.

## What is measured

Each provider records a CSV artifact with task durations (seconds):

- `cache_restore_time`
- `frontend_pnpm_install`
- `frontend_lint`
- `frontend_build`
- `backend_pip_install`
- `backend_pytest_install`
- `backend_pytest`
- `cache_save_time`

GitHub Actions measures `cache_restore_time` and `cache_save_time` around explicit `actions/cache/restore` and `actions/cache/save` steps.
GitLab CI/CD and Bitbucket Pipelines restore and save native caches outside the user script, so their CSV records `0` for those cache boundary metrics and the provider logs should be used for exact native cache transfer timing.

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
   - Install-time delta between cold and warm runs
   - Failure rate (%)
   - Queue/wait time (from provider UI)

## Cache Interpretation

GitHub Actions:

- Frontend cache path: pnpm global store.
- Frontend cache key: OS + `frontend/pnpm-lock.yaml` hash.
- Backend cache path: pip cache directory.
- Backend cache key: OS + `backend/requirements.txt` hash.
- Cache invalidation happens when the corresponding lockfile or requirements file changes.

GitLab CI/CD:

- Frontend cache path: `frontend/.pnpm-store/`.
- Frontend cache key: `frontend-${CI_COMMIT_REF_SLUG}`.
- Backend cache path: `.cache/pip/`.
- Backend cache key: `backend-${CI_COMMIT_REF_SLUG}`.
- Cache invalidation happens when the branch slug changes, or when caches are manually cleared.

Bitbucket Pipelines:

- Frontend cache path: `frontend/.pnpm-store`.
- Frontend cache name: `pnpm`.
- Backend cache path: `~/.cache/pip`.
- Backend cache name: `pip`.
- Cache invalidation is managed by Bitbucket for each named cache; clear caches manually for an explicit cold run.

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
