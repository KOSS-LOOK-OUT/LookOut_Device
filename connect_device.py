import string
import uuid
import random
import firebase_db

device_id = str(uuid.uuid4())  # 디바이스 id
certification_no = ""  # 인증 번호
for i in range(6):
    certification_no += str(random.randrange(0, 10))
response = False  # 인증 상태값

f = firebase_db.FirebaseDB()

f.update({certification_no: {
    "id": device_id,
    "state": response}
})

print("id: ", device_id)
print("no: ", certification_no)

input_no = input()

if input_no == certification_no:
    f.delete(str(certification_no))
    f.update({device_id: {
        "info": {
            "id": device_id
        },
        "content": {
            "message": "text",
            "datetime": "time"
        }}})
