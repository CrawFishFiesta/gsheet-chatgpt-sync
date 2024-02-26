import ast
import gspread
from gspread import Spreadsheet
from oauth2client.service_account import ServiceAccountCredentials
from openai import OpenAI
import os

def setup_google_client():
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive']
    cred_directory = os.path.join("..", "creds")

    # TODO: (when-time permits) get these creds from an env-var or secret-store instead of a local file
    gcp_creds = ServiceAccountCredentials.from_json_keyfile_name(f"{cred_directory}/fifth-jigsaw-415008-eda0700e6e1a.json", scope)
    client = gspread.authorize(gcp_creds)
    return client

def create_questions_from_gsheet(
        spreadsheet: Spreadsheet,
        sheet_tab="cc-test"):

    records = spreadsheet.worksheet(sheet_tab).get_all_records()
    questions = []
    for record in records:
        fmt_inputs = (ast.literal_eval(record.get("inputs")))
        questions.append(f"{record.get('question')} {' or '.join(fmt_inputs)}")

    return questions


# def ask_chat_gpt():
#     client = OpenAI()


def main():
    client = setup_google_client()
    spreadsheet_name = 'WHAT-WHO-WHY Survey WIP (Responses)'
    try:
        spreadsheet = client.open(spreadsheet_name)
    except gspread.SpreadsheetNotFound:
        print(f"Spreadsheet '{spreadsheet_name}' not found. Check the name and share settings.")
        return

    questions = create_questions_from_gsheet(spreadsheet)
    print(questions)


if __name__ == "__main__":
    main()
