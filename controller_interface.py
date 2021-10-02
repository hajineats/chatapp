from abc import abstractmethod

class ControllerBase():
    @abstractmethod
    def changePageTo(self,index):
        pass
    @abstractmethod
    def exitTheApp(self):
        pass

    @abstractmethod
    def setup_signal_handler(self, worker):
        pass