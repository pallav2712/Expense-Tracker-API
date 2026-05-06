import psycopg2
from psycopg2.extras import RealDictCursor
import time

from .config import settings


try:
    conn = psycopg2.connect(host=settings.database_hostname, database=settings.database_name, 
                            user=settings.database_username, password=settings.database_password,
                            cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Database connection was sucessfull!")

except Exception as error:
    print("Connecting to database failed")
    print("Error: ", error)   
    time.sleep(2)



#expense schema
expense_table = '''
    CREATE TABLE IF NOT EXISTS expense (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    item VARCHAR NOT NULL,
    quantity INT NOT NULL,
    price INT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
'''

cursor.execute(expense_table)
conn.commit()

print("Expense table created successfully!")