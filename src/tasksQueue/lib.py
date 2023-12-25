

class Lib:
    def __init__(self) -> None:
        super().__init__()
        self.name = None
        self.version = None
        self.fullname = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Lib, cls).__new__(cls)
        return cls.instance


lib = Lib()

