import tkinter as tk
from tkinter import messagebox, simpledialog
from Star import Star
from StarCollection import StarCollection



class StarManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Star Manager")
        self.collection = StarCollection.deserialize_collection("stars.json")

        # Lista gwiazd
        self.listbox = tk.Listbox(root, width=50, height=15)
        self.listbox.pack(pady=10)
        self.update_listbox()

        # Przyciski
        self.add_button = tk.Button(root, text="Add Star", command=self.add_star)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.edit_button = tk.Button(root, text="Edit Star", command=self.edit_star)
        self.edit_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = tk.Button(root, text="Delete Star", command=self.delete_star)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.save_button = tk.Button(root, text="Save", command=self.save_to_file)
        self.save_button.pack(side=tk.LEFT, padx=5)

    def update_listbox(self):
        """
        Aktualizuje listę gwiazd w listboxie.
        """
        self.listbox.delete(0, tk.END)
        for star in self.collection.list_stars():
            self.listbox.insert(tk.END, f"{star.name} - {star.distance} ly")

    def add_star(self):
        """
        Dodaje nową gwiazdę do kolekcji.
        """
        name = simpledialog.askstring("Input", "Enter star name:")
        if not name:
            return
        try:
            distance = float(simpledialog.askstring("Input", "Enter distance (light-years):"))
            mass = float(simpledialog.askstring("Input", "Enter mass (solar masses):"))
            radius = float(simpledialog.askstring("Input", "Enter radius (solar radii):"))
            new_star = Star(name, distance, mass, radius)
            self.collection.add_star(new_star)
            self.update_listbox()
        except (ValueError, TypeError):
            messagebox.showerror("Error", "Invalid input. Please enter numeric values for distance, mass, and radius.")

    def edit_star(self):
        """
        Edytuje wybraną gwiazdę z listy.
        """
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "No star selected.")
            return
        star_name = self.listbox.get(selected[0]).split(" - ")[0]
        star = self.collection.find_star(star_name)

        if star:
            new_name = simpledialog.askstring("Input", "Enter new star name:", initialvalue=star.name)
            if not new_name:
                return
            try:
                new_distance = float(
                    simpledialog.askstring("Input", "Enter new distance (light-years):", initialvalue=star.distance))
                new_mass = float(
                    simpledialog.askstring("Input", "Enter new mass (solar masses):", initialvalue=star.mass))
                new_radius = float(
                    simpledialog.askstring("Input", "Enter new radius (solar radii):", initialvalue=star.radius))
                star.name = new_name
                star.distance = new_distance
                star.mass = new_mass
                star.radius = new_radius
                self.update_listbox()
            except (ValueError, TypeError):
                messagebox.showerror("Error",
                                     "Invalid input. Please enter numeric values for distance, mass, and radius.")

    def delete_star(self):
        """
        Usuwa wybraną gwiazdę z kolekcji.
        """
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "No star selected.")
            return
        star_name = self.listbox.get(selected[0]).split(" - ")[0]
        self.collection.remove_star(star_name)
        self.update_listbox()

    def save_to_file(self):
        """
        Zapisuje kolekcję do pliku JSON.
        """
        self.collection.serialize_collection("stars.json")
        messagebox.showinfo("Info", "Collection saved to stars.json!")

