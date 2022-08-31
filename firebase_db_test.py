"""
test.py
파이어베이스에 일정 주기마다 더미데이터를 전송하는 테스트파일입니다.
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
            "message":"조심해",
            "datetime":datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }}},
        {
            "device_"+str(DEVICE_ID):{
            "device_status":DEVICE_STATUS,
            "content":{
            "message":"도둑이야",
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
            sleep(10)

    # listener.close()

    