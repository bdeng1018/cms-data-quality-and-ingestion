# 🔐 Security Policy

This project implements a multi‑stage CMS ingestion and data‑quality pipeline.
Although it does not expose a public API, contributors and users may discover issues related to:

- ingestion correctness
- schema validation
- data‑quality metrics
- reporting logic
- pipeline runner behavior
- diagnostics scripts
- reproducibility and deterministic execution

If you believe you have found a security‑relevant issue, please follow the guidelines below.

---

## 📣 Reporting a Vulnerability

Please report all security or data‑integrity issues privately.

Maintainer: **Brian Deng** <br>
Email: **<bdeng.data.pipelines@gmail.com>**

You may report:

- ingestion failures that could corrupt downstream stages
- schema violations not caught by Stage 01
- data‑quality logic that produces incorrect metrics
- reporting layer inconsistencies
- pipeline runner misbehavior (Stage 05)
- diagnostics scripts that expose sensitive data
- any reproducibility issue that affects deterministic execution

Do **not** open a public GitHub Issue for security‑related findings.

---

## 🕒 Response Expectations

You will receive an initial response within **72 hours**.
A full assessment or fix may take longer depending on complexity.

---

## 🔄 Disclosure Process

If the issue is confirmed:

- it will be patched in a dedicated branch
- tests will be added to prevent regression
- documentation will be updated
- the fix will be included in the next semantic version release
- the changelog will record the resolution under `[Unreleased]`

---

## 🧪 Non‑Security Bugs

For non‑security issues (tests, formatting, diagnostics, Makefile targets, etc.), please use:

- GitHub Issues
- GitHub Discussions (if enabled)
- Pull Requests
