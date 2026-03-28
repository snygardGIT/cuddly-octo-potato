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
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Develop teamwork and soccer fundamentals through drills and matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "ava@mergington.edu"]
    },
    "Swimming Club": {
        "description": "Build endurance and technique with guided swim practice",
        "schedule": "Saturdays, 9:00 AM - 10:30 AM",
        "max_participants": 18,
        "participants": ["noah@mergington.edu", "mia@mergington.edu"]
    },
    "Drama Society": {
        "description": "Practice acting, stage presence, and live performance skills",
        "schedule": "Wednesdays, 3:45 PM - 5:15 PM",
        "max_participants": 16,
        "participants": ["charlotte@mergington.edu", "henry@mergington.edu"]
    },
    "Painting Workshop": {
        "description": "Explore watercolor and acrylic techniques through creative projects",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 14,
        "participants": ["amelia@mergington.edu", "lucas@mergington.edu"]
    },
    "Debate Team": {
        "description": "Sharpen research, public speaking, and argumentation skills",
        "schedule": "Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": ["evelyn@mergington.edu", "james@mergington.edu"]
    },
    "Robotics Club": {
        "description": "Design, build, and program robots for collaborative challenges",
        "schedule": "Fridays, 3:30 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["benjamin@mergington.edu", "harper@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]
    normalized_email = email.strip().lower()

    if normalized_email in {participant.strip().lower() for participant in activity["participants"]}:
        raise HTTPException(status_code=409, detail="Student is already signed up for this activity")

    # Add student
    activity["participants"].append(normalized_email)
    return {"message": f"Signed up {normalized_email} for {activity_name}"}


@app.delete("/activities/{activity_name}/participants")
def unregister_from_activity(activity_name: str, email: str):
    """Remove a student from an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]
    normalized_email = email.strip().lower()

    matching_participant = next(
        (participant for participant in activity["participants"] if participant.strip().lower() == normalized_email),
        None,
    )

    if matching_participant is None:
        raise HTTPException(status_code=404, detail="Student is not signed up for this activity")

    activity["participants"].remove(matching_participant)
    return {"message": f"Removed {normalized_email} from {activity_name}"}
