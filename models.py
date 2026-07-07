from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class Category(BaseModel):
    slug: str = ""
    voice: Dict[str, Any] = {}
class Merchant(BaseModel):
    identity: Dict[str, Any] = {}
    performance: Dict[str, Any] = {}
    offers: List[Dict[str, Any]] = []
    signals: List[str] = []
    conversation_history: List[Dict[str, Any]] = []
    customer_aggregate: Dict[str, Any] = {}

    subscription: Dict[str, Any] = {}
class Trigger(BaseModel):
    kind: str
    urgency: int = 1
    suppression_key: str = ""
    payload: Dict[str, Any] = {}

    source: str = ""
    scope: str = ""

class Customer(BaseModel):
    identity: Dict[str, Any] = {}
    relationship: Dict[str, Any] = {}
    preferences: Dict[str, Any] = {}
    consent: Dict[str, Any] = {}

class ReplyRequest(BaseModel):
    category: Category
    merchant: Merchant
    trigger: Trigger
    customer: Optional[Customer] = None


class ReplyResponse(BaseModel):
    body: str
    cta: str
    send_as: str
    suppression_key: str
    rationale: str