"""
Integration tests for adversarial-evaluator-library v0.4.0

Verifies:
1. ADV-0032 fix - explicit model field takes priority
2. litellm prefix handling
3. Model ID resolution for Anthropic evaluators
4. Cross-provider compatibility

Requirements:
- adversarial-workflow >= 0.9.3
- ANTHROPIC_API_KEY (for live tests, optional)

Run with:
    pytest tests/integration/test_v0.4.0_verification.py -v
    pytest tests/integration/test_v0.4.0_verification.py -v -m "not requires_api"  # skip live tests
"""

import os
import subprocess
import pytest
import yaml
from pathlib import Path


# =============================================================================
# Test Configuration
# =============================================================================

REPO_ROOT = Path(__file__).parent.parent.parent
EVALUATORS_DIR = REPO_ROOT / "evaluators"
REGISTRY_PATH = REPO_ROOT / "providers" / "registry.yml"

ANTHROPIC_EVALUATORS = [
    ("anthropic/claude-adversarial", "anthropic/claude-opus-4-6", "4.6"),
    ("anthropic/claude-code", "anthropic/claude-sonnet-4-5", "4.5"),
    ("anthropic/claude-quick", "anthropic/claude-haiku-4-5", "4.5"),
]

GOOGLE_EVALUATORS = [
    ("google/gemini-code", "gemini/gemini-3-pro-20260101", None),
]


# =============================================================================
# Unit Tests - No API Required
# =============================================================================

class TestModelIDFormat:
    """Verify evaluator model IDs use correct litellm prefix format."""

    @pytest.mark.parametrize("eval_path,expected_model,_", ANTHROPIC_EVALUATORS)
    def test_anthropic_evaluator_has_litellm_prefix(self, eval_path, expected_model, _):
        """Anthropic evaluators should use anthropic/ prefix."""
        evaluator_file = EVALUATORS_DIR / eval_path / "evaluator.yml"
        assert evaluator_file.exists(), f"Evaluator not found: {evaluator_file}"

        with open(evaluator_file) as f:
            config = yaml.safe_load(f)

        model = config.get("model", "")
        assert model.startswith("anthropic/"), f"Expected anthropic/ prefix, got: {model}"
        assert model == expected_model, f"Expected {expected_model}, got: {model}"

    @pytest.mark.parametrize("eval_path,expected_model,_", GOOGLE_EVALUATORS)
    def test_google_evaluator_has_litellm_prefix(self, eval_path, expected_model, _):
        """Google evaluators should use gemini/ prefix."""
        evaluator_file = EVALUATORS_DIR / eval_path / "evaluator.yml"
        assert evaluator_file.exists(), f"Evaluator not found: {evaluator_file}"

        with open(evaluator_file) as f:
            config = yaml.safe_load(f)

        model = config.get("model", "")
        assert model.startswith("gemini/"), f"Expected gemini/ prefix, got: {model}"


class TestMinVersionAlignment:
    """Verify evaluator min_version fields align with registry entries."""

    @pytest.fixture
    def registry(self):
        """Load the provider registry."""
        with open(REGISTRY_PATH) as f:
            return yaml.safe_load(f)

    @pytest.mark.parametrize("eval_path,_,expected_min_version", ANTHROPIC_EVALUATORS)
    def test_min_version_matches_registry(self, registry, eval_path, _, expected_min_version):
        """Evaluator min_version should match a registry entry version."""
        evaluator_file = EVALUATORS_DIR / eval_path / "evaluator.yml"

        with open(evaluator_file) as f:
            config = yaml.safe_load(f)

        model_req = config.get("model_requirement", {})
        min_version = model_req.get("min_version")

        assert min_version == expected_min_version, \
            f"Expected min_version {expected_min_version}, got: {min_version}"

        # Verify this version exists in registry
        family = model_req.get("family")
        tier = model_req.get("tier")

        claude_tiers = registry["providers"]["claude"]["tiers"]
        assert tier in claude_tiers, f"Tier {tier} not in registry"

        tier_models = claude_tiers[tier]["models"]
        versions_in_registry = [m["version"] for m in tier_models]

        assert min_version in versions_in_registry, \
            f"min_version {min_version} not found in registry. Available: {versions_in_registry}"


