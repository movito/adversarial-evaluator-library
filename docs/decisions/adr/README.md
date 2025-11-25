# Architecture Decision Records (ADRs)

This directory contains Architecture Decision Records (ADRs) documenting significant architectural and design decisions for thematic-cuts.

## What are ADRs?

ADRs capture important architectural decisions along with their context and consequences. Each ADR describes:
- **Context**: The forces and factors influencing the decision
- **Decision**: What was decided and why
- **Consequences**: The positive, negative, and neutral implications

ADRs are **immutable** once accepted. If a decision changes, we create a new ADR that supersedes the old one, preserving the historical context.

## Format

We use [Michael Nygard's ADR format](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions):

```markdown
# ADR-####: Title
(Filename: ADR-####-description.md)

**Status**: Accepted | Deprecated | Superseded by ADR-XXXX

**Date**: YYYY-MM-DD

**Deciders**: [Decision makers]

## Context
[Forces, factors, and constraints influencing the decision]

## Decision
[What we decided and why]

## Consequences

### Positive
[What becomes easier or better]

### Negative
[What becomes harder or what we lose]

### Neutral
[Other implications]
```

## Naming Convention

ADRs use the format **`ADR-####-description.md`** where:
- `ADR-` is the required prefix
- `####` is a four-digit sequential number (0001, 0002, etc.)
- `-description` is a short kebab-case description of the decision

**Examples**:
- `ADR-0001-exact-timecode-arithmetic.md`
- `ADR-0013-tldraw-visual-review-tool.md`
- `ADR-0029-native-macos-gui-strategy.md`

Numbers are not reused, even if an ADR is superseded. **Why four digits?** This project aims for long-term maintainability, and four digits provide clear ordering without ambiguity.

## Index

### Active ADRs

| ADR | Title | Date | Status |
|-----|-------|------|--------|
| [0001](ADR-0001-exact-timecode-arithmetic.md) | Exact Timecode Arithmetic Using Fractions | 2024-10-10 | Accepted |
| [0002](ADR-0002-two-phase-consistent-assembly.md) | Two-Phase Consistent Assembly Architecture | 2025-10-13 | Accepted |
| [0003](ADR-0003-multi-speaker-workflow.md) | Multi-Speaker Workflow Design | 2024-09-13 | Accepted |
| [0004](ADR-0004-timeline-offset-approach.md) | Timeline Offset Approach | 2025-10-21 | Accepted |
| [0005](ADR-0005-semantic-parser-integration.md) | Semantic Parser Integration Strategy | 2024-09-14 (2025-10-19) | Accepted |
| [0006](ADR-0006-otio-integration.md) | OpenTimelineIO (OTIO) Integration | 2024-09-12 (2025-10-13) | Accepted |
| [0007](ADR-0007-validation-architecture.md) | Validation Architecture with Separation of Concerns | 2025-10-13 | Accepted |
| [0008](ADR-0008-davinci-api-integration.md) | DaVinci Resolve API Integration Strategy | 2024-09-12 | Accepted |
| [0009](ADR-0009-cli-wizard-workflow.md) | Interactive CLI Wizard Workflow | 2024-09-12 | Accepted |
| [0010](ADR-0010-frame-rate-handling.md) | Frame Rate Handling Strategy | 2024-09-12 | Accepted |
| [0011](ADR-0011-adversarial-workflow-integration.md) | Adversarial Workflow Integration for Quality Development | 2025-10-17 | Accepted |
| [0012](ADR-0012-test-infrastructure-strategy.md) | Test Infrastructure Strategy with Quality Gates | 2024-10-10 | Accepted |
| [0013](ADR-0013-tldraw-visual-review-tool.md) | TLDraw Visual Review Tool Integration | 2025-10-28 | Accepted |
| [0014](ADR-0014-crdt-collaboration-architecture.md) | CRDT Collaboration Architecture | 2025-10-28 | Accepted (Deferred) |
| [0015](ADR-0015-multi-camera-metadata-model.md) | Multi-Camera Metadata Model | 2025-10-28 | Accepted (Deferred) |
| [0016](ADR-0016-media-file-syncing-strategy.md) | Media File Syncing Strategy | 2025-10-28 | Accepted (Simplified) |
| [0017](ADR-0017-electron-gui-integration.md) | Electron GUI Integration for Your Project | 2025-10-29 | Accepted |
| [0018](ADR-0018-cli-entry-point-gui-processor.md) | CLI Entry Point and Non-Interactive GUI Processor | 2025-11-04 | Accepted |
| [0019](ADR-0019-data-model-hierarchy.md) | Three-Tier Data Model Hierarchy for Thematic Organization | 2024-09-13 (2025-11-05) | Accepted |
| [0020](ADR-0020-aaf-export-strategy.md) | AAF Export Strategy via OpenTimelineIO for Pro Tools Integration | 2025-10-19 (2025-11-05) | Accepted |
| [0022](ADR-0022-logging-observability-architecture.md) | Logging and Observability Architecture | 2025-11-04 | Accepted |
| [0024](ADR-0024-structured-prompt-template-architecture.md) | Structured Prompt and Template Architecture | 2025-11-04 | Accepted |
| [0025](ADR-0025-workflow-observation-architecture.md) | Workflow Observation and Learning Architecture | 2025-11-04 | Accepted |
| [0026](ADR-0026-diagnostic-tooling-performance-monitoring.md) | Diagnostic Tooling and Performance Monitoring | 2025-11-04 | Accepted |
| [0027](ADR-0027-configuration-architecture.md) | Configuration Architecture and Hierarchy | 2025-11-04 | Accepted |
| [0028](ADR-0028-exception-hierarchy-design.md) | Exception Hierarchy Design | 2025-11-04 | Accepted |
| [0029](ADR-0029-native-macos-gui-strategy.md) | Native macOS GUI Strategy | TBD | Proposed |
| [0030](ADR-0030-swift-python-communication.md) | Swift-Python Communication Architecture | TBD | Proposed |
| [0031](ADR-0031-dual-gui-maintenance-strategy.md) | Dual GUI Maintenance Strategy | TBD | Proposed |
| [0032](ADR-0032-backend-language-python-vs-swift.md) | Backend Language Choice - Python vs Swift | TBD | Accepted |

### ADR Categories

**Priority 1 - Core Architecture**:
- ADR-0001: Exact Timecode Arithmetic Using Fractions
- ADR-0002: Two-Phase Consistent Assembly Architecture
- ADR-0003: Multi-Speaker Workflow Design

**Priority 2 - Data Model & Integration Foundations**:
- ADR-0019: Three-Tier Data Model Hierarchy for Thematic Organization
- ADR-0006: OpenTimelineIO (OTIO) Integration
- ADR-0020: AAF Export Strategy via OpenTimelineIO for Pro Tools Integration
- ADR-0004: Timeline Offset Approach
- ADR-0005: Semantic Parser Integration Strategy

**Priority 3 - API & Infrastructure**:
- ADR-0007: Validation Architecture Separation
- ADR-0008: DaVinci Resolve API Integration Strategy
- ADR-0009: CLI Wizard Workflow Design
- ADR-0010: Frame Rate Handling Strategy

**Priority 4 - Development Infrastructure**:
- ADR-0011: Adversarial Workflow Integration
- ADR-0012: Test Infrastructure Strategy

**Priority 5 - Visual Review Tool (TLDraw)**:
- ADR-0013: TLDraw Visual Review Tool Integration
- ADR-0014: CRDT Collaboration Architecture
- ADR-0015: Multi-Camera Metadata Model
- ADR-0016: Media File Syncing Strategy

**Priority 6 - User Interface & Experience**:
- ADR-0017: Electron GUI Integration for Your Project
- ADR-0018: CLI Entry Point and Non-Interactive GUI Processor

**Priority 7 - Supporting Infrastructure**:
- ADR-0022: Logging and Observability Architecture
- ADR-0024: Structured Prompt and Template Architecture
- ADR-0025: Workflow Observation and Learning Architecture
- ADR-0026: Diagnostic Tooling and Performance Monitoring
- ADR-0027: Configuration Architecture and Hierarchy
- ADR-0028: Exception Hierarchy Design

**Priority 8 - Native macOS GUI (Proposed)**:
- ADR-0029: Native macOS GUI Strategy
- ADR-0030: Swift-Python Communication Architecture
- ADR-0031: Dual GUI Maintenance Strategy
- ADR-0032: Backend Language Choice - Python vs Swift

### Superseded ADRs

None yet.

### ADR Numbering Notes

**ADR-0021**: Reserved for future use. The numbering sequence intentionally skips from ADR-0020 (AAF Export Strategy) to ADR-0022 (Logging Architecture). This gap may be filled with a future ADR related to export format expansion or data interchange strategies.

## Historical Decision Documents

Prior to adopting ADRs (2025-10-21), architectural decisions were documented in:
- Task files (`delegation/tasks/`)
- Planning documents (`docs/RECOVERY-PLAN-2024.md`)
- Commit messages and pull requests
- Issue discussions

These are preserved for historical reference but may be converted to ADRs over time.

## Process

### Creating a New ADR

1. **Identify the decision**: Is this an architectural decision that affects the project's structure, behavior, or future direction?

2. **Assign a number**: Use the next sequential number (check this index)

3. **Draft the ADR**: Use the format above, focusing on:
   - **Context**: What forces led to this decision?
   - **Decision**: What was decided and why?
   - **Consequences**: What are the trade-offs?

4. **Review**: Get feedback from project stakeholders

5. **Accept**: Mark status as "Accepted" and update this index

6. **Commit**: Include the ADR in your commit with appropriate message

### Superseding an ADR

When a decision changes:

1. **Create a new ADR** documenting the new decision
2. **Update the old ADR**: Change status to "Superseded by ADR-XXXX"
3. **Update this index**: Move the old ADR to "Superseded" section
4. **Preserve history**: Never delete or significantly modify accepted ADRs

## When to Write an ADR

**Write an ADR when:**
- ✅ Making architectural choices that affect project structure
- ✅ Choosing between competing technical approaches
- ✅ Establishing patterns or conventions
- ✅ Making trade-offs with significant implications
- ✅ Decisions that future developers will need to understand

**Don't write an ADR for:**
- ❌ Routine bug fixes
- ❌ Feature implementations following established patterns
- ❌ Temporary experimental code
- ❌ Configuration changes without architectural impact

## Related Documentation

- [README.md](../../../README.md) - Project overview
- [docs/RECOVERY-PLAN-2024.md](../../RECOVERY-PLAN-2024.md) - Project recovery timeline
- [delegation/tasks/](../../../delegation/tasks/) - Task specifications
- [docs/roadmap/](../../roadmap/) - Feature roadmaps and enhancements
- [CHANGELOG.md](../../../CHANGELOG.md) - Version history

## References

- [Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) - Michael Nygard
- [ADR GitHub Organization](https://adr.github.io/) - ADR tools and resources
- [Why Write ADRs](https://github.blog/2020-08-13-why-write-adrs/) - GitHub Engineering blog
- [adversarial-workflow ADRs](https://github.com/movito/adversarial-workflow/tree/main/docs/decisions/adr) - Example implementation

## Project-Specific Guidelines

### thematic-cuts ADR Focus Areas

This project's ADRs should particularly focus on:

1. **Precision Engineering**: Decisions affecting frame-perfect accuracy (timecode arithmetic, frame calculations)
2. **DaVinci Resolve Integration**: API integration patterns and workarounds
3. **Multi-Speaker Workflows**: Architectural patterns for handling multiple audio sources
4. **Validation & Quality**: Testing strategies and quality gates
5. **User Experience**: CLI wizard design, workflow patterns

### Examples from thematic-cuts

**Good ADR candidates:**
- ✅ "Why we use Fraction arithmetic instead of floating-point for timecodes" → ADR-0001
- ✅ "Two-phase assembly architecture for consistent track composition" → ADR-0002
- ✅ "Multi-speaker workflow with sequential track assignment" → ADR-0003

**Not ADR candidates:**
- ❌ "Fixed bug in timeline offset calculation" → Bug fix, not architectural
- ❌ "Updated CLI help text" → Documentation improvement, not architecture
- ❌ "Bumped version to 1.0.3" → Version management, not architecture

---

**Maintainer**: document-reviewer agent, coordinator, tycho
**Last Updated**: 2025-11-09
**ADR Count**: 30 active (27 accepted, 3 proposed), 0 superseded
**Phase**: Phase 2 complete + GUI Integration + Infrastructure Documentation + Native macOS GUI (Proposed)
**Naming Convention**: ADR-####-description.md (standardized 2025-11-09)
**Status**: All ADRs follow consistent naming convention. Native macOS GUI strategy proposals added (ADRs 0029-0032).
