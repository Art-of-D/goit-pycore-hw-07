from .field import Field
class Phone(Field):
    
    def __init__(self, value):
        self.validation(value)
        super().__init__(value)
    
    def validation(self, value):
        try:
            int(value)
        except ValueError:
            raise ValueError("Phone number must contain only digits.")
        if len(value) != 10:
            raise ValueError("Phone number must be 10 digits long.")
        
    def get_value(self):
        return self.value
