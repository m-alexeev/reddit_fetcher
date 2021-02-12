import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv
import os

load_dotenv()


USERNAME = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASS")
DATABASE = os.getenv("DB")
URL = os.getenv("DB_URL")

class Database:
    connection = None
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(host = URL,
                                                user = USERNAME, 
                                                password = PASSWORD,
                                                database = DATABASE)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCES_DENIED_ERROR:
                print("Invalid Credentials")
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)


    def getConnection(self):
        return self.connection

    def clearDB(self):
        tables = ['pennystocks', 'general']
        for table in tables:
            query = "DELETE FROM " + table
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()


    def insert(self, data):
        table = data['subreddit']


        values = data['stocks']
        vals = []
        for val in values:
            vals.append((val['stock'], val['upvotes'], val['like_ratio'], val["num_comments"]) )

        insert = "INSERT INTO "
        if table == "pennystocks":
            insert += table
        else: 
            insert += "general"
        
        query = insert + "( symbol, likes, like_ratio, num_comments) VALUES (%s ,%s, %s ,%s)" 
        
        cursor = self.connection.cursor()
        cursor.executemany(query, vals)
        self.connection.commit()


