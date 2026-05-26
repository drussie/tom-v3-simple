# Repo Branch Hygiene

## Current Status

As of Milestone 1A, GitHub reports the default branch as:

```text
main
```

The Milestone 0 branch/default branch issue is resolved.

## Recommended Final State

```text
main = consolidated Milestone 0 baseline
default branch = main
milestone codex branches = preserved or deleted by owner preference
```

## Exact Cleanup Steps

If this issue reappears after future branch work:

```bash
git fetch origin --prune
git switch codex/m0e-integration-qa-repo-consolidation
git pull --ff-only
git switch -c main
git push -u origin main
```

Then set GitHub's default branch to `main`.

With GitHub CLI:

```bash
gh auth login
gh repo edit drussie/tom-v3-simple --default-branch main
git remote set-head origin -a
```

Or use the GitHub UI:

```text
Repository -> Settings -> Branches -> Default branch -> switch to main
```

## Optional Milestone Branch Cleanup

Keep milestone branches if they are useful as durable handoff history.

If the owner wants only tags plus `main`, delete old remote branches after confirming tags exist:

```bash
git push origin --delete codex/m0a-repo-memory-architecture-schema
git push origin --delete codex/m0b-backend-api
git push origin --delete codex/m0c-worker-synthetic-pipeline
git push origin --delete codex/m0d-visual-evidence-viewer
git push origin --delete codex/m0e-integration-qa-repo-consolidation
```

Do not delete milestone branches until the consolidated `main` branch and milestone tags are confirmed on GitHub.
