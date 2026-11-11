# A'Space Spynel Adapter DOX

## Purpose

- Own the A'Space adapter for spynel (`fiber:a0:spynel`): a read-only
  contract that observes the frozen spynel orchestration surface (entry
  point, harness workers, orchestrator, jobs, channels, local API) and
  references `fiber:a0:agent-zero` as its orchestration target without
  duplicating the agent-zero loop or any spynel code.

## Local Contracts

- The adapter is Python, standard library only: no network import, no
  network call, no write, no upstream file modified.
- The adapter never imports spynel code and never calls a coding harness
  directly; it reads the frozen tree and reports measurements.
- Spynel itself is described as in the repository DOX: a classic, non-AI
  program that coordinates and oversees external AI/coding harnesses.
  "Simplicity at scale." No invented capabilities, integrations,
  guarantees, or adoption claims.
- This directory is A'Space-owned adapter scope inside the sovereign fork
  `Amdkn/spynel` (D-N053 pas B); the upstream remains byte-identical to
  the gel except for the one-line DOX index entry in the root AGENTS.md
  that registers this directory (DOX-required, see the adaptation sheet).

## Child DOX Index

Direct child DOX files:

| Child | Scope |
| --- | --- |
| [aspace_spynel_adapter/AGENTS.md](aspace_spynel_adapter/AGENTS.md) | Adapter package (validate / doctor / describe). |
| [tests/AGENTS.md](tests/AGENTS.md) | Adapter smoke tests. |
