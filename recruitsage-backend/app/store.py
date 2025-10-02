from typing import Dict, Any
from threading import RLock

_store: Dict[str, Dict[str, Any]] = {}
_lock = RLock()

def save_resume(resume_id: str, data: Dict[str, Any]) -> None:
    with _lock:
        _store[resume_id] = data

def get_resume(resume_id: str) -> Dict[str, Any] | None:
    with _lock:
        return _store.get(resume_id)
