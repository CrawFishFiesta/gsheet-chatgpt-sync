import ast
import gspread
from gspread import Spreadsheet
from oauth2client.service_account import ServiceAccountCredentials
from openai import OpenAI
import os

def setup_google_client():
    """
    Method creates a google-client for interacting with google sheets
    """
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
    """
    Extract questions from gsheet and format them properly for chat-gpt

    :param spreadsheet: google-sheet name
    :param sheet_tab: gsheet tab name
    :return: A list of questions
    """

    records = spreadsheet.worksheet(sheet_tab).get_all_records()
    questions = []
    for record in records:
        fmt_inputs = (ast.literal_eval(record.get("inputs")))
        questions.append(f"{record.get('question')} {' or '.join(fmt_inputs)}")

    return questions


def ask_chat_gpt(question: str) -> str:
    """
    Ask chat gpt a question

    :param question: a question to ask chat gpt
    :return: the chat-gpt answer as a string
    """
    client = OpenAI(
        # check the README.md for instrs on setting the api-key as an env-var
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": question,
            }
        ],
        model="gpt-3.5-turbo",
    )

    return response.choices[0].message.content


def output_to_gsheet(spreadsheet: Spreadsheet, answers: list[str] = None, sheet_tab="cc-test"):
    sh = spreadsheet.worksheet(sheet_tab)
    sh.batch_clear(ranges=['C2:C10'])

    for i in range(len(answers)):
        # worksheet.update_cell(1, 2, 'Bingo!')
        sh.update_cell(i+2, 3, value = answers[i])

def main():
    client = setup_google_client()

    # parametrize the sheet name
    spreadsheet_name = 'WHAT-WHO-WHY Survey WIP (Responses)'
    try:
        spreadsheet = client.open(spreadsheet_name)
    except gspread.SpreadsheetNotFound:
        print(f"Spreadsheet '{spreadsheet_name}' not found. Check the name and share settings.")
        return

    fmtd_questions = create_questions_from_gsheet(spreadsheet)
    answers = []
    for q in fmtd_questions:
        answers.append(ask_chat_gpt(q))

    output_to_gsheet(
        spreadsheet=spreadsheet,
        answers=answers,
        sheet_tab="cc-test")

if __name__ == "__main__":
    main()
