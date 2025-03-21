from abc import ABC, abstractmethod

class Schema(ABC):
    @abstractmethod
    def request(self):
        pass
    
    @abstractmethod
    def response(self):
        pass

    @abstractmethod
    def error(self):
        pass
    