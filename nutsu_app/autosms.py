import os
import sys
import django
from decouple import config

project_root = config("PROJECT_ROOT")
sys.path.append(project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prescribemate.settings')
django.setup()

import requests
from cleanphonenumber import normalize_bd_phone_number

url = "https://api.sms.net.bd/sendsms"

def send_autosms(to,msg):
    try:
        normalized = normalize_bd_phone_number(to)
        payload = {'api_key': config('SMS_API_KEY'),
            'msg': msg,
            'to': normalized,
            }

        response = requests.request("POST", url, data=payload)

        return True if response.status_code==200 else False
    
    except ValueError as e:
        return False