import pandas as pd
from pathlib import Path
from utilities.customLogger import LogMaker

logger = LogMaker.log_gen()


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


from openpyxl import load_workbook
import time


def update_amounts(excel_path):
    logger.info("Updating Excel Amounts")
    start_amount = get_next_start_amount()

    wb = load_workbook(excel_path)
    sheet = wb['Payment_Entry']  # wb.active

    HEADER_ROW = 3
    DATA_START_ROW = HEADER_ROW + 1

    # Read headers from row 3
    headers = [
        cell.value for cell in sheet[HEADER_ROW]
        if cell.value is not None
    ]

    invoice_col = headers.index("Invoice Amount") + 1
    total_col = headers.index("Total Amount") + 1

    row = DATA_START_ROW
    amount = start_amount

    # Find number of rows with data (like expand("table"))
    logger.info(f"Updating Excel Amounts for {start_amount} Amount")
    while sheet.cell(row=row, column=1).value is not None:
        sheet.cell(row=row, column=invoice_col).value = round(amount, 2)
        sheet.cell(row=row, column=total_col).value = round(amount, 2)

        amount += 11
        row += 1
    wb.calculation.fullCalcOnLoad = True
    logger.info("******* Formulas Re Calculated and excel sheet refreshed *******")

    wb.save(excel_path)
    logger.info(f"Updated Excel file saved Successfully")
    wb.close()

    time.sleep(1)

    print(
        f"Invoice amounts updated successfully "
        f"(start={start_amount}, end={amount - 11})"
    )


from openpyxl import load_workbook


def read_excel_totals(excel_path):
    logger.info(f"Reading Excel Totals for {excel_path}")

    df = pd.read_excel(excel_path, sheet_name="Payment_Entry")

    payments_total = df.iloc[2:, 8].sum()  # Column I (skip header rows)
    invoice_total = df.iloc[2:, 25].sum()  # Column Z

    if payments_total is None or invoice_total is None:
        raise ValueError(f"Excel totals missing: Payments={payments_total}, Invoice={invoice_total}")

    logger.info(f"Payments Total: {payments_total}")
    logger.info(f"Invoice Total: {invoice_total}")

    return float(payments_total), float(invoice_total)
