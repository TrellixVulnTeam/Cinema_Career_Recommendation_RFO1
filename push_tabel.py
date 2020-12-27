import mysql.connector
import csv
import json
import pandas as pd
import os
"""
using mysql connector we can connect to our mysql server and use queries to fetch data from DB
"""

#when we run server.py locally
def push_csv_to_table(file_name,mysql_conn,cursor):
    df = pd.read_csv(f"./BreakJsonToAllTables/{file_name}" + ".csv")
    rows_n = len(df)
    print (f"starting pushing csv: {file_name}")
    for i, row in df.iterrows():
        sql = f"INSERT INTO {file_name} VALUES (%s,%s)"
        cursor.execute(sql, tuple(row))
        # the connection is not autocommitted by default, so we
        mysql_conn.commit()
        if i % 1000 == 0:
            print(f"commited {i}/{rows_n}")
    print(f"finished {file_name} table")

if __name__ == '__main__':
    mysql = mysql.connector.connect(
        host="localhost",
        user="DbMysql11",
        password="DbMysql11",
        database="DbMysql11",
        port="3305"
    )
    cur = mysql.cursor()
    #push_csv_to_table("Production",mysql,cur)
    push_csv_to_table("Actors", mysql, cur)
    push_csv_to_table("Director", mysql, cur)
    push_csv_to_table("Film", mysql, cur)
    push_csv_to_table("Film_Director", mysql, cur)
    push_csv_to_table("Film_Genre", mysql, cur)
    push_csv_to_table("Film_Production", mysql, cur)
    push_csv_to_table("Film_writer", mysql, cur)
    push_csv_to_table("Genre", mysql, cur)
    push_csv_to_table("Writer", mysql, cur)
    print("finished pushing all tables")