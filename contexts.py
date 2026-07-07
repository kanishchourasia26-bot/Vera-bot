from dataclasses import dataclass
from typing import Dict, List, Any, Optional


@dataclass
class CategoryContext:
    slug: str


@dataclass
class MerchantContext:
    identity: Dict[str, Any]
    performance: Dict[str, Any]
    offers: List[Dict[str, Any]]
    signals: List[str]
    conversation_history: List[Dict[str, Any]]


@dataclass
class TriggerContext:
    kind: str
    suppression_key: str


@dataclass
class CustomerContext:
    identity: Dict[str, Any]
    relationship: Dict[str, Any]