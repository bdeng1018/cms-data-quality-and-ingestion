# Changelog

All notable changes to this project will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and semantic versioning.

---

## [Unreleased]

### In Progress

- Stage 05 pipeline runner (Branch 1 final component)
- Additional diagnostics for multi-stage execution
- README updates for Stage 05
- Makefile integration for full pipeline orchestration

---

## [0.1.0] — Pending Release

### Branch 1 MVP — Stages 1–4 Complete

### Added

- Stage 01 — Schema Definition & Validation  
- Stage 02 — Raw Ingestion  
- Stage 03 — Data Quality Profiling  
- Stage 04 — Reporting Layer  
- Makefile workflow (stage01–stage04, reset, diagnostics, tests)  
- Logging system (ingestion, quality, runner)  
- Full test suite across all stages  
- Diagnostics scripts for each stage  
- Repository structure and environment setup  
- Diagrams for pipeline architecture and schema overview

### Changed

- Updated root README to include Stage 04  
- Improved Makefile reset target  
- Standardized directory structure  
- Unified logging configuration

### Fixed

- POS/QIES dtype inconsistencies  
- Stage 03 missing-key behavior  
- Stage 04 manifest generation  
- Facility health classification edge cases

### Notes

- Stage 05 scaffold exists but is not part of v0.1.0  
- Data directories included for reproducibility  
