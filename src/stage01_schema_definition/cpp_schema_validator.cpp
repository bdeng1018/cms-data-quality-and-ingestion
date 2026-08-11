/**
 * =============================================================================
 * CMS Data Quality & Ingestion Pipeline
 * Stage 01 — Deterministic CSV Schema Validator (C++)
 * =============================================================================
 *
 * Summary
 * -------
 * A deterministic, test‑driven schema validator used at the ingestion boundary
 * of the CMS Data Quality & Ingestion Pipeline. This validator enforces strict
 * schema contracts for Stage 01 and guarantees reproducible behavior across
 * local development, CI/CD, Docker, and Kubernetes environments.
 *
 * Purpose
 * -------
 * The validator ensures that incoming CSV files conform exactly to the schema
 * defined in a separate schema file. It performs:
 *
 *   - exact column count validation
 *   - exact column order validation
 *   - exact column name validation
 *   - deterministic error signaling
 *
 * This validator is intentionally minimal and stable. It produces single‑token
 * outputs that are consumed by Python tests, diagnostics, and provenance
 * tracking. No logging, no prefixes, and no descriptive messages are emitted.
 *
 * Inputs
 * ------
 * 1. schema_path : string
 *      Path to a text file containing one column name per line, in order.
 *
 * 2. csv_path : string
 *      Path to a CSV file whose header row will be validated.
 *
 * Expected Output Contract
 * ------------------------
 * The validator must emit exactly one of the following uppercase tokens:
 *
 *   VALID
 *       The CSV header matches the schema exactly.
 *
 *   COLUMN_COUNT_MISMATCH
 *       The number of columns in the CSV header differs from the schema.
 *
 *   COLUMN_NAME_MISMATCH
 *       One or more column names differ from the schema at the same position.
 *
 *   EMPTY_CSV
 *       The CSV file is unreadable, missing, or contains no header row.
 *
 * Determinism Requirements
 * ------------------------
 * - Output must be a single token with no additional text.
 * - No logging prefixes (e.g., "[info]", "[error]").
 * - No error codes (e.g., "E001").
 * - No descriptive messages or contextual details.
 * - No trailing whitespace or extra newlines.
 * - Exit code 0 for VALID, non‑zero for all error conditions.
 *
 * Why C++
 * -------
 * - Compiled determinism across environments
 * - Stable, audit‑friendly boundary enforcement
 * - Zero dependency on Python runtime
 * - Predictable performance for large schema files
 *
 * Example
 * -------
 * Schema file (schema.txt):
 *     id
 *     facility_name
 *     address
 *     city
 *     state
 *     zip
 *
 * CSV file (input.csv):
 *     id,facility_name,address,city,state,zip
 *
 * Invocation:
 *     ./cpp_schema_validator schema.txt input.csv
 *
 * Output:
 *     VALID
 *
 * Integration
 * -----------
 * This validator is invoked by:
 *   - Stage 01 diagnostics
 *   - Python ingestion pipeline
 *   - CI/CD validation suite
 *   - provenance + manifest generation
 *
 * It is a deterministic boundary component and must remain stable across
 * versions unless schema contracts change.
 *
 * =============================================================================
 */

#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>

using namespace std;

// =============================================================================
// Utility: trim whitespace
// =============================================================================
string trim(const string &s) {
    size_t start = s.find_first_not_of(" \t\r\n");
    size_t end = s.find_last_not_of(" \t\r\n");
    if (start == string::npos) return "";
    return s.substr(start, end - start + 1);
}

// =============================================================================
// Load schema file (list of required columns)
// =============================================================================
vector<string> load_schema(const string &schema_path) {
    vector<string> schema;
    ifstream file(schema_path);

    if (!file.is_open()) {
        cerr << "EMPTY_CSV" << endl;
        exit(1);
    }

    string line;
    while (getline(file, line)) {
        string col = trim(line);
        if (!col.empty()) {
            schema.push_back(col);
        }
    }

    if (schema.empty()) {
        cerr << "EMPTY_CSV" << endl;
        exit(1);
    }

    return schema;
}

// =============================================================================
// Load first row of CSV (header)
// =============================================================================
vector<string> load_csv_header(const string &csv_path) {
    ifstream file(csv_path);

    if (!file.is_open()) {
        cerr << "EMPTY_CSV" << endl;
        exit(1);
    }

    string header_line;
    if (!getline(file, header_line)) {
        cerr << "EMPTY_CSV" << endl;
        exit(1);
    }

    vector<string> header;
    string token;
    stringstream ss(header_line);

    while (getline(ss, token, ',')) {
        header.push_back(trim(token));
    }

    return header;
}

// =============================================================================
// Main validation logic
// =============================================================================
int main(int argc, char *argv[]) {
    if (argc != 3) {
        cerr << "EMPTY_CSV" << endl;
        return 1;
    }

    string schema_path = argv[1];
    string csv_path = argv[2];

    vector<string> schema = load_schema(schema_path);
    vector<string> header = load_csv_header(csv_path);

    // 1. Column count check
    if (schema.size() != header.size()) {
        cerr << "COLUMN_COUNT_MISMATCH" << endl;
        return 1;
    }

    // 2. Column name + order check
    for (size_t i = 0; i < schema.size(); i++) {
        if (schema[i] != header[i]) {
            cerr << "COLUMN_NAME_MISMATCH" << endl;
            return 1;
        }
    }

    // If everything matches:
    cout << "VALID" << endl;
    return 0;
}
