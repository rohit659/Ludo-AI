from abc import ABCMeta, abstractmethod
class Strategy(metaclass=ABCMeta):
    def __init__(self):
        pass
    @abstractmethod
    def move(self):
        pass






