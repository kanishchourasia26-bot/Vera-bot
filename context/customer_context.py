from dataclasses import dataclass


@dataclass
class CustomerContext:
    identity: dict
    relationship: dict
    preferences: dict

    @classmethod
    def from_request(cls, customer):

        if customer is None:
            return None

        return cls(
            identity=customer.identity,
            relationship=customer.relationship,
            preferences=customer.preferences
        )