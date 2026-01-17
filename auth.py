# FILE: auth.py
# Handles user authentication and session management.

import hashlib

class AuthenticationService:
    def __init__(self):
        from data_manager import load_users
        self.users = load_users()
        self.current_user = None
    
    def _hash_password(self, password: str) -> str:
        """Hash a password for storage."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def login(self, username: str, password: str):
        """Attempt to log in with username and password."""
        for user in self.users:
            if user.username == username:
                # Compare hashed passwords
                hashed_input = self._hash_password(password)
                if user.password == hashed_input:
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
    import hashlib
    
    users = load_users()
    print(f"DEBUG: Checking for existing admins in {len(users)} users")
    
    # Check if any user has the Administrator role
    admin_exists = any(hasattr(user, 'role') and getattr(user.role, 'value', None) == "Administrator" for user in users)
    
    if not admin_exists:
        print("DEBUG: Creating default admin...")
        # Hash the default password
        hashed_password = hashlib.sha256("admin123".encode()).hexdigest()
        
        default_admin = Administrator(
            user_id="admin001",
            username="admin",
            password=hashed_password,
            name="System Administrator"
        )
        save_user(default_admin)
        print("Default admin created. Username: 'admin', Password: 'admin123'")
    else:
        print("Default admin already exists.")

# Run this function when the auth module is loaded
create_default_admin()
print("Authentication module loaded successfully.")