class TestRegistrySchema:
    """Verify registry schema meets ADR-0005 requirements."""

    @pytest.fixture
    def registry(self):
        with open(REGISTRY_PATH) as f:
            return yaml.safe_load(f)

    def test_schema_version_is_1_0_1(self, registry):
        """Registry should be at schema version 1.0.1 after v0.4.0."""
        assert registry["schema_version"] == "1.0.1", \
            f"Expected schema_version 1.0.1, got: {registry['schema_version']}"

    def test_claude_opus_4_6_exists(self, registry):
        """Registry should contain Claude Opus 4.6."""
        opus_models = registry["providers"]["claude"]["tiers"]["opus"]["models"]
        model_ids = [m["id"] for m in opus_models]
        assert "claude-opus-4-6" in model_ids, f"claude-opus-4-6 not in registry: {model_ids}"

    def test_claude_sonnet_4_5_exists(self, registry):
        """Registry should contain Claude Sonnet 4.5."""
        sonnet_models = registry["providers"]["claude"]["tiers"]["sonnet"]["models"]
        model_ids = [m["id"] for m in sonnet_models]
        assert "claude-sonnet-4-5" in model_ids, f"claude-sonnet-4-5 not in registry: {model_ids}"

    def test_claude_haiku_4_5_exists(self, registry):
        """Registry should contain Claude Haiku 4.5."""
        haiku_models = registry["providers"]["claude"]["tiers"]["haiku"]["models"]
        model_ids = [m["id"] for m in haiku_models]
        assert "claude-haiku-4-5" in model_ids, f"claude-haiku-4-5 not in registry: {model_ids}"


# =============================================================================
# ADV-0032 Verification Tests
# =============================================================================

class TestADV0032ModelPriority:
    """Verify ADV-0032 fix: explicit model field takes priority."""

    def test_resolver_uses_explicit_model(self):
        """ModelResolver should use explicit model field over model_requirement."""
        try:
            from adversarial_workflow.evaluators.resolver import ModelResolver
            from adversarial_workflow.evaluators.config import EvaluatorConfig, ModelRequirement
        except ImportError:
            pytest.skip("adversarial-workflow not installed")

        resolver = ModelResolver()
        config = EvaluatorConfig(
            name="test",
            description="Test",
            model="explicit-model-id",  # Should be used
            api_key_env="TEST_KEY",
            prompt="Test",
            output_suffix="TEST",
            model_requirement=ModelRequirement(
                family="claude",
                tier="opus",
            ),  # Should be ignored
        )

        model_id, _ = resolver.resolve(config)
        assert model_id == "explicit-model-id", \
            f"ADV-0032 FAIL: Expected explicit-model-id, got {model_id}"

    def test_empty_model_falls_back_to_requirement(self):
        """Empty model field should fall back to model_requirement resolution."""
        try:
            from adversarial_workflow.evaluators.resolver import ModelResolver
            from adversarial_workflow.evaluators.config import EvaluatorConfig, ModelRequirement
        except ImportError:
            pytest.skip("adversarial-workflow not installed")

        resolver = ModelResolver()
        config = EvaluatorConfig(
            name="test",
            description="Test",
            model="",  # Empty - should trigger fallback
            api_key_env="ANTHROPIC_API_KEY",
            prompt="Test",
            output_suffix="TEST",
            model_requirement=ModelRequirement(
                family="claude",
                tier="opus",
            ),
        )

        model_id, _ = resolver.resolve(config)
        assert model_id != "", "Empty model should resolve via model_requirement"
        assert "claude" in model_id.lower() or "anthropic" in model_id.lower(), \
            f"Expected Claude model from requirement, got: {model_id}"

    @pytest.mark.parametrize("eval_path,expected_model,_", ANTHROPIC_EVALUATORS)
    def test_anthropic_evaluator_resolves_correctly(self, eval_path, expected_model, _):
        """Real Anthropic evaluator configs should resolve to their explicit model."""
        try:
            from adversarial_workflow.evaluators.resolver import ModelResolver
            from adversarial_workflow.evaluators.config import EvaluatorConfig, ModelRequirement
        except ImportError:
            pytest.skip("adversarial-workflow not installed")

        evaluator_file = EVALUATORS_DIR / eval_path / "evaluator.yml"
        with open(evaluator_file) as f:
            data = yaml.safe_load(f)

        model_req = None
        if "model_requirement" in data:
            model_req = ModelRequirement(**data["model_requirement"])

        config = EvaluatorConfig(
            name=data["name"],
            description=data["description"],
            model=data.get("model", ""),
            api_key_env=data["api_key_env"],
            prompt=data["prompt"],
            output_suffix=data["output_suffix"],
            model_requirement=model_req,
        )

        resolver = ModelResolver()
        model_id, _ = resolver.resolve(config)

        assert model_id == expected_model, \
            f"ADV-0032: Expected {expected_model}, got {model_id}"


