"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
        "participant_names": {}
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
        "participant_names": {}
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"],
        "participant_names": {}
    },
    "Basketball Club": {
        "description": "Practice basketball skills and play friendly games",
        "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": [],
        "participant_names": {}
    },
    "Soccer Club": {
        "description": "Build soccer skills and compete in team matches",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 22,
        "participants": [],
        "participant_names": {}
    },
    "Drama Club": {
        "description": "Act, create scenes, and perform in school productions",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": [],
        "participant_names": {}
    },
    "Art Club": {
        "description": "Explore drawing, painting, and other visual arts",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": [],
        "participant_names": {}
    },
    "Debate Club": {
        "description": "Develop research, reasoning, and public speaking skills",
        "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
        "max_participants": 16,
        "participants": [],
        "participant_names": {}
    },
    "Science Club": {
        "description": "Explore scientific ideas through experiments and projects",
        "schedule": "Fridays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": [],
        "participant_names": {}
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str, name: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    name = name.strip()
    if not name:
        raise HTTPException(status_code=422, detail="Name cannot be empty")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")

    # Add student
    activity["participants"].append(email)
    activity.setdefault("participant_names", {})[email] = name
    return {"message": f"Signed up {name} for {activity_name}"}
