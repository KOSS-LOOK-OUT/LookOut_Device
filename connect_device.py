from genericpath import isfile
import uuid
import random
import time
import datetime
import pickle
import os.path
import firebase_db

fb = firebase_db.FirebaseDB()
file = 'device_id.pickle'

if os.path.isfile(file):
    with open(file, 'rb') as f:
        device_id = str(pickle.load(f))  # 디바이스 id 로드
else:
    with open(file, 'wb') as f:
        pickle.dump(uuid.uuid4(), f)  # 디바이스 id 생성
    with open(file, 'rb') as f:
        device_id = str(pickle.load(f))

certification_no = ""  # 인증번호
response = False  # 인증 상태값

# 인증번호 생성
for i in range(6):
    certification_no += str(random.randrange(0, 10))
# 인증번호 중복 차단
while certification_no in sorted(fb.get().keys()):
    certification_no = ""
    for i in range(6):
        certification_no += str(random.randrange(0, 10))


fb.update({certification_no: {  # 인증번호 컬렉션 생성
    "id": device_id,
    "state": response}
})

current = datetime.datetime.now()  # 인증번호 유효 시간 체크를 위한 현재 시간 저장
goal = current + datetime.timedelta(minutes=3)  # 저장한 현재 시간 + 3분 -> 목표값
# goal = current + datetime.timedelta(seconds=30)  # 테스트용 코드

print("id: ", device_id)  # 테스트용 코드
print("no: ", certification_no)  # 테스트용 코드

# input_no = input()  # 테스트용 코드

# 인증번호 3분 유효 체크
while current != goal:  # 3분 전
    # if input_no == certification_no:  # 테스트용 코드
    if fb.get(response)[certification_no]['state'] == True:  # 인증번호 인증 성공 후
        fb.delete(str(certification_no))  # 인증번호 컬렉션 삭제
        fb.update({device_id: {  # id 컬렉션 생성
            "info": {
                "id": device_id
            },
            "content": {
                "message": "text",
                "datetime": "time"
            }}})
        break
    else:  # 인증번호 인증 성공 전
        goal -= datetime.timedelta(seconds=1)  # 1초씩 시간 삭감
        time.sleep(1)  # 1초 딜레이
else:  # 3분 후
    fb.delete(str(certification_no))  # 인증번호 컬렉션 삭제
