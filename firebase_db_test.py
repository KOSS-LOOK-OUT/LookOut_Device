"""
test.py
to test firebase db with dummy data
"""

from firebase_db import FirebaseDB
from datetime import datetime
from time import sleep

DEVICE_ID = 1  # Write your device id
DEVICE_STATUS = True  # Device power True: ON 

def yield_dummy():
    yield from[
        {   "device_"+str(DEVICE_ID):{
            "device_status":DEVICE_STATUS,
            "content":{
            "message":"불이야",
            "datetime":datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }}},
        {
            "device_"+str(DEVICE_ID):{
            "device_status":DEVICE_STATUS,
            "content":{
            "message":"위험해",
            "datetime":datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }}},
        {
            "device_"+str(DEVICE_ID):{
            "device_status":DEVICE_STATUS,
            "content":{
            "message":"도와주세요",
            "datetime":datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }}},
    ]


if __name__ == "__main__":
    fb = FirebaseDB()
    listener = fb.listen_data(DEVICE_ID)  # listener, 파이어베이스에 데이터가 갱신될때마다 수신함

    # 무한으로 더미 데이터 생성
    while True:
        for data in yield_dummy():
            fb.update(data)
            sleep(2)

    # listener.close()

    