import psycopg2
import pandas as pd

def connection(database_name)
    conn = psycopg2.connect(
        host="localhost",
        database=database_name,
        user="user",
        password="password"
    )