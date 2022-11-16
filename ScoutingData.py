import matplotlib
import matplotlib.pyplot as plt


# plt.show()

plt.savefig("books_read")



import pandas as pd
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow,Flow
from google.auth.transport.requests import Request
import os
import pickle

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# here enter the id of your google sheet
SAMPLE_SPREADSHEET_ID_input = '1eu_a1sr2UnHWufIdA9ELHDFShpXIsKeGs56YM_KQMi8'
TEAM_NUMBERS = 'C2:C200'
DID_THEY_TAXI = "E2:E200"

def main():
    global values_input, service
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES) # here enter the name of your downloaded JSON file
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result_input = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID_input,
                                range=TEAM_NUMBERS).execute()
    team_nums = result_input.get('values', [])

    result_input = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID_input,
                                range=DID_THEY_TAXI).execute()
    did_they_taxi = result_input.get('values', [])

    plt.plot(team_nums, did_they_taxi)

    plt.xlabel("Team Number")
    plt.ylabel("Did they taxi")

    plt.save("data")

    if not values_input and not values_expansion:
        print('No data found.')

main()

df=pd.DataFrame(values_input[1:], columns=values_input[0])