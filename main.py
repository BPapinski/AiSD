from Star import Star
from StarCollection import StarCollection

sun = Star("Sun", 0, 1, 1)
sirius = Star("Sirius", 8.6, 2.1, 1.7)
betelgeuse = Star("Betelgeuse", 642.5, 18, 887)

# Tworzenie kolekcji gwiazd
star_collection = StarCollection()

# Dodawanie gwiazd do kolekcji
star_collection.add_star(sun)
star_collection.add_star(sirius)
star_collection.add_star(betelgeuse)

# Zapis kolekcji do pliku JSON
star_collection.serialize_collection("stars.json")

# Odczyt kolekcji z pliku JSON
new_collection = StarCollection.deserialize_collection("stars.json")
for star in new_collection.list_stars():
    print(star)
