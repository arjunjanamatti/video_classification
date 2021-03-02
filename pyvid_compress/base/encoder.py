from abc import ABC, abstractmethod
from base.config import Config
from base.tdv import Tdv
from base.util import file_to_tensor
import tensorly as tl
tl.set_backend('pytorch')


class Encoder(ABC):
    def __init__(self, config: Config) -> None:
        super().__init__()
        self.config = config

    @abstractmethod
    def encode_tensor(self, tensor) -> Tdv:
        pass

    def encode_file(self, src_file) -> Tdv:
        tensor, fps = file_to_tensor(src_file)
        return self.encode_tensor(tensor)
