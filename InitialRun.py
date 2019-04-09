from __future__ import print_function
import pickle
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Since we have to only read the files.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
def main():

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
            # Print Message incase Token already exists as a file
            print("Your initial run is already completed, you can run JsonExport.py now")
            quit()
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server()
            except Exception as e:
                print("credentials.json is missing, please download the file from Google Cloud")
                quit()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
        # Print Message after token is saved in a file.
        print("Your initial run is completed, you can run JsonExport.py now")
        quit()

if __name__ == '__main__':
    main()
