import psycopg2
import pprint as pp

conn = psycopg2.connect(
    "dbname='connect_api' user='hassan' host='localhost' password='yahya' port='5432'"
)
print(conn)
conn.close()