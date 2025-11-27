# [PREFIX]-0001: CI/CD and TDD Infrastructure Setup

<!--
ONBOARDING AGENT: When creating this task, replace:
- [PREFIX] with the project's task prefix (e.g., AL2, PROJ)
- [DATE] with today's date (YYYY-MM-DD)
- [PROJECT-NAME] with the project name
- [LANGUAGES] section: Keep only relevant language sections
- Customize requirements based on project architecture
-->

**Status**: Todo
**Priority**: critical
**Assigned To**: feature-developer
**Estimated Effort**: 3-4 hours
**Created**: [DATE]
**Phase**: 0 (Foundation - blocks all other work)

## Overview

Set up the testing and CI/CD infrastructure for [PROJECT-NAME] so that all future development follows Test-Driven Development (TDD) practices. This foundational task must be completed before writing any feature code.

**Why this matters**: TDD catches bugs early, documents expected behavior, and makes refactoring safe. Setting this up first ensures good habits from day one and prevents accumulating untested code.

**Why feature-developer**: Planner coordinates and assigns tasks. Feature-developer implements infrastructure code. This is an implementation task.

## Existing Assets to Leverage

The starter kit includes these files - **adapt them, don't replace**:

| File | Status | Action |
|------|--------|--------|
| `tests/test_template.py` | ✅ Exists | Use as reference for test patterns |
| `.pre-commit-config.yaml` | ✅ Exists | Adapt (remove starter-kit specific hooks) |
| `tests/` directory | ✅ Exists | Add project-specific tests here |
| `pyproject.toml` | ❌ Missing | Create for Python projects |
| `.github/workflows/ci.yml` | ❌ Missing | Create CI workflow |

## Requirements

### Must Have
- [ ] **Python config**: Create `pyproject.toml` with pytest, black, ruff configuration
- [ ] **Virtual environment**: Set up and document (`python -m venv venv`)
- [ ] **Adapt pre-commit**: Update `.pre-commit-config.yaml` (remove starter-kit references)
- [ ] **Install hooks**: Run `pre-commit install`
- [ ] **Smoke test**: Create `tests/test_smoke.py` to verify project structure
- [ ] **CI workflow**: Create `.github/workflows/ci.yml`
- [ ] **Documentation**: Create `docs/TESTING.md`

### Should Have
- [ ] Test coverage reporting configured (>70% target)
- [ ] Pre-commit runs fast tests (<30 seconds)
- [ ] CI provides clear failure messages

### Nice to Have
- [ ] Coverage badge in README
- [ ] Test results summary in CI output

## Implementation Steps

### Step 1: Create `pyproject.toml`

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "[PROJECT-NAME]"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    # Add your project dependencies here
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov",
    "pytest-asyncio",
    "black",
    "ruff",
    "pre-commit",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: integration tests",
]

[tool.black]
line-length = 88
target-version = ["py310"]

[tool.ruff]
line-length = 88
select = ["E", "F", "I"]
```

### Step 2: Set Up Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -e ".[dev]"
```

### Step 3: Adapt `.pre-commit-config.yaml`

Review and update the existing file:
- Remove any project-specific hooks from the starter kit
- Keep: black, isort/ruff, flake8, basic file checks
- Simplify pytest hook (remove hardcoded paths)

### Step 4: Create Smoke Test (`tests/test_smoke.py`)

```python
"""Smoke tests to verify project structure."""
import pytest
from pathlib import Path


def test_project_structure():
    """Verify basic project structure exists."""
    project_root = Path(__file__).parent.parent
    assert (project_root / "README.md").exists()
    assert (project_root / ".agent-context").is_dir()
    assert (project_root / "tests").is_dir()


def test_pyproject_exists():
    """Verify pyproject.toml is configured."""
    project_root = Path(__file__).parent.parent
    assert (project_root / "pyproject.toml").exists()
```

### Step 5: Create GitHub Actions CI (`.github/workflows/ci.yml`)

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e ".[dev]"

      - name: Run tests
        run: pytest tests/ -v --cov --cov-report=term-missing

      - name: Check code formatting
        run: |
          black --check .
          ruff check .
```

### Step 6: Install Pre-commit Hooks

```bash
pre-commit install
pre-commit run --all-files  # Verify it works
```

### Step 7: Document Testing Workflow (`docs/TESTING.md`)

```markdown
# Testing Guide

## Quick Start
```bash
# Run all tests
pytest tests/ -v

# Run fast tests only
pytest tests/ -v -m "not slow"

# Run with coverage
pytest tests/ --cov --cov-report=html
```

## Writing Tests
- Use `tests/test_template.py` as reference
- Follow AAA pattern: Arrange, Act, Assert
- Mark slow tests: `@pytest.mark.slow`

## CI/CD
- Tests run automatically on push via GitHub Actions
- Pre-commit hooks run before each commit
- Skip pre-commit (use sparingly): `git commit --no-verify`
```

## Acceptance Criteria

- [ ] `pytest tests/ -v` runs successfully
- [ ] `pre-commit run --all-files` passes
- [ ] GitHub Actions CI workflow exists and runs on push
- [ ] Smoke test verifies project structure
- [ ] `pyproject.toml` configures project and dev dependencies
- [ ] Virtual environment documented in README or TESTING.md
- [ ] `docs/TESTING.md` explains testing workflow

## Success Metrics

**Quantitative**:
- Smoke test runs in <1 second
- Pre-commit hooks complete in <30 seconds
- CI workflow completes in <3 minutes

**Qualitative**:
- Developers can write tests following the template
- TDD workflow is clear and documented
- CI failures are actionable

## Notes

This task was auto-generated during project onboarding. It blocks all feature development - complete it first.

**After completing this task**, ensure all subsequent feature tasks include:
- Test requirements section
- TDD workflow (Red-Green-Refactor)
- Coverage targets (80%+ for new code)

---

**Template Version**: 2.0.0
**Purpose**: First task for new projects to establish TDD practices
