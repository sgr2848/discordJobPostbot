
from dotenv import load_dotenv
import pytz
import os
import pandas as pd
import datetime
import psycopg2
from psycopg2.extras import execute_values

load_dotenv(".env")
# DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")


class db_conn:
    def __init__(self):
        self.usr_name = os.environ.get("USER_NAME")
        self.usr_pass = os.environ.get("USER_PASS")
        self.host = os.environ.get("HOST_IP")
        self.port = os.environ.get("HOST_PORT")
        self.engine = self.get_connection()
        print("started __init__ for db_conn")

    def get_connection(self):
        try:
            conn = psycopg2.connect(
                f"dbname='career_bot' user='{self.usr_name}' password='{self.usr_pass}' host='{self.host}' port='{self.port}'")
            print("connected to db")
            return conn
        except Exception as e:
            print("Couldn't access the db")

    def insert(self, payload):
        '''
            payload should be a list of dictionary of jobs
        '''
        print("started insertion")
        columns = payload[0].keys()
        print(columns)
        query = 'INSERT INTO cs_bot.jobs ({}) VALUES %s'.format(
            ",".join(columns))
        print(query)
        values = [[value for value in item.values()] for item in payload]
        cursor = self.engine.cursor()
        # cursor.execute("Select * FROM cs_bot.Jobs LIMIT 0")
        # colnames = [desc[0] for desc in cursor.description]
        # print(colnames)
        execute_values(cursor, query, values)
        self.engine.commit()
        cursor.close()


if __name__ == "__main__":
    db = db_conn()
