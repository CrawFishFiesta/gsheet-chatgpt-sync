js-intelliven-gsheet-integration

## Description
A repo to manually trigger chatgpt results using a google-sheet input.

## Dependencies
- Python 3.10.3
  
## Configuring credentails
- Setup google creds:
  <br> Move the file `fifth-jigsaw-415008-eda0700e6e1a.json` 
  <br> to the `./src/creds` folder in this repo
  <br>
- Setup environment variables:
    - On a Mac/Linux Machine:
        ```bash
        # add this to your bash profile
        OPENAI_API_KEY='<your-api-key-here>'
        ```
    - On a Windows Machine:
        ```
        setx OPENAI_API_KEY "<your-api-key-here>"
        ```

## References
- [Chatgpt API docs](https://platform.openai.com/docs/api-reference)
- [Google Sheets API docs](https://developers.google.com/sheets/api/guides/concepts)