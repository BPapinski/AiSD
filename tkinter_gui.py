import tkinter as tk
from tkinter import messagebox, simpledialog
from Star import Star
from StarCollection import StarCollection

class StarManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Star Manager")
        self.root.geometry("600x400")
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
            command=self.add_star,
            bg="#4a7a8c",
            fg="white",
            font=("Helvetica", 12),
            width=15,
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            self.button_frame,
            text="Edit Star",
            command=self.edit_star,
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
        star_data = self.listbox.get(selected[0])
        star_name = star_data.split(" - ")[0].replace("name: ", "")
        star = self.collection.find_star(star_name)

        if star:
            new_name = simpledialog.askstring("Input", "Enter new star name:", initialvalue=star.name)
            if not new_name:
                return
            try:
                new_distance = float(simpledialog.askstring("Input", "Enter new distance (light-years):", initialvalue=star.distance))
                new_mass = float(simpledialog.askstring("Input", "Enter new mass (solar masses):", initialvalue=star.mass))
                new_radius = float(simpledialog.askstring("Input", "Enter new radius (solar radii):", initialvalue=star.radius))
                star.name = new_name
                star.distance = new_distance
                star.mass = new_mass
                star.radius = new_radius
                self.update_listbox()
            except (ValueError, TypeError):
                messagebox.showerror("Error", "Invalid input. Please enter numeric values for distance, mass, and radius.")

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