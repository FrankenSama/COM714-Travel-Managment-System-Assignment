# FILE: models.py
# A hypothetical structure showing the classes and their relationships.

from datetime import datetime
from enum import Enum
from typing import List, Optional

class UserRole(Enum):
    COORDINATOR = "Trip Coordinator"
    MANAGER = "Trip Manager"
    ADMIN = "Administrator"

class TransportMode(Enum):
    FLIGHT = "Flight"
    TRAIN = "Train"
    BUS = "Bus"
    TAXI = "Taxi"
    SHIP = "Ship"

class TripLegType(Enum):
    ACCOMMODATION = "Accommodation"
    POINT_OF_INTEREST = "Point of Interest"
    TRANSFER = "Transfer Point"

class User:
    def __init__(self, user_id: str, username: str, password: str, name: str, role: UserRole):
        self.user_id = user_id
        self.username = username
        self.password = password  # In a real system, this would be hashed
        self.name = name
        self.role = role

    def login(self, username: str, password: str) -> bool:
        return self.username == username and self.password == password

    # This class is abstract. Specific methods are in the child classes.

class TripCoordinator(User):
    def __init__(self, user_id: str, username: str, password: str, name: str):
        super().__init__(user_id, username, password, name, UserRole.COORDINATOR)
        self.managed_trips: List['Trip'] = []

    def add_traveller_to_trip(self, trip: 'Trip', traveller: 'Traveller') -> bool:
        # Implementation logic here
        pass

    def update_trip_leg(self, trip: 'Trip', old_leg: 'TripLeg', new_leg: 'TripLeg') -> bool:
        # Implementation logic here
        pass

    def generate_itinerary(self, trip: 'Trip') -> 'Itinerary':
        # Implementation logic here
        pass

    def record_payment(self, trip: 'Trip', amount: float, description: str) -> 'Payment':
        # Implementation logic here
        pass

class TripManager(User):
    def __init__(self, user_id: str, username: str, password: str, name: str):
        super().__init__(user_id, username, password, name, UserRole.MANAGER)
        self.managed_coordinators: List[TripCoordinator] = []

    # Inherits all TripCoordinator methods
    def create_trip_coordinator(self, user_id: str, username: str, password: str, name: str) -> TripCoordinator:
        # Implementation logic here
        pass

    def generate_total_invoice(self, trip: 'Trip') -> 'Invoice':
        # Implementation logic here
        pass

class Administrator(User):
    def __init__(self, user_id: str, username: str, password: str, name: str):
        super().__init__(user_id, username, password, name, UserRole.ADMIN)

    def create_trip_manager(self, user_id: str, username: str, password: str, name: str) -> TripManager:
        # Implementation logic here
        pass

    def view_all_invoices(self) -> List['Invoice']:
        # Implementation logic here
        pass

class Traveller:
    def __init__(self, traveller_id: str, name: str, address: str, date_of_birth: datetime, emergency_contact: str, government_id: str):
        self.traveller_id = traveller_id
        self.name = name
        self.address = address
        self.date_of_birth = date_of_birth
        self.emergency_contact = emergency_contact
        self.government_id = government_id

class Trip:
    def __init__(self, trip_id: str, name: str, start_date: datetime, duration_days: int, coordinator: TripCoordinator):
        self.trip_id = trip_id
        self.name = name
        self.start_date = start_date
        self.duration_days = duration_days
        self.coordinator = coordinator
        self.travellers: List[Traveller] = []
        self.trip_legs: List[TripLeg] = []
        self.is_active = True

class TripLeg:
    def __init__(self, leg_id: str, sequence: int, start_location: str, destination: str, 
                 transport_provider: str, transport_mode: TransportMode, 
                 leg_type: TripLegType, cost: float = 0.0, description: str = ""):
        self.leg_id = leg_id
        self.sequence = sequence
        self.start_location = start_location
        self.destination = destination
        self.transport_provider = transport_provider
        self.transport_mode = transport_mode
        self.leg_type = leg_type
        self.cost = cost
        self.description = description

    def __str__(self):
        return f"{self.sequence}. {self.start_location} → {self.destination} ({self.transport_mode.value})"

class Invoice:
    def __init__(self, invoice_id: str, trip: Trip, issue_date: datetime, total_amount: float):
        self.invoice_id = invoice_id
        self.trip = trip
        self.issue_date = issue_date
        self.total_amount = total_amount
        self.payments: List[Payment] = []
        self.is_paid = False

    def calculate_balance(self) -> float:
        total_paid = sum(payment.amount for payment in self.payments)
        return self.total_amount - total_paid

class Payment:
    def __init__(self, payment_id: str, invoice: Invoice, amount: float, date: datetime, method: str):
        self.payment_id = payment_id
        self.invoice = invoice
        self.amount = amount
        self.date = date
        self.method = method
        
class Invoice:
    def __init__(self, invoice_id: str, trip: Trip, issue_date: datetime, total_amount: float, status: str = "Pending"):
        self.invoice_id = invoice_id
        self.trip = trip
        self.issue_date = issue_date
        self.total_amount = total_amount
        self.status = status  # Pending, Paid, Cancelled
        self.payments = []

    def add_payment(self, amount: float, payment_date: datetime, method: str = "Cash"):
        payment = Payment(
            payment_id=f"PAY{datetime.now().strftime('%Y%m%d%H%M%S')}",
            invoice=self,
            amount=amount,
            date=payment_date,
            method=method
        )
        self.payments.append(payment)
        return payment

    def calculate_balance(self) -> float:
        total_paid = sum(payment.amount for payment in self.payments)
        return self.total_amount - total_paid

    def is_fully_paid(self) -> bool:
        return self.calculate_balance() <= 0

    def __str__(self):
        balance = self.calculate_balance()
        status_icon = "✓" if self.is_fully_paid() else "●"
        return f"{status_icon} Invoice {self.invoice_id} - £{self.total_amount:.2f} ({self.status}) - Balance: £{balance:.2f}"

class Payment:
    def __init__(self, payment_id: str, invoice: Invoice, amount: float, date: datetime, method: str):
        self.payment_id = payment_id
        self.invoice = invoice
        self.amount = amount
        self.date = date
        self.method = method

    def __str__(self):
        return f"Payment {self.payment_id} - £{self.amount:.2f} via {self.method} on {self.date.strftime('%Y-%m-%d')}"

class Itinerary:
    def __init__(self, trip: Trip):
        self.trip = trip
        self.legs = sorted(trip.trip_legs, key=lambda leg: leg.sequence)

    def display(self) -> str:
        """Formats the itinerary for printing/displaying"""
        if not self.legs:
            return "No itinerary available for this trip."
        
        output = f"ITINERARY FOR: {self.trip.name}\n"
        output += f"Start Date: {self.trip.start_date.strftime('%Y-%m-%d')}\n"
        output += f"Duration: {self.trip.duration_days} days\n"
        output += "=" * 50 + "\n"
        
        for leg in self.legs:
            output += f"{leg}\n"
            output += f"   Provider: {leg.transport_provider}\n"
            output += f"   Type: {leg.leg_type.value}\n"
            if leg.cost > 0:
                output += f"   Cost: £{leg.cost:.2f}\n"
            if leg.description:
                output += f"   Notes: {leg.description}\n"
            output += "\n"
        
        total_cost = sum(leg.cost for leg in self.legs)
        output += f"TOTAL ESTIMATED COST: £{total_cost:.2f}\n"
        
        return output
    
# Reporting Class (Uses Matplotlib/Plotly)
class ReportGenerator:
    @staticmethod
    def generate_financial_summary(trips: List[Trip]) -> None:
        # Uses matplotlib to plot a chart
        pass

    @staticmethod
    def generate_traveller_statistics(travellers: List[Traveller]) -> None:
        # Uses matplotlib to plot a chart
        pass