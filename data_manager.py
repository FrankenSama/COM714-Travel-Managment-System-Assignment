# FILE: data_manager.py
# Handles all data persistence using JSON files.

import json
import os
from datetime import datetime
from typing import List, Dict, Any
from models import User, TripCoordinator, TripManager, Administrator, Traveller, Trip, TripLeg, Invoice, Payment, TransportMode, TripLegType

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
        'role': user.role.value,
        '_type': type(user).__name__
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
    users_data = _load_json(USER_FILE)
    users = []
    
    for user_data in users_data:
        try:
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
                    role=user_data['role']
                )
            users.append(user)
        except Exception as e:
            print(f"Error loading user {user_data.get('username', 'unknown')}: {e}")
            continue
    
    return users

def create_trip_manager(user_id: str, username: str, password: str, name: str) -> TripManager:
    """Create a new Trip Manager user."""
    import hashlib
    
    # Check if username already exists
    existing_users = load_users()
    if any(user.username == username for user in existing_users):
        raise ValueError(f"Username '{username}' already exists.")
    
    # Hash the password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    new_manager = TripManager(
        user_id=user_id,
        username=username,
        password=hashed_password,
        name=name
    )
    
    save_user(new_manager)
    return new_manager

def create_trip_coordinator(user_id: str, username: str, password: str, name: str) -> TripCoordinator:
    """Create a new Trip Coordinator user."""
    import hashlib
    
    # Check if username already exists
    existing_users = load_users()
    if any(user.username == username for user in existing_users):
        raise ValueError(f"Username '{username}' already exists.")
    
    # Hash the password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    new_coordinator = TripCoordinator(
        user_id=user_id,
        username=username,
        password=hashed_password,
        name=name
    )
    
    save_user(new_coordinator)
    return new_coordinator

def delete_user(user_id: str) -> None:
    """Permanently delete a user from the system."""
    users = _load_json(USER_FILE)
    updated_users = [u for u in users if u['user_id'] != user_id]
    _save_json(USER_FILE, updated_users)

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

def delete_traveller(traveller_id: str) -> None:
    """Permanently delete a traveller from the JSON file."""
    travellers = _load_json(TRAVELLER_FILE)
    updated_travellers = [t for t in travellers if t['traveller_id'] != traveller_id]
    _save_json(TRAVELLER_FILE, updated_travellers)
    
    # Also remove the traveller from any trips they were assigned to
    trips = _load_json(TRIP_FILE)
    for trip in trips:
        if 'traveller_ids' in trip and traveller_id in trip['traveller_ids']:
            trip['traveller_ids'].remove(traveller_id)
    _save_json(TRIP_FILE, trips)

def assign_traveller_to_trip(trip_id: str, traveller_id: str) -> bool:
    """Assign a traveller to a trip."""
    trips = _load_json(TRIP_FILE)
    travellers = load_travellers()
    
    # Find the traveller
    traveller = next((t for t in travellers if t.traveller_id == traveller_id), None)
    if not traveller:
        print(f"Traveller {traveller_id} not found.")
        return False
    
    # Find the trip and assign traveller
    trip_updated = False
    for trip_data in trips:
        if trip_data['trip_id'] == trip_id:
            if 'traveller_ids' not in trip_data:
                trip_data['traveller_ids'] = []
            
            # Check if traveller already assigned
            if traveller_id not in trip_data['traveller_ids']:
                trip_data['traveller_ids'].append(traveller_id)
                trip_updated = True
            break
    
    if trip_updated:
        _save_json(TRIP_FILE, trips)
        return True
    else:
        print(f"Trip {trip_id} not found or traveller already assigned.")
        return False

def remove_traveller_from_trip(trip_id: str, traveller_id: str) -> bool:
    """Remove a traveller from a trip."""
    trips = _load_json(TRIP_FILE)
    
    trip_updated = False
    for trip_data in trips:
        if trip_data['trip_id'] == trip_id:
            if 'traveller_ids' in trip_data and traveller_id in trip_data['traveller_ids']:
                trip_data['traveller_ids'].remove(traveller_id)
                trip_updated = True
            break
    
    if trip_updated:
        _save_json(TRIP_FILE, trips)
        return True
    else:
        print(f"Traveller {traveller_id} not found in trip {trip_id}.")
        return False

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
        'is_active': trip.is_active,
        'trip_legs': []
    }
    
    # Save trip legs within the trip
    for leg in trip.trip_legs:
        leg_dict = {
            'leg_id': leg.leg_id,
            'sequence': leg.sequence,
            'start_location': leg.start_location,
            'destination': leg.destination,
            'transport_provider': leg.transport_provider,
            'transport_mode': leg.transport_mode.value,
            'leg_type': leg.leg_type.value,
            'cost': leg.cost,
            'description': leg.description
        }
        trip_dict['trip_legs'].append(leg_dict)
    
    trip_found = False
    for i, t in enumerate(trips):
        if t['trip_id'] == trip.trip_id:
            trips[i] = trip_dict
            trip_found = True
            break
    
    if not trip_found:
        trips.append(trip_dict)
    
    _save_json(TRIP_FILE, trips)

