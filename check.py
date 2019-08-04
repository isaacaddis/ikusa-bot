import mysql.connector
conn = mysql.connector.connect(
       host = "us-cdbr-iron-east-02.cleardb.net",
       user = "b90bd7aafae0d8",
       password = "bb45d6ec",
       #database = "heroku_1cdd89260bd4c7d"
       database = "heroku_1492cb9b2e7e903"
        )
cursor = conn.cursor()
cursor.execute("SELECT * FROM calendar")
#cursor.execute("DESCRIBE calendar")
for x in cursor:
    print(x)
#cursor.execute(sql, multi=True)
#conn.commit()
