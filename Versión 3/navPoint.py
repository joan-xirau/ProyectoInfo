class NavPoint:
    def __init__(self, number, name, latitude, longitude):
        self.number = number
        self.name = name
        self.latitude = float(latitude)
        self.longitude = float(longitude)
    
    def __str__(self):
        return f"NavPoint({self.number}, {self.name}, {self.latitude}, {self.longitude})"