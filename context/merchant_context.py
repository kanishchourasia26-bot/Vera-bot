from dataclasses import dataclass, field


@dataclass
class MerchantContext:
    identity: dict
    performance: dict
    offers: list
    signals: list
    conversation_history: list
    customer_aggregate: dict = field(default_factory=dict)

    @classmethod
    def from_request(cls, merchant):
        return cls(
            identity=merchant.identity,
            performance=merchant.performance,
            offers=merchant.offers,
            signals=merchant.signals,
            conversation_history=merchant.conversation_history,
            customer_aggregate=merchant.customer_aggregate
        )