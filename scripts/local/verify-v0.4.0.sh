#!/bin/bash
# =============================================================================
# v0.4.0 Verification Script
# =============================================================================
# Quick verification that adversarial-evaluator-library v0.4.0 works correctly
# with adversarial-workflow.
#
# Usage:
#   ./scripts/verify-v0.4.0.sh          # Run all tests
#   ./scripts/verify-v0.4.0.sh --quick  # Quick smoke test only
#   ./scripts/verify-v0.4.0.sh --live   # Include live API tests
#
# Requirements:
#   - adversarial-workflow >= 0.9.3
#   - ANTHROPIC_API_KEY (for --live tests)
# =============================================================================

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=============================================="
echo "adversarial-evaluator-library v0.4.0 Verification"
echo "=============================================="
echo ""

# Parse arguments
QUICK_ONLY=false
INCLUDE_LIVE=false
for arg in "$@"; do
    case $arg in
        --quick) QUICK_ONLY=true ;;
        --live) INCLUDE_LIVE=true ;;
    esac
done

# -----------------------------------------------------------------------------
# Test 1: Check adversarial-workflow version
# -----------------------------------------------------------------------------
echo -e "${YELLOW}[1/6] Checking adversarial-workflow version...${NC}"

if ! command -v adversarial &> /dev/null; then
    echo -e "${RED}FAIL: adversarial CLI not found${NC}"
    echo "Install with: pip install adversarial-workflow>=0.9.3"
    exit 1
fi

VERSION=$(pip show adversarial-workflow 2>/dev/null | grep "^Version:" | cut -d' ' -f2)
echo "Installed version: $VERSION"

# Simple version check (0.9.3 or higher)
MAJOR=$(echo $VERSION | cut -d'.' -f1)
MINOR=$(echo $VERSION | cut -d'.' -f2)
PATCH=$(echo $VERSION | cut -d'.' -f3)

if [[ "$MAJOR" -eq 0 && "$MINOR" -eq 9 && "$PATCH" -lt 3 ]]; then
    echo -e "${RED}FAIL: Requires adversarial-workflow >= 0.9.3${NC}"
    echo "Upgrade with: pip install --upgrade adversarial-workflow"
    exit 1
fi
echo -e "${GREEN}✓ Version OK${NC}"
echo ""

# -----------------------------------------------------------------------------
# Test 2: ADV-0032 Smoke Test
# -----------------------------------------------------------------------------
echo -e "${YELLOW}[2/6] Testing ADV-0032 (model field priority)...${NC}"

python -c "
from adversarial_workflow.evaluators.resolver import ModelResolver
from adversarial_workflow.evaluators.config import EvaluatorConfig, ModelRequirement

resolver = ModelResolver()
config = EvaluatorConfig(
    name='test', description='Test',
    model='explicit-model-id',
    api_key_env='TEST',
    prompt='Test', output_suffix='TEST',
    model_requirement=ModelRequirement(family='claude', tier='opus'),
)
model_id, _ = resolver.resolve(config)
assert model_id == 'explicit-model-id', f'FAIL: got {model_id}'
print('✓ Explicit model takes priority')
" || { echo -e "${RED}FAIL: ADV-0032 test failed${NC}"; exit 1; }
echo -e "${GREEN}✓ ADV-0032 verified${NC}"
echo ""

if [ "$QUICK_ONLY" = true ]; then
    echo -e "${GREEN}=============================================="
    echo "Quick verification PASSED"
    echo "==============================================${NC}"
    exit 0
fi

# -----------------------------------------------------------------------------
# Test 3: Verify Anthropic evaluator model IDs
# -----------------------------------------------------------------------------
echo -e "${YELLOW}[3/6] Verifying Anthropic evaluator model IDs...${NC}"

check_evaluator() {
    local path=$1
    local expected=$2
    local actual=$(grep "^model:" "evaluators/$path/evaluator.yml" | cut -d' ' -f2)
    if [ "$actual" = "$expected" ]; then
        echo "  ✓ $path: $actual"
        return 0
    else
        echo "  ✗ $path: expected $expected, got $actual"
        return 1
    fi
}

