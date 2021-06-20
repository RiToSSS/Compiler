from abc import ABC, abstractmethod

class Node(ABC):
    @abstractmethod
    def print(self):
        pass
    @abstractmethod
    def get_value(self):
        pass