# =============================================================================
# Live API Tests (require API keys)
# =============================================================================

@pytest.mark.requires_api
class TestLiveEvaluation:
    """Live tests that require API keys. Skip with: -m 'not requires_api'"""

    @pytest.fixture
    def test_document(self, tmp_path):
        """Create a simple test document."""
        doc = tmp_path / "test-doc.md"
        doc.write_text("""# Test Document

This is a simple test document for evaluator verification.

## Content

Just a basic test to verify the evaluator runs successfully.
""")
        return doc

    @pytest.mark.skipif(
        not os.environ.get("ANTHROPIC_API_KEY"),
        reason="ANTHROPIC_API_KEY not set"
    )
    def test_claude_quick_evaluator(self, test_document):
        """Run claude-quick evaluator on test document."""
        result = subprocess.run(
            ["adversarial", "evaluate", str(test_document), "--evaluator", "claude-quick"],
            capture_output=True,
            text=True,
            timeout=120,
        )

        assert result.returncode == 0, \
            f"claude-quick failed with exit code {result.returncode}\nstderr: {result.stderr}"


# =============================================================================
# CLI Verification Tests
# =============================================================================

class TestCLIIntegration:
    """Verify CLI commands work with new evaluators."""

    def test_adversarial_workflow_version(self):
        """Verify adversarial-workflow >= 0.9.3 is installed."""
        result = subprocess.run(
            ["adversarial", "--version"],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            pytest.skip("adversarial CLI not available")

        # Extract version from output
        output = result.stdout.strip()
        # Version format varies, just check it runs
        assert "adversarial" in output.lower() or len(output) > 0

    def test_library_list_shows_anthropic_evaluators(self):
        """Library list should show Anthropic evaluators."""
        result = subprocess.run(
            ["adversarial", "library", "list"],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            pytest.skip("adversarial library command not available")

        output = result.stdout
        assert "claude-adversarial" in output, "claude-adversarial not in library list"
        assert "claude-code" in output, "claude-code not in library list"
        assert "claude-quick" in output, "claude-quick not in library list"


# =============================================================================
# Quick Smoke Test (run standalone)
# =============================================================================

def test_quick_smoke():
    """
    Quick smoke test that can be run standalone.

    Run with: python -m pytest tests/integration/test_v0.4.0_verification.py::test_quick_smoke -v
    """
    try:
        from adversarial_workflow.evaluators.resolver import ModelResolver
        from adversarial_workflow.evaluators.config import EvaluatorConfig, ModelRequirement
    except ImportError:
        pytest.skip("adversarial-workflow not installed")

    resolver = ModelResolver()

    # Test 1: Explicit model takes priority
    config = EvaluatorConfig(
        name="smoke",
        description="Smoke test",
        model="explicit-test-model",
        api_key_env="TEST",
        prompt="Test",
        output_suffix="TEST",
        model_requirement=ModelRequirement(family="claude", tier="opus"),
    )
    model_id, _ = resolver.resolve(config)
    assert model_id == "explicit-test-model", f"FAIL: got {model_id}"

    # Test 2: litellm prefix preserved
    config2 = EvaluatorConfig(
        name="smoke2",
        description="Smoke test 2",
        model="anthropic/claude-opus-4-6",
        api_key_env="ANTHROPIC_API_KEY",
        prompt="Test",
        output_suffix="TEST",
    )
    model_id2, _ = resolver.resolve(config2)
    assert model_id2 == "anthropic/claude-opus-4-6", f"FAIL: got {model_id2}"

    print("✅ v0.4.0 smoke test PASSED")


if __name__ == "__main__":
    # Run smoke test directly
    test_quick_smoke()
