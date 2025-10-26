from passlib.context import CryptContext

# Initialize bcrypt hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    """
    Safely hash a plain password using bcrypt.
    Ensures valid string input, trims spaces, and limits length to 72 bytes.
    """
    if not password:
        raise ValueError("Password cannot be empty")

    # Ensure it's a string (not bytes, int, etc.)
    if isinstance(password, bytes):
        password = password.decode("utf-8")

    # Trim extra spaces and truncate if longer than 72 characters
    password = str(password).strip()[:72]

    # Return the hashed password
    return pwd_context.hash(password)
