from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
load_dotenv(".env")

DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
class db_connection:
    def __init__(self, db_name,logger_name):
        self.usr_name = os.environ.get("USER_NAME")
        self.usr_pass = os.environ.get("USER_PASS")
        self.host = os.environ.get("HOST_IP")        
        self.host = os.environ.get("PORT")

    def get_connection(self):
        conn = create_engine(f"postgresql://{self.usr_name}:{self.usr_pass}@{self.host}:{self.port}")
        return conn
    def insert(self, query):
        pass
    def get(self, query):
        pass
if __name__ == "__main__":
    
