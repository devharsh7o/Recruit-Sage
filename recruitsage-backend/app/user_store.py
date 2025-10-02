from typing import Dict, Any
from threading import RLock

_users: Dict[str, Dict[str, Any]] = {}
_lock = RLock()

def create_user(email: str, data: Dict[str, Any]) -> None:
    with _lock:
        _users[email.lower()] = data

def get_user(email: str) -> Dict[str, Any] | None:
    with _lock:
        return _users.get(email.lower())
