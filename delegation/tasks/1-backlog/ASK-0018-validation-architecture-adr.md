# ASK-0018: Validation Architecture ADR

**Status**: Backlog
**Priority**: low
**Assigned To**: planner
**Estimated Effort**: 2-3 hours
**Created**: 2025-11-28

## Related Tasks

**Parent Task**: None (ADR Migration - Tier 3: API & Quality)
**Depends On**: None
**Blocks**: None
**Related**: ASK-0015 (OpenAPI Specification)

## Overview

Adapt and document the Validation Architecture from thematic-cuts (TC ADR-0007) for the agentive-starter-kit. This ADR establishes a two-tier validation pattern: type safety at construction vs comprehensive validation on demand.

**Source**: `thematic-cuts/docs/decisions/adr/ADR-0007-validation-architecture.md`

**Why Valuable**: Enables better UX by separating "can this object exist?" from "is this object valid for this operation?". Allows working with partially valid data during editing.

## Key Concepts to Document

### Two-Tier Validation

```
Tier 1: Construction (Type Safety)
    - Runs automatically
    - Catches type errors
    - Allows partially valid objects

Tier 2: Comprehensive (Explicit)
    - Runs on demand (.validate())
    - Full business rule validation
    - Required before operations
```

### Example Pattern

```python
from pydantic import BaseModel, field_validator
from typing import Optional

class Task(BaseModel):
    """Tier 1: Type safety at construction"""
    id: str
    title: str
    status: Optional[str] = None  # Can be None during editing

    def validate_for_sync(self) -> list[str]:
        """Tier 2: Comprehensive validation for Linear sync"""
        errors = []
        if not self.status:
            errors.append("Status required for sync")
        if self.status and self.status not in VALID_STATUSES:
            errors.append(f"Invalid status: {self.status}")
        return errors
```

### When to Use Each Tier

| Scenario | Tier 1 | Tier 2 |
|----------|--------|--------|
| Creating object | ✅ | ❌ |
| Editing in UI | ✅ | ❌ |
| Saving draft | ✅ | ❌ |
| Syncing to Linear | ✅ | ✅ |
| API response | ✅ | ✅ |

### Benefits

1. **Better UX** - Don't fail during editing
2. **Clearer errors** - Context-specific validation messages
3. **Flexibility** - Work with incomplete data
4. **Testability** - Validate in isolation

## Requirements

### Functional Requirements
1. Document the two-tier validation pattern as an ADR
2. Explain when to use each tier
3. Show Pydantic implementation
4. Provide practical examples

### Non-Functional Requirements
- ADR follows project template
- Applicable to any data model
- Clear decision criteria

## Acceptance Criteria

### Must Have
- [ ] ADR created following project template
- [ ] Documents two-tier pattern
- [ ] Shows Pydantic example
- [ ] Explains tier selection criteria
- [ ] Lists benefits of separation

### Should Have
- [ ] Error message patterns
- [ ] Testing strategies
- [ ] Integration with API responses

## Implementation Plan

1. **Read source ADR** from thematic-cuts
2. **Adapt for starter-kit** - Generic validation guidance
3. **Create ADR** in `docs/decisions/adr/`

## Time Estimate

| Phase | Time |
|-------|------|
| Read source ADR | 30 min |
| Adapt and write | 1.5-2 hours |
| Review and finalize | 30 min |
| **Total** | **2-3 hours** |

## References

- Source: `thematic-cuts/docs/decisions/adr/ADR-0007-validation-architecture.md`
- Pydantic: https://docs.pydantic.dev/
- Pydantic validators: https://docs.pydantic.dev/latest/concepts/validators/

## Notes

- This pattern is useful for any data model
- Pydantic v2 recommended for performance
- Consider attrs as alternative to Pydantic

---

**Template Version**: 1.0.0
**Created**: 2025-11-28
