class Star:
    def __init__(self, name, distance, mass, radius):
        self.name = name
        self.distance = distance
        self.mass = mass
        self.radius = radius

    def __str__(self):
        return (f"Star Details:\n"
                f"  Name: {self.name}\n"
                f"  Distance from Earth: {self.distance} light-years\n"
                f"  Mass: {self.mass} solar masses\n"
                f"  Radius: {self.radius} solar radii")

    def to_dict(self):
        return {
            "name": self.name,
            "distance": self.distance,
            "mass": self.mass,
            "radius": self.radius
        }

    @staticmethod
    def from_dict(data):
        return Star(
            name=data["name"],
            distance=data["distance"],
            mass=data["mass"],
            radius=data["radius"]
        )