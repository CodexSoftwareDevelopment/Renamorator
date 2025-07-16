# excel_utils.py

import pandas as pd

def read_document_names(filepath, sheet_name="Document Scanning Tracker"):
    try:
        df = pd.read_excel(filepath, sheet_name=sheet_name)
        document_names = df["Document Name"].dropna().tolist()
        print("First 10 document names:")
        for name in document_names[:10]:
            print(name)
        return df
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return None
