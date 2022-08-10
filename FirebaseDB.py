import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import os
from dotenv import load_dotenv


class FirebaseDB:
    def __init__(self):
        load_dotenv(verbose=True)
        DATABASE_URL = os.getenv('DATABASE_URL')
        cred = credentials.Certificate('certification.json')
        firebase_admin.initialize_app(cred,{
            'databaseURL' : 'https://lookout-c073f-default-rtdb.firebaseio.com/'
        })

    # create/update
    def update(self, key, value):
        ref = db.reference()
        ref.update({key:value})

    # get
    def get(self, v=None):
        if v: ref = db.reference(v)
        else: ref = db.reference()
        return ref.get()


f = FirebaseDB()
f.update('ㅇㅇ', 'ㄴㄴㄴ')
print(f.get('테스트'))