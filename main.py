# FILE: main.py
# Main entry point for the Travel Management System console application.

from auth import AuthenticationService
from data_manager import load_users, load_travellers, save_traveller, load_trips, save_trip
from models import Traveller, TripCoordinator, TripManager, Administrator, Trip
from datetime import datetime
import os

class TravelManagementSystem:
    def __init__(self):
        self.auth_service = AuthenticationService()
        self.is_running = True

    def clear_screen(self):
        """Clear the console screen for better readability."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_header(self):
        """Display application header."""
        print("=" * 50)
        print("    SOLENT TRIPS - TRAVEL MANAGEMENT SYSTEM")
        print("=" * 50)
        if self.auth_service.current_user:
            user = self.auth_service.current_user
            print(f"Logged in as: {user.name} ({user.role.value})")
        print()

    def login_menu(self):
        """Handle user login."""
        self.clear_screen()
        self.display_header()
        print("=== LOGIN ===")
        username = input("Username: ")
        password = input("Password: ")
        
        success, message, user = self.auth_service.login(username, password)
        print(f"\n{message}")
        
        if success:
            input("\nPress Enter to continue to main menu...")
        else:
            input("\nPress Enter to try again...")

    def admin_menu(self):
        """Menu for Administrator users."""
        while True:
            self.clear_screen()
            self.display_header()
            print("=== ADMINISTRATOR MENU ===")
            print("1. Manage Trip Managers")
            print("2. View All Invoices")
            print("3. Generate Reports")
            print("4. Coordinator Functions")
            print("5. Logout")
            print("6. Exit System")
            
            choice = input("\nEnter your choice (1-6): ")
            
            if choice == "1":
                self.manage_trip_managers()
            elif choice == "2":
                self.view_all_invoices()
            elif choice == "3":
                self.generate_reports()
            elif choice == "4":
                self.trip_coordinator_menu()
            elif choice == "5":
                self.auth_service.logout()
                print("Logged out successfully.")
                input("Press Enter to continue...")
                break
            elif choice == "6":
                self.is_running = False
                break
            else:
                print("Invalid choice. Please try again.")
                input("Press Enter to continue...")

    def trip_manager_menu(self):
        """Menu for Trip Manager users."""
        while True:
            self.clear_screen()
            self.display_header()
            print("=== TRIP MANAGER MENU ===")
            print("1. Manage Trip Coordinators")
            print("2. Generate Total Invoice")
            print("3. Coordinator Functions")
            print("4. Logout")
            print("5. Exit System")
            
            choice = input("\nEnter your choice (1-5): ")
            
            if choice == "1":
                self.manage_trip_coordinators()
            elif choice == "2":
                self.generate_total_invoice()
            elif choice == "3":
                self.trip_coordinator_menu()
            elif choice == "4":
                self.auth_service.logout()
                print("Logged out successfully.")
                input("Press Enter to continue...")
                break
            elif choice == "5":
                self.is_running = False
                break
            else:
                print("Invalid choice. Please try again.")
                input("Press Enter to continue...")

    def trip_coordinator_menu(self):
        """Menu for Trip Coordinator users."""
        while True:
            self.clear_screen()
            self.display_header()
            print("=== TRIP COORDINATOR MENU ===")
            print("1. Manage Trips")
            print("2. Manage Travellers")
            print("3. Manage Trip Legs")
            print("4. Manage Trip Assignments")
            print("5. Generate Itinerary")
            print("6. Handle Payments")
            print("7. Back to Previous Menu")
            print("8. Logout")
            print("9. Exit System")
            
            choice = input("\nEnter your choice (1-9): ")
            
            if choice == "1":
                self.manage_trips()
            elif choice == "2":
                self.manage_travellers()
            elif choice == "3":
                self.manage_trip_legs()
            elif choice == "4":
                self.manage_trip_assignments()
            elif choice == "5":
                self.generate_itinerary()
            elif choice == "6":
                self.handle_payments()
            elif choice == "7":
                break
            elif choice == "8":
                self.auth_service.logout()
                print("Logged out successfully.")
                input("Press Enter to continue...")
                break
            elif choice == "9":
                self.is_running = False
                break
            else:
                print("Invalid choice. Please try again.")
                input("Press Enter to continue...")

    def main_menu(self):
        """Main application loop."""
        while self.is_running:
            if not self.auth_service.current_user:
                self.login_menu()
            else:
                user = self.auth_service.current_user
                if isinstance(user, Administrator):
                    self.admin_menu()
                elif isinstance(user, TripManager):
                    self.trip_manager_menu()
                elif isinstance(user, TripCoordinator):
                    self.trip_coordinator_menu()
                else:
                    print("Unknown user role. Logging out...")
                    self.auth_service.logout()
                    input("Press Enter to continue...")

    def manage_trips(self):
        """Manage trips - create, view, update, delete."""
        from data_manager import load_trips, save_trip
        from models import Trip
        from datetime import datetime
        
        while True:
            self.clear_screen()
            self.display_header()
            print("=== MANAGE TRIPS ===")
            
            trips = load_trips()
            current_user = self.auth_service.current_user
            
            # Filter trips based on user role
            if isinstance(current_user, TripCoordinator):
                user_trips = [t for t in trips if t.coordinator and t.coordinator.user_id == current_user.user_id]
            else:
                user_trips = trips
            
            print(f"\nYour trips: {len(user_trips)}")
            
            print("\n1. View All Trips")
            print("2. Create New Trip")
            print("3. Update Trip")
            print("4. Delete Trip")
            print("5. Back to Main Menu")
            
            choice = input("\nEnter your choice (1-5): ")
            
            if choice == "1":
                self.clear_screen()
                self.display_header()
                print("=== ALL TRIPS ===")
                if user_trips:
                    for i, trip in enumerate(user_trips, 1):
                        status = "Active" if trip.is_active else "Inactive"
                        print(f"{i}. {trip.name} (ID: {trip.trip_id})")
                        print(f"   Start: {trip.start_date.strftime('%Y-%m-%d')}, Duration: {trip.duration_days} days")
                        print(f"   Coordinator: {trip.coordinator.name if trip.coordinator else 'None'}")
                        print(f"   Travellers: {len(trip.travellers)}, Status: {status}")
                        print()
                else:
                    print("No trips found.")
                input("\nPress Enter to continue...")
                
            elif choice == "2":
                self.clear_screen()
                self.display_header()
                print("=== CREATE NEW TRIP ===")
                
                trip_id = f"TR{datetime.now().strftime('%Y%m%d%H%M%S')}"
                name = input("Trip Name: ")
                start_date = input("Start Date (YYYY-MM-DD): ")
                duration = input("Duration (days): ")
                
                try:
                    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
                    duration_days = int(duration)
                    
                    coordinator = current_user
                    if not isinstance(coordinator, TripCoordinator):
                        print("Note: Only Trip Coordinators can be assigned to trips.")
                        print("Please assign this trip to a coordinator later.")
                        coordinator = None
                    
                    new_trip = Trip(
                        trip_id=trip_id,
                        name=name,
                        start_date=start_date_obj,
                        duration_days=duration_days,
                        coordinator=coordinator
                    )
                    
                    save_trip(new_trip)
                    print(f"Trip '{name}' created successfully with ID: {trip_id}")
                    
                except ValueError as e:
                    print(f"Error: Invalid input. {e}")
                except Exception as e:
                    print(f"Error creating trip: {e}")
                
                input("Press Enter to continue...")
                
            elif choice == "3":
                if not user_trips:
                    print("No trips available to update.")
                    input("Press Enter to continue...")
                    continue
                    
                self.clear_screen()
                self.display_header()
                print("=== UPDATE TRIP ===")
                for i, trip in enumerate(user_trips, 1):
                    print(f"{i}. {trip.name} (ID: {trip.trip_id})")
                
                try:
                    trip_num = int(input("\nSelect trip to update (number): ")) - 1
                    if 0 <= trip_num < len(user_trips):
                        trip = user_trips[trip_num]
                        print(f"\nUpdating: {trip.name}")
                        
                        new_name = input(f"New name [{trip.name}]: ") or trip.name
                        new_start = input(f"New start date (YYYY-MM-DD) [{trip.start_date.strftime('%Y-%m-%d')}]: ") or trip.start_date.strftime('%Y-%m-%d')
                        new_duration = input(f"New duration (days) [{trip.duration_days}]: ") or str(trip.duration_days)
                        
                        trip.name = new_name
                        trip.start_date = datetime.strptime(new_start, '%Y-%m-%d')
                        trip.duration_days = int(new_duration)
                        
                        save_trip(trip)
                        print("Trip updated successfully!")
                    else:
                        print("Invalid trip selection.")
                except (ValueError, IndexError):
                    print("Invalid input.")
                except Exception as e:
                    print(f"Error updating trip: {e}")
                
                input("Press Enter to continue...")
                
            elif choice == "4":
                if not user_trips:
                    print("No trips available to delete.")
                    input("Press Enter to continue...")
                    continue
                    
                self.clear_screen()
                self.display_header()
                print("=== DELETE TRIP ===")
                for i, trip in enumerate(user_trips, 1):
                    print(f"{i}. {trip.name} (ID: {trip.trip_id})")
                
                try:
                    trip_num = int(input("\nSelect trip to delete (number): ")) - 1
                    if 0 <= trip_num < len(user_trips):
                        trip = user_trips[trip_num]
                        confirm = input(f"Are you sure you want to PERMANENTLY delete '{trip.name}'? This cannot be undone! (y/n): ")
                        if confirm.lower() == 'y':
                            from data_manager import delete_trip
                            delete_trip(trip.trip_id)
                            print("Trip permanently deleted!")
                        else:
                            print("Deletion cancelled.")
                    else:
                        print("Invalid trip selection.")
                except (ValueError, IndexError):
                    print("Invalid input.")
                
                input("Press Enter to continue...")
                
            elif choice == "5":
                break
            else:
                print("Invalid choice. Please try again.")
                input("Press Enter to continue...")

    def manage_trip_legs(self):
        """Manage trip legs - add, view, update, delete legs for trips."""
        from data_manager import load_trips, save_trip_legs
        from models import TripLeg, TransportMode, TripLegType
        from datetime import datetime
        
        while True:
            self.clear_screen()
            self.display_header()
            print("=== MANAGE TRIP LEGS ===")
            
            trips = load_trips()
            current_user = self.auth_service.current_user
            
            # Filter trips based on user role
            if isinstance(current_user, TripCoordinator):
                user_trips = [t for t in trips if t.coordinator and t.coordinator.user_id == current_user.user_id]
            else:
                user_trips = trips
            
            if not user_trips:
                print("No trips available. Please create a trip first.")
                input("Press Enter to continue...")
                return
            
            print("\nSelect a trip to manage its legs:")
            for i, trip in enumerate(user_trips, 1):
                print(f"{i}. {trip.name} (ID: {trip.trip_id}) - {len(trip.trip_legs)} legs")
            
            print(f"{len(user_trips) + 1}. Back to Main Menu")
            
            try:
                choice = int(input("\nEnter your choice: "))
                if choice == len(user_trips) + 1:
                    break
                elif 1 <= choice <= len(user_trips):
                    selected_trip = user_trips[choice - 1]
                    self.manage_legs_for_trip(selected_trip)
                else:
                    print("Invalid choice.")
                    input("Press Enter to continue...")
            except ValueError:
                print("Please enter a valid number.")
                input("Press Enter to continue...")

    def manage_legs_for_trip(self, trip: Trip):
        """Manage legs for a specific trip."""
        from models import TripLeg, TransportMode, TripLegType
        from data_manager import save_trip_legs
        
        while True:
            self.clear_screen()
            self.display_header()
            print(f"=== MANAGING LEGS FOR: {trip.name} ===")
            print(f"Trip ID: {trip.trip_id}")
            print(f"Current legs: {len(trip.trip_legs)}")
            
            # Display current legs
            if trip.trip_legs:
                print("\nCurrent Legs:")
                for i, leg in enumerate(sorted(trip.trip_legs, key=lambda l: l.sequence), 1):
                    print(f"{i}. {leg}")
                    print(f"   Type: {leg.leg_type.value}, Cost: £{leg.cost:.2f}")
            else:
                print("\nNo legs added yet.")
            
            print("\n1. Add New Leg")
            print("2. Update Leg")
            print("3. Delete Leg")
            print("4. Generate Itinerary Preview")
            print("5. Back to Trip Selection")
            
            choice = input("\nEnter your choice (1-5): ")
            
            if choice == "1":
                self.clear_screen()
                self.display_header()
                print("=== ADD NEW TRIP LEG ===")
                
                leg_id = f"LG{datetime.now().strftime('%Y%m%d%H%M%S')}"
                sequence = len(trip.trip_legs) + 1
                start_location = input("Start Location: ")
                destination = input("Destination: ")
                transport_provider = input("Transport Provider: ")
                
                print("\nTransport Modes:")
                for i, mode in enumerate(TransportMode, 1):
                    print(f"{i}. {mode.value}")
                transport_choice = input("Select transport mode (number): ")
                
                print("\nLeg Types:")
                for i, leg_type in enumerate(TripLegType, 1):
                    print(f"{i}. {leg_type.value}")
                type_choice = input("Select leg type (number): ")
                
                cost = input("Cost (£): ") or "0.0"
                description = input("Description/Notes: ")
                
                try:
                    transport_mode = list(TransportMode)[int(transport_choice) - 1]
                    leg_type = list(TripLegType)[int(type_choice) - 1]
                    cost_float = float(cost)
                    
                    new_leg = TripLeg(
                        leg_id=leg_id,
                        sequence=sequence,
                        start_location=start_location,
                        destination=destination,
                        transport_provider=transport_provider,
                        transport_mode=transport_mode,
                        leg_type=leg_type,
                        cost=cost_float,
                        description=description
                    )
                    
                    trip.trip_legs.append(new_leg)
                    save_trip_legs(trip)
                    print("Trip leg added successfully!")
                    
                except (ValueError, IndexError):
                    print("Invalid input. Please try again.")
                except Exception as e:
                    print(f"Error adding trip leg: {e}")
                
                input("Press Enter to continue...")
                
            elif choice == "2":
                if not trip.trip_legs:
                    print("No legs available to update.")
                    input("Press Enter to continue...")
                    continue
                    
                print("Update leg functionality coming soon...")
                input("Press Enter to continue...")
                
            elif choice == "3":
                if not trip.trip_legs:
                    print("No legs available to delete.")
                    input("Press Enter to continue...")
                    continue
                    
                print("\nSelect leg to delete:")
                for i, leg in enumerate(sorted(trip.trip_legs, key=lambda l: l.sequence), 1):
                    print(f"{i}. {leg}")
                
                try:
                    leg_choice = int(input("Enter leg number: ")) - 1
                    if 0 <= leg_choice < len(trip.trip_legs):
                        leg_to_delete = sorted(trip.trip_legs, key=lambda l: l.sequence)[leg_choice]
                        confirm = input(f"Delete leg: {leg_to_delete}? (y/n): ")
                        if confirm.lower() == 'y':
                            trip.trip_legs = [leg for leg in trip.trip_legs if leg.leg_id != leg_to_delete.leg_id]
                            save_trip_legs(trip)
                            print("Leg deleted successfully!")
                        else:
                            print("Deletion cancelled.")
                    else:
                        print("Invalid selection.")
                except ValueError:
                    print("Please enter a valid number.")
                
                input("Press Enter to continue...")
                
            elif choice == "4":
                self.clear_screen()
                self.display_header()
                print("=== ITINERARY PREVIEW ===")
                from models import Itinerary
                itinerary = Itinerary(trip)
                print(itinerary.display())
                input("\nPress Enter to continue...")
                
            elif choice == "5":
                break
            else:
                print("Invalid choice. Please try again.")
                input("Press Enter to continue...")

    def manage_trip_assignments(self):
        """Manage traveller assignments to trips."""
        from data_manager import load_trips, load_travellers, assign_traveller_to_trip, remove_traveller_from_trip
        
        while True:
            self.clear_screen()
            self.display_header()
            print("=== MANAGE TRIP ASSIGNMENTS ===")
            
            trips = load_trips()
            travellers = load_travellers()
            current_user = self.auth_service.current_user
            
            # Filter trips based on user role
            if isinstance(current_user, TripCoordinator):
                user_trips = [t for t in trips if t.coordinator and t.coordinator.user_id == current_user.user_id]
            else:
                user_trips = trips
            
            if not user_trips:
                print("No trips available. Please create a trip first.")
                input("Press Enter to continue...")
                return
            
            print("\nSelect a trip to manage traveller assignments:")
            for i, trip in enumerate(user_trips, 1):
                assigned_count = len(trip.travellers)
                print(f"{i}. {trip.name} - {assigned_count} travellers assigned")
            
            print(f"{len(user_trips) + 1}. Back to Main Menu")
            
            try:
                choice = int(input("\nEnter your choice: "))
                if choice == len(user_trips) + 1:
                    break
                elif 1 <= choice <= len(user_trips):
                    selected_trip = user_trips[choice - 1]
                    self.manage_assignments_for_trip(selected_trip, travellers)
                else:
                    print("Invalid choice.")
                    input("Press Enter to continue...")
            except ValueError:
                print("Please enter a valid number.")
                input("Press Enter to continue...")

    def manage_assignments_for_trip(self, trip: Trip, all_travellers: list):
        """Manage assignments for a specific trip."""
        from data_manager import assign_traveller_to_trip, remove_traveller_from_trip
        
        while True:
            self.clear_screen()
            self.display_header()
            print(f"=== MANAGING ASSIGNMENTS FOR: {trip.name} ===")
            print(f"Trip ID: {trip.trip_id}")
            
            # Display currently assigned travellers
            print(f"\nCurrently assigned travellers ({len(trip.travellers)}):")
            if trip.travellers:
                for i, traveller in enumerate(trip.travellers, 1):
                    print(f"{i}. {traveller.name} (ID: {traveller.traveller_id})")
            else:
                print("No travellers assigned yet.")
            
            # Display available travellers
            available_travellers = [t for t in all_travellers if t not in trip.travellers]
            print(f"\nAvailable travellers ({len(available_travellers)}):")
            if available_travellers:
                for i, traveller in enumerate(available_travellers, 1):
                    print(f"{i}. {traveller.name} (ID: {traveller.traveller_id})")
            else:
                print("No available travellers.")
            
            print("\n1. Assign Traveller to Trip")
            print("2. Remove Traveller from Trip")
            print("3. Back to Trip Selection")
            
            choice = input("\nEnter your choice (1-3): ")
            
            if choice == "1":
                if not available_travellers:
                    print("No available travellers to assign.")
                    input("Press Enter to continue...")
                    continue
                    
                print("\nSelect traveller to assign:")
                for i, traveller in enumerate(available_travellers, 1):
                    print(f"{i}. {traveller.name} (ID: {traveller.traveller_id})")
                
                try:
                    traveller_choice = int(input("\nEnter traveller number: ")) - 1
                    if 0 <= traveller_choice < len(available_travellers):
                        traveller_to_assign = available_travellers[traveller_choice]
                        if assign_traveller_to_trip(trip.trip_id, traveller_to_assign.traveller_id):
                            print(f"Traveller '{traveller_to_assign.name}' assigned successfully!")
                            # Refresh the trip data
                            from data_manager import load_trips
                            trips = load_trips()
                            trip.travellers = next((t.travellers for t in trips if t.trip_id == trip.trip_id), [])
                        else:
                            print("Failed to assign traveller.")
                    else:
                        print("Invalid selection.")
                except ValueError:
                    print("Please enter a valid number.")
                
                input("Press Enter to continue...")
                
            elif choice == "2":
                if not trip.travellers:
                    print("No travellers assigned to remove.")
                    input("Press Enter to continue...")
                    continue
                    
                print("\nSelect traveller to remove:")
                for i, traveller in enumerate(trip.travellers, 1):
                    print(f"{i}. {traveller.name} (ID: {traveller.traveller_id})")
                
                try:
                    traveller_choice = int(input("\nEnter traveller number: ")) - 1
                    if 0 <= traveller_choice < len(trip.travellers):
                        traveller_to_remove = trip.travellers[traveller_choice]
                        if remove_traveller_from_trip(trip.trip_id, traveller_to_remove.traveller_id):
                            print(f"Traveller '{traveller_to_remove.name}' removed successfully!")
                            # Refresh the trip data
                            from data_manager import load_trips
                            trips = load_trips()
                            trip.travellers = next((t.travellers for t in trips if t.trip_id == trip.trip_id), [])
                        else:
                            print("Failed to remove traveller.")
                    else:
                        print("Invalid selection.")
                except ValueError:
                    print("Please enter a valid number.")
                
                input("Press Enter to continue...")
                
            elif choice == "3":
                break
            else:
                print("Invalid choice. Please try again.")
                input("Press Enter to continue...")

    def handle_payments(self):
        """Handle invoices and payments for trips."""
        from data_manager import load_trips, load_invoices, save_invoice, delete_invoice
        from models import Invoice, Payment
        from datetime import datetime
        
        while True:
            self.clear_screen()
            self.display_header()
            print("=== MANAGE INVOICES & PAYMENTS ===")
            
            trips = load_trips()
            invoices = load_invoices()
            current_user = self.auth_service.current_user
            
            # Filter trips based on user role
            if isinstance(current_user, TripCoordinator):
                user_trips = [t for t in trips if t.coordinator and t.coordinator.user_id == current_user.user_id]
            else:
                user_trips = trips
            
            # Filter invoices based on user role
            if isinstance(current_user, TripCoordinator):
                user_invoices = [inv for inv in invoices if inv.trip.coordinator and inv.trip.coordinator.user_id == current_user.user_id]
            else:
                user_invoices = invoices
            
            print(f"\nYour trips: {len(user_trips)}")
            print(f"Your invoices: {len(user_invoices)}")
            
            print("\n1. View All Invoices")
            print("2. Create Invoice for Trip")
            print("3. Record Payment")
            print("4. Delete Invoice")
            print("5. Back to Main Menu")
            
            choice = input("\nEnter your choice (1-5): ")
            
            if choice == "1":
                self.clear_screen()
                self.display_header()
                print("=== ALL INVOICES ===")
                if user_invoices:
                    for i, invoice in enumerate(user_invoices, 1):
                        print(f"{i}. {invoice}")
                        print(f"   Trip: {invoice.trip.name}")
                        print(f"   Issue Date: {invoice.issue_date.strftime('%Y-%m-%d')}")
                        if invoice.payments:
                            print(f"   Payments: {len(invoice.payments)}")
                            for payment in invoice.payments:
                                print(f"     - {payment}")
                        print()
                else:
                    print("No invoices found.")
                input("\nPress Enter to continue...")
                
            elif choice == "2":
                if not user_trips:
                    print("No trips available to invoice.")
                    input("Press Enter to continue...")
                    continue
                    
                self.clear_screen()
                self.display_header()
                print("=== CREATE INVOICE ===")
                print("Select a trip to invoice:")
                for i, trip in enumerate(user_trips, 1):
                    total_trip_cost = sum(leg.cost for leg in trip.trip_legs)
                    print(f"{i}. {trip.name} - Estimated cost: £{total_trip_cost:.2f}")
                
                try:
                    trip_choice = int(input("\nSelect trip (number): ")) - 1
                    if 0 <= trip_choice < len(user_trips):
                        selected_trip = user_trips[trip_choice]
                        
                        # Calculate total cost from trip legs
                        total_cost = sum(leg.cost for leg in selected_trip.trip_legs)
                        if total_cost == 0:
                            print("This trip has no costs associated. Please add trip legs with costs first.")
                            input("Press Enter to continue...")
                            continue
                        
                        invoice_id = f"INV{datetime.now().strftime('%Y%m%d%H%M%S')}"
                        
                        print(f"\nCreating invoice for: {selected_trip.name}")
                        print(f"Total trip cost: £{total_cost:.2f}")
                        
                        confirm = input(f"Create invoice for £{total_cost:.2f}? (y/n): ")
                        if confirm.lower() == 'y':
                            new_invoice = Invoice(
                                invoice_id=invoice_id,
                                trip=selected_trip,
                                issue_date=datetime.now(),
                                total_amount=total_cost
                            )
                            save_invoice(new_invoice)
                            print(f"Invoice {invoice_id} created successfully!")
                        else:
                            print("Invoice creation cancelled.")
                    else:
                        print("Invalid trip selection.")
                except ValueError:
                    print("Please enter a valid number.")
                
                input("Press Enter to continue...")
                
            elif choice == "3":
                if not user_invoices:
                    print("No invoices available for payment.")
                    input("Press Enter to continue...")
                    continue
                    
                # Filter to show only invoices with balance due
                unpaid_invoices = [inv for inv in user_invoices if not inv.is_fully_paid()]
                if not unpaid_invoices:
                    print("All invoices are fully paid!")
                    input("Press Enter to continue...")
                    continue
                    
                self.clear_screen()
                self.display_header()
                print("=== RECORD PAYMENT ===")
                print("Select invoice to record payment:")
                for i, invoice in enumerate(unpaid_invoices, 1):
                    balance = invoice.calculate_balance()
                    print(f"{i}. {invoice.trip.name} - Balance: £{balance:.2f}")
                
                try:
                    invoice_choice = int(input("\nSelect invoice (number): ")) - 1
                    if 0 <= invoice_choice < len(unpaid_invoices):
                        selected_invoice = unpaid_invoices[invoice_choice]
                        balance = selected_invoice.calculate_balance()
                        
                        print(f"\nInvoice: {selected_invoice.invoice_id}")
                        print(f"Trip: {selected_invoice.trip.name}")
                        print(f"Total Amount: £{selected_invoice.total_amount:.2f}")
                        print(f"Balance Due: £{balance:.2f}")
                        
                        amount = input(f"Payment amount (£): ") or str(balance)
                        method = input("Payment method (Cash/Card/Transfer): ") or "Cash"
                        
                        try:
                            payment_amount = float(amount)
                            if payment_amount > balance:
                                print(f"Warning: Payment amount exceeds balance. Recording £{balance:.2f} instead.")
                                payment_amount = balance
                            
                            selected_invoice.add_payment(payment_amount, datetime.now(), method)
                            save_invoice(selected_invoice)
                            
                            if selected_invoice.is_fully_paid():
                                selected_invoice.status = "Paid"
                                save_invoice(selected_invoice)
                                print("Invoice fully paid! Status updated to Paid.")
                            else:
                                print(f"Payment of £{payment_amount:.2f} recorded successfully.")
                                
                        except ValueError:
                            print("Invalid amount. Please enter a number.")
                    else:
                        print("Invalid invoice selection.")
                except ValueError:
                    print("Please enter a valid number.")
                
                input("Press Enter to continue...")
                
            elif choice == "4":
                if not user_invoices:
                    print("No invoices available to delete.")
                    input("Press Enter to continue...")
                    continue
                    
                self.clear_screen()
                self.display_header()
                print("=== DELETE INVOICE ===")
                for i, invoice in enumerate(user_invoices, 1):
                    print(f"{i}. {invoice}")
                
                try:
                    invoice_num = int(input("\nSelect invoice to delete (number): ")) - 1
                    if 0 <= invoice_num < len(user_invoices):
                        invoice = user_invoices[invoice_num]
                        confirm = input(f"Are you sure you want to PERMANENTLY delete invoice {invoice.invoice_id}? (y/n): ")
                        if confirm.lower() == 'y':
                            delete_invoice(invoice.invoice_id)
                            print("Invoice permanently deleted!")
                        else:
                            print("Deletion cancelled.")
                    else:
                        print("Invalid invoice selection.")
                except (ValueError, IndexError):
                    print("Invalid input.")
                
                input("Press Enter to continue...")
                
            elif choice == "5":
                break
            else:
                print("Invalid choice. Please try again.")
                input("Press Enter to continue...")

    def manage_travellers(self):
        """Manage travellers - view, add, delete."""
        from data_manager import load_travellers, save_traveller, delete_traveller
        
        while True:
            self.clear_screen()
            self.display_header()
            print("=== MANAGE TRAVELLERS ===")
            
            travellers = load_travellers()
            print(f"\nCurrent travellers in system: {len(travellers)}")
            
            print("\n1. View All Travellers")
            print("2. Add New Traveller")
            print("3. Delete Traveller")
            print("4. Back")
            
            choice = input("\nEnter your choice (1-4): ")
            
            if choice == "1":
                self.clear_screen()
                self.display_header()
                print("=== ALL TRAVELLERS ===")
                if travellers:
                    for i, traveller in enumerate(travellers, 1):
                        print(f"{i}. {traveller.name} (ID: {traveller.traveller_id})")
                        print(f"   Address: {traveller.address}")
                        print(f"   Date of Birth: {traveller.date_of_birth.strftime('%Y-%m-%d')}")
                        print(f"   Emergency Contact: {traveller.emergency_contact}")
                        print(f"   Government ID: {traveller.government_id}")
                        print()
                else:
                    print("No travellers found.")
                input("\nPress Enter to continue...")
                
            elif choice == "2":
                self.clear_screen()
                self.display_header()
                print("=== ADD NEW TRAVELLER ===")
                traveller_id = f"T{datetime.now().strftime('%Y%m%d%H%M%S')}"
                name = input("Full Name: ")
                address = input("Address: ")
                dob = input("Date of Birth (YYYY-MM-DD): ")
                emergency_contact = input("Emergency Contact: ")
                government_id = input("Government ID: ")
                
                try:
                    dob_date = datetime.strptime(dob, '%Y-%m-%d')
                    new_traveller = Traveller(
                        traveller_id=traveller_id,
                        name=name,
                        address=address,
                        date_of_birth=dob_date,
                        emergency_contact=emergency_contact,
                        government_id=government_id
                    )
                    save_traveller(new_traveller)
                    print(f"Traveller '{name}' added successfully with ID: {traveller_id}")
                except ValueError:
                    print("Invalid date format. Please use YYYY-MM-DD.")
                except Exception as e:
                    print(f"Error adding traveller: {e}")
                
                input("Press Enter to continue...")
                
            elif choice == "3":
                if not travellers:
                    print("No travellers available to delete.")
                    input("Press Enter to continue...")
                    continue
                    
                self.clear_screen()
                self.display_header()
                print("=== DELETE TRAVELLER ===")
                for i, traveller in enumerate(travellers, 1):
                    print(f"{i}. {traveller.name} (ID: {traveller.traveller_id})")
                
                try:
                    traveller_num = int(input("\nSelect traveller to delete (number): ")) - 1
                    if 0 <= traveller_num < len(travellers):
                        traveller = travellers[traveller_num]
                        confirm = input(f"Are you sure you want to PERMANENTLY delete '{traveller.name}'? This cannot be undone! (y/n): ")
                        if confirm.lower() == 'y':
                            delete_traveller(traveller.traveller_id)
                            print(f"Traveller '{traveller.name}' permanently deleted!")
                        else:
                            print("Deletion cancelled.")
                    else:
                        print("Invalid traveller selection.")
                except (ValueError, IndexError):
                    print("Invalid input.")
                
                input("Press Enter to continue...")
                
            elif choice == "4":
                break
            else:
                print("Invalid choice. Please try again.")
                input("Press Enter to continue...")

    def manage_trip_managers(self):
        """Allow Administrators to manage Trip Manager accounts."""
        from data_manager import load_users, create_trip_manager, delete_user
        from datetime import datetime
        
        while True:
            self.clear_screen()
            self.display_header()
            print("=== MANAGE TRIP MANAGERS ===")
            
            all_users = load_users()
            trip_managers = [user for user in all_users if isinstance(user, TripManager)]
            
            print(f"\nCurrent Trip Managers: {len(trip_managers)}")
            
            print("\n1. View All Trip Managers")
            print("2. Create New Trip Manager")
            print("3. Delete Trip Manager")
            print("4. Back to Admin Menu")
            
            choice = input("\nEnter your choice (1-4): ")
            
            if choice == "1":
                self.clear_screen()
                self.display_header()
                print("=== ALL TRIP MANAGERS ===")
                if trip_managers:
                    for i, manager in enumerate(trip_managers, 1):
                        print(f"{i}. {manager.name} (Username: {manager.username})")
                        print(f"   User ID: {manager.user_id}")
                        print()
                else:
                    print("No Trip Managers found.")
                input("\nPress Enter to continue...")
                
            elif choice == "2":
                self.clear_screen()
                self.display_header()
                print("=== CREATE NEW TRIP MANAGER ===")
                
                user_id = f"TM{datetime.now().strftime('%Y%m%d%H%M%S')}"
                username = input("Username: ")
                password = input("Password: ")
                name = input("Full Name: ")
                
                try:
                    if not username or not password or not name:
                        print("All fields are required.")
                    else:
                        new_manager = create_trip_manager(user_id, username, password, name)
                        print(f"Trip Manager '{name}' created successfully!")
                        print(f"Username: {username}, Password: {password}")
                except ValueError as e:
                    print(f"Error: {e}")
                except Exception as e:
                    print(f"Error creating Trip Manager: {e}")
                
                input("Press Enter to continue...")
                
            elif choice == "3":
                if not trip_managers:
                    print("No Trip Managers available to delete.")
                    input("Press Enter to continue...")
                    continue
                    
                self.clear_screen()
                self.display_header()
                print("=== DELETE TRIP MANAGER ===")
                for i, manager in enumerate(trip_managers, 1):
                    print(f"{i}. {manager.name} (Username: {manager.username})")
                
                try:
                    manager_num = int(input("\nSelect Trip Manager to delete (number): ")) - 1
                    if 0 <= manager_num < len(trip_managers):
                        manager = trip_managers[manager_num]
                        
                        # Prevent deleting yourself
                        if manager.user_id == self.auth_service.current_user.user_id:
                            print("You cannot delete your own account!")
                            input("Press Enter to continue...")
                            continue
                        
                        confirm = input(f"Are you sure you want to PERMANENTLY delete Trip Manager '{manager.name}'? (y/n): ")
                        if confirm.lower() == 'y':
                            delete_user(manager.user_id)
                            print(f"Trip Manager '{manager.name}' permanently deleted!")
                        else:
                            print("Deletion cancelled.")
                    else:
                        print("Invalid selection.")
                except (ValueError, IndexError):
                    print("Invalid input.")
                
                input("Press Enter to continue...")
                
            elif choice == "4":
                break
            else:
                print("Invalid choice. Please try again.")
                input("Press Enter to continue...")

    def manage_trip_coordinators(self):
        """Allow Trip Managers to manage Trip Coordinator accounts."""
        from data_manager import load_users, create_trip_coordinator, delete_user
        from datetime import datetime
        
        while True:
            self.clear_screen()
            self.display_header()
            print("=== MANAGE TRIP COORDINATORS ===")
            
            all_users = load_users()
            trip_coordinators = [user for user in all_users if isinstance(user, TripCoordinator)]
            
            print(f"\nCurrent Trip Coordinators: {len(trip_coordinators)}")
            
            print("\n1. View All Trip Coordinators")
            print("2. Create New Trip Coordinator")
            print("3. Delete Trip Coordinator")
            print("4. Back to Manager Menu")
            
            choice = input("\nEnter your choice (1-4): ")
            
            if choice == "1":
                self.clear_screen()
                self.display_header()
                print("=== ALL TRIP COORDINATORS ===")
                if trip_coordinators:
                    for i, coordinator in enumerate(trip_coordinators, 1):
                        print(f"{i}. {coordinator.name} (Username: {coordinator.username})")
                        print(f"   User ID: {coordinator.user_id}")
                        print()
                else:
                    print("No Trip Coordinators found.")
                input("\nPress Enter to continue...")
                
            elif choice == "2":
                self.clear_screen()
                self.display_header()
                print("=== CREATE NEW TRIP COORDINATOR ===")
                
                user_id = f"TC{datetime.now().strftime('%Y%m%d%H%M%S')}"
                username = input("Username: ")
                password = input("Password: ")
                name = input("Full Name: ")
                
                try:
                    if not username or not password or not name:
                        print("All fields are required.")
                    else:
                        new_coordinator = create_trip_coordinator(user_id, username, password, name)
                        print(f"Trip Coordinator '{name}' created successfully!")
                        print(f"Username: {username}, Password: {password}")
                except ValueError as e:
                    print(f"Error: {e}")
                except Exception as e:
                    print(f"Error creating Trip Coordinator: {e}")
                
                input("Press Enter to continue...")
                
            elif choice == "3":
                if not trip_coordinators:
                    print("No Trip Coordinators available to delete.")
                    input("Press Enter to continue...")
                    continue
                    
                self.clear_screen()
                self.display_header()
                print("=== DELETE TRIP COORDINATOR ===")
                for i, coordinator in enumerate(trip_coordinators, 1):
                    print(f"{i}. {coordinator.name} (Username: {coordinator.username})")
                
                try:
                    coordinator_num = int(input("\nSelect Trip Coordinator to delete (number): ")) - 1
                    if 0 <= coordinator_num < len(trip_coordinators):
                        coordinator = trip_coordinators[coordinator_num]
                        confirm = input(f"Are you sure you want to PERMANENTLY delete Trip Coordinator '{coordinator.name}'? (y/n): ")
                        if confirm.lower() == 'y':
                            delete_user(coordinator.user_id)
                            print(f"Trip Coordinator '{coordinator.name}' permanently deleted!")
                        else:
                            print("Deletion cancelled.")
                    else:
                        print("Invalid selection.")
                except (ValueError, IndexError):
                    print("Invalid input.")
                
                input("Press Enter to continue...")
                
            elif choice == "4":
                break
            else:
                print("Invalid choice. Please try again.")
                input("Press Enter to continue...")

    def view_all_invoices(self):
        """Allow Administrators to view all invoices in the system."""
        from data_manager import load_invoices
        
        self.clear_screen()
        self.display_header()
        print("=== ALL SYSTEM INVOICES ===")
        
        invoices = load_invoices()
        
        if invoices:
            total_invoices = len(invoices)
            total_value = sum(invoice.total_amount for invoice in invoices)
            paid_invoices = len([inv for inv in invoices if inv.is_fully_paid()])
            pending_invoices = total_invoices - paid_invoices
            
            print(f"Summary: {total_invoices} invoices, Total Value: £{total_value:.2f}")
            print(f"Paid: {paid_invoices}, Pending: {pending_invoices}")
            print("-" * 50)
            
            for i, invoice in enumerate(invoices, 1):
                status = "PAID" if invoice.is_fully_paid() else "PENDING"
                balance = invoice.calculate_balance()
                print(f"{i}. {invoice.trip.name} - £{invoice.total_amount:.2f} ({status})")
                print(f"   Coordinator: {invoice.trip.coordinator.name if invoice.trip.coordinator else 'Unassigned'}")
                print(f"   Balance: £{balance:.2f}, Invoice ID: {invoice.invoice_id}")
                print()
        else:
            print("No invoices found in the system.")
        
        input("\nPress Enter to continue...")

    def generate_total_invoice(self):
        print("\n--- Generate Total Invoice ---")
        print("To be added.")
        input("Press Enter to continue...")

    def generate_reports(self):
        print("\n--- Generate Reports ---")
        print("To be added.")
        input("Press Enter to continue...")

    def generate_itinerary(self):
        print("\n--- Generate Itinerary ---")
        print("To be added.")
        input("Press Enter to continue...")

if __name__ == "__main__":
    app = TravelManagementSystem()
    app.main_menu()
    print("\nThank you for using Solent Trips Travel Management System!")