// =============================================================================
// schema_validator.cpp
// Deterministic lightweight schema validator for Stage 05 mechanization layer.
// This is NOT the Stage 01 validator. It performs a minimal comparison between
// expected and actual schema strings and returns stable exit codes:
//
//   0 → VALID
//   1 → argument error
//   2 → INVALID:SCHEMA_MISMATCH
//
// Used by run_schema_validator.py and Stage 05 diagnostics.
// =============================================================================

#include <iostream>
#include <vector>
#include <string>
#include <algorithm>

// =============================================================================
// Minimal deterministic schema validator for mechanization layer (Stage 05)
// This is NOT the Stage 01 validator. It is intentionally lightweight.
// =============================================================================

int main(int argc, char** argv) {
    if (argc < 3) {
        std::cout << "ERROR:SCHEMA_VALIDATOR:ARGS" << std::endl;
        return 1;
    }

    std::string expected = argv[1];
    std::string actual   = argv[2];

    // Deterministic comparison
    if (expected == actual) {
        std::cout << "VALID" << std::endl;
        return 0;
    }

    std::cout << "INVALID:SCHEMA_MISMATCH" << std::endl;
    return 2;
}
