# ADR 0010: Keep a local `nodalia-ai-core` until nodalia-libs has what it lacks

- **Status:** accepted 20/10/2026
- **Source:** [CORE-SYNC.md](../CORE-SYNC.md)

## Context

The contract crate has landed in `getnodalia/foundation (nodalia/libs)`, but it lacks `ConsentTerm` and `model_folders`. Dropping either would break consumers or lose a person's model-folder map on a rewrite.

## Decision

This workspace keeps its own copy of `nodalia-ai-core`. Safety fixes stay aligned in both copies. The switch to one pinned nodalia-libs revision waits until the missing additions are reviewed upstream.

## Consequences

Two copies exist for now and must not be mixed in one app. CORE-SYNC.md lists the steps to switch.
