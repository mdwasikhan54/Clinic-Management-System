import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from database import *

class DoctorMixin:
    # ====================== DOCTOR DASHBOARD ======================
    def show_doctor_dashboard(self):
        self.clear_frame()
        header = ttk.Frame(self.root, style="Sidebar.TFrame", padding=15)
        header.pack(fill="x")
        ttk.Label(header, text=f"Doctor Dashboard 🩺 | Dr. {self.current_user}", style="White.TLabel").pack(side="left")
        ttk.Button(header, text="Logout", style="Danger.TButton", command=self.show_role_selection).pack(side="right")
        nb = ttk.Notebook(self.root); nb.pack(fill="both", expand=True, padx=20, pady=20)
        nb.add(ttk.Frame(nb, style="Main.TFrame"), text="  Prescribe Medicine  "); self.doctor_prescribe(nb.nametowidget(nb.tabs()[0]))
        nb.add(ttk.Frame(nb, style="Main.TFrame"), text="  Medical History  "); self.doctor_history_fixed(nb.nametowidget(nb.tabs()[1]))
        nb.add(ttk.Frame(nb, style="Main.TFrame"), text="  Live Queue  "); self.doctor_queue(nb.nametowidget(nb.tabs()[2]))

    def doctor_prescribe(self, tab):
        top_card = ttk.Frame(tab, style="Card.TFrame", padding=15); top_card.pack(fill="x", padx=20, pady=(20, 10))
        self.patient_info_label = ttk.Label(top_card, text="No Patient Selected", font=("Segoe UI", 16, "bold"), foreground="gray", background="white")
        self.patient_info_label.pack(side="left")
        btn_box = ttk.Frame(top_card, style="Card.TFrame"); btn_box.pack(side="right")
        ttk.Button(btn_box, text="Select from Queue 📋", style="Primary.TButton", command=self.select_patient_from_queue).pack(side="left", padx=5)
        self.btn_call_next = ttk.Button(btn_box, text="Call Next ⏩", style="TButton", command=self.call_next_patient); self.btn_call_next.pack(side="left", padx=5)

        form_area = ttk.Frame(tab, style="Main.TFrame"); form_area.pack(fill="both", expand=True, padx=20)
        
        vitals_frame = ttk.LabelFrame(form_area, text=" Patient Vitals ", padding=15); vitals_frame.pack(fill="x", pady=5)
        ttk.Label(vitals_frame, text="Age:").pack(side="left", padx=(0,5)); self.age_entry = ttk.Entry(vitals_frame, width=15); self.age_entry.pack(side="left", padx=(0,20))
        ttk.Label(vitals_frame, text="Gender:").pack(side="left", padx=(0,5)); self.gender_entry = ttk.Entry(vitals_frame, width=20); self.gender_entry.pack(side="left")

        input_row = ttk.Frame(form_area, style="Main.TFrame"); input_row.pack(fill="x", pady=5)
        med_grp = ttk.LabelFrame(input_row, text=" Add Medicine ", padding=15); med_grp.pack(side="left", fill="both", expand=True, padx=(0,10))
        f_meds = ttk.Frame(med_grp, style="Card.TFrame"); f_meds.pack(fill="x")
        ttk.Label(f_meds, text="Name", style="Small.TLabel").grid(row=0, column=0, sticky="w"); ttk.Label(f_meds, text="Dose (1+0+1)", style="Small.TLabel").grid(row=0, column=1, sticky="w"); ttk.Label(f_meds, text="Days", style="Small.TLabel").grid(row=0, column=2, sticky="w")
        self.med_name = ttk.Entry(f_meds, width=20); self.med_name.grid(row=1, column=0, padx=2); self.med_dose = ttk.Entry(f_meds, width=15); self.med_dose.grid(row=1, column=1, padx=2); self.med_days = ttk.Entry(f_meds, width=10); self.med_days.grid(row=1, column=2, padx=2)
        ttk.Button(f_meds, text="Add ✚", style="Primary.TButton", command=self.add_medicine).grid(row=1, column=3, padx=10)

        test_grp = ttk.LabelFrame(input_row, text=" Add Test ", padding=15); test_grp.pack(side="right", fill="both", expand=True)
        self.test_entry = ttk.Entry(test_grp); self.test_entry.pack(side="left", fill="x", expand=True, padx=5); ttk.Button(test_grp, text="Add ✚", style="TButton", command=self.add_test).pack(side="left")

        list_row = ttk.Frame(form_area, style="Main.TFrame"); list_row.pack(fill="both", expand=True, pady=5)
        lm = ttk.Frame(list_row); lm.pack(side="left", fill="both", expand=True, padx=(0,10))
        self.med_listbox = tk.Listbox(lm, height=6, relief="solid", borderwidth=1, font=("Segoe UI", 10)); self.med_listbox.pack(fill="both", expand=True)
        ttk.Button(lm, text="Remove Medicine ❌", style="Danger.TButton", command=self.remove_medicine).pack(fill="x", pady=2)
        lt = ttk.Frame(list_row); lt.pack(side="right", fill="both", expand=True)
        self.test_listbox = tk.Listbox(lt, height=6, relief="solid", borderwidth=1, font=("Segoe UI", 10)); self.test_listbox.pack(fill="both", expand=True)
        ttk.Button(lt, text="Remove Test ❌", style="Danger.TButton", command=self.remove_test).pack(fill="x", pady=2)

        footer = ttk.Frame(form_area, style="Main.TFrame", padding=10); footer.pack(fill="x", pady=10)
        self.btn_save = ttk.Button(footer, text="💾 SAVE PRESCRIPTION", style="Success.TButton", command=self.save_prescription); self.btn_save.pack(fill="x")
        self.meds = []; self.tests = []

    def select_patient_from_queue(self):
        win = tk.Toplevel(self.root); win.title("Queue"); win.geometry("600x400")
        tree = ttk.Treeview(win, columns=("ID", "Name", "Phone"), show="headings"); tree.pack(fill="both", expand=True)
        for c in ("ID", "Name", "Phone"): tree.heading(c, text=c)
        serials = load_data("serials.txt")
        for s in serials:
            if len(s)>=4: tree.insert("", "end", values=(s[4] if len(s)>4 else "N/A", s[1], s[2]))
        def select():
            sel = tree.selection()
            if sel:
                val = tree.item(sel[0])["values"]
                self.current_patient = {"smart_id": str(val[0]), "name": val[1], "phone": str(val[2])}
                self.patient_info_label.config(text=f"Prescribing: {val[1]}  |  📞 {val[2]}", foreground=self.colors["primary"])
                for i, s in enumerate(serials):
                    if len(s)>4 and s[4] == str(val[0]): self.current_patient_index = i; break
                win.destroy()
        ttk.Button(win, text="Confirm", style="Success.TButton", command=select).pack(pady=10)

    def add_medicine(self):
        n, d, dur = self.med_name.get().strip(), self.med_dose.get().strip(), self.med_days.get().strip()
        if n and d and dur:
            val = f"{n} - {d} - {dur}"
            self.meds.append(val); self.med_listbox.insert(tk.END, f"• {val}")
            self.med_name.delete(0, tk.END); self.med_dose.delete(0, tk.END); self.med_days.delete(0, tk.END); self.med_name.focus()

    def add_test(self):
        t = self.test_entry.get().strip()
        if t: self.tests.append(t); self.test_listbox.insert(tk.END, f"• {t}"); self.test_entry.delete(0, tk.END)

    def remove_medicine(self):
        s = self.med_listbox.curselection()
        if s: self.meds.pop(s[0]); self.med_listbox.delete(s[0])
    def remove_test(self):
        s = self.test_listbox.curselection()
        if s: self.tests.pop(s[0]); self.test_listbox.delete(s[0])

    def save_prescription(self):
        if not self.current_patient: return messagebox.showwarning("Error", "Select patient first")
        rx = self.current_patient.copy()
        rx.update({"age": self.age_entry.get(), "gender": self.gender_entry.get(), "meds": self.meds, "tests": self.tests, "date": datetime.now().strftime('%Y-%m-%d %H:%M')})
        rec = f"Name: {rx['name']} │ Phone: {rx['phone']} │ SmartID: {rx['smart_id']}\n Visit: {format_datetime(rx['date'])}\n"
        if rx['age']: rec += f"Age: {rx['age']} │ Gender: {rx['gender']}\n"
        if rx['meds']: rec += "Medicines:\n" + "\n".join([f" • {m}" for m in rx['meds']]) + "\n"
        if rx['tests']: rec += "Tests:\n" + "\n".join([f" • {t}" for t in rx['tests']]) + "\n"
        rec += "════════════════════════════════════════════════════════════\n"
        append_data("patients.txt", rec)
        if self.current_patient_index is not None:
            rem = delete_line("serials.txt", self.current_patient_index)
            if rem: append_data("old_patients.txt", "|".join(rem))
        messagebox.showinfo("Saved", "Prescription Saved!")
        self.clear_prescribe_fields(); self.patient_info_label.config(text="Status: Saved. Ready for Next.", foreground="green"); self.btn_call_next.configure(style="Primary.TButton")

    def clear_prescribe_fields(self):
        self.age_entry.delete(0, tk.END); self.gender_entry.delete(0, tk.END)
        self.med_listbox.delete(0, tk.END); self.test_listbox.delete(0, tk.END)
        self.meds = []; self.tests = []; self.current_patient = None; self.current_patient_index = None

    def call_next_patient(self):
        self.clear_prescribe_fields()
        serials = load_data("serials.txt")
        if serials:
            s = serials[0]
            self.current_patient = {"smart_id": s[4] if len(s)>4 else "N/A", "name": s[1], "phone": s[2]}
            self.current_patient_index = 0
            self.patient_info_label.config(text=f"Prescribing: {s[1]}  |  📞 {s[2]}", foreground=self.colors["primary"])
            self.btn_call_next.configure(style="TButton")
        else: messagebox.showinfo("Empty", "No patients waiting")

    def doctor_history_fixed(self, tab):
        paned = ttk.PanedWindow(tab, orient="horizontal"); paned.pack(fill="both", expand=True, padx=20, pady=20)
        left = ttk.Frame(paned, style="Card.TFrame", padding=1); paned.add(left, weight=1)
        ttk.Label(left, text="  Old Patients List", style="CardTitle.TLabel", font=("Segoe UI", 12, "bold")).pack(pady=10)
        tree = ttk.Treeview(left, columns=("Name", "Phone", "Date"), show="headings", style="Treeview")
        for c in ("Name", "Phone", "Date"): tree.heading(c, text=c)
        tree.column("Name", width=120); tree.column("Phone", width=100); tree.column("Date", width=120)
        sb = ttk.Scrollbar(left, orient="vertical", command=tree.yview); tree.configure(yscrollcommand=sb.set); tree.pack(side="left", fill="both", expand=True); sb.pack(side="right", fill="y")
        right = ttk.Frame(paned, style="Card.TFrame", padding=20); paned.add(right, weight=2)
        ttk.Label(right, text="Prescription Details", style="CardTitle.TLabel").pack(anchor="center", pady=(0,10))
        txt = tk.Text(right, font=("Consolas", 11), borderwidth=0, bg="#F9F9F9", padx=10, pady=10); txt.pack(fill="both", expand=True)
        def load():
            for i in tree.get_children(): tree.delete(i)
            for row in reversed(load_data("old_patients.txt")):
                if len(row) >= 4: tree.insert("", "end", values=(row[1], row[2], format_datetime(row[3])))
        def show(event):
            sel = tree.selection()
            if not sel: return
            val = tree.item(sel[0])["values"]; name, phone = val[0], str(val[1])
            full = "".join(load_raw_lines("patients.txt")); records = full.split("════════════════════════════════════════════════════════════")
            txt.delete(1.0, tk.END); found = False
            for rec in records:
                if (f"Name: {name}" in rec) and (f"Phone: {phone}" in rec):
                    txt.insert(tk.END, rec.strip() + "\n\n" + "-"*40 + "\n\n"); found = True
            if not found: txt.insert(tk.END, "No details found.")
        tree.bind("<<TreeviewSelect>>", show); ttk.Button(left, text="Refresh List", command=load).pack(side="bottom", fill="x"); load()

    def doctor_queue(self, tab):
        card = ttk.Frame(tab, style="Card.TFrame", padding=20); card.pack(fill="both", expand=True, padx=20, pady=20)
        tree = ttk.Treeview(card, columns=("SL", "Name", "Phone"), show="headings", style="Treeview")
        for c in ("SL", "Name", "Phone"): tree.heading(c, text=c)
        tree.pack(fill="both", expand=True)
        def r():
            for i in tree.get_children(): tree.delete(i)
            for i, d in enumerate(load_data("serials.txt"), 1): tree.insert("", "end", values=(i, d[1], d[2]))
        ttk.Button(card, text="Refresh", command=r).pack(pady=10); r()