def save_trip_legs(trip) -> None:
    """Saves all trip legs for a trip (calls save_trip internally)."""
    save_trip(trip)

def load_trip_legs_for_trip(trip_data: dict) -> List:
    """Loads trip legs for a specific trip from trip data."""
    trip_legs = []
    if 'trip_legs' in trip_data:
        for leg_data in trip_data['trip_legs']:
            try:
                leg = TripLeg(
                    leg_id=leg_data['leg_id'],
                    sequence=leg_data['sequence'],
                    start_location=leg_data['start_location'],
                    destination=leg_data['destination'],
                    transport_provider=leg_data['transport_provider'],
                    transport_mode=TransportMode(leg_data['transport_mode']),
                    leg_type=TripLegType(leg_data['leg_type']),
                    cost=leg_data.get('cost', 0.0),
                    description=leg_data.get('description', '')
                )
                trip_legs.append(leg)
            except Exception as e:
                print(f"Error loading trip leg {leg_data.get('leg_id', 'unknown')}: {e}")
                continue
    
    return trip_legs

def load_trips() -> List:
    """Loads all trips from the JSON file."""
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
            if data.get('coordinator_id'):
                coordinator = next((u for u in all_users if u.user_id == data['coordinator_id']), None)
            
            # Find travellers by their IDs
            travellers = []
            for traveller_id in data.get('traveller_ids', []):
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
            trip.trip_legs = load_trip_legs_for_trip(data)
            
            trips.append(trip)
        except Exception as e:
            print(f"Error loading trip {data.get('trip_id', 'unknown')}: {e}")
            continue
    
    return trips

def delete_trip(trip_id: str) -> None:
    """Permanently delete a trip from the JSON file."""
    trips = _load_json(TRIP_FILE)
    updated_trips = [t for t in trips if t['trip_id'] != trip_id]
    _save_json(TRIP_FILE, updated_trips)

def save_invoice(invoice) -> None:
    """Saves an invoice to the JSON file."""
    invoices = _load_json(INVOICE_FILE)
    
    invoice_dict = {
        'invoice_id': invoice.invoice_id,
        'trip_id': invoice.trip.trip_id,
        'issue_date': invoice.issue_date.isoformat() if hasattr(invoice.issue_date, 'isoformat') else str(invoice.issue_date),
        'total_amount': invoice.total_amount,
        'status': invoice.status,
        'payments': []
    }
    
    # Convert payments to dictionaries
    for payment in invoice.payments:
        payment_dict = {
            'payment_id': payment.payment_id,
            'amount': payment.amount,
            'date': payment.date.isoformat() if hasattr(payment.date, 'isoformat') else str(payment.date),
            'method': payment.method
        }
        invoice_dict['payments'].append(payment_dict)
    
    # Check if invoice exists, if so, update. Else, append.
    invoice_found = False
    for i, inv in enumerate(invoices):
        if inv['invoice_id'] == invoice.invoice_id:
            invoices[i] = invoice_dict
            invoice_found = True
            break
    
    if not invoice_found:
        invoices.append(invoice_dict)
    
    _save_json(INVOICE_FILE, invoices)

def load_invoices() -> List:
    """Loads all invoices from the JSON file."""
    invoices_data = _load_json(INVOICE_FILE)
    trips = load_trips()
    invoices = []
    
    for data in invoices_data:
        try:
            # Find the trip for this invoice
            trip = next((t for t in trips if t.trip_id == data['trip_id']), None)
            if not trip:
                continue
                
            # Convert string dates back to datetime objects
            issue_date = datetime.fromisoformat(data['issue_date'])
            
            # Create invoice object
            invoice = Invoice(
                invoice_id=data['invoice_id'],
                trip=trip,
                issue_date=issue_date,
                total_amount=data['total_amount'],
                status=data.get('status', 'Pending')
            )
            
            # Load payments
            for payment_data in data.get('payments', []):
                payment_date = datetime.fromisoformat(payment_data['date'])
                payment = Payment(
                    payment_id=payment_data['payment_id'],
                    invoice=invoice,
                    amount=payment_data['amount'],
                    date=payment_date,
                    method=payment_data['method']
                )
                invoice.payments.append(payment)
            
            invoices.append(invoice)
        except Exception as e:
            print(f"Error loading invoice {data.get('invoice_id', 'unknown')}: {e}")
            continue
    
    return invoices

def delete_invoice(invoice_id: str) -> None:
    """Permanently delete an invoice from the JSON file."""
    invoices = _load_json(INVOICE_FILE)
    updated_invoices = [inv for inv in invoices if inv['invoice_id'] != invoice_id]
    _save_json(INVOICE_FILE, updated_invoices)

print("Data Manager module loaded successfully.")