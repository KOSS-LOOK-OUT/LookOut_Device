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
        #cred = credentials.Certificate('certification.json')
        cred = credentials.Certificate(
            'test.json')
        firebase_admin.initialize_app(cred, {
            # 'databaseURL' : DATABASE_URL
            'databaseURL': 'https://test-51406-default-rtdb.firebaseio.com/'
        })

    # create/update
    def update(self, data: dict):
        ref = db.reference()
        ref.update(data)

    # get
    def get(self, v=None):
        if v:
            ref = db.reference(v)
        else:
            ref = db.reference()
        return ref.get()

    # delete
    def delete(self, v):
        ref = db.reference(v)
        ref.delete()

    def listener(self, event):
        print(event.event_type)
        print(event.path)
        print(event.data)

    def listen_data(self, device_id):
        return db.reference('device_'+str(device_id)+'/').listen(self.listener)


def main():
    f = FirebaseDB()
    # f.delete('726034')

    # f.update({'hello': 'world'})
    # print(f.get())


if __name__ == "__main__":
    main()
