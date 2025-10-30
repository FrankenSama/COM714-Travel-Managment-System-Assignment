# FILE: auth.py
# Handles user authentication and session management.

# Import the specific classes we need directly from models
from models import User, TripCoordinator, TripManager, Administrator

class AuthenticationService:
    def __init__(self):
        # We'll import load_users inside the method to avoid circular imports
        from data_manager import load_users
        self.users = load_users()
        self.current_user = None

    def login(self, username: str, password: str):
        """
        Attempts to log in a user.
        Returns (success, message, user_object)
        """
        for user in self.users:
            if user.username == username:
                if user.password == password:  # In a real system, compare hashed passwords
                    self.current_user = user
                    return True, f"Login successful! Welcome, {user.name}.", user
                else:
                    return False, "Incorrect password.", None
        return False, "Username not found.", None

    def logout(self):
        """Logs out the current user."""
        self.current_user = None

    def get_current_user(self):
        """Returns the currently logged-in user, or None."""
        return self.current_user

def create_default_admin():
    """Create a default administrator for initial testing."""
    # Import inside function to avoid circular imports
    from data_manager import load_users, save_user
    
    users = load_users()
    admin_exists = any(user.role.value == "Administrator" for user in users)
    
    if not admin_exists:
        default_admin = Administrator(
            user_id="admin001",
            username="admin",
            password="admin123",  # Change this in a real system!
            name="System Administrator"
        )
        save_user(default_admin)
        print("Default admin created. Username: 'admin', Password: 'admin123'")
    else:
        print("Default admin already exists.")

# Run this function when the auth module is loaded
create_default_admin()
print("Authentication module loaded successfully.")