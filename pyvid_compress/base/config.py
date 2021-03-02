class Config:
    def __init__(self) -> None:
        super().__init__()
        self.device = "cpu"
        self.conf = {}

    def set(self, setting, value):
        self.conf[setting] = value

    def has(self, setting):
        return setting in self.conf

    def get(self, setting):
        return self.conf[setting]

    def use_device(self, device):
        self.device = device
