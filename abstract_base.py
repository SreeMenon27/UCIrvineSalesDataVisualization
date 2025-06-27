from abc import ABC, abstractmethod

## Abstract class
class BaseAnalysis(ABC):
    @abstractmethod
    def run_analysis(self):
        pass
