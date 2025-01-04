from .field import Field
class Name(Field):
    def __init__(self, value):
        super().__init__(value)

    def get_value(self):
        return self.value