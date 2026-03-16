---
name: gh-code-quality
description: GitHub code quality analysis — language stack, file structure, test coverage signals, CI/CD configuration, linting, complexity indicators, dependency hygiene.
---

# GitHub Code Quality Skill

Assess the structural and qualitative health of the codebase.

## Data to Collect

- `GET /repos/{owner}/{repo}/languages` → language breakdown
- `GET /repos/{owner}/{repo}/contents` → root-level file listing
- `GET /repos/{owner}/{repo}/contents/.github/workflows` → CI/CD workflow files
- Check for test directories: `test/`, `tests/`, `__tests__/`, `spec/`, `*.test.*`, `*.spec.*`
- Check for config files: `.eslintrc`, `.prettierrc`, `pyproject.toml`, `Makefile`, `jest.config.*`, `vitest.config.*`
- `GET /repos/{owner}/{repo}/contents/package.json` → if Node project, parse dependencies
- `GET /repos/{owner}/{repo}/dependency-graph/compare` → if available

## What to Analyse

### Project Structure Signals
Look for:
- Monorepo indicators (`packages/`, `apps/`, `libs/`, `turbo.json`, `nx.json`)
- Separation of concerns (`src/`, `lib/`, `components/`, `utils/`, `services/`)
- Docker/container (`Dockerfile`, `docker-compose.yml`)
- Environment management (`.env.example`, no committed `.env`)

### Test Coverage Signals (heuristic)
- Presence of test directories → +signal
- Presence of coverage config (`coverageThreshold` in jest/vitest) → strong signal
- CI/CD runs tests (look for `run: jest`, `pytest`, `npm test` in workflows)
- Badge in README mentioning coverage %

### CI/CD Quality
Count and assess GitHub Actions workflows:
- Build workflow
- Test workflow
- Lint/format workflow
- Deploy workflow
- Security scan (CodeQL, Snyk, Dependabot alerts)

### Dependency Hygiene
- Parse `package.json` / `requirements.txt` / `go.mod` if accessible
- Count total dependencies, devDependencies
- Flag if `package-lock.json` / `yarn.lock` is committed (good)
- Flag pinned vs unpinned versions

## Scoring (0–100)

| Signal | Points |
|---|---|
| Has test directory | +20 |
| CI runs tests | +20 |
| Has linting config | +10 |
| Has CI/CD workflows ≥ 2 | +15 |
| Has Dockerfile / containerization | +10 |
| Clear src structure | +10 |
| Lock file committed | +10 |
| No secrets in root | +5 |

## Output

1. Code quality score with grade
2. Tech stack summary (languages + frameworks detected)
3. CI/CD pipeline map (which workflows exist)
4. Structure quality checklist
5. Top 3 recommendations (prioritized)

## Important Note

You are doing static analysis from the file tree and metadata — not running the code. Be clear about what is inferred vs confirmed.
