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
            
            choice = input("\nEnter your choice (1-5): ")
            
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
                self.trip_coordinator_menu()  # Access coordinator functions
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
            print("4. Generate Itinerary")
            print("5. Handle Payments")
            print("6. Back to Previous Menu")
            print("7. Logout")
            print("8. Exit System")
            
            choice = input("\nEnter your choice (1-8): ")
            
            if choice == "1":
                self.manage_trips()
            elif choice == "2":
                self.manage_travellers()
            elif choice == "3":
                self.manage_trip_legs()
            elif choice == "4":
                self.generate_itinerary()
            elif choice == "5":
                self.handle_payments()
            elif choice == "6":
                break  # Go back to previous menu
            elif choice == "7":
                self.auth_service.logout()
                print("Logged out successfully.")
                input("Press Enter to continue...")
                break
            elif choice == "8":
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
                    
                    # For coordinators, they are automatically assigned as coordinator
                    # For managers/admins, they could choose a coordinator
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
                            # HARD DELETE - permanently remove the trip
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

    # PLACEHOLDER METHODS - We will implement these in the next steps
    def manage_trip_managers(self):
        print("\n--- Manage Trip Managers ---")
        print("This feature will be implemented in the next phase.")
        input("Press Enter to continue...")

    def view_all_invoices(self):
        print("\n--- View All Invoices ---")
        print("This feature will be implemented in the next phase.")
        input("Press Enter to continue...")

    def generate_reports(self):
        print("\n--- Generate Reports ---")
        print("This feature will be implemented in the next phase.")
        input("Press Enter to continue...")

    def manage_trip_coordinators(self):
        print("\n--- Manage Trip Coordinators ---")
        print("This feature will be implemented in the next phase.")
        input("Press Enter to continue...")

    def generate_total_invoice(self):
        print("\n--- Generate Total Invoice ---")
        print("This feature will be implemented in the next phase.")
        input("Press Enter to continue...")

    def manage_travellers(self):
        print("\n--- Manage Travellers ---")
        # Let's implement a basic version of this to test our system
        travellers = load_travellers()
        print(f"\nCurrent travellers in system: {len(travellers)}")
        
        print("\n1. View All Travellers")
        print("2. Add New Traveller")
        print("3. Back")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == "1":
            if travellers:
                for traveller in travellers:
                    print(f"- {traveller.name} (ID: {traveller.traveller_id})")
            else:
                print("No travellers found.")
            input("\nPress Enter to continue...")
            
        elif choice == "2":
            print("\n--- Add New Traveller ---")
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
                print(f"Traveller '{name}' added successfully!")
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")
            except Exception as e:
                print(f"Error adding traveller: {e}")
            
            input("Press Enter to continue...")

    def manage_trip_legs(self):
        print("\n--- Manage Trip Legs ---")
        print("This feature will be implemented in the next phase.")
        input("Press Enter to continue...")

    def generate_itinerary(self):
        print("\n--- Generate Itinerary ---")
        print("This feature will be implemented in the next phase.")
        input("Press Enter to continue...")

    def handle_payments(self):
        print("\n--- Handle Payments ---")
        print("This feature will be implemented in the next phase.")
        input("Press Enter to continue...")

if __name__ == "__main__":
    app = TravelManagementSystem()
    app.main_menu()
    print("\nThank you for using Solent Trips Travel Management System!")