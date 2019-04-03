import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def returnThisMonth():
    return datetime.datetime.utcnow().month


def credentialsHendler():

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def returnWorkingHoursInMonth(month=datetime.datetime.utcnow().month, year=datetime.datetime.utcnow().year):
    """workinHoursForEachMonthOfYear array of tuple of 0-year, 1-12 working hours in month ,13 working hours in year """
    workinHoursForEachMonthOfYear=[
        (2019,176,160,168,168,168,152,184,168,168,184,152,160,2008),
        (2020,168,160,176,168,160,168,184,160,176,176,160,168,2024),
    ]
    return workinHoursForEachMonthOfYear[year-workinHoursForEachMonthOfYear[0][0]][month]

def setBoundryDatesForMonth(month):
    now = datetime.datetime.utcnow()
    startOfMonth = datetime.datetime(now.year,month,1,0,0,0)
    print(startOfMonth)
def main():

    credentials = credentialsHendler()

    service = build('calendar', 'v3', credentials=credentials)


    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='nt597vd9gmakr5abrg1cr2pncc@group.calendar.google.com',
                                          timeMin='2019-03-01T20:09:47.791863Z',
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


if __name__ == '__main__':

    setBoundryDatesForMonth(3)
    main()
