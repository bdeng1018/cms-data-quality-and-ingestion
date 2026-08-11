/**
 * @file csv_row_counter.cpp
 * @brief Deterministic CSV row-counting utility for ingestion diagnostics.
 *
 * This tool must produce *pure* deterministic output:
 *   - stdout: ONLY the integer row count
 *   - stderr: EMPTY on success
 *   - exit code: 0 on success
 */

#include <iostream>
#include <fstream>
#include <string>

int main(int argc, char* argv[]) {
    if (argc < 2) {
        // Contract: stderr must be empty on success, but errors may print.
        std::cerr << "Usage: csv_row_counter <file.csv>\n";
        return 1;
    }

    const std::string filepath = argv[1];

    std::ifstream file(filepath);
    if (!file.is_open()) {
        std::cerr << "Cannot open file: " << filepath << "\n";
        return 2;
    }

    std::string line;
    long long count = 0;

    while (std::getline(file, line)) {
        count++;
    }

    // Contract: stdout must contain ONLY the integer.
    std::cout << count << std::endl;

    return 0;
}
