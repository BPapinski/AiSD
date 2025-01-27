import tkinter as tk
from tkinter import messagebox, simpledialog
from Star import Star
from StarCollection import StarCollection

class StarManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Star Manager")
        self.root.geometry("650x500")
        self.root.configure(bg="#f0f0f5")

        self.collection = StarCollection.deserialize_collection("stars.json")
        self.collection.sort_by_distance()

        header = tk.Label(
            root, text="Star Manager", bg="#4a7a8c", fg="white", font=("Helvetica", 16, "bold"), pady=10
        )
        header.pack(fill=tk.X)

        self.listbox_frame = tk.Frame(root, bg="#f0f0f5")
        self.listbox_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.listbox = tk.Listbox(
            self.listbox_frame, width=80, height=15, font=("Helvetica", 12), bg="white", fg="black", selectbackground="#4a7a8c"
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

        scrollbar = tk.Scrollbar(self.listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        self.update_listbox()

        self.button_frame = tk.Frame(root, bg="#f0f0f5")
        self.button_frame.pack(pady=10, fill=tk.X)

        tk.Button(
            self.button_frame,
            text="Add Star",
            command=self.add_star_window,
            bg="#4a7a8c",
            fg="white",
            font=("Helvetica", 12),
            width=15,
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            self.button_frame,
            text="Edit Star",
            command=self.edit_star_window,
            bg="#4a7a8c",
            fg="white",
            font=("Helvetica", 12),
            width=15,
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            self.button_frame,
            text="Delete Star",
            command=self.delete_star,
            bg="#4a7a8c",
            fg="white",
            font=("Helvetica", 12),
            width=15,
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            self.button_frame,
            text="Find Star",
            command=self.find_star_window,
            bg="#4a7a8c",
            fg="white",
            font=("Helvetica", 12),
            width=15,
        ).pack(side=tk.LEFT, padx=10)

        self.bottom_frame = tk.Frame(root, bg="#f0f0f5")
        self.bottom_frame.pack(pady=10, fill=tk.X)

        tk.Button(
            self.bottom_frame,
            text="Save",
            command=self.save_to_file,
            bg="#4a7a8c",
            fg="white",
            font=("Helvetica", 12),
            width=20,
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            self.bottom_frame,
            text="Exit",
            command=root.quit,
            bg="#4a7a8c",
            fg="white",
            font=("Helvetica", 12),
            width=20,
        ).pack(side=tk.RIGHT, padx=10)

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for star in self.collection.list_stars():
            self.listbox.insert(
                tk.END, f"name: {star.name} - distance: {star.distance} - mass: {star.mass} - radius: {star.radius}"
            )

    def add_star_window(self):
        self.create_star_form("Add Star")

    def edit_star_window(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "No star selected.")
            return
        star_data = self.listbox.get(selected[0])
        star_name = star_data.split(" - ")[0].replace("name: ", "")
        star = self.collection.find_star(star_name)

        if star:
            self.create_star_form("Edit Star", star)

    def create_star_form(self, title, star=None):
        form_window = tk.Toplevel(self.root)
        form_window.title(title)
        form_window.geometry("400x300")

        tk.Label(form_window, text="Name:").pack(pady=5)
        name_entry = tk.Entry(form_window)
        name_entry.pack(pady=5)
        name_entry.insert(0, star.name if star else "")

        tk.Label(form_window, text="Distance (light-years):").pack(pady=5)
        distance_entry = tk.Entry(form_window)
        distance_entry.pack(pady=5)
        distance_entry.insert(0, star.distance if star else "")

        tk.Label(form_window, text="Mass (solar masses):").pack(pady=5)
        mass_entry = tk.Entry(form_window)
        mass_entry.pack(pady=5)
        mass_entry.insert(0, star.mass if star else "")

        tk.Label(form_window, text="Radius (solar radii):").pack(pady=5)
        radius_entry = tk.Entry(form_window)
        radius_entry.pack(pady=5)
        radius_entry.insert(0, star.radius if star else "")

        def save_star():
            name = name_entry.get().strip()
            distance_str = distance_entry.get().strip()
            mass_str = mass_entry.get().strip()
            radius_str = radius_entry.get().strip()

            if not name or not distance_str or not mass_str or not radius_str:
                messagebox.showerror("Error", "All fields must be filled out.")
                return

            try:
                distance = float(distance_str)
                mass = float(mass_str)
                radius = float(radius_str)

                if distance <= 0 or mass <= 0 or radius <= 0:
                    messagebox.showerror("Error", "Distance, mass, and radius must be greater than 0.")
                    return

                # Check for duplicate star names
                if not star:  # Adding a new star
                    if any(existing_star.name.lower() == name.lower() for existing_star in
                           self.collection.list_stars()):
                        messagebox.showerror("Error", f"A star with the name '{name}' already exists.")
                        return
                    new_star = Star(name, distance, mass, radius)
                    self.collection.add_star(new_star)
                else:  # Editing an existing star
                    if name.lower() != star.name.lower() and any(
                            existing_star.name.lower() == name.lower() for existing_star in
                            self.collection.list_stars()):
                        messagebox.showerror("Error", f"A star with the name '{name}' already exists.")
                        return
                    star.name = name
                    star.distance = distance
                    star.mass = mass
                    star.radius = radius

                self.collection.sort_by_distance()
                self.update_listbox()
                form_window.destroy()
            except ValueError:
                messagebox.showerror("Error",
                                     "Invalid input. Please enter numeric values for distance, mass, and radius.")

        tk.Button(form_window, text="Save", command=save_star, bg="#4a7a8c", fg="white").pack(pady=10)

    def delete_star(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "No star selected.")
            return
        star_data = self.listbox.get(selected[0])
        star_name = star_data.split(" - ")[0].replace("name: ", "")
        self.collection.remove_star(star_name)
        self.update_listbox()

    def find_star_window(self):
        find_window = tk.Toplevel(self.root)
        find_window.title("Find Star")
        find_window.geometry("300x150")

        tk.Label(find_window, text="Enter Star Name:").pack(pady=10)
        name_entry = tk.Entry(find_window)
        name_entry.pack(pady=10)

        def search_star():
            name = name_entry.get().strip().lower()  # Ignorowanie wielkości liter

            if not name:
                messagebox.showerror("Error", "Star name must be filled out.")
                return

            star = next((star for star in self.collection.list_stars() if star.name.lower() == name), None)

            if star:
                messagebox.showinfo(
                    "Star Found",
                    f"Name: {star.name}\nDistance: {star.distance} light-years\n"
                    f"Mass: {star.mass} solar masses\nRadius: {star.radius} solar radii"
                )
            else:
                messagebox.showerror("Error", f"Star '{name}' not found.")

            find_window.destroy()

        tk.Button(find_window, text="Search", command=search_star, bg="#4a7a8c", fg="white").pack(pady=10)

    def save_to_file(self):
        self.collection.serialize_collection("stars.json")
        messagebox.showinfo("Info", "Collection saved to stars.json!")

if __name__ == "__main__":
    root = tk.Tk()
    app = StarManagerApp(root)
    root.mainloop()
