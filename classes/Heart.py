

class Heart:
    def __init__(self, source):
        self.rate = source.get("value")
        self.unit = source.get("unit")
        self.source = source.get("source")
        self.date = source.get("timestamp")

    