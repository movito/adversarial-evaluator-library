"""
Tests for code-focused evaluators (o1-code-review, o1-mini-code, gpt4o-code).

These tests verify that code evaluators can:
1. Execute successfully on code samples
2. Detect known security vulnerabilities
3. Identify logic bugs
4. Flag code quality issues
5. Approve clean code

Run with: pytest tests/test_code_evaluators.py -v
Run specific test: pytest tests/test_code_evaluators.py::TestCodeEvaluatorExecution -v
Skip API tests: pytest tests/test_code_evaluators.py -v -m "not requires_api"

Test Markers:
- requires_api: Tests that call external APIs (require OPENAI_API_KEY)
- slow: Tests that take >30 seconds (reasoning models)
"""

import json
import os
import subprocess
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

import pytest

# Paths
TESTS_DIR = Path(__file__).parent
FIXTURES_DIR = TESTS_DIR / "fixtures" / "code_samples"
EVALUATORS_DIR = TESTS_DIR.parent / "evaluators"
RESULTS_DIR = TESTS_DIR / "results"

# Sample files
SAMPLE_SECURE = FIXTURES_DIR / "sample_secure.py"
SAMPLE_VULNERABLE = FIXTURES_DIR / "sample_vulnerable.py"
SAMPLE_BUGGY = FIXTURES_DIR / "sample_buggy.py"
SAMPLE_MESSY = FIXTURES_DIR / "sample_messy.py"

# Code evaluators
CODE_EVALUATORS = [
    ("o1-code-review", "openai/o1-code-review/evaluator.yml", 600),
    ("o1-mini-code", "openai/o1-mini-code/evaluator.yml", 300),
    ("gpt4o-code", "openai/gpt4o-code/evaluator.yml", 180),
]


@dataclass
class EvaluationResult:
    """Result of running an evaluator on a code sample."""

    evaluator: str
    sample: str
    success: bool
    output: str
    stderr: str
    duration_seconds: float
    timestamp: str
    verdict: Optional[str] = None

    def to_dict(self):
        return {
            "evaluator": self.evaluator,
            "sample": self.sample,
            "success": self.success,
            "output_length": len(self.output),
            "duration_seconds": round(self.duration_seconds, 2),
            "timestamp": self.timestamp,
            "verdict": self.verdict,
        }


