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
    
    def generate_kml(self, output_file="airspace.kml"):

        """Genera un archivo KML para visualizar en Google Earth"""
        kml_header = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
    <name>Airspace Navigation</name>
    <description>Navigation points, segments and airports</description>
    <Style id="yellowLineGreenPoly">
        <LineStyle>
            <color>7f00ffff</color>
            <width>2</width>
        </LineStyle>
        <PolyStyle>
            <color>7f00ff00</color>
        </PolyStyle>
    </Style>
    <Style id="navPointStyle">
        <IconStyle>
            <Icon>
                <href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png</href>
            </Icon>
            <scale>0.8</scale>
        </IconStyle>
    </Style>
    <Style id="airportStyle">
        <IconStyle>
            <Icon>
                <href>http://maps.google.com/mapfiles/kml/shapes/airports.png</href>
            </Icon>
            <scale>1.2</scale>
        </IconStyle>
    </Style>"""
        
        kml_footer = "</Document>\n</kml>"
        
        # Generar contenido para puntos de navegación
        navpoints_content = ""
        for np in self.navpoints:
            navpoints_content += f"""
    <Placemark>
        <name></name>
        <description>NavPoint {np.number}</description>
        <styleUrl>#navPointStyle</styleUrl>
        <Point>
            <coordinates>{np.longitude},{np.latitude},0</coordinates>
        </Point>
    </Placemark>"""
        
        # Generar contenido para segmentos
        segments_content = ""
        for seg in self.navsegments:
            origin = self.find_navpoint_by_number(seg.origin_number)
            dest = self.find_navpoint_by_number(seg.destination_number)
            if origin and dest:
                segments_content += f"""
    <Placemark>
        <name></name>
        <description>Distance: {seg.distance} km</description>
        <styleUrl>#yellowLineGreenPoly</styleUrl>
        <LineString>
            <tessellate>1</tessellate>
            <coordinates>
                {origin.longitude},{origin.latitude},0
                {dest.longitude},{dest.latitude},0
            </coordinates>
        </LineString>
    </Placemark>"""
        
        # Generar contenido para aeropuertos
        airports_content = ""
        for airport in self.navairports:
            # Buscar un punto de referencia para el aeropuerto (usamos el primer SID o STAR si existe)
            ref_point = None
            if airport.sids:
                ref_point = airport.sids[0]
            elif airport.stars:
                ref_point = airport.stars[0]
            
            if ref_point:
                lon = ref_point.longitude
                lat = ref_point.latitude
            else:
                # Si no hay puntos de referencia, buscar cualquier punto de navegación con nombre similar
                for np in self.navpoints:
                    if airport.name in np.name:
                        lon = np.longitude
                        lat = np.latitude
                        break
                else:
                    # Si no encontramos nada, usar coordenadas por defecto (centro de España)
                    lon = -3.703790
                    lat = 40.416775
                
            airports_content += f"""
    <Placemark>
        <name>{airport.name}</name>
        <description>Airport with {len(airport.sids)} SIDs and {len(airport.stars)} STARs</description>
        <styleUrl>#airportStyle</styleUrl>
        <Point>
            <coordinates>{lon},{lat},0</coordinates>
        </Point>
    </Placemark>"""
        
        # Escribir el archivo KML
        with open(output_file, 'w') as f:
            f.write(kml_header)
            f.write("\n    <!-- Navigation Points -->")
            f.write(navpoints_content)
            f.write("\n    <!-- Navigation Segments -->")
            f.write(segments_content)
            f.write("\n    <!-- Airports -->")
            f.write(airports_content)
            f.write("\n" + kml_footer)
        
        return output_file


