## ExpenseTrackerPy

### Overview

This repository contains a Python script designed to categorize bank transactions and export them to a Google Sheets document. The script takes a CSV file containing transaction data as input, categorizes each transaction based on predefined categories, calculates total spending, total income, and leftover amount, and then writes the categorized transactions and summary to a Google Sheets document.

### Contents

- **bank_transaction_categorizer.py**: This Python script is the main component of the project. It contains functions to read the transaction data from a CSV file, categorize transactions, calculate financial summaries, and write the results to a Google Sheets document.

### Dependencies

- [gspread](https://github.com/burnash/gspread): Python API for Google Sheets.
- [Google APIs Client Library for Python](https://github.com/googleapis/google-api-python-client): Required for interacting with Google Sheets APIs.
- [Python CSV module](https://docs.python.org/3/library/csv.html): Used for reading and writing CSV files.
- [time module](https://docs.python.org/3/library/time.html): Used for adding delays to avoid API rate limits.
- [google-auth module](https://github.com/googleapis/google-auth-library-python): Required for authentication with Google services.

### Usage

1. Ensure you have installed the required dependencies mentioned above.
2. Prepare your bank transaction data in a CSV file with the following format: [Date, Description, Amount, Currency].
3. Update the script with your Google Sheets document name and desired worksheet name.
4. Define your transaction categories in the `categories` dictionary within the script.
5. Run the script, and it will categorize the transactions and write them to the specified Google Sheets document.

### Contributions

Contributions to this project are welcome! If you have any suggestions, improvements, or bug fixes, feel free to open an issue or submit a pull request.

### License

This project is licensed under the [MIT License](LICENSE).
