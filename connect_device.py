from genericpath import isfile
import uuid
import random
import time
import datetime
import pickle
import os.path
import firebase_db


fb = firebase_db.FirebaseDB()
# 디바이스 uuid를 저장할 파일
file = 'device_id.pickle'

if os.path.isfile(file):
    # 파일에서 디바이스 uuid 로드
    with open(file, 'rb') as f:
        device_id = str(pickle.load(f))
else:
    # 파일에 디바이스 uuid 생성
    with open(file, 'wb') as f:
        pickle.dump(uuid.uuid4(), f)
    # 파일에서 디바이스 uuid 로드
    with open(file, 'rb') as f:
        device_id = str(pickle.load(f))

# 인증번호
certification_no = ""
# 인증번호 인증 성공 여부
response = False

# 인증번호 랜덤 생성
for i in range(6):
    certification_no += str(random.randrange(0, 10))
# 생성된 인증번호가 DB에 있으면 인증번호를 다시 생성
while certification_no in sorted(fb.get().keys()):
    certification_no = ""
    for i in range(6):
        certification_no += str(random.randrange(0, 10))

# DB에 인증번호 컬렉션 생성
fb.update({certification_no: {
    "id": device_id,
    "state": response}
})

# 인증번호 유효 시간 체크를 위한 현재 시간 저장
current = datetime.datetime.now()
# 저장한 현재 시간에서 3분을 더한 시간
goal = current + datetime.timedelta(minutes=3)

print("id: ", device_id)  # 테스트용 코드
print("no: ", certification_no)  # 테스트용 코드

# 인증번호 3분 유효 체크
while current != goal:
    # 인증시간이 3분 이전
    # 인증번호 인증이 성공했는지 DB 값 가져와 확인
    if fb.get(response)[certification_no]['state'] == True:
        # 인증번호 인증 성공 후
        # 인증번호 컬렉션 삭제
        fb.delete(str(certification_no))
        # DB에 id 컬렉션 생성
        fb.update({device_id: {
            "info": {
                "id": device_id
            },
            "content": {
                "message": "text",
                "datetime": "time"
            }}})
        break
    else:
        # 인증번호 인증 성공 전
        # 1초씩 시간 삭감
        goal -= datetime.timedelta(seconds=1)
        time.sleep(1)
else:
    # 인증시간이 3분 이후
    # 인증번호 컬렉션 삭제
    fb.delete(str(certification_no))