check_evaluator "anthropic/claude-adversarial" "anthropic/claude-opus-4-6"
check_evaluator "anthropic/claude-code" "anthropic/claude-sonnet-4-5"
check_evaluator "anthropic/claude-quick" "anthropic/claude-haiku-4-5"
echo -e "${GREEN}✓ Model IDs correct${NC}"
echo ""

# -----------------------------------------------------------------------------
# Test 4: Verify registry has new models
# -----------------------------------------------------------------------------
echo -e "${YELLOW}[4/6] Verifying registry entries...${NC}"

if grep -q "claude-opus-4-6" providers/registry.yml && \
   grep -q "claude-sonnet-4-5" providers/registry.yml && \
   grep -q "claude-haiku-4-5" providers/registry.yml; then
    echo "  ✓ claude-opus-4-6 in registry"
    echo "  ✓ claude-sonnet-4-5 in registry"
    echo "  ✓ claude-haiku-4-5 in registry"
    echo -e "${GREEN}✓ Registry updated${NC}"
else
    echo -e "${RED}FAIL: Missing models in registry${NC}"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: Verify min_version alignment
# -----------------------------------------------------------------------------
echo -e "${YELLOW}[5/6] Verifying min_version alignment...${NC}"

python -c "
import yaml

with open('providers/registry.yml') as f:
    registry = yaml.safe_load(f)

evaluators = [
    ('anthropic/claude-adversarial', 'opus', '4.6'),
    ('anthropic/claude-code', 'sonnet', '4.5'),
    ('anthropic/claude-quick', 'haiku', '4.5'),
]

for eval_path, tier, expected_version in evaluators:
    with open(f'evaluators/{eval_path}/evaluator.yml') as f:
        config = yaml.safe_load(f)

    min_version = config['model_requirement']['min_version']
    assert min_version == expected_version, f'{eval_path}: min_version {min_version} != {expected_version}'

    # Check registry has this version
    tier_models = registry['providers']['claude']['tiers'][tier]['models']
    versions = [m['version'] for m in tier_models]
    assert min_version in versions, f'{tier} tier missing version {min_version}'

    print(f'  ✓ {eval_path}: min_version {min_version} → registry {tier} ✓')

print('All alignments verified')
" || { echo -e "${RED}FAIL: min_version alignment check failed${NC}"; exit 1; }
echo -e "${GREEN}✓ min_version aligned${NC}"
echo ""

# -----------------------------------------------------------------------------
# Test 6: Live API test (optional)
# -----------------------------------------------------------------------------
if [ "$INCLUDE_LIVE" = true ]; then
    echo -e "${YELLOW}[6/6] Running live API test...${NC}"

    if [ -z "$ANTHROPIC_API_KEY" ]; then
        echo -e "${YELLOW}SKIP: ANTHROPIC_API_KEY not set${NC}"
    else
        # Create test document
        TEST_DOC=$(mktemp /tmp/test-doc-XXXXX.md)
        cat > "$TEST_DOC" << 'EOF'
# Test Document

This is a test document for v0.4.0 verification.

## Content

Simple test content.
EOF

        echo "Testing claude-quick evaluator..."
        if adversarial evaluate "$TEST_DOC" --evaluator claude-quick; then
            echo -e "${GREEN}✓ Live evaluation successful${NC}"
        else
            echo -e "${RED}FAIL: Live evaluation failed${NC}"
            rm -f "$TEST_DOC"
            exit 1
        fi

        rm -f "$TEST_DOC"
    fi
else
    echo -e "${YELLOW}[6/6] Skipping live API test (use --live to include)${NC}"
fi
echo ""

# -----------------------------------------------------------------------------
# Summary
# -----------------------------------------------------------------------------
echo -e "${GREEN}=============================================="
echo "v0.4.0 Verification PASSED"
echo "==============================================${NC}"
echo ""
echo "All checks passed:"
echo "  ✓ adversarial-workflow >= 0.9.3"
echo "  ✓ ADV-0032 model priority fix"
echo "  ✓ Anthropic evaluator model IDs"
echo "  ✓ Registry entries"
echo "  ✓ min_version alignment"
if [ "$INCLUDE_LIVE" = true ] && [ -n "$ANTHROPIC_API_KEY" ]; then
    echo "  ✓ Live API evaluation"
fi
echo ""
echo "The library is ready for cross-provider evaluation!"
