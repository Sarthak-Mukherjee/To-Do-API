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

def verify_password(plain_password: str, hashed_password: str) -> bool:
    
    """ Verify a plain password against its hashed version and returns True if they match, else False. """

    return pwd_context.verify(plain_password, hashed_password)
