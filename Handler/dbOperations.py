from abc import ABC, abstractmethod


class DatabaseOperations(ABC):

    @abstractmethod
    def updateDb(self, identity: int) -> None:
        pass

    @abstractmethod
    def executeQuery(self, query: str) -> None:
        pass
