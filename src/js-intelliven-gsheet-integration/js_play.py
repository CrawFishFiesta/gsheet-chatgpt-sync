import gspread
from oauth2client.service_account import ServiceAccountCredentials

def setup_google_client():
    scope = ['https://spreadsheets.google.com/feeds', 
             'https://www.googleapis.com/auth/spreadsheets', 
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('fifth-jigsaw-415008-eda0700e6e1a.json', scope)
    client = gspread.authorize(creds)
    return client

def analyze_www_entries(entries):
    analysis_results = []
    for entry in entries:
        # Assuming 'entry' is a dictionary with the keys 'What', 'Who', and 'Why'
        analysis_result = {
            'Original WHAT': entry.get('What', 'N/A'),
            'Original WHO': entry.get('Who', 'N/A'),
            'Original WHY': entry.get('Why', 'N/A'),
            # Include any analysis logic here and append results
        }
        analysis_results.append(analysis_result)
    return analysis_results

def main():
    client = setup_google_client()
    spreadsheet_name = 'WHAT-WHO-WHY Survey WIP (Responses)'
    try:
        spreadsheet = client.open(spreadsheet_name)
    except gspread.SpreadsheetNotFound:
        print(f"Spreadsheet '{spreadsheet_name}' not found. Check the name and share settings.")
        return

    worksheet = spreadsheet.worksheet('Form Responses 1')  # Adjust if your worksheet has a different title
    entries = worksheet.get_all_records()
    analysis_results = analyze_www_entries(entries)

    headers = ["Original WHAT", "Original WHO", "Original WHY", "Analysis Results"]
    values = [headers] + [[res[key] for key in res] for res in analysis_results]

    output_sheet_title = 'Analysis and Suggestions'
    try:
        output_sheet = spreadsheet.worksheet(output_sheet_title)
    except gspread.WorksheetNotFound:
        output_sheet = spreadsheet.add_worksheet(title=output_sheet_title, rows="100", cols=str(len(headers)))
    
    # Correct approach to use update with named arguments for values and range
    output_sheet.update(values=values, range='A1', value_input_option='RAW')

    print("Analysis and suggestions have been written to the 'Analysis and Suggestions' sheet.")

if __name__ == "__main__":
    main()
