# import pandas as pd
# from pathlib import Path
# import xlwings as xw
#
#
# def read_payment_excel(file_path):
#     # Row 1 contains actual headers
#     df = pd.read_excel(file_path, header=2)
#
#     # Keep only required columns
#     df = df[
#         [
#             "Intercept Email Address",
#             "Supplier Name",
#             "Gateway Supplier ID"
#         ]
#     ]
#
#     # Remove rows where email is missing
#     df = df.dropna(subset=["Intercept Email Address"])
#
#     # Remove duplicate emails (DOES NOT TOUCH ORIGINAL FILE)
#     df = df.drop_duplicates(subset=["Intercept Email Address"])
#
#     return df
#
#
# # STATE_FILE = Path("last_start_amount.txt")
# #
# #
# # def get_next_start_amount():
# #     if STATE_FILE.exists():
# #         start = int(STATE_FILE.read_text().strip())
# #     else:
# #         start = 211  # first run
# #
# #     if start > 510:
# #         raise ValueError("Amount exceeded 510. Reset required.")
# #
# #     # Save next start for future run
# #     STATE_FILE.write_text(str(start + 100))
# #
# #     return start
#
#
# def generate_amounts(start_amount, count):
#     """
#     Generates amounts like:
#     211.00, 222.00, 233.00 ...
#     """
#     return [f"{start_amount + i * 11:.2f}" for i in range(count)]
#
#
# # def update_invoice_amounts(excel_path, amount_column_1="Invoice Amount", amount_column_2="Total Amount"):
# #     df = pd.read_excel(excel_path, header=2)
# #
# #     start_amount = get_next_start_amount()
# #     amounts = generate_amounts(start_amount, len(df))
# #
# #     df[amount_column_1] = amounts
# #     df[amount_column_2] = df[amount_column_1]
# #
# #     # Save back to SAME file (overwrite)
# #     # df.to_excel(excel_path, index=False)
# #     with pd.ExcelWriter(excel_path, engine="openpyxl", mode="w") as writer:
# #         df.to_excel(writer, index=False)
# #
# #     return start_amount
#
#
#
# STATE_FILE = Path("last_start_amount.txt")
#
#
# def get_next_start_amount():
#     if STATE_FILE.exists():
#         start = int(STATE_FILE.read_text().strip())
#     else:
#         start = 211
#
#     if start > 510:
#         raise ValueError("Amount exceeded 510. Reset required.")
#
#     STATE_FILE.write_text(str(start + 100))
#     return start
#
#
# def update_invoice_amounts_safe(excel_path):
#     start_amount = get_next_start_amount()
#
#     app = xw.App(visible=False)
#     try:
#         wb = app.books.open(str(excel_path))
#         sheet = wb.sheets[0]  # or use name if known
#
#         # Find header row (you said headers start at row 3)
#         header_row = 3
#
#         invoice_col = sheet.range(f"A{header_row}").expand("right").value.index("Invoice Amount") + 1
#         total_col = sheet.range(f"A{header_row}").expand("right").value.index("Total Amount") + 1
#
#         row = header_row + 1
#         amount = start_amount
#
#         while sheet.range(row, invoice_col).value is not None:
#             sheet.range(row, invoice_col).value = amount
#             sheet.range(row, total_col).value = amount
#             amount += 11
#             row += 1
#
#         # Refresh formulas (for your date column)
#         wb.app.calculate()
#         wb.save()
#         wb.close()
#
#         print(f"Invoice amounts updated safely. Start amount = {start_amount}")
#
#     finally:
#         app.quit()
#
#
#
# def refresh_excel_formulas(excel_path):
#     app = xw.App(visible=False)  # Excel opens in background
#     try:
#         wb = app.books.open(excel_path)
#         wb.app.csalculate()  # force full recalculation
#         wb.save()
#         wb.close()
#     finally:
#         app.quit()
import re
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
        sheet = wb.sheets[0]   # change if needed

        HEADER_ROW = 3  # headers are on row 3

        headers = sheet.range(f"A{HEADER_ROW}").expand("right").value

        invoice_col = headers.index("Invoice Amount") + 1
        total_col = headers.index("Total Amount") + 1

        row = HEADER_ROW + 1
        amount = start_amount

        #  EXACTLY 10 ROWS
        for _ in range(10):
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




