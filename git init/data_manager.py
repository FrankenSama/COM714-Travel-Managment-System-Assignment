# FILE: data_manager.py (check these imports)

import json
import os
from models import User, TripCoordinator, TripManager, Administrator, Traveller, Trip, TripLeg, Invoice, Payment
from typing import List, Dict, Any

DATA_DIR = "data"
USER_FILE = os.path.join(DATA_DIR, "users.json")
TRAVELLER_FILE = os.path.join(DATA_DIR, "travellers.json")
TRIP_FILE = os.path.join(DATA_DIR, "trips.json")
INVOICE_FILE = os.path.join(DATA_DIR, "invoices.json")

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

def _load_json(filepath: str) -> List[Dict[str, Any]]:
    """Helper function to load data from a JSON file."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def _save_json(filepath: str, data: List[Dict[str, Any]]) -> None:
    """Helper function to save data to a JSON file."""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4, default=str)  # `default=str` handles datetime objects

def save_user(user: User) -> None:
    """Saves a single user to the JSON file."""
    users = _load_json(USER_FILE)
    
    # Check if user exists, if so, update. Else, append.
    user_found = False
    for i, u in enumerate(users):
        if u['user_id'] == user.user_id:
            users[i] = user.__dict__
            user_found = True
            break
    
    if not user_found:
        users.append(user.__dict__)
    
    _save_json(USER_FILE, users)

def load_users() -> List[User]:
    """Loads all users from the JSON file and returns them as User objects."""
    users_data = _load_json(USER_FILE)
    users = []
    
    for user_data in users_data:
        role = user_data['role']
        if role == "Trip Coordinator":
            user = TripCoordinator(**user_data)
        elif role == "Trip Manager":
            user = TripManager(**user_data)
        elif role == "Administrator":
            user = Administrator(**user_data)
        else:
            continue  # Skip unknown roles
        users.append(user)
    
    return users

def save_traveller(traveller: Traveller) -> None:
    """Saves a single traveller to the JSON file."""
    travellers = _load_json(TRAVELLER_FILE)
    
    traveller_found = False
    for i, t in enumerate(travellers):
        if t['traveller_id'] == traveller.traveller_id:
            travellers[i] = traveller.__dict__
            traveller_found = True
            break
    
    if not traveller_found:
        travellers.append(traveller.__dict__)
    
    _save_json(TRAVELLER_FILE, travellers)

def load_travellers() -> List[Traveller]:
    """Loads all travellers from the JSON file."""
    travellers_data = _load_json(TRAVELLER_FILE)
    return [Traveller(**data) for data in travellers_data]

# We will add similar save/load functions for Trip, Invoice, etc. as we need them.
# For now, let's focus on getting Users and Authentication working.

print("Data Manager module loaded successfully.")