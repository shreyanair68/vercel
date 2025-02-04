from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import json

# Load student data from JSON file
with open("q-vercel-python.json", "r") as file:
    data = json.load(file)

df = pd.DataFrame(data)  # Convert JSON data to Pandas DataFrame

# Initialize FastAPI app
app = FastAPI()

# Enable CORS (allow all origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api")
async def get_marks(name: list[str] = Query(...)):
    """Fetch marks for the given list of student names."""
    marks = []
    for n in name:
        matched = df.loc[df['name'] == n, 'marks'].values
        marks.append(int(matched[0]) if len(matched) > 0 else None)  # Convert to int explicitly

    return {"marks": marks}
