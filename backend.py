from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from supabase import create_client, Client
import os

app = FastAPI()

# Supabase project URL and API key (paste yours here or use env variables)
SUPABASE_URL = "https://fkfspbjyxgwpvximzsdj.supabase.co"  # Replace with your actual URL
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZrZnNwYmp5eGd3cHZ4aW16c2RqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDY4Nzg2NjAsImV4cCI6MjA2MjQ1NDY2MH0.ZUdVFuKxzsf4l0rvisCFvdSnKuAofnaUJzReNId5zIg"         # Replace with your actual key

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class User(BaseModel):
    name: str
    passcode: str

# Store data in Supabase
@app.post("/store")
def store_data(user: User):
    response = supabase.table("users").insert({"name": user.name, "passcode": user.passcode}).execute()
    if response.status_code == 201:
        return {"message": "Data stored!"}
    else:
        return {"error": response.data}

# Retrieve data from Supabase
@app.get("/retrieve")
def retrieve_data():
    response = supabase.table("users").select("*").execute()
    return {"data": response.data}

