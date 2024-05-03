import csv
import gspread
import sys
import time
from googleapiclient.errors import HttpError

def write_to_google_sheets(worksheet, output_file, total_spending, total_income, leftover_amount):
    # Open the CSV file and read the data
    with open(output_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)
    
    # Clear the worksheet
    worksheet.clear()
    
    # Update the worksheet with data
    batch_data = [data[0]] + data[1:]
    worksheet.update(batch_data)

    # Write total spending, total income, and leftover amount horizontally starting at row 2
    values = [
        [f'Total spending: ${total_spending:.2f}'],
        [f'Total income: ${total_income:.2f}'],
        [f'Leftover amount: ${leftover_amount:.2f}']
    ]
    worksheet.update(values, 'G2:I4')

    # Apply formatting to header row
    header_format = {
        "textFormat": {"fontSize": 14, "bold": True, "foregroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0}},
        "backgroundColor": {"red": 0.2, "green": 0.4, "blue": 0.8},
        "horizontalAlignment": "CENTER",
        "verticalAlignment": "MIDDLE",
        "wrapStrategy": "WRAP",
        "borders": {"bottom": {"style": "SOLID", "width": 1}},
    }
    worksheet.format("A1:H1", header_format)

    # Apply alternating row colors to body
    num_rows = len(data)
    for i in range(2, num_rows + 1, 2):
        body_format = {
            "backgroundColor": {"red": 0.95, "green": 0.95, "blue": 0.95},
            "borders": {"bottom": {"style": "SOLID", "width": 1}},
        }
        worksheet.format(f"A{i}:H{i}", body_format)

    # Apply currency formatting to Amount column
    currency_format = {
        "numberFormat": {"type": "CURRENCY", "pattern": "$#,##0.00"},
        "horizontalAlignment": "RIGHT",
    }
    worksheet.format(f"D2:D{num_rows}", currency_format)

    # Align numeric data to the right
    numeric_format = {"horizontalAlignment": "RIGHT"}
    worksheet.format(f"D2:D{num_rows}", numeric_format)

    # Set column widths
    column_widths = {
        1: 120,  # Adjust the width of column A
        2: 120,  # Adjust the width of column B
        3: 180,  # Adjust the width of column C
        4: 300,  # Adjust the width of column D
        5: 120,  # Adjust the width of column E
        6: 120,  # Adjust the width of column F
        7: 120,  # Adjust the width of column G
        8: 120,  # Adjust the width of column H
    }
    for col, width in column_widths.items():
        worksheet.adjust_column_width(col, width)

    # Freeze the header row
    worksheet.freeze(rows=1)

    # Autofit columns
    worksheet.resize(columns="A:H")

    # Apply additional formatting to alternating rows for better visibility
    for i in range(2, num_rows + 1, 2):
        body_format = {
            "backgroundColor": {"red": 0.92, "green": 0.92, "blue": 0.92},
            "borders": {"bottom": {"style": "SOLID", "width": 1}},
        }
        worksheet.format(f"A{i}:H{i}", body_format)

    # Apply bold text and different colors to total spending, total income, and leftover amount rows
    total_format = {
        "textFormat": {"fontSize": 12, "bold": True, "foregroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0}},
        "backgroundColor": {"red": 0.3, "green": 0.6, "blue": 0.4},
        "horizontalAlignment": "CENTER",
        "verticalAlignment": "MIDDLE",
        "wrapStrategy": "WRAP",
        "borders": {"bottom": {"style": "SOLID", "width": 1}},
    }
    worksheet.format("G2:I4", total_format)

    # Apply borders to the total spending, total income, and leftover amount rows
    for i in range(2, 5):
        border_format = {"borders": {"top": {"style": "SOLID", "width": 1}}}
        worksheet.format(f"G{i}:I{i}", border_format)

def main():
    try:
        MONTH = 'apr2024'
        file = f"transactions_{MONTH}.csv"
        output_file = f"categorized_transactions_{MONTH}.csv"

        total_spend = 0
        total_income = 0

        categories = {
            # Define your categories here
        }

        # Authenticate with Google Sheets
        gc = gspread.service_account()

        # Open the Google Sheets document
        sh = gc.open("Your Google Sheets Document Name")

        # Access the desired worksheet (replace 'Sheet1' with the actual name)
        wks = sh.worksheet("Your Worksheet Name") 

        with open(file, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header row
            batch_rows = []
            for row in reader:
                if len(row) >= 6:
                    date = row[0]
                    description = row[2]
                    debit = row[3].replace('$', '').replace(',', '')
                    credit = row[4].replace('$', '').replace(',', '')
                    amount = float(debit) if debit else float(credit)
                    if "deposit transfer" not in description.lower():
                        category, matched_keyword = categorize_transaction(description, categories)
                        if debit:
                            total_spend += amount
                        else:
                            total_income += amount
                        batch_rows.append([date, category, description, f"${amount:.2f}", matched_keyword])
                else:
                    print("Error: Row does not contain enough columns.")

                # Batch write every 50 rows
                if len(batch_rows) >= 50:
                    wks.append_rows(batch_rows)
                    batch_rows = []
                    time.sleep(1)  # Add a short delay to avoid quota issues

        # Write remaining rows
        if batch_rows:
            wks.append_rows(batch_rows)
            time.sleep(1)  # Add a short delay to avoid quota issues

        # Output total spending, total income, and savings
        print(f"Total spending: ${total_spend:.2f}")
        print(f"Total income: ${total_income:.2f}")
        print(f"Savings: ${total_income - total_spend:.2f}")
        
        # Calculate leftover amount
        leftover_amount = total_income - total_spend

        # Export categorized transactions
        export_categorized_transactions(file, output_file, categories)

        # Write data to Google Sheets
        write_to_google_sheets(wks, output_file, total_spend, total_income, leftover_amount)


    except FileNotFoundError:
        print(f"Error: File '{file}' not found.")
        sys.exit(1)
    except csv.Error as e:
        print(f"CSV Error: {e}")
        sys.exit(1)
    except HttpError as err:
        if err.resp.status == 429:
            print("Quota exceeded. Waiting for 1 minute before retrying...")
            time.sleep(60)
            main()  # Retry
        else:
            print(f"HTTP Error: {err}")
            sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

def categorize_transaction(description, categories):
    matched_category = 'Other'
    matched_keyword = 'N/A'
    max_matches = 0
    for category, keywords in categories.items():
        num_matches = sum(1 for keyword in keywords if keyword.lower() in description.lower())
        if num_matches > max_matches:
            max_matches = num_matches
            matched_category = category
            matched_keyword = ", ".join([keyword for keyword in keywords if keyword.lower() in description.lower()])
    return matched_category, matched_keyword

def export_categorized_transactions(input_file, output_file, categories):
    categorized_transactions = []
    with open(input_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row
        for row in reader:
            if len(row) >= 6:
                date = row[0]
                description = row[2]
                debit = row[3].replace('$', '').replace(',', '')
                credit = row[4].replace('$', '').replace(',', '')
                amount = float(debit) if debit else float(credit)
                if "deposit transfer" not in description.lower():
                    category, matched_keyword = categorize_transaction(description, categories)
                    categorized_transactions.append([date, category, description, amount, matched_keyword])

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Date', 'Category', 'Description', 'Amount', 'Matched Keyword'])
        writer.writerows(categorized_transactions)

if __name__ == "__main__":
    main()
