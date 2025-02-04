from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import json

# Load student data
with open("q-vercel-python.json", "r") as file:
    data = json.load(file)

df = pd.DataFrame(data)  # Convert JSON data to DataFrame

# Initialize FastAPI app
app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api")
async def get_marks(name: list[str] = Query(None)):  # Make 'name' optional
    """Fetch marks for the given list of student names."""
    if not name:
        return {"error": "Please provide at least one name"}

    marks = []
    for n in name:
        matched = df.loc[df['name'] == n, 'marks'].values
        marks.append(int(matched[0]) if len(matched) > 0 else None)  # Convert to int

    return {"marks": marks}
