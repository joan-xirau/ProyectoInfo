from navPoint import NavPoint
from navSegment import NavSegment
from navAirport import NavAirport

class AirSpace:
    def __init__(self):
        self.navpoints = []
        self.navsegments = []
        self.navairports = []
    
    def load_from_files(self, nav_file, seg_file, aer_file):
        # Load navigation points
        with open(nav_file, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 4:
                    number = parts[0]
                    name = parts[1]
                    lat = parts[2]
                    lon = parts[3]
                    self.navpoints.append(NavPoint(number, name, lat, lon))
        
        # Load segments
        with open(seg_file, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 3:
                    origin = parts[0]
                    dest = parts[1]
                    dist = parts[2]
                    self.navsegments.append(NavSegment(origin, dest, dist))
        
        # Load airports
        current_airport = None
        with open(aer_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line:  # Skip empty lines
                    if line.startswith(('LE', 'GC', 'EH')):  # Airport codes
                        if current_airport:
                            self.navairports.append(current_airport)
                        current_airport = NavAirport(line)
                    else:  # SID or STAR
                        parts = line.split('.')
                        if len(parts) > 1:
                            point_name = line
                            # Find the navpoint with this name
                            for np in self.navpoints:
                                if np.name == point_name:
                                    if parts[1] == 'D':  # SID
                                        current_airport.add_sid(np)
                                    elif parts[1] == 'A':  # STAR
                                        current_airport.add_star(np)
                                    break
            if current_airport:
                self.navairports.append(current_airport)
    
    def find_navpoint_by_name(self, name):
        for np in self.navpoints:
            if np.name == name:
                return np
        return None
    
    def find_navpoint_by_number(self, number):
        for np in self.navpoints:
            if np.number == number:
                return np
        return None
    
    def get_segments_from(self, origin_number):
        return [seg for seg in self.navsegments if seg.origin_number == origin_number]
    
    def get_segments_to(self, dest_number):
        return [seg for seg in self.navsegments if seg.destination_number == dest_number]
    
    def get_airport(self, name):
        for airport in self.navairports:
            if airport.name == name:
                return airport
        return None
    
    def __str__(self):
        return f"AirSpace with {len(self.navpoints)} points, {len(self.navsegments)} segments, {len(self.navairports)} airports"