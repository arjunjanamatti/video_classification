from abc import ABC, abstractmethod
from base.config import Config
from base.tdv import Tdv
import tensorly as tl
import numpy as np
import skvideo.io


def to_image(tensor):
    """A convenience function to convert from a float dtype back to uint8"""
    im = tl.to_numpy(tensor)
    im -= im.min()
    im /= im.max()
    im *= 255
    return im.astype(np.uint8)


class Decoder(ABC):
    def __init__(self, config: Config) -> None:
        super().__init__()
        self.config = config

    @abstractmethod
    def decode_to_tensor(self, tdv: Tdv):
        """
        returns the tensor correspoding to the tdv
        """
        pass

    def decode_to_file(self, tdv: Tdv, out_file: str):
        tensr = self.decode_to_tensor(tdv)
        skvideo.io.vwrite(out_file, tensr.cpu())
