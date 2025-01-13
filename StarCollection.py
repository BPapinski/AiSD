from Star import Star
import json

class StarCollection:
    """
    Klasa zarządzająca kolekcją gwiazd.
    """
    def __init__(self):
        """
        Inicjalizuje pustą kolekcję gwiazd.
        """
        self.stars = []

    def add_star(self, star):
        """
        Dodaje gwiazdę do kolekcji.

        :param star: Obiekt klasy Star do dodania
        """
        if not isinstance(star, Star):
            raise TypeError("Only objects of type Star can be added to the collection.")
        self.stars.append(star)

    def remove_star(self, name):
        """
        Usuwa gwiazdę z kolekcji na podstawie jej nazwy.

        :param name: Nazwa gwiazdy do usunięcia
        """
        self.stars = [star for star in self.stars if star.name != name]

    def find_star(self, name):
        """
        Wyszukuje gwiazdę w kolekcji na podstawie jej nazwy.

        :param name: Nazwa gwiazdy do wyszukania
        :return: Obiekt klasy Star lub None, jeśli nie znaleziono
        """
        for star in self.stars:
            if star.name == name:
                return star
        return None

    def list_stars(self):
        """
        Zwraca listę wszystkich gwiazd w kolekcji.
        """
        return self.stars

    def serialize_collection(self, filename):
        """
        Zapisuje kolekcję gwiazd do pliku JSON.

        :param filename: Nazwa pliku JSON
        """
        with open(filename, "w") as file:
            json.dump([star.to_dict() for star in self.stars], file, indent=4)

    @staticmethod
    def deserialize_collection(filename):
        """
        Odczytuje kolekcję gwiazd z pliku JSON.

        :param filename: Nazwa pliku JSON
        :return: Obiekt klasy StarCollection
        """
        collection = StarCollection()
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                for star_data in data:
                    collection.add_star(Star.from_dict(star_data))
        except FileNotFoundError:
            print(f"File {filename} not found. Returning an empty collection.")
        return collection