from uuid import UUID


class DocumentId:
    """Value object para ID de documento."""

    def __init__(self, value: UUID):
        self._value = value

    @property
    def value(self) -> UUID:
        return self._value

    def __eq__(self, other) -> bool:
        if not isinstance(other, DocumentId):
            return False
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)

    def __str__(self) -> str:
        return str(self.value)