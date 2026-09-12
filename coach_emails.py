import pandas as pd

# Your Google Sheet ID
SHEET_ID = "1bA1W6lVIt2ifJJjGRYYLK27faRPqKNLSLOLyVPr4zPg"

# Google Sheets CSV export URL
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"


def get_coach_emails():
    try:
        df = pd.read_csv(SHEET_URL)

        # Make sure the column is named "email"
        if "email" not in df.columns:
            return []

        # Clean up emails
        emails = (
            df["email"]
            .dropna()
            .astype(str)
            .str.strip()
            .str.lower()
            .tolist()
        )

        return emails

    except Exception:
        return []
