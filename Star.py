class Star:
    """
    Klasa reprezentująca pojedynczą gwiazdę w kosmosie.
    """
    def __init__(self, name, distance, mass, radius):
        """
        Inicjalizuje obiekt gwiazdy.

        :param name: Nazwa gwiazdy
        :param distance: Odległość od Ziemi w latach świetlnych
        :param mass: Masa gwiazdy w jednostkach masy Słońca
        :param radius: Promień gwiazdy w jednostkach promienia Słońca
        """
        self.name = name
        self.distance = distance
        self.mass = mass
        self.radius = radius

    def __str__(self):
        """
        Zwraca czytelną reprezentację gwiazdy.
        """
        return (f"Star Details:\n"
                f"  Name: {self.name}\n"
                f"  Distance from Earth: {self.distance} light-years\n"
                f"  Mass: {self.mass} solar masses\n"
                f"  Radius: {self.radius} solar radii")

    def to_dict(self):
        """
        Konwertuje obiekt Star na słownik.
        """
        return {
            "name": self.name,
            "distance": self.distance,
            "mass": self.mass,
            "radius": self.radius
        }

    @staticmethod
    def from_dict(data):
        """
        Tworzy obiekt Star z słownika.
        """
        return Star(
            name=data["name"],
            distance=data["distance"],
            mass=data["mass"],
            radius=data["radius"]
        )