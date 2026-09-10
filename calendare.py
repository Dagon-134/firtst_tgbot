from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import datetime
from googleapiclient.errors import HttpError

from datetime import timedelta

from sql import isTokenExist, refreshToken, addToken

import sys, os, json
import asyncio

# SCOPES = ["https://www.googleapis.com/auth/calendar"]
# creds = None

def addAllInCalendare(task, date_and_time, tg_id):
    SCOPES = ["https://www.googleapis.com/auth/calendar"]
    creds = isTokenExist(tg_id)
    if creds == False:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
    try:
        date_and_time2 = date_and_time + timedelta(hours=1)
        service = build("calendar", "v3", credentials=creds)
        event = {
            "summary": task,
            "colorId": 8,
            "start": {
                "dateTime": date_and_time.isoformat(),
                "timeZone": "Europe/Moscow",
            },
            "end": {
                "dateTime": date_and_time2.isoformat(),
                "timeZone": "Europe/Moscow",
            },
        }
        eventing = service.events().insert(calendarId="primary", body=event).execute()
        # Call the Calendar API
            
    except HttpError as error:
        print(f"An error occurred: {error}")
        
    creds = creds.to_json()
    print(creds)
    creds = json.dumps(creds)
    print(creds)
    addToken(tg_id, creds)