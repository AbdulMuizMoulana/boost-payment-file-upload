import time

import pandas as pd
import xlwings as xw
from pathlib import Path


# =========================
# READ DATA (SAFE – READ ONLY)
# =========================
def read_payment_excel(file_path):
    df = pd.read_excel(file_path, header=2)

    df = df[
        [
            "Intercept Email Address",
            "Supplier Name",
            "Gateway Supplier ID"
        ]
    ]
    # Remove rows where email is missing
    df = df.dropna(subset=["Intercept Email Address"])
    # Remove duplicate emails (DOES NOT TOUCH ORIGINAL FILE)

    total_transactions = len(df)

    df = df.drop_duplicates(subset=["Intercept Email Address"])
    return df


# =========================
# STATE MANAGEMENT
# =========================
STATE_FILE = Path("last_start_amount.txt")


def get_next_start_amount():
    if STATE_FILE.exists():
        start = int(STATE_FILE.read_text().strip())
    else:
        start = 211

    #  AUTO RESET AFTER 510
    if start > 411:
        start = 211

    STATE_FILE.write_text(str(start + 100))
    return start


# =========================
# SAFE EXCEL UPDATE (NO FORMAT LOSS)
# =========================
def update_amounts(excel_path):
    start_amount = get_next_start_amount()

    # app = xw.App(visible=False)
    app = xw.App(visible=False, add_book=False)

    try:
        wb = app.books.open(str(excel_path))
        sheet = wb.sheets[0]  # change if needed

        HEADER_ROW = 3  # headers are on row 3
        DATA_START_ROW = HEADER_ROW + 1

        headers = sheet.range(f"A{HEADER_ROW}").expand("right").value

        invoice_col = headers.index("Invoice Amount") + 1
        total_col = headers.index("Total Amount") + 1

        row = HEADER_ROW + 1
        amount = start_amount

        data_range = sheet.range(f"A{DATA_START_ROW}").expand("table")
        num_rows = data_range.rows.count

        #  EXACTLY 10 ROWS
        for _ in range(num_rows):
            sheet.range(row, invoice_col).value = f"{amount:.2f}"
            sheet.range(row, total_col).value = f"{amount:.2f}"
            amount += 11
            row += 1

        # refresh formulas (date column etc.)
        wb.app.calculate()
        wb.save()
        wb.close()
        time.sleep(1)
        print(
            f"Invoice amounts updated successfully "
            f"(start={start_amount}, end={amount - 11})"
        )

    finally:
        app.quit()


from openpyxl import load_workbook


def read_excel_totals(excel_path):
    """
       Reads:
       Payments Total  -> cell H1
       Invoice Total   -> cell Z1

       Sheet name: 'payment entry'
       """

    wb = load_workbook(excel_path, data_only=True)
    sheet = wb["Payment_Entry"]

    payments_total = sheet["I1"].value
    invoice_total = sheet["Z1"].value

    if payments_total is None or invoice_total is None:
        raise ValueError(
            f"Excel totals missing: Payments={payments_total}, Invoice={invoice_total}"
        )

    # Normalize → float
    payments_total = float(str(payments_total).replace(",", ""))
    invoice_total = float(str(invoice_total).replace(",", ""))

    return payments_total, invoice_total


"""
def update_amounts(excel_path):
    # Get the starting amount for this run
    # (211, 311, or 411 depending on previous runs)
    start_amount = get_next_start_amount()

    # Launch Excel in background (no UI)
    app = xw.App(visible=False)
    try:
        # Open the Excel file using xlwings
        wb = app.books.open(str(excel_path))

        # Access the first worksheet
        # (change index or name if required)
        sheet = wb.sheets[0]

        # Row number where column headers exist in Excel
        HEADER_ROW = 3

        # Read all header names from header row
        # expand("right") reads until last non-empty cell
        headers = sheet.range(f"A{HEADER_ROW}").expand("right").value

        # Find column index of "Invoice Amount"
        # +1 because Excel columns are 1-based
        invoice_col = headers.index("Invoice Amount") + 1

        # Find column index of "Total Amount"
        total_col = headers.index("Total Amount") + 1

        # Start writing data from the row below headers
        row = HEADER_ROW + 1

        # Initialize amount with the start amount
        amount = start_amount

        # Update EXACTLY 10 rows
        for _ in range(10):
            # Write amount in "Invoice Amount" column
            sheet.range(row, invoice_col).value = f"{amount:.2f}"

            # Write same amount in "Total Amount" column
            sheet.range(row, total_col).value = f"{amount:.2f}"

            # Increase amount by 11 for next row
            amount += 11

            # Move to next row
            row += 1

        # Force Excel to recalculate formulas
        # (important for date or calculated columns)
        wb.app.calculate()

        # Save changes to the same file
        wb.save()

        # Close workbook
        wb.close()

        # Log success info
        print(
            f"Invoice amounts updated successfully "
            f"(start={start_amount}, end={amount - 11})"
        )

    finally:
        # Always close Excel application to avoid zombie processes
        app.quit()
"""
