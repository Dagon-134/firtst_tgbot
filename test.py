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


dict = {
    'user':{
        'tasks':[
            {'task':'что', 'time':'10'},
            {'task':'v', 'time':'1'}
            ]
    }
}

for i in dict['user']['tasks']:
    if i['task'] == 'что':
        i['time'] = '2'
        
print(dict)