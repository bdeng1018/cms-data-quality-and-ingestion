# 🔐 Security Policy

This repository implements a deterministic, multi‑stage CMS ingestion and data‑quality pipeline.
Although it does not expose a public API, contributors may encounter issues related to:

- ingestion correctness
- schema validation
- data‑quality metrics
- reporting logic
- pipeline runner behavior
- diagnostics scripts
- reproducibility and deterministic execution
- C++ mechanization (validators, row counters, ingestion utilities)

---

## 🛡 Branch 1 Security Scope

Branch 1 processes **only public CMS datasets** and contains **no PHI/PII**.
All execution is deterministic, reproducible, and infrastructure‑only (Stages 01–06).

### C++ Mechanization (v1.1.0)

Stage 01 and Stage 02 now include deterministic C++ binaries:

- schema validator
- row counter
- ingestion utilities

These binaries run in a **sandboxed subprocess environment** and must:

- never mutate source data
- never write outside `/app/data` or `/app/logs`
- produce deterministic output
- propagate exit codes correctly
- comply with CONTRACTS.md and MANIFEST_SPEC.md

AI/RAG/agentic inference will be introduced in **Branch 2**.
No AI‑driven logic should be added to Branch 1.

If you believe you have found a security‑relevant issue, please follow the guidelines below.

---

## 📣 Reporting a Vulnerability

Please report all security or data‑integrity issues privately.

Maintainer: **Brian Deng** <br>
Email: **<bdeng.data.pipelines@gmail.com>**

You may report:

- ingestion failures that could corrupt downstream stages
- schema violations not caught by Stage 01 (Python or C++)
- C++ mechanization errors, nondeterministic behavior, or unsafe subprocess execution
- data‑quality logic producing incorrect metrics
- reporting layer inconsistencies
- pipeline runner misbehavior (Stage 05)
- diagnostics scripts that expose sensitive data
- reproducibility issues affecting deterministic execution
- any behavior violating deployment contracts (CONTRACTS.md, OPERATIONS.md, MANIFEST_SPEC.md)
- compiler‑related reproducibility issues (e.g., mismatched `cpp_compiler_version`)

Do **not** open a public GitHub Issue for security‑related findings.

---

## 🕒 Response Expectations

You will receive an initial response within **72 hours**.
A full assessment or fix may take longer depending on complexity.

---

## 🔄 Disclosure Process

If the issue is confirmed:

- a dedicated patch branch will be created
- regression tests will be added (Python + C++)
- documentation will be updated
- mechanization provenance fields will be validated
- the fix will be included in the next semantic version release
- the changelog will record the resolution under `[Unreleased]`

---

## 🧪 Non‑Security Bugs

For non‑security issues (tests, formatting, diagnostics, Makefile targets, mechanization build failures, etc.), please use:

- GitHub Issues
- GitHub Discussions (if enabled)
- Pull Requests
