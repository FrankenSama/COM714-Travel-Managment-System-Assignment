# FILE: data_manager.py
# Handles all data persistence using JSON files.

import json
import os
from datetime import datetime
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
        json.dump(data, f, indent=4)

def save_user(user) -> None:
    """Saves a single user to the JSON file."""
    users = _load_json(USER_FILE)
    
    # Convert user object to dictionary
    user_dict = {
        'user_id': user.user_id,
        'username': user.username,
        'password': user.password,
        'name': user.name,
        'role': user.role.value,  # Store the enum value as string
        '_type': type(user).__name__  # Store the class name for reconstruction
    }
    
    # Check if user exists, if so, update. Else, append.
    user_found = False
    for i, u in enumerate(users):
        if u['user_id'] == user.user_id:
            users[i] = user_dict
            user_found = True
            break
    
    if not user_found:
        users.append(user_dict)
    
    _save_json(USER_FILE, users)

def load_users() -> List:
    """Loads all users from the JSON file and returns them as User objects."""
    from models import User, TripCoordinator, TripManager, Administrator
    
    users_data = _load_json(USER_FILE)
    users = []
    
    for user_data in users_data:
        try:
            role = user_data['role']
            user_type = user_data.get('_type', 'User')
            
            # Reconstruct the user object based on stored type
            if user_type == 'Administrator':
                user = Administrator(
                    user_id=user_data['user_id'],
                    username=user_data['username'],
                    password=user_data['password'],
                    name=user_data['name']
                )
            elif user_type == 'TripManager':
                user = TripManager(
                    user_id=user_data['user_id'],
                    username=user_data['username'],
                    password=user_data['password'],
                    name=user_data['name']
                )
            elif user_type == 'TripCoordinator':
                user = TripCoordinator(
                    user_id=user_data['user_id'],
                    username=user_data['username'],
                    password=user_data['password'],
                    name=user_data['name']
                )
            else:
                # Fallback to base User class
                user = User(
                    user_id=user_data['user_id'],
                    username=user_data['username'],
                    password=user_data['password'],
                    name=user_data['name'],
                    role=role
                )
            users.append(user)
        except Exception as e:
            print(f"Error loading user {user_data.get('username', 'unknown')}: {e}")
            continue
    
    return users

def save_traveller(traveller) -> None:
    """Saves a single traveller to the JSON file."""
    travellers = _load_json(TRAVELLER_FILE)
    
    traveller_dict = {
        'traveller_id': traveller.traveller_id,
        'name': traveller.name,
        'address': traveller.address,
        'date_of_birth': traveller.date_of_birth.isoformat() if hasattr(traveller.date_of_birth, 'isoformat') else str(traveller.date_of_birth),
        'emergency_contact': traveller.emergency_contact,
        'government_id': traveller.government_id
    }
    
    traveller_found = False
    for i, t in enumerate(travellers):
        if t['traveller_id'] == traveller.traveller_id:
            travellers[i] = traveller_dict
            traveller_found = True
            break
    
    if not traveller_found:
        travellers.append(traveller_dict)
    
    _save_json(TRAVELLER_FILE, travellers)

def load_travellers() -> List:
    """Loads all travellers from the JSON file."""
    from models import Traveller
    
    travellers_data = _load_json(TRAVELLER_FILE)
    travellers = []
    
    for data in travellers_data:
        try:
            # Convert string date back to datetime object
            if 'date_of_birth' in data:
                data['date_of_birth'] = datetime.fromisoformat(data['date_of_birth'])
            
            traveller = Traveller(**data)
            travellers.append(traveller)
        except Exception as e:
            print(f"Error loading traveller: {e}")
            continue
    
    return travellers

# Add these trip management functions to your data_manager.py

def save_trip(trip) -> None:
    """Saves a single trip to the JSON file."""
    trips = _load_json(TRIP_FILE)
    
    trip_dict = {
        'trip_id': trip.trip_id,
        'name': trip.name,
        'start_date': trip.start_date.isoformat() if hasattr(trip.start_date, 'isoformat') else str(trip.start_date),
        'duration_days': trip.duration_days,
        'coordinator_id': trip.coordinator.user_id if trip.coordinator else None,
        'traveller_ids': [t.traveller_id for t in trip.travellers],
        'trip_leg_ids': [leg.leg_id for leg in trip.trip_legs],
        'is_active': trip.is_active
    }
    
    trip_found = False
    for i, t in enumerate(trips):
        if t['trip_id'] == trip.trip_id:
            trips[i] = trip_dict
            trip_found = True
            break
    
    if not trip_found:
        trips.append(trip_dict)
    
    _save_json(TRIP_FILE, trips)