# def read_excel_totals(excel_path):
#     """
#     Automatically finds:
#     - Payments Total
#     - Invoice Total
#     from the row above headers (no hardcoding)
#     """
#
#     app = xw.App(visible=False)
#     try:
#         wb = app.books.open(str(excel_path))
#         sheet = wb.sheets[0]   # first sheet
#
#         # Read entire first row
#         first_row = sheet.range("1:1").value
#
#         payments_total = None
#         invoice_total = None
#
#         for idx, cell_value in enumerate(first_row):
#             if cell_value and "Payments Total" in str(cell_value):
#                 payments_total = sheet.range((1, idx + 2)).value
#
#             if cell_value and "Invoice Total" in str(cell_value):
#                 invoice_total = sheet.range((1, idx + 2)).value
#
#         wb.close()
#
#         return float(payments_total), float(invoice_total)
#
#     finally:
#         app.quit()




# def read_excel_totals(excel_path):
#     """
#     Reads Payments Total and Invoice Total from Excel
#     based on label + next cell value (robust & safe).
#     """
#
#     app = xw.App(visible=False)
#     try:
#         wb = app.books.open(str(excel_path))
#         sheet = wb.sheets[0]
#
#         first_row = sheet.range("1:1").value
#
#         payments_total = None
#         invoice_total = None
#
#         for idx, cell_value in enumerate(first_row):
#             if not cell_value:
#                 continue
#
#             cell_text = str(cell_value).strip()
#
#             # Payments Total → next cell
#             if cell_text == "Payments Total":
#                 payments_total = sheet.range((1, idx + 2)).value
#
#             # Invoice Total → next cell
#             if cell_text == "Invoice Total":
#                 invoice_total = sheet.range((1, idx + 2)).value
#
#         wb.close()
#
#         if payments_total is None or invoice_total is None:
#             raise ValueError("Could not find Payments/Invoice totals in Excel")
#
#         return float(payments_total), float(invoice_total)
#
#     finally:
#         app.quit()
# import xlwings as xw
# import re
#
# def read_excel_totals(excel_path):
#     """
#     Reads Payments Total & Invoice Total from row 1
#     Handles:
#     - Label and amount in same cell
#     - Label in one cell, amount in next cell
#     - Merged cells
#     """
#
#     app = xw.App(visible=False, add_book=False)
#     try:
#         wb = app.books.open(str(excel_path))
#         sheet = wb.sheets[0]
#
#         first_row = sheet.range("1:1").value
#
#         payments_total = None
#         invoice_total = None
#
#         for idx, cell_value in enumerate(first_row):
#             if not cell_value:
#                 continue
#
#             text = str(cell_value).strip().lower()
#
#             # -------- PAYMENTS TOTAL --------
#             if "payments total" in text:
#                 # 1️⃣ Try extracting from same cell
#                 match = re.search(r"([\d,]+\.\d{2})", text)
#                 if match:
#                     payments_total = float(match.group(1).replace(",", ""))
#                 else:
#                     # 2️⃣ Else read next cell safely
#                     next_val = sheet.range((1, idx + 2)).value
#                     if next_val:
#                         payments_total = float(str(next_val).replace(",", ""))
#
#             # -------- INVOICE TOTAL --------
#             if "invoice total" in text:
#                 match = re.search(r"([\d,]+\.\d{2})", text)
#                 if match:
#                     invoice_total = float(match.group(1).replace(",", ""))
#                 else:
#                     next_val = sheet.range((1, idx + 2)).value
#                     if next_val:
#                         invoice_total = float(str(next_val).replace(",", ""))
#
#         wb.close()

    #     if payments_total is None or invoice_total is None:
    #         raise ValueError(
    #             f"Could not read totals from Excel. "
    #             f"Payments={payments_total}, Invoice={invoice_total}"
    #         )
    #
    #     return payments_total, invoice_total
    #
    # finally:
    #     app.quit()



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

