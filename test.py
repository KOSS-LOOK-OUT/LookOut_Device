"""
test.py
to test firebase db with dummy data
"""

from firebase_db import FirebaseDB
from datetime import datetime

DEVICE_ID = 2  # Write your device id
DEVICE_STATUS = True  # Device power True: ON 

def yield_dummy():
    yield from[
        {   "device_"+str(DEVICE_ID):{
            "device_status":DEVICE_STATUS,
            "content":{
            "message":"불이야",
            "datetime":datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }}}
    ]


if __name__ == "__main__":
    fb = FirebaseDB()
    data = yield_dummy()
    fb.update(*data)