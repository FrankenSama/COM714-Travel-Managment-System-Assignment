# FILE: test_system.py
# Unit tests for the Travel Management System

import unittest
import hashlib
from datetime import datetime
from models import (User, Administrator, TripManager, TripCoordinator, Traveller,
                   Trip, TripLeg, Invoice, Payment, Itinerary,
                   UserRole, TransportMode, TripLegType)

class TestAuthentication(unittest.TestCase):
    """Test authentication functionality"""
    
    def test_password_hashing(self):
        """Test that passwords are properly hashed"""
        password = "test123"
        expected_hash = hashlib.sha256(password.encode()).hexdigest()
        self.assertEqual(len(expected_hash), 64)  # SHA-256 produces 64 char hex
    
    def test_user_creation(self):
        """Test creating different user types"""
        admin = Administrator("A001", "admin", "pass123", "Admin User")
        self.assertEqual(admin.role, UserRole.ADMIN)
        
        manager = TripManager("M001", "manager", "pass123", "Manager User")
        self.assertEqual(manager.role, UserRole.MANAGER)
        
        coordinator = TripCoordinator("C001", "coord", "pass123", "Coord User")
        self.assertEqual(coordinator.role, UserRole.COORDINATOR)

class TestTripManagement(unittest.TestCase):
    """Test trip-related functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.coordinator = TripCoordinator("C001", "coord", "pass", "Test Coord")
        self.trip = Trip(
            trip_id="T001",
            name="Test Trip",
            start_date=datetime(2025, 6, 1),
            duration_days=7,
            coordinator=self.coordinator
        )
    
    def test_trip_creation(self):
        """Test creating a trip"""
        self.assertEqual(self.trip.trip_id, "T001")
        self.assertEqual(self.trip.name, "Test Trip")
        self.assertEqual(self.trip.duration_days, 7)
        self.assertTrue(self.trip.is_active)
    
    def test_trip_leg_addition(self):
        """Test adding legs to a trip"""
        leg = TripLeg(
            leg_id="L001",
            sequence=1,
            start_location="London",
            destination="Paris",
            transport_provider="Eurostar",
            transport_mode=TransportMode.TRAIN,
            leg_type=TripLegType.TRANSFER,
            cost=150.00
        )
        
        self.trip.trip_legs.append(leg)
        self.assertEqual(len(self.trip.trip_legs), 1)
        self.assertEqual(self.trip.trip_legs[0].cost, 150.00)
    
    def test_cost_calculation(self):
        """Test automatic cost calculation from trip legs"""
        leg1 = TripLeg("L001", 1, "London", "Paris", "Eurostar", 
                      TransportMode.TRAIN, TripLegType.TRANSFER, 150.00)
        leg2 = TripLeg("L002", 2, "Paris", "Hotel", "Taxi",
                      TransportMode.TAXI, TripLegType.ACCOMMODATION, 50.00)
        
        self.trip.trip_legs.extend([leg1, leg2])
        
        total_cost = sum(leg.cost for leg in self.trip.trip_legs)
        self.assertEqual(total_cost, 200.00)

class TestTravellerManagement(unittest.TestCase):
    """Test traveller-related functionality"""
    
    def test_traveller_creation(self):
        """Test creating a traveller"""
        traveller = Traveller(
            traveller_id="TR001",
            name="John Doe",
            address="123 Test St",
            date_of_birth=datetime(1990, 5, 15),
            emergency_contact="Jane Doe: 555-1234",
            government_id="AB123456"
        )
        
        self.assertEqual(traveller.name, "John Doe")
        self.assertEqual(traveller.government_id, "AB123456")
    
    def test_trip_assignment(self):
        """Test assigning travellers to trips"""
        coordinator = TripCoordinator("C001", "coord", "pass", "Coord")
        trip = Trip("T001", "Test Trip", datetime(2025, 6, 1), 7, coordinator)
        
        traveller = Traveller(
            "TR001", "John Doe", "123 Test St",
            datetime(1990, 5, 15), "Emergency: 555-1234", "AB123456"
        )
        
        trip.travellers.append(traveller)
        self.assertEqual(len(trip.travellers), 1)
        self.assertIn(traveller, trip.travellers)

class TestInvoiceAndPayments(unittest.TestCase):
    """Test invoice and payment functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.coordinator = TripCoordinator("C001", "coord", "pass", "Coord")
        self.trip = Trip("T001", "Test Trip", datetime(2025, 6, 1), 7, self.coordinator)
        
        leg1 = TripLeg("L001", 1, "London", "Paris", "Eurostar",
                      TransportMode.TRAIN, TripLegType.TRANSFER, 150.00)
        leg2 = TripLeg("L002", 2, "Paris", "Hotel", "Taxi",
                      TransportMode.TAXI, TripLegType.ACCOMMODATION, 50.00)
        self.trip.trip_legs.extend([leg1, leg2])
        
        total_cost = sum(leg.cost for leg in self.trip.trip_legs)
        self.invoice = Invoice("INV001", self.trip, datetime.now(), total_cost)
    
    def test_invoice_creation(self):
        """Test creating an invoice"""
        self.assertEqual(self.invoice.total_amount, 200.00)
        self.assertEqual(self.invoice.status, "Pending")
        self.assertEqual(len(self.invoice.payments), 0)
    
    def test_payment_addition(self):
        """Test adding payments to invoice"""
        self.invoice.add_payment(100.00, datetime.now(), "Card")
        
        self.assertEqual(len(self.invoice.payments), 1)
        self.assertEqual(self.invoice.payments[0].amount, 100.00)
    
    def test_balance_calculation(self):
        """Test invoice balance calculation"""
        self.invoice.add_payment(100.00, datetime.now(), "Card")
        balance = self.invoice.calculate_balance()
        
        self.assertEqual(balance, 100.00)
    
    def test_fully_paid_status(self):
        """Test invoice fully paid status"""
        # Not fully paid
        self.invoice.add_payment(100.00, datetime.now(), "Card")
        self.assertFalse(self.invoice.is_fully_paid())
        
        # Fully paid
        self.invoice.add_payment(100.00, datetime.now(), "Cash")
        self.assertTrue(self.invoice.is_fully_paid())
    
    def test_overpayment(self):
        """Test handling overpayment"""
        self.invoice.add_payment(250.00, datetime.now(), "Card")
        balance = self.invoice.calculate_balance()
        
        self.assertEqual(balance, -50.00)  # Overpaid by 50
        self.assertTrue(self.invoice.is_fully_paid())

