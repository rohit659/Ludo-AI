from abc import ABCMeta, abstractmethod
class Strategy(metaclass=ABCMeta):
    def __init__(self,name):
        self.strategy = name
    @abstractmethod
    def getCoinToMove(self,idx,colors,face):
        pass






