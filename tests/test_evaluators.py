"""
Smoke tests for evaluator configurations.

These tests verify:
1. YAML files are valid and parseable
2. Required fields are present
3. Evaluators can be invoked (requires API keys)

Run with: pytest tests/test_evaluators.py -v
Skip API tests: pytest tests/test_evaluators.py -v -m "not requires_api"
"""

import json
import os
import subprocess
from pathlib import Path

import pytest
import yaml

# Path to evaluators directory
EVALUATORS_DIR = Path(__file__).parent.parent / "evaluators"
INDEX_FILE = EVALUATORS_DIR / "index.json"

# Required fields in evaluator YAML
REQUIRED_FIELDS = ["name", "description", "model", "api_key_env", "prompt"]


def get_all_evaluator_paths():
    """Find all evaluator.yml files."""
    return list(EVALUATORS_DIR.glob("**/evaluator.yml"))


def load_index():
    """Load the evaluator index."""
    with open(INDEX_FILE) as f:
        return json.load(f)


class TestEvaluatorYAML:
    """Test evaluator YAML files are valid."""

    @pytest.mark.parametrize("yaml_path", get_all_evaluator_paths())
    def test_yaml_is_valid(self, yaml_path):
        """Each evaluator YAML should be parseable."""
        with open(yaml_path) as f:
            config = yaml.safe_load(f)
        assert config is not None, f"Failed to parse {yaml_path}"

    @pytest.mark.parametrize("yaml_path", get_all_evaluator_paths())
    def test_required_fields_present(self, yaml_path):
        """Each evaluator should have required fields."""
        with open(yaml_path) as f:
            config = yaml.safe_load(f)

        for field in REQUIRED_FIELDS:
            assert field in config, f"Missing required field '{field}' in {yaml_path}"

    @pytest.mark.parametrize("yaml_path", get_all_evaluator_paths())
    def test_prompt_has_content_placeholder(self, yaml_path):
        """Prompt should include {content} placeholder."""
        with open(yaml_path) as f:
            config = yaml.safe_load(f)

        prompt = config.get("prompt", "")
        assert (
            "{content}" in prompt
        ), f"Prompt missing {{content}} placeholder in {yaml_path}"


class TestIndex:
    """Test the evaluator index."""

    def test_index_is_valid_json(self):
        """Index should be valid JSON."""
        index = load_index()
        assert "evaluators" in index
        assert "categories" in index
        assert "providers" in index

    def test_all_evaluators_in_index(self):
        """All evaluator files should be listed in index."""
        index = load_index()
        indexed_paths = {e["path"] for e in index["evaluators"]}

        for yaml_path in get_all_evaluator_paths():
            relative = yaml_path.relative_to(EVALUATORS_DIR)
            assert str(relative) in indexed_paths, f"{relative} not in index"

    def test_index_paths_exist(self):
        """All paths in index should exist."""
        index = load_index()

        for evaluator in index["evaluators"]:
            path = EVALUATORS_DIR / evaluator["path"]
            assert (
                path.exists()
            ), f"Index references non-existent path: {evaluator['path']}"


class TestDocumentation:
    """Test evaluator documentation."""

    @pytest.mark.parametrize("yaml_path", get_all_evaluator_paths())
    def test_readme_exists(self, yaml_path):
        """Each evaluator should have a README."""
        readme = yaml_path.parent / "README.md"
        assert readme.exists(), f"Missing README for {yaml_path.parent.name}"

    @pytest.mark.parametrize("yaml_path", get_all_evaluator_paths())
    def test_changelog_exists(self, yaml_path):
        """Each evaluator should have a CHANGELOG."""
        changelog = yaml_path.parent / "CHANGELOG.md"
        assert changelog.exists(), f"Missing CHANGELOG for {yaml_path.parent.name}"


@pytest.mark.requires_api
class TestEvaluatorExecution:
    """Test evaluators can actually run (requires API keys)."""

    # Small test document
    TEST_DOC = "This is a test document for evaluator validation."
    TEST_FILE = Path("/tmp/evaluator-test-doc.md")

    @pytest.fixture(autouse=True)
    def setup_test_doc(self):
        """Create test document."""
        self.TEST_FILE.write_text(self.TEST_DOC)
        yield
        self.TEST_FILE.unlink(missing_ok=True)

    def _has_api_key(self, env_var):
        """Check if API key is available."""
        return bool(os.environ.get(env_var))

    @pytest.mark.skipif(
        not os.environ.get("OPENAI_API_KEY"), reason="OPENAI_API_KEY not set"
    )
    def test_fast_check_runs(self):
        """fast-check evaluator should run successfully."""
        result = subprocess.run(
            [
                "adversarial",
                "evaluate",
                str(EVALUATORS_DIR / "openai/fast-check/evaluator.yml"),
                str(self.TEST_FILE),
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )
        assert result.returncode == 0, f"fast-check failed: {result.stderr}"

    @pytest.mark.skipif(
        not os.environ.get("GEMINI_API_KEY"), reason="GEMINI_API_KEY not set"
    )
    def test_gemini_flash_runs(self):
        """gemini-flash evaluator should run successfully."""
        result = subprocess.run(
            [
                "adversarial",
                "evaluate",
                str(EVALUATORS_DIR / "google/gemini-flash/evaluator.yml"),
                str(self.TEST_FILE),
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )
        assert result.returncode == 0, f"gemini-flash failed: {result.stderr}"
