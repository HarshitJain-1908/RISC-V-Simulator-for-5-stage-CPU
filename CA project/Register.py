class Register:
    
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def setValue(self, value):
        self.value = value

    def getValue(self):
        return self.value