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

def addAllInCalendare(task: str, date_and_time: datetime, tg_id: int):
    SCOPES = ["https://www.googleapis.com/auth/calendar"]
    creds = None
    token = isTokenExist(tg_id)
    token = json.loads(token)
    if token is not None:
            
        creds = Credentials.from_authorized_user_info(token, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            
            refreshToken(tg_id, creds.to_json())
        
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
                    )
            creds = flow.run_local_server(port=0)
            token = creds.to_json()
            addToken(tg_id, token)
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
        