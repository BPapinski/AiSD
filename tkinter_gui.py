import tkinter as tk
from tkinter import messagebox, simpledialog
from Star import Star
from StarCollection import StarCollection

class StarManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Star Manager")
        self.root.geometry("500x500")
        self.root.configure(bg="#f0f0f5")  # Delikatny szary kolor tła

        # Kolekcja gwiazd
        self.collection = StarCollection.deserialize_collection("stars.json")

        # Główne okno aplikacji
        header = tk.Label(
            root, text="Star Manager", bg="#4a7a8c", fg="white", font=("Helvetica", 16, "bold"), pady=10
        )
        header.pack(fill=tk.X)

        # Lista gwiazd
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

        # Przyciski akcji
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

        # Przyciski dolne (Save i Exit)
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
        """
        Aktualizuje listę gwiazd w listboxie.
        """
        self.listbox.delete(0, tk.END)
        for star in self.collection.list_stars():
            self.listbox.insert(
                tk.END, f"name: {star.name} - distance: {star.distance} - mass: {star.mass} - radius: {star.radius}"
            )

    def add_star_window(self):
        """
        Tworzy okno do dodania nowej gwiazdy.
        """
        self.create_star_form("Add Star")

    def edit_star_window(self):
        """
        Tworzy okno do edycji wybranej gwiazdy.
        """
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
        """
        Tworzy okno formularza do dodawania/edycji gwiazdy.
        """
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
            name = name_entry.get()
            try:
                distance = float(distance_entry.get())
                mass = float(mass_entry.get())
                radius = float(radius_entry.get())

                if not star:  # Add new star
                    new_star = Star(name, distance, mass, radius)
                    self.collection.add_star(new_star)
                else:  # Edit existing star
                    star.name = name
                    star.distance = distance
                    star.mass = mass
                    star.radius = radius

                self.update_listbox()
                form_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Invalid input. Please enter numeric values for distance, mass, and radius.")

        tk.Button(form_window, text="Save", command=save_star, bg="#4a7a8c", fg="white").pack(pady=10)

    def delete_star(self):
        """
        Usuwa wybraną gwiazdę z kolekcji.
        """
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "No star selected.")
            return
        star_data = self.listbox.get(selected[0])
        star_name = star_data.split(" - ")[0].replace("name: ", "")
        self.collection.remove_star(star_name)
        self.update_listbox()

    def save_to_file(self):
        """
        Zapisuje kolekcję do pliku JSON.
        """
        self.collection.serialize_collection("stars.json")
        messagebox.showinfo("Info", "Collection saved to stars.json!")