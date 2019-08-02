import mysql.connector
sql = """
CREATE TABLE Calendar (
  d DATE,
  PRIMARY KEY (d),
  event VARCHAR(255),
  t TIME,
  zone VARCHAR(255),
  role VARCHAR(255)
)
"""
conn = mysql.connector.connect(
       host = "us-cdbr-iron-east-02.cleardb.net",
       user = "b90bd7aafae0d8",
       password = "bb45d6ec",
       #database = "heroku_1cdd89260bd4c7d"
       database = "heroku_1492cb9b2e7e903"
        )
cursor = conn.cursor()
cursor.execute(sql)
#cursor.execute(sql, multi=True)
#conn.commit()
