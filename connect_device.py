import string
import uuid
import random
import firebase_db

f = firebase_db.FirebaseDB()

total_dict = f.get()  # DB 전체 데이터
total_key = sorted(total_dict.keys())  # DB 정렬된 키

device_id = str(uuid.uuid4())  # 디바이스 id
certification_no = ""  # 인증번호
response = False  # 인증 상태값

# 인증번호 생성
for i in range(6):
    certification_no += str(random.randrange(0, 10))
# 인증번호 중복 차단
while certification_no in total_key:
    certification_no = ""
    for i in range(6):
        certification_no += str(random.randrange(0, 10))

f.update({certification_no: {  # 인증번호 컬렉션
    "id": device_id,
    "state": response}
})

print("id: ", device_id)  # 테스트용 코드
print("no: ", certification_no)  # 테스트용 코드

input_no = input()  # 테스트용 코드

if input_no == certification_no:
    # if response == True:
    f.delete(str(certification_no))
    device_name = "device_" + str(int(total_key[-1][-1]) + 1)
    f.update({device_name: {  # id 컬렉션
        "info": {
            "id": device_id
        },
        "content": {
            "message": "text",
            "datetime": "time"
        }}})
