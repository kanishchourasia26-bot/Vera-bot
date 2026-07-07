from dataclasses import dataclass


@dataclass
class TriggerContext:
    kind: str
    urgency: int
    suppression_key: str
    payload: dict

    @classmethod
    def from_request(cls, trigger):
        return cls(
            kind=trigger.kind,
            urgency=trigger.urgency,
            suppression_key=trigger.suppression_key,
            payload=trigger.payload
        )