from pymongo import MongoClient
from dotenv import load_dotenv
import os
def get_db(db_name=None):
    if not db_name:
        load_dotenv(os.path.join(os.path.dirname(__file__), '.env'), verbose=True)
        db_cred = os.environ.get("ENDPOINT")
        client = MongoClient(db_cred)
        print(f"loaded db -- {client}")
        return client
    else:
        load_dotenv(os.path.join(os.path.dirname(
            __file__), '.env'), verbose=True)
        db_cred = os.environ.get("ENDPOINT")
        client = MongoClient(db_cred)
        db = client[db_name]
        return db
if __name__ == "__main__":
    get_db()