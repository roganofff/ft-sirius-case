from jose import jwt, JWTError
from datetime import datetime, timedelta
from app.config import EMAIL_SECRET_KEY

ALGORITHM = "HS256"

def generate_email_token(email: str) -> str:
    expire = datetime.utcnow() + timedelta(hours=2)
    to_encode = {"sub": email, "exp": expire}
    return jwt.encode(to_encode, EMAIL_SECRET_KEY, algorithm=ALGORITHM)

def verify_email_token(token: str) -> str:
    try:
        payload = jwt.decode(token, EMAIL_SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None