def load_trips() -> List:
    """Loads all trips from the JSON file."""
    from models import Trip
    from data_manager import load_users, load_travellers
    
    trips_data = _load_json(TRIP_FILE)
    all_users = load_users()
    all_travellers = load_travellers()
    trips = []
    
    for data in trips_data:
        try:
            # Convert string date back to datetime object
            if 'start_date' in data:
                data['start_date'] = datetime.fromisoformat(data['start_date'])
            
            # Find coordinator by user_id
            coordinator = None
            if data['coordinator_id']:
                coordinator = next((u for u in all_users if u.user_id == data['coordinator_id']), None)
            
            # Find travellers by their IDs
            travellers = []
            for traveller_id in data['traveller_ids']:
                traveller = next((t for t in all_travellers if t.traveller_id == traveller_id), None)
                if traveller:
                    travellers.append(traveller)
            
            # Create trip object
            trip = Trip(
                trip_id=data['trip_id'],
                name=data['name'],
                start_date=data['start_date'],
                duration_days=data['duration_days'],
                coordinator=coordinator
            )
            trip.travellers = travellers
            trip.is_active = data.get('is_active', True)
            
            trips.append(trip)
        except Exception as e:
            print(f"Error loading trip {data.get('trip_id', 'unknown')}: {e}")
            continue
    
    return trips

# Add these trip management functions to your data_manager.py

def save_trip(trip) -> None:
    """Saves a single trip to the JSON file."""
    trips = _load_json(TRIP_FILE)
    
    trip_dict = {
        'trip_id': trip.trip_id,
        'name': trip.name,
        'start_date': trip.start_date.isoformat() if hasattr(trip.start_date, 'isoformat') else str(trip.start_date),
        'duration_days': trip.duration_days,
        'coordinator_id': trip.coordinator.user_id if trip.coordinator else None,
        'traveller_ids': [t.traveller_id for t in trip.travellers],
        'trip_leg_ids': [leg.leg_id for leg in trip.trip_legs],
        'is_active': trip.is_active
    }
    
    trip_found = False
    for i, t in enumerate(trips):
        if t['trip_id'] == trip.trip_id:
            trips[i] = trip_dict
            trip_found = True
            break
    
    if not trip_found:
        trips.append(trip_dict)
    
    _save_json(TRIP_FILE, trips)

def load_trips() -> List:
    """Loads all trips from the JSON file."""
    from models import Trip
    from data_manager import load_users, load_travellers
    
    trips_data = _load_json(TRIP_FILE)
    all_users = load_users()
    all_travellers = load_travellers()
    trips = []
    
    for data in trips_data:
        try:
            # Convert string date back to datetime object
            if 'start_date' in data:
                data['start_date'] = datetime.fromisoformat(data['start_date'])
            
            # Find coordinator by user_id
            coordinator = None
            if data['coordinator_id']:
                coordinator = next((u for u in all_users if u.user_id == data['coordinator_id']), None)
            
            # Find travellers by their IDs
            travellers = []
            for traveller_id in data['traveller_ids']:
                traveller = next((t for t in all_travellers if t.traveller_id == traveller_id), None)
                if traveller:
                    travellers.append(traveller)
            
            # Create trip object
            trip = Trip(
                trip_id=data['trip_id'],
                name=data['name'],
                start_date=data['start_date'],
                duration_days=data['duration_days'],
                coordinator=coordinator
            )
            trip.travellers = travellers
            trip.is_active = data.get('is_active', True)
            
            trips.append(trip)
        except Exception as e:
            print(f"Error loading trip {data.get('trip_id', 'unknown')}: {e}")
            continue
    
    return trips

def save_trip_leg(trip_leg) -> None:
    """Saves a single trip leg to the JSON file."""
    # We'll store trip legs within the trip data for simplicity
    # In a more complex system, this would be in a separate file
    pass

def load_trip_legs() -> List:
    """Loads all trip legs from the JSON file."""
    # We'll implement this when we add trip leg management
    return []

def delete_trip(trip_id: str) -> None:
    """Permanently delete a trip from the JSON file."""
    trips = _load_json(TRIP_FILE)
    # Filter out the trip to be deleted
    updated_trips = [t for t in trips if t['trip_id'] != trip_id]
    _save_json(TRIP_FILE, updated_trips)
    
print("Data Manager module loaded successfully.")