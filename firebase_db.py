import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import os
from dotenv import load_dotenv


class FirebaseDB:
    def __init__(self):
        """Authentication"""
        load_dotenv(verbose=True)
        DATABASE_URL = os.getenv('DATABASE_URL')
        cred = credentials.Certificate('certification.json')
        firebase_admin.initialize_app(cred,{
            'databaseURL' : DATABASE_URL
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


def main():
    f = FirebaseDB()
    f.update('hello', 'world')
    print(f.get())


if __name__ == "__main__":
    main()