from base.decoder import Decoder
from base.encoder import Encoder
from base.config import Config
from base.tdv import Tdv
from tensorly.decomposition import tucker
import tensorly as tl
import cloudpickle


class TuckerTdv(Tdv):
    def __init__(self, core, factors) -> None:
        super().__init__()
        self.core = core
        self.factors = factors

    def persist(self, file_path):
        with open(file_path, "wb") as f:
            cloudpickle.dump(self, f)


class TuckerEncoder(Encoder):

    def __init__(self, config: Config) -> None:
        super().__init__(config)

    def encode_tensor(self, tensor) -> TuckerTdv:
        if not self.config.has("ranks"):
            raise Exception("Property `ranks` should be set to the config")
        tensor = tl.tensor(tensor.astype(float), device=self.config.device)
        core, factors = tucker(tensor, ranks=self.config.get("ranks"))
        return TuckerTdv(core, factors)


class TuckerDecoder(Decoder):
    def decode_to_tensor(self, tdv: TuckerTdv):
        """
        returns the tensor correspoding to the tdv
        """
        return tl.tucker_to_tensor((tdv.core, tdv.factors))
