# FILE: auth.py (UPDATED VERSION)
# Handles user authentication and session management.

class AuthenticationService:
    def __init__(self):
        from data_manager import load_users
        self.users = load_users()
        self.current_user = None
        print(f"DEBUG: Loaded {len(self.users)} users")  # Debug line

    def login(self, username: str, password: str):
        """
        Attempts to log in a user.
        Returns (success, message, user_object)
        """
        print(f"DEBUG: Attempting login for username: {username}")  # Debug line
        print(f"DEBUG: Available users: {[user.username for user in self.users]}")  # Debug line
        
        for user in self.users:
            print(f"DEBUG: Checking user: {user.username}")  # Debug line
            if user.username == username:
                if user.password == password:
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
    from data_manager import load_users, save_user
    from models import Administrator
    
    users = load_users()
    print(f"DEBUG: Checking for existing admins in {len(users)} users")  # Debug line
    
    # Check if any user has the Administrator role
    admin_exists = any(hasattr(user, 'role') and getattr(user.role, 'value', None) == "Administrator" for user in users)
    
    if not admin_exists:
        print("DEBUG: Creating default admin...")  # Debug line
        default_admin = Administrator(
            user_id="admin001",
            username="admin",
            password="admin123",
            name="System Administrator"
        )
        save_user(default_admin)
        print("Default admin created. Username: 'admin', Password: 'admin123'")
    else:
        print("Default admin already exists.")

# Run this function when the auth module is loaded
create_default_admin()
print("Authentication module loaded successfully.")