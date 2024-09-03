class Request:
    def __init__(self, id: int, state: str, item_id: int, interested_id: int, supplier_id: int):
        self._id = id
        self._state = state
        self._item_id = item_id
        self._interested_id = interested_id
        self._supplier_id = supplier_id

    @property
    def state(self) -> str:
        """get state"""
        return self._state

    @property
    def item_id(self) -> int:
        """get item id"""
        return self._item_id

    @property
    def interested_id(self) -> int:
        """get interested id"""
        return self._interested_id

    @property
    def supplier_id(self) -> int:
        """get supplier id"""
        return self._supplier_id

    @state.setter
    def state(self, value: str) -> str:
        """set state"""
        self._state = value

    def to_dict(self) -> dict[str, any]:
        """parse object to dict"""
        return {
            "id": self._id,
            "state": self._state,
            "item_id": self._item_id,
            "interested_id": self._interested_id,
            "supplier_id": self._supplier_id,
        }
