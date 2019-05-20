from __future__ import print_function
import datetime
from os import path
import pickle
from googleapiclient.discovery import build

print("Hello, World!")


def getCalendarClient(token_pickle_path=None):
    if token_pickle_path is None:
        token_pickle_path = 'token.pickle'
    if path.exists(token_pickle_path):
        with open(token_pickle_path, 'rb') as token:
            creds = pickle.load(token)
    service = build('calendar', 'v3', credentials=creds)
    return service


def getNextEvents(calendarClient, calId, maxResultCount=5):
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTCtime
    print(f'Getting the upcoming {maxResultCount} events')
    events_result = calendarClient.events().list(calendarId=calId,
                                                 timeMin=now,
                                                 maxResults=maxResultCount,
                                                 singleEvents=True,
                                                 orderBy='startTime'
                                                 ).execute()
    events = events_result.get('items', [])
    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event)
        print("\n")


if __name__ == '__main__':
    cc = getCalendarClient('google/token.pickle')
    print("\n")
    getNextEvents(cc, 'tipan.verella@gmail.com', 1)
    print("\n\n")
    # getNextEvents(cc, 'sameena.mulla@gmail.com')
