import string
import uuid
import random
import firebase_db

device_uuid = uuid.uuid4()  # 디바이스 id
device_id = str(device_uuid)
certification_no = ""  # 인증 번호
for i in range(6):
    certification_no += str(random.randrange(0, 10))
response = False  # 인증 상태값

dict = {device_id: response}

f = firebase_db.FirebaseDB()
f.update({certification_no: dict})
print("id: ", device_id)
print("no: ", certification_no)

input_no = input()

if input_no == certification_no:
    dict[device_id] = True
    f.update({certification_no: dict})
    f.delete(str(certification_no))
    info = {"id": device_id}
    f.update({device_id: info})

# 형태 => {인증번호: {id: 상태값}}
