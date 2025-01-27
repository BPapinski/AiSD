from Star import Star
import json

class StarCollection:
    def __init__(self):
        self.stars = []

    def add_star(self, star):
        if not isinstance(star, Star):
            raise TypeError("Only objects of type Star can be added to the collection.")
        self.stars.append(star)

    def remove_star(self, name):
        self.stars = [star for star in self.stars if star.name != name]

    def find_star(self, name):
        for star in self.stars:
            if star.name == name:
                return star
        return None

    def list_stars(self):
        return self.stars

    def serialize_collection(self, filename):
        with open(filename, "w") as file:
            json.dump([star.to_dict() for star in self.stars], file, indent=4)

    @staticmethod
    def deserialize_collection(filename):
        collection = StarCollection()
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                for star_data in data:
                    collection.add_star(Star.from_dict(star_data))
        except FileNotFoundError:
            print(f"File {filename} not found. Returning an empty collection.")
        return collection

    def merge_sort(self, stars):
        if len(stars) <= 1:
            return stars

        mid = len(stars) // 2
        left_half = self.merge_sort(stars[:mid])
        right_half = self.merge_sort(stars[mid:])

        return self.merge(left_half, right_half)

    def merge(self, left, right):
        sorted_list = []
        i = j = 0

        while i < len(left) and j < len(right):
            if left[i].distance <= right[j].distance:
                sorted_list.append(left[i])
                i += 1
            else:
                sorted_list.append(right[j])
                j += 1

        sorted_list.extend(left[i:])
        sorted_list.extend(right[j:])
        return sorted_list

    def sort_by_distance(self):
        self.stars = self.merge_sort(self.stars)

