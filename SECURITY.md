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

---

## 🛡 Branch 1 Security Scope

Branch 1 processes **only public CMS datasets** and contains **no PHI/PII**.  
All execution is deterministic, reproducible, and infrastructure‑only (Stages 01–06).

AI/RAG/agentic inference will be introduced in **Branch 2**.  
No AI‑driven logic should be added to Branch 1.

If you believe you have found a security‑relevant issue, please follow the guidelines below.

---

## 📣 Reporting a Vulnerability

Please report all security or data‑integrity issues privately.

Maintainer: **Brian Deng**  
Email: **<bdeng.data.pipelines@gmail.com>**

You may report:

- ingestion failures that could corrupt downstream stages  
- schema violations not caught by Stage 01  
- data‑quality logic producing incorrect metrics  
- reporting layer inconsistencies  
- pipeline runner misbehavior (Stage 05)  
- diagnostics scripts that expose sensitive data  
- reproducibility issues affecting deterministic execution  
- any behavior violating deployment contracts (CONTRACTS.md, OPERATIONS.md, MANIFEST_SPEC.md)

Do **not** open a public GitHub Issue for security‑related findings.

---

## 🕒 Response Expectations

You will receive an initial response within **72 hours**.  
A full assessment or fix may take longer depending on complexity.

---

## 🔄 Disclosure Process

If the issue is confirmed:

- a dedicated patch branch will be created  
- regression tests will be added  
- documentation will be updated  
- the fix will be included in the next semantic version release  
- the changelog will record the resolution under `[Unreleased]`  

---

## 🧪 Non‑Security Bugs

For non‑security issues (tests, formatting, diagnostics, Makefile targets, etc.), please use:

- GitHub Issues  
- GitHub Discussions (if enabled)  
- Pull Requests  
