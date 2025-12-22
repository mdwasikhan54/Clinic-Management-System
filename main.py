import tkinter as tk
from tkinter import ttk
from database import *
from login_module import LoginMixin
from manager_module import ManagerMixin
from doctor_module import DoctorMixin

class ClinicApp(LoginMixin, ManagerMixin, DoctorMixin):
    def __init__(self, root):
        self.root = root
        self.root.title("Clinic Management System - Professional")
        self.root.geometry("1300x800")
        self.root.minsize(1024, 768)
        
        # --- UI Theme & Styles ---
        self.colors = {
            "bg": "#F0F2F5", "sidebar": "#2C3E50", "primary": "#3498DB",
            "success": "#27AE60", "danger": "#E74C3C", "text": "#34495E", "white": "#FFFFFF"
        }
        self.setup_styles()
        self.root.configure(bg=self.colors["bg"])
        
        # Session State
        self.current_user = None
        self.role = None
        self.current_patient = None
        self.current_patient_index = None
        
        self.show_role_selection()

    def setup_styles(self):
        """Configures custom TTK styles for a modern look."""
        style = ttk.Style()
        style.theme_use("clam")
        
        # Frames
        style.configure("Main.TFrame", background=self.colors["bg"])
        style.configure("Card.TFrame", background=self.colors["white"], relief="flat")
        style.configure("Sidebar.TFrame", background=self.colors["sidebar"])
        
        # Labels
        style.configure("TLabel", background=self.colors["bg"], foreground=self.colors["text"], font=("Segoe UI", 11))
        style.configure("Header.TLabel", font=("Segoe UI", 24, "bold"), background=self.colors["bg"], foreground=self.colors["sidebar"])
        style.configure("CardTitle.TLabel", font=("Segoe UI", 16, "bold"), background=self.colors["white"], foreground=self.colors["sidebar"])
        style.configure("CardBody.TLabel", font=("Segoe UI", 11), background=self.colors["white"], foreground=self.colors["text"])
        style.configure("White.TLabel", background=self.colors["sidebar"], foreground=self.colors["white"], font=("Segoe UI", 12))
        style.configure("Small.TLabel", background=self.colors["white"], foreground="gray", font=("Segoe UI", 9))

        # Buttons
        style.configure("TButton", font=("Segoe UI", 11), padding=8, borderwidth=0)
        style.map("TButton", background=[("active", "#BDC3C7")])
        
        style.configure("Primary.TButton", background=self.colors["primary"], foreground=self.colors["white"])
        style.map("Primary.TButton", background=[("active", "#2980B9")])
        
        style.configure("Success.TButton", background=self.colors["success"], foreground=self.colors["white"])
        style.map("Success.TButton", background=[("active", "#219150")])
        
        style.configure("Danger.TButton", background=self.colors["danger"], foreground=self.colors["white"])
        style.map("Danger.TButton", background=[("active", "#C0392B")])

        # Treeview
        style.configure("Treeview", background=self.colors["white"], fieldbackground=self.colors["white"], font=("Segoe UI", 10), rowheight=28)
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background=self.colors["sidebar"], foreground=self.colors["white"])
        style.map("Treeview", background=[('selected', self.colors["primary"])])

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ClinicApp(root)
    root.mainloop()