from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import sqlite3

app = FastAPI()

# Connect to database (creates file if not exists)
conn = sqlite3.connect("data.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, passcode TEXT)")
conn.commit()

class User(BaseModel):
    name: str
    passcode: str

# Store data
@app.post("/store")
def store_data(user: User):
    cursor.execute("INSERT INTO users (name, passcode) VALUES (?, ?)", (user.name, user.passcode))
    conn.commit()
    return {"message": "Data stored!"}

# Retrieve data
@app.get("/retrieve")
def retrieve_data():
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()
    return {"data": data}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)