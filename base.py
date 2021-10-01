from abc import abstractmethod

class ControllerBase():
    @abstractmethod
    def changePageTo(self,index):
        pass
    @abstractmethod
    def exitTheApp(self):
        pass