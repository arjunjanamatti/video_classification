from base.decoder import Decoder
from base.encoder import Encoder
from base.config import Config
from base.tdv import Tdv
from tensorly.decomposition import parafac
import tensorly as tl
import cloudpickle


class CPTdv(Tdv):
    def __init__(self, factors) -> None:
        super().__init__()
        self.factors = factors

    def persist(self, file_path):
        with open(file_path, "wb") as f:
            cloudpickle.dump(self, f)


class CPEncoder(Encoder):

    def __init__(self, config: Config) -> None:
        super().__init__(config)

    def encode_tensor(self, tensor) -> CPTdv:
        if not self.config.has("rank"):
            raise Exception("Property `rank` should be set to the config")
        tensor = tl.tensor(tensor.astype(float), device=self.config.device)
        factors = parafac(tensor, rank=self.config.get("rank"))
        return CPTdv(factors)


class CPDecoder(Decoder):
    def decode_to_tensor(self, tdv: CPTdv):
        """
        returns the tensor correspoding to the tdv
        """
        return tl.cp_to_tensor(tdv.factors)