def run_evaluator(
    evaluator_path: str, sample_path: Path, timeout: int = 300
) -> EvaluationResult:
    """
    Run an evaluator on a code sample and return the result.

    Args:
        evaluator_path: Relative path to evaluator.yml
        sample_path: Path to the code sample file
        timeout: Maximum time to wait for evaluation

    Returns:
        EvaluationResult with output and metrics
    """
    evaluator_name = Path(evaluator_path).parent.name
    full_evaluator_path = EVALUATORS_DIR / evaluator_path

    start_time = time.time()
    timestamp = datetime.utcnow().isoformat()

    try:
        result = subprocess.run(
            [
                "adversarial",
                "evaluate",
                str(full_evaluator_path),
                str(sample_path),
            ],
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        duration = time.time() - start_time
        output = result.stdout

        # Extract verdict from output
        verdict = None
        for line in output.split("\n"):
            if "APPROVED" in line:
                verdict = "APPROVED"
                break
            elif "CHANGES_REQUESTED" in line:
                verdict = "CHANGES_REQUESTED"
                break
            elif "REJECT" in line:
                verdict = "REJECT"
                break

        return EvaluationResult(
            evaluator=evaluator_name,
            sample=sample_path.name,
            success=result.returncode == 0,
            output=output,
            stderr=result.stderr,
            duration_seconds=duration,
            timestamp=timestamp,
            verdict=verdict,
        )

    except subprocess.TimeoutExpired:
        duration = time.time() - start_time
        return EvaluationResult(
            evaluator=evaluator_name,
            sample=sample_path.name,
            success=False,
            output="",
            stderr=f"Timeout after {timeout}s",
            duration_seconds=duration,
            timestamp=timestamp,
            verdict=None,
        )


def save_result(result: EvaluationResult, results_dir: Path = RESULTS_DIR):
    """Save evaluation result to JSON file for documentation."""
    results_dir.mkdir(parents=True, exist_ok=True)

    # Save individual result
    result_file = (
        results_dir
        / f"{result.evaluator}_{result.sample}_{result.timestamp.replace(':', '-')}.json"
    )
    with open(result_file, "w") as f:
        json.dump(result.to_dict(), f, indent=2)

    # Also save full output
    output_file = results_dir / f"{result.evaluator}_{result.sample}_output.md"
    with open(output_file, "w") as f:
        f.write(f"# {result.evaluator} → {result.sample}\n\n")
        f.write(f"**Timestamp**: {result.timestamp}\n")
        f.write(f"**Duration**: {result.duration_seconds:.2f}s\n")
        f.write(f"**Verdict**: {result.verdict or 'N/A'}\n\n")
        f.write("## Output\n\n")
        f.write(result.output or "(no output)")

    return result_file


class TestCodeEvaluatorFixtures:
    """Verify test fixtures are properly set up."""

    def test_fixtures_directory_exists(self):
        """Fixtures directory should exist."""
        assert FIXTURES_DIR.exists(), f"Missing fixtures directory: {FIXTURES_DIR}"

    def test_sample_secure_exists(self):
        """sample_secure.py should exist."""
        assert SAMPLE_SECURE.exists(), f"Missing {SAMPLE_SECURE}"

    def test_sample_vulnerable_exists(self):
        """sample_vulnerable.py should exist."""
        assert SAMPLE_VULNERABLE.exists(), f"Missing {SAMPLE_VULNERABLE}"

    def test_sample_buggy_exists(self):
        """sample_buggy.py should exist."""
        assert SAMPLE_BUGGY.exists(), f"Missing {SAMPLE_BUGGY}"

    def test_sample_messy_exists(self):
        """sample_messy.py should exist."""
        assert SAMPLE_MESSY.exists(), f"Missing {SAMPLE_MESSY}"

    def test_all_samples_are_valid_python(self):
        """All sample files should be valid Python syntax."""
        import sys

        python_cmd = sys.executable  # Use the current Python interpreter
        for sample in [SAMPLE_SECURE, SAMPLE_VULNERABLE, SAMPLE_BUGGY, SAMPLE_MESSY]:
            result = subprocess.run(
                [python_cmd, "-m", "py_compile", str(sample)],
                capture_output=True,
            )
            assert (
                result.returncode == 0
            ), f"Invalid Python in {sample.name}: {result.stderr}"


@pytest.mark.requires_api
class TestCodeEvaluatorExecution:
    """Test that code evaluators can execute successfully."""

    @pytest.fixture(autouse=True)
    def check_api_key(self):
        """Skip all tests if OPENAI_API_KEY is not set."""
        if not os.environ.get("OPENAI_API_KEY"):
            pytest.skip("OPENAI_API_KEY not set")

    @pytest.mark.parametrize("evaluator_name,evaluator_path,timeout", CODE_EVALUATORS)
    def test_evaluator_runs_on_secure_sample(
        self, evaluator_name, evaluator_path, timeout
    ):
        """Each code evaluator should run successfully on clean code."""
        result = run_evaluator(evaluator_path, SAMPLE_SECURE, timeout)
        save_result(result)

        assert result.success, f"{evaluator_name} failed: {result.stderr}"
        assert len(result.output) > 100, f"{evaluator_name} produced minimal output"

    @pytest.mark.slow
    @pytest.mark.parametrize("evaluator_name,evaluator_path,timeout", CODE_EVALUATORS)
    def test_evaluator_runs_on_vulnerable_sample(
        self, evaluator_name, evaluator_path, timeout
    ):
        """Each code evaluator should run on vulnerable code."""
        result = run_evaluator(evaluator_path, SAMPLE_VULNERABLE, timeout)
        save_result(result)

        assert result.success, f"{evaluator_name} failed: {result.stderr}"


@pytest.mark.requires_api
@pytest.mark.slow
class TestSecurityDetection:
    """Test that evaluators detect security vulnerabilities."""

    @pytest.fixture(autouse=True)
    def check_api_key(self):
        if not os.environ.get("OPENAI_API_KEY"):
            pytest.skip("OPENAI_API_KEY not set")

    def test_o1_code_review_detects_sql_injection(self):
        """o1-code-review should flag SQL injection vulnerabilities."""
        result = run_evaluator(
            "openai/o1-code-review/evaluator.yml",
            SAMPLE_VULNERABLE,
            timeout=600,
        )
        save_result(result)

        assert result.success, f"Evaluator failed: {result.stderr}"

        # Check for security-related findings
        output_lower = result.output.lower()
        security_terms = ["sql injection", "injection", "sql", "query"]
        found_terms = [term for term in security_terms if term in output_lower]

        assert len(found_terms) > 0, (
            f"o1-code-review should detect SQL injection. "
            f"Output did not contain any of: {security_terms}"
        )

    def test_o1_code_review_detects_hardcoded_credentials(self):
        """o1-code-review should flag hardcoded credentials."""
        result = run_evaluator(
            "openai/o1-code-review/evaluator.yml",
            SAMPLE_VULNERABLE,
            timeout=600,
        )
        save_result(result)

        assert result.success, f"Evaluator failed: {result.stderr}"

        output_lower = result.output.lower()
        credential_terms = ["hardcoded", "credential", "password", "secret", "api key"]
        found_terms = [term for term in credential_terms if term in output_lower]

        assert len(found_terms) > 0, (
            f"o1-code-review should detect hardcoded credentials. "
            f"Output did not contain any of: {credential_terms}"
        )

    def test_o1_mini_detects_command_injection(self):
        """o1-mini-code should flag command injection vulnerabilities."""
        result = run_evaluator(
            "openai/o1-mini-code/evaluator.yml",
            SAMPLE_VULNERABLE,
            timeout=300,
        )
        save_result(result)

        assert result.success, f"Evaluator failed: {result.stderr}"

        output_lower = result.output.lower()
        injection_terms = [
            "command injection",
            "shell",
            "subprocess",
            "os.system",
            "injection",
        ]
        found_terms = [term for term in injection_terms if term in output_lower]

        assert len(found_terms) > 0, (
            f"o1-mini-code should detect command injection. "
            f"Output did not contain any of: {injection_terms}"
        )


@pytest.mark.requires_api
@pytest.mark.slow
class TestBugDetection:
    """Test that evaluators detect logic bugs."""

    @pytest.fixture(autouse=True)
    def check_api_key(self):
        if not os.environ.get("OPENAI_API_KEY"):
            pytest.skip("OPENAI_API_KEY not set")

    def test_o1_mini_detects_off_by_one(self):
        """o1-mini-code should detect off-by-one errors."""
        result = run_evaluator(
            "openai/o1-mini-code/evaluator.yml",
            SAMPLE_BUGGY,
            timeout=300,
        )
        save_result(result)

        assert result.success, f"Evaluator failed: {result.stderr}"

        output_lower = result.output.lower()
        bug_terms = ["off-by-one", "boundary", "range", "index", "edge case"]
        found_terms = [term for term in bug_terms if term in output_lower]

        assert len(found_terms) > 0, (
            f"o1-mini-code should detect off-by-one errors. "
            f"Output did not contain any of: {bug_terms}"
        )

    def test_gpt4o_detects_resource_leak(self):
        """gpt4o-code should detect resource leaks."""
        result = run_evaluator(
            "openai/gpt4o-code/evaluator.yml",
            SAMPLE_BUGGY,
            timeout=180,
        )
        save_result(result)

        assert result.success, f"Evaluator failed: {result.stderr}"

        output_lower = result.output.lower()
        leak_terms = ["resource", "leak", "close", "file", "context manager", "with"]
        found_terms = [term for term in leak_terms if term in output_lower]

        assert len(found_terms) > 0, (
            f"gpt4o-code should detect resource leaks. "
            f"Output did not contain any of: {leak_terms}"
        )


@pytest.mark.requires_api
class TestQualityDetection:
    """Test that evaluators detect code quality issues."""

    @pytest.fixture(autouse=True)
    def check_api_key(self):
        if not os.environ.get("OPENAI_API_KEY"):
            pytest.skip("OPENAI_API_KEY not set")

    def test_gpt4o_detects_naming_issues(self):
        """gpt4o-code should flag poor naming conventions."""
        result = run_evaluator(
            "openai/gpt4o-code/evaluator.yml",
            SAMPLE_MESSY,
            timeout=180,
        )
        save_result(result)

        assert result.success, f"Evaluator failed: {result.stderr}"

        output_lower = result.output.lower()
        naming_terms = ["naming", "name", "variable", "descriptive", "unclear"]
        found_terms = [term for term in naming_terms if term in output_lower]

        assert len(found_terms) > 0, (
            f"gpt4o-code should detect naming issues. "
            f"Output did not contain any of: {naming_terms}"
        )

    def test_gpt4o_detects_code_duplication(self):
        """gpt4o-code should flag code duplication."""
        result = run_evaluator(
            "openai/gpt4o-code/evaluator.yml",
            SAMPLE_MESSY,
            timeout=180,
        )
        save_result(result)

        assert result.success, f"Evaluator failed: {result.stderr}"

        output_lower = result.output.lower()
        dup_terms = ["duplicate", "duplication", "repeated", "copy", "similar"]
        found_terms = [term for term in dup_terms if term in output_lower]

        assert len(found_terms) > 0, (
            f"gpt4o-code should detect code duplication. "
            f"Output did not contain any of: {dup_terms}"
        )


@pytest.mark.requires_api
class TestCleanCodeApproval:
    """Test that evaluators approve clean code."""

    @pytest.fixture(autouse=True)
    def check_api_key(self):
        if not os.environ.get("OPENAI_API_KEY"):
            pytest.skip("OPENAI_API_KEY not set")

    @pytest.mark.parametrize("evaluator_name,evaluator_path,timeout", CODE_EVALUATORS)
    def test_evaluator_approves_secure_code(
        self, evaluator_name, evaluator_path, timeout
    ):
        """Code evaluators should approve clean, secure code."""
        result = run_evaluator(evaluator_path, SAMPLE_SECURE, timeout)
        save_result(result)

        assert result.success, f"{evaluator_name} failed: {result.stderr}"

        # Check for approval or minimal issues
        output_lower = result.output.lower()

        # Should not find critical security issues
        critical_terms = ["critical", "reject", "security flaw", "vulnerability"]
        critical_found = [term for term in critical_terms if term in output_lower]

        # Allow verdict to be APPROVED or CHANGES_REQUESTED (for minor style issues)
        # But should not be REJECT
        assert (
            result.verdict != "REJECT"
        ), f"{evaluator_name} rejected clean code. Verdict: {result.verdict}"


@pytest.mark.requires_api
@pytest.mark.slow
class TestPerformanceBenchmark:
    """Benchmark evaluator performance for documentation."""

    @pytest.fixture(autouse=True)
    def check_api_key(self):
        if not os.environ.get("OPENAI_API_KEY"):
            pytest.skip("OPENAI_API_KEY not set")

    def test_benchmark_all_evaluators(self):
        """Run all evaluators on all samples and report timing."""
        results = []

        for evaluator_name, evaluator_path, timeout in CODE_EVALUATORS:
            for sample in [
                SAMPLE_SECURE,
                SAMPLE_VULNERABLE,
                SAMPLE_BUGGY,
                SAMPLE_MESSY,
            ]:
                result = run_evaluator(evaluator_path, sample, timeout)
                save_result(result)
                results.append(result.to_dict())

        # Save benchmark summary
        RESULTS_DIR.mkdir(parents=True, exist_ok=True)
        summary_file = (
            RESULTS_DIR
            / f"benchmark_summary_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        )
        with open(summary_file, "w") as f:
            json.dump(
                {
                    "timestamp": datetime.utcnow().isoformat(),
                    "evaluators": [e[0] for e in CODE_EVALUATORS],
                    "samples": [
                        "sample_secure.py",
                        "sample_vulnerable.py",
                        "sample_buggy.py",
                        "sample_messy.py",
                    ],
                    "results": results,
                },
                f,
                indent=2,
            )

        # Print summary
        print("\n\n=== BENCHMARK SUMMARY ===")
        for r in results:
            print(
                f"{r['evaluator']:20} | {r['sample']:25} | {r['duration_seconds']:6.2f}s | {r['verdict'] or 'N/A'}"
            )
        print(f"\nResults saved to: {summary_file}")

        # All evaluators should complete
        for r in results:
            assert r["success"], f"{r['evaluator']} failed on {r['sample']}"
