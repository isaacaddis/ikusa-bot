import mysql.connector

sql = """
    ALTER TABLE calendar ADD COLUMN event VARCHAR(255) AFTER d
"""

'''
sql = """
INSERT INTO calendar (d, event, t, zone, role) VALUES ('2019-08-04', 'Group game', '07:30:15', 'PDT-0700', 'Splatoon2')
"""
'''
'''
sql = """
 CREATE TABLE calendar(
 id int AUTO_INCREMENT,
 PRIMARY KEY (id),
 d DATE,
 t TIME,
 zone VARCHAR(255),
 role VARCHAR(255))
"""
'''
conn = mysql.connector.connect(
       host = "us-cdbr-iron-east-02.cleardb.net",
       user = "b90bd7aafae0d8",
       password = "bb45d6ec",
       #database = "heroku_1cdd89260bd4c7d"
       database = "heroku_1492cb9b2e7e903"
        )
cursor = conn.cursor()
cursor.execute(sql)
conn.commit()
print(cursor.rowcount, "record inserted.")
#cursor.execute(sql, multi=True)
#conn.commit()
