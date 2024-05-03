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


### Usage Instructions

#### Step 1: Prepare Your Data

1. **Organize Transaction Data**: Ensure your bank transaction data is saved in a CSV file with the following format: Date, Description, Amount, and Currency.

#### Step 2: Install Dependencies

1. **Install Python**: If Python is not already installed, download and install it from the [official website](https://www.python.org/downloads/).

2. **Install Required Packages**: Open a terminal or command prompt and run: "pip install gspread google-auth csv"

   
#### Step 3: Configure Google Sheets

1. **Create/Open Google Sheets Document**: Access [Google Sheets](https://sheets.google.com/) and create a new document or open an existing one.

2. **Enable Google Sheets API**: Follow the [instructions](https://developers.google.com/sheets/api/quickstart/python) to enable the Google Sheets API for your project.

3. **Generate Service Account Key**: Create a service account key with permissions to edit the Google Sheets document. Download the JSON key file and note its location.

4. **Share Google Sheets Document**: Share the Google Sheets document with the email address associated with the service account.

#### Step 4: Update Script Configuration

1. **Edit the Script**: Open the `bank_transaction_categorizer.py` script in a text editor.

2. **Set File Paths**: Update the `MONTH`, `file`, and `output_file` variables with the appropriate file paths.

3. **Set Google Sheets Credentials**: Set the path to the JSON key file generated for the service account in the `gc = gspread.service_account()` line.

4. **Set Google Sheets Document Name**: Update the `sh = gc.open("Your Google Sheets Document Name")` line with the name of your Google Sheets document.

5. **Set Worksheet Name**: Update the `wks = sh.worksheet("Your Worksheet Name")` line with the name of the worksheet within your Google Sheets document.

6. **Define Transaction Categories**: Define your transaction categories in the `categories` dictionary within the script.

#### Step 5: Run the Script

1. **Execute the Script**: Open a terminal or command prompt, navigate to the directory containing the script and CSV file, and run: "python bank_transaction_categorizer.py"

   
2. **Review Output**: The script will categorize the transactions, update the Google Sheets document, and display total spending, total income, and savings in the terminal.

### Help

If you need extra help with this code due to confusion, utilize something like chatgp to help you through.
The pretty visuals in the gspread portion of code came from chatgpt so you can do something similar.

### Contributions

Contributions to this project are welcome! If you have any suggestions, improvements, or bug fixes, feel free to open an issue or submit a pull request.

### License

This project is licensed under the [MIT License](LICENSE).
