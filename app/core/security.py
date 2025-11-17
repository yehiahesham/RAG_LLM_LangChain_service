from fastapi import HTTPException, status


def get_current_user():
    return {"user_id": 1, "email": "demo@my_company.ai"}


def ensure_authenticated():
    user = get_current_user()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthenticated")
    return user