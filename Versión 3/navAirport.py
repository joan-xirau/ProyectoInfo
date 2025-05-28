class NavAirport:
    def __init__(self, name):
        self.name = name
        self.sids = []
        self.stars = []
    
    def add_sid(self, navpoint):
        self.sids.append(navpoint)
    
    def add_star(self, navpoint):
        self.stars.append(navpoint)
    
    def __str__(self):
        return f"NavAirport({self.name}, SIDs: {[p.name for p in self.sids]}, STARs: {[p.name for p in self.stars]})"