import sqlite3
import pandas as pd

conn = sqlite3.connect("output/merlin.db")

df = pd.read_sql("SELECT * FROM merlin_sales", conn)
print(df.head())

conn.close()