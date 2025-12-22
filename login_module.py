import tkinter as tk
from tkinter import ttk, messagebox
from database import load_data

class LoginMixin:
    # ------------------ LOGIN SCREEN (With Version info) ------------------
    def show_role_selection(self):
        self.clear_frame()
        container = ttk.Frame(self.root, style="Main.TFrame"); container.pack(fill="both", expand=True)
        
        card = ttk.Frame(container, style="Card.TFrame", padding=50)
        card.place(relx=0.5, rely=0.5, anchor="center")
        
        ttk.Label(card, text="🏥 CLINIC MANAGEMENT SYSTEM", style="CardTitle.TLabel", font=("Segoe UI", 26, "bold")).pack(pady=20)
        
        ttk.Button(card, text="Manager Login 👔", style="Primary.TButton", width=30, command=lambda: self.show_login("Manager")).pack(pady=10)
        ttk.Button(card, text="Doctor Login 🩺", style="Danger.TButton", width=30, command=lambda: self.show_login("Doctor")).pack(pady=10)
        ttk.Button(card, text="Exit Application 🚪", style="TButton", width=30, command=self.root.quit).pack(pady=20)

        ttk.Label(container, text="Version 2.0", font=("Segoe UI", 12), foreground="gray").pack(side="bottom", pady=30)

    def show_login(self, role):
        self.role = role
        self.clear_frame()
        container = ttk.Frame(self.root, style="Main.TFrame"); container.pack(fill="both", expand=True)
        card = ttk.Frame(container, style="Card.TFrame", padding=50)
        card.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(card, text=f"{role.upper()} PORTAL", style="CardTitle.TLabel").pack(pady=20)
        
        ttk.Label(card, text="Username", style="CardBody.TLabel").pack(anchor="center")
        self.username_entry = ttk.Entry(card, width=35, font=("Segoe UI", 12))
        self.username_entry.pack(pady=5)
        
        ttk.Label(card, text="Password", style="CardBody.TLabel").pack(anchor="center")
        self.password_entry = ttk.Entry(card, width=35, show="•", font=("Segoe UI", 12))
        self.password_entry.pack(pady=15)
        
        ttk.Button(card, text="LOGIN", style="Primary.TButton" if role=="Manager" else "Danger.TButton", width=35, command=self.attempt_login).pack(pady=10)
        ttk.Button(card, text="Back", style="TButton", command=self.show_role_selection).pack()

    def attempt_login(self):
        u = self.username_entry.get().strip()
        p = self.password_entry.get().strip()
        users = load_data("users.txt")
        for user in users:
            if len(user) >= 3 and user[0] == u and user[1] == p and user[2] == self.role:
                self.current_user = u
                if self.role == "Manager": self.show_manager_dashboard()
                else: self.show_doctor_dashboard()
                return
        messagebox.showerror("Error", "Invalid Credentials")