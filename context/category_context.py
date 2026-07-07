from dataclasses import dataclass


@dataclass
class CategoryContext:
    slug: str
    voice: str = "professional"

    @classmethod
    def from_request(cls, category):
        return cls(
            slug=category.slug,
            voice=category.voice or "professional"
        )