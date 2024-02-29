import gspread
from oauth2client.service_account import ServiceAccountCredentials
import openai
import os

# Function to set up the Google client
def setup_google_client():
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive.file',
        'https://www.googleapis.com/auth/drive'
    ]

    cred_directory = os.path.join("..", "creds")
    # TODO: (when-time permits) get these creds from an env-var or secret-store instead of a local file
    gcp_creds = ServiceAccountCredentials.from_json_keyfile_name(f"{cred_directory}/fifth-jigsaw-415008-eda0700e6e1a.json", scope)
    client = gspread.authorize(gcp_creds)
    return client

# Function to extract WHAT, WHO, WHY entries
def create_questions_from_gsheet(spreadsheet: gspread.Spreadsheet, sheet_tab="WWW Indiv Inputs"):
    worksheet = spreadsheet.worksheet(sheet_tab)
    records = worksheet.get_all_records()
    questions = [{"what": record.get("WHAT"), "who": record.get("WHO"), "why": record.get("WHY")} for record in records]
    return questions

# Function to analyze and suggest improvements using OpenAI's GPT-4

def ask_chat_gpt(what: str, who: str, why: str) -> str:
    openai.api_key = os.getenv("OPENAI_API_KEY")

    prompt = f"Please provide feedback and suggestions for improvement on the following WWW entries:\n\n" \
             f"WHAT: {what}\nWHO: {who}\nWHY: {why}\n\n"

    response = openai.Completion.create(
        model="gpt-3.5-turbo",  # Adjust the model as necessary
        prompt=prompt,
        max_tokens=1024,  # You may adjust this value
        temperature=0.7,  # Adjust for creativity. Lower is more deterministic.
        stop=None  # Specify stopping criteria if needed
    )

    # Make sure to access the 'text' attribute correctly based on the API's response structure
    return response['choices'][0]['text'].strip()
# Function to output processed answers back to the specified Google Sheets document
def output_to_gsheet(spreadsheet: gspread.Spreadsheet, answers: list[str], sheet_tab="Output Indiv"):
    try:
        worksheet = spreadsheet.worksheet(sheet_tab)
    except gspread.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(title=sheet_tab, rows="100", cols="2")

    cells_range = f'A1:A{len(answers)}'
    worksheet.update(cells_range, [[answer] for answer in answers], value_input_option='USER_ENTERED')

# Main execution function
def main():
    openai.api_key = os.getenv("OPENAI_API_KEY")

    client = setup_google_client()
    spreadsheet_name = 'WHAT-WHO-WHY Survey WIP (Responses)'
    input_sheet_tab = 'WWW Indiv Inputs'
    output_sheet_tab = 'Output Indiv'

    spreadsheet = client.open(spreadsheet_name)
    questions = create_questions_from_gsheet(spreadsheet, sheet_tab=input_sheet_tab)
    answers = [ask_chat_gpt(q['what'], q['who'], q['why']) for q in questions]
    output_to_gsheet(spreadsheet, answers, sheet_tab=output_sheet_tab)

if __name__ == "__main__":
    main()