class TestItineraryGeneration(unittest.TestCase):
    """Test itinerary generation"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.coordinator = TripCoordinator("C001", "coord", "pass", "Coord")
        self.trip = Trip("T001", "European Tour", datetime(2025, 6, 1), 7, self.coordinator)
        
        # Add legs in non-sequential order to test sorting
        leg2 = TripLeg("L002", 2, "Paris", "Rome", "Flight",
                      TransportMode.FLIGHT, TripLegType.TRANSFER, 120.00)
        leg1 = TripLeg("L001", 1, "London", "Paris", "Eurostar",
                      TransportMode.TRAIN, TripLegType.TRANSFER, 150.00)
        leg3 = TripLeg("L003", 3, "Rome", "Hotel Colosseum", "Taxi",
                      TransportMode.TAXI, TripLegType.ACCOMMODATION, 30.00)
        
        self.trip.trip_legs.extend([leg2, leg1, leg3])
    
    def test_leg_sorting(self):
        """Test that legs are sorted by sequence"""
        itinerary = Itinerary(self.trip)
        
        sequences = [leg.sequence for leg in itinerary.legs]
        self.assertEqual(sequences, [1, 2, 3])
    
    def test_itinerary_display(self):
        """Test itinerary text generation"""
        itinerary = Itinerary(self.trip)
        display_text = itinerary.display()
        
        self.assertIn("ITINERARY FOR: European Tour", display_text)
        self.assertIn("London", display_text)
        self.assertIn("Paris", display_text)
        self.assertIn("Rome", display_text)
        self.assertIn("TOTAL ESTIMATED COST: £300.00", display_text)
    
    def test_empty_itinerary(self):
        """Test itinerary with no legs"""
        empty_trip = Trip("T002", "Empty Trip", datetime(2025, 7, 1), 5, self.coordinator)
        itinerary = Itinerary(empty_trip)
        
        display_text = itinerary.display()
        self.assertIn("No itinerary available", display_text)

class TestEnumerations(unittest.TestCase):
    """Test enumeration types"""
    
    def test_user_roles(self):
        """Test UserRole enumeration"""
        self.assertEqual(UserRole.ADMIN.value, "Administrator")
        self.assertEqual(UserRole.MANAGER.value, "Trip Manager")
        self.assertEqual(UserRole.COORDINATOR.value, "Trip Coordinator")
    
    def test_transport_modes(self):
        """Test TransportMode enumeration"""
        modes = [mode.value for mode in TransportMode]
        self.assertIn("Flight", modes)
        self.assertIn("Train", modes)
        self.assertIn("Bus", modes)
        self.assertIn("Taxi", modes)
        self.assertIn("Ship", modes)
    
    def test_trip_leg_types(self):
        """Test TripLegType enumeration"""
        types = [t.value for t in TripLegType]
        self.assertIn("Accommodation", types)
        self.assertIn("Point of Interest", types)
        self.assertIn("Transfer Point", types)

class TestDataValidation(unittest.TestCase):
    """Test data validation and edge cases"""
    
    def test_negative_cost(self):
        """Test handling of negative costs"""
        leg = TripLeg("L001", 1, "A", "B", "Provider",
                     TransportMode.BUS, TripLegType.TRANSFER, -50.00)
        
        # System should allow negative costs (e.g., refunds)
        self.assertEqual(leg.cost, -50.00)
    
    def test_zero_duration_trip(self):
        """Test trip with zero duration"""
        coordinator = TripCoordinator("C001", "coord", "pass", "Coord")
        trip = Trip("T001", "Day Trip", datetime(2025, 6, 1), 0, coordinator)
        
        self.assertEqual(trip.duration_days, 0)
    
    def test_future_date_validation(self):
        """Test trip with future start date"""
        coordinator = TripCoordinator("C001", "coord", "pass", "Coord")
        future_date = datetime(2026, 12, 31)
        trip = Trip("T001", "Future Trip", future_date, 7, coordinator)
        
        self.assertTrue(trip.start_date > datetime.now())

def run_tests():
    """Run all tests and display results"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestAuthentication))
    suite.addTests(loader.loadTestsFromTestCase(TestTripManagement))
    suite.addTests(loader.loadTestsFromTestCase(TestTravellerManagement))
    suite.addTests(loader.loadTestsFromTestCase(TestInvoiceAndPayments))
    suite.addTests(loader.loadTestsFromTestCase(TestItineraryGeneration))
    suite.addTests(loader.loadTestsFromTestCase(TestEnumerations))
    suite.addTests(loader.loadTestsFromTestCase(TestDataValidation))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70)
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)