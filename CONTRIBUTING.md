# Contributing

## Setup

```bash
poetry install
pre-commit install
```

## Git workflow

We maintain a **linear history**. No merge commits.

1. Create a feature branch from `main`
2. Make your changes — commit often, these will be squashed
3. Before opening a PR/MR, rebase onto `main`:
   ```bash
   git fetch origin
   git rebase origin/main
   ```
4. Open a pull/merge request against `main`
5. Merge using **squash merge** — the PR/MR title becomes the commit message

## Commit messages

We follow [Conventional Commits](https://www.conventionalcommits.org/). This is enforced by `gitlint` in CI.

Format: `<type>: <description>`

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`

Examples:
```
feat: add user authentication
fix: resolve race condition in data loader
docs: update API usage examples
refactor: extract validation logic into service
```

## Code standards

- Linting and formatting: **Ruff** (runs via pre-commit)
- Type checking: **Pyright**
- Docstrings: **Google** style
- Tests go in `tests/`, mirroring the `app/` structure

Run all checks locally:
```bash
pre-commit run --all-files
pytest --cov
```
