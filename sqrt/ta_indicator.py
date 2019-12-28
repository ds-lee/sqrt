import pandas as pd
from abc import *

class TAIndicator(metaclass=ABCMeta):

    def __init__(self):
        pass

    @abstractmethod
    def signal(self) -> pd.DataFrame:
        raise NotImplementedError()
