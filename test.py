from datetime import datetime
lovare = {1: 4}
num =  [1, 9, 7]
num.pop()
#здесь самый необходимый код, если его не запустите, можете просто брать и сливать всё в унитаз

[i for i in range(5)]
now = datetime.now()

print(now.isoformat())


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import datetime
from googleapiclient.errors import HttpError

from datetime import datetime, timedelta

import sys, os

SCOPES = ["https://www.googleapis.com/auth/calendar"]
creds = None
if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)
    with open("token.json", "w") as token:
        token.write(creds.to_json())
# date_and_time2 = date_and_time + timedelta(hours=1)
service = build("calendar", "v3", credentials=creds)
event = {
    "summary": f"some",
    "colorId": 8,
    "start": {
        "dateTime": f"2026-09-20T21:09:00",
        "timeZone": "Europe/Moscow",
    },
    "end": {
        "dateTime": f"2026-09-20T22:09:00",
        "timeZone": "Europe/Moscow",
    },
}
eventing = service.events().insert(calendarId="primary", body=event).execute()