from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

#  WHY BCRYPT OVER MD5 / SHA-256? -- BY BALAJI A
# A modern GPU can compute BILLIONS of MD5 hashes per second.
# If a hacker steals your database, they can crack all passwords quickly.
# bcrypt is intentionally SLOW — each hash takes ~100ms on purpose.
# 1 million password guesses = over 27 hours with bcrypt.
# bcrypt also auto-adds a random "salt" per hash, blocking
# rainbow table attacks (pre-computed lookup tables).
#
# Rule: bcrypt/argon2/scrypt for PASSWORDS
#       SHA-256 for checksums and file integrity only

SECRET_KEY = "change-this-in-production-use-a-random-256-bit-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login/")


def get_password_hash(password: str) -> str:
    """Hash plain-text password with bcrypt. NEVER store plain text."""
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    """Check if plain password matches the stored bcrypt hash."""
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict) -> str:
    """Create a signed JWT that expires in 30 minutes."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    # IMPORTANT: JWT payload is base64-encoded, NOT encrypted!
    # Anyone can decode it. NEVER put passwords or card numbers in JWT.
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str):
    """Decode and validate JWT. Returns payload dict or None if invalid/expired."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None