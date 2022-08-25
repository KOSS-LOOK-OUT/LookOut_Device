import string
import uuid
import random
import firebase_db

device_id = str(uuid.uuid4())  # 디바이스 id
certification_no = ""  # 인증번호
for i in range(6):
    certification_no += str(random.randrange(0, 10))
response = False  # 인증 상태값


f = firebase_db.FirebaseDB()

f.update({certification_no: {  # 인증번호 컬렉션
    "id": device_id,
    "state": response}
})

print("id: ", device_id)  # 확인용 코드
print("no: ", certification_no)  # 확인용 코드

input_no = input()
total_dict = f.get()
total_key = sorted(total_dict.keys())

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
