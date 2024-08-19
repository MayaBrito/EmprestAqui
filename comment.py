class Comment:
    def __init__(self, id: int, comment: str, score: float):
        self._comment = comment
        self._score = score
        self._id = id

    @property
    def comment(self) -> str:
        """get comment content"""
        return self._comment

    @property
    def score(self) -> float:
        """get comment score"""
        return self._score

    @property
    def id(self) -> int:
        """get id"""
        return self._id

    def to_dict(self) -> dict[str, any]:
        """parse object to dict"""
        return {
            "id": self._id,
            "comment": self._comment,
            "score": self._score
        }
