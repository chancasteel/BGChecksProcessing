# BGChecksProcessing

A Python script for processing background check data.

## Description

This script processes background check data from a CSV file, formats the data, and outputs the results to a text file. The script performs the following tasks:

1. Reads the input CSV file.
2. Processes each row to format the name, gender, race, and other details.
3. Removes duplicates based on Social Security Number (SSN).
4. Sorts the data by name.
5. Outputs the formatted data to a text file.

## Requirements

- Python 3.x
- pandas library

## Installation

Install the required dependencies:
    ```sh
    pip install pandas
    pip install logging
    ```

## Usage

1. Place the input CSV file (e.g., `BGChecks.csv`) in the repository directory.

2. Run the script:
    ```sh
    python bg_checks_processing.py
    ```

3. The processed data will be output to `BG_Checks_Export.txt`.

## Script Details

### Functions

- `get_gender_code(gender: str) -> str`
  - Converts a gender string to a single-character code ('M', 'F', or 'E' for error/unknown).

- `get_race_code(race: str) -> str`
  - Converts a race string to a single-character code ('W', 'B', 'U' for unknown, or 'W' for Hispanic as white).

- `format_name(name: str) -> str`
  - Formats the name by removing certain characters and reordering it to "LAST,FIRST" format padded to 30 characters.

- `process_row(row: pd.Series) -> dict`
  - Processes a DataFrame row and returns a dictionary with formatted data.

### Logging

The script uses the `logging` module to provide detailed debug information during execution. This helps in tracing the computation values step-by-step.

## Example

Input CSV (`BGChecks.csv`):
```csv
Applicant Full Name,Gender,Local Race,Date of Birth,Social Security Number
Doe, John,M,White,1990-01-01,123-45-6789
Smith, Jane,F,Black,1985-05-15,987-65-4321
