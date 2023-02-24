from abc import ABC, abstractmethod


class DatabaseOperations(ABC):

    @abstractmethod
    def updateDb(self):
        pass

