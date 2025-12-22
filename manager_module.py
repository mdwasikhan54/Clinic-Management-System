import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import re
from database import *

class ManagerMixin:
    # ====================== MANAGER DASHBOARD ======================
    def show_manager_dashboard(self):
        self.clear_frame()
        # Header
        header = ttk.Frame(self.root, style="Sidebar.TFrame", padding=15)
        header.pack(fill="x")
        ttk.Label(header, text=f"Manager Dashboard | {self.current_user}", style="White.TLabel").pack(side="left")
        ttk.Button(header, text="Logout", style="Danger.TButton", command=self.show_role_selection).pack(side="right")

        # Tabs
        nb = ttk.Notebook(self.root)
        nb.pack(fill="both", expand=True, padx=20, pady=20)
        
        t1 = ttk.Frame(nb, style="Main.TFrame"); nb.add(t1, text=" Take Serial ")
        t2 = ttk.Frame(nb, style="Main.TFrame"); nb.add(t2, text=" Manage Serials ")
        t3 = ttk.Frame(nb, style="Main.TFrame"); nb.add(t3, text=" Drugs & Sales ")
        t4 = ttk.Frame(nb, style="Main.TFrame"); nb.add(t4, text=" Sales Reports ")

        self.manager_take_serial(t1)
        self.manager_manage_serials(t2)
        self.manager_drugs_sales(t3)
        self.manager_sales_reports_full(t4)

    def manager_take_serial(self, tab):
        card = ttk.Frame(tab, style="Card.TFrame", padding=40)
        card.place(relx=0.5, rely=0.5, anchor="center")
        ttk.Label(card, text="New Patient Entry", style="CardTitle.TLabel").pack(pady=20)
        
        ttk.Label(card, text="Patient Name", style="CardBody.TLabel").pack(anchor="center")
        name_e = ttk.Entry(card, width=40, font=("Segoe UI", 11)); name_e.pack(pady=5)
        ttk.Label(card, text="Phone", style="CardBody.TLabel").pack(anchor="center")
        phone_e = ttk.Entry(card, width=40, font=("Segoe UI", 11)); phone_e.pack(pady=5)

        def save():
            n, p = name_e.get().strip(), phone_e.get().strip()
            if not n or not p: return messagebox.showwarning("Warning", "Fields empty")
            if not re.match(r"^[\d\+-]+$", p) or len(p) < 4: return messagebox.showwarning("Warning", "Invalid phone")
            today = datetime.now().strftime('%Y-%m-%d')
            if any(s[2] == p and s[3].startswith(today) for s in load_data("serials.txt")):
                return messagebox.showwarning("Warning", "Already exists today")
            
            sid = get_next_id("serials.txt")
            now = datetime.now().strftime('%Y-%m-%d %H:%M')
            smart = generate_smart_id(p, now)
            append_data("serials.txt", f"{sid}|{n}|{p}|{now}|{smart}")
            messagebox.showinfo("Success", f"Serial: {sid}\nSmartID: {smart}")
            name_e.delete(0, tk.END); phone_e.delete(0, tk.END)

        ttk.Button(card, text="Generate Serial ✅", style="Success.TButton", width=30, command=save).pack(pady=20)

    def manager_manage_serials(self, tab):
        tree_frame = ttk.Frame(tab, style="Card.TFrame", padding=10)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        cols = ("SL", "SmartID", "Name", "Phone", "Time")
        tree = ttk.Treeview(tree_frame, columns=cols, show="headings", style="Treeview")
        for c in cols: tree.heading(c, text=c)
        tree.pack(fill="both", expand=True)

        def refresh():
            for i in tree.get_children(): tree.delete(i)
            for i, row in enumerate(load_data("serials.txt"), 1):
                if len(row)>=4: tree.insert("", "end", values=(i, row[4] if len(row)>4 else "N/A", row[1], row[2], format_datetime(row[3])))

        def cancel():
            sel = tree.selection()
            if sel and messagebox.askyesno("Confirm", "Cancel Serial?"):
                delete_line("serials.txt", int(tree.item(sel[0])["values"][0])-1)
                refresh()

        btn_bar = ttk.Frame(tab, style="Main.TFrame"); btn_bar.pack(pady=10)
        ttk.Button(btn_bar, text="Refresh", command=refresh).pack(side="left", padx=5)
        ttk.Button(btn_bar, text="Cancel Selected", style="Danger.TButton", command=cancel).pack(side="left", padx=5)
        refresh()
        
    # ====================== MANAGER: DRUGS & SALES ======================
    def manager_drugs_sales(self, tab):
        sn = ttk.Notebook(tab); sn.pack(fill="both", expand=True, padx=20, pady=20)
        t1, t2, t3 = ttk.Frame(sn, style="Main.TFrame"), ttk.Frame(sn, style="Main.TFrame"), ttk.Frame(sn, style="Main.TFrame")
        sn.add(t1, text=" Stock (Edit/Delete) "); sn.add(t2, text=" Add Drug "); sn.add(t3, text=" Sell Drug ")

        self.manager_stock(t1)
        self.manager_add_drug(t2)
        self.manager_sell_drug_fixed(t3)

    # --- STOCK (With Edit & Delete Fix) ---
    def manager_stock(self, tab):
        frame = ttk.Frame(tab, style="Card.TFrame", padding=10)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        tree = ttk.Treeview(frame, columns=("ID", "Name", "Qty", "Price", "Expiry"), show="headings", style="Treeview")
        for c in ("ID", "Name", "Qty", "Price", "Expiry"): tree.heading(c, text=c)
        tree.pack(side="left", fill="both", expand=True)
        
        sb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview); tree.configure(yscrollcommand=sb.set); sb.pack(side="right", fill="y")

        def refresh():
            for i in tree.get_children(): tree.delete(i)
            today = datetime.now().date()
            for i, d in enumerate(load_data("drugs.txt"), 1):
                tag = "exp" if datetime.strptime(d[3], "%Y-%m-%d").date() < today else ""
                tree.insert("", "end", values=(i, d[0], d[1], f"৳{d[2]}", d[3]), tags=(tag,))
            tree.tag_configure("exp", foreground="red")

        def edit():
            sel = tree.selection()
            if not sel: return
            idx = tree.index(sel[0])
            all_drugs = load_data("drugs.txt")
            if not (0 <= idx < len(all_drugs)): return
            
            target = all_drugs[idx]
            
            # Edit Popup
            win = tk.Toplevel(self.root)
            win.title("Edit Drug")
            win.geometry("400x350")
            win.configure(bg="white")
            
            ttk.Label(win, text="Edit Details", style="CardTitle.TLabel").pack(pady=15)
            f = ttk.Frame(win, style="Card.TFrame"); f.pack(pady=5)
            
            entries = []
            labels = ["Name", "Qty", "Price", "Expiry"]
            for i, l in enumerate(labels):
                ttk.Label(f, text=l, style="CardBody.TLabel").grid(row=i, column=0, sticky="e", pady=5)
                e = ttk.Entry(f, width=25)
                e.insert(0, target[i])
                e.grid(row=i, column=1, pady=5, padx=5)
                entries.append(e)
            
            def save_changes():
                vals = [e.get().strip() for e in entries]
                try:
                    datetime.strptime(vals[3], "%Y-%m-%d")
                    if vals[1].isdigit():
                        all_drugs[idx] = vals
                        save_data("drugs.txt", all_drugs)
                        messagebox.showinfo("Success", "Drug Updated!")
                        refresh(); win.destroy()
                    else: raise ValueError
                except: messagebox.showerror("Error", "Invalid Date or Number")
            
            ttk.Button(win, text="Save Changes", style="Success.TButton", command=save_changes).pack(pady=20)

        def delete():
            sel = tree.selection()
            if sel and messagebox.askyesno("Delete", "Permanently Delete Drug?"):
                delete_line("drugs.txt", tree.index(sel[0]))
                refresh()

        btn_bar = ttk.Frame(tab, style="Main.TFrame"); btn_bar.pack(pady=10)
        ttk.Button(btn_bar, text="Refresh", command=refresh).pack(side="left", padx=5)
        ttk.Button(btn_bar, text="✏️ Edit Drug", style="Primary.TButton", command=edit).pack(side="left", padx=5)
        ttk.Button(btn_bar, text="🗑️ Delete Drug", style="Danger.TButton", command=delete).pack(side="left", padx=5)
        refresh()

    def manager_add_drug(self, tab):
        card = ttk.Frame(tab, style="Card.TFrame", padding=30); card.place(relx=0.5, rely=0.5, anchor="center")
        entries = []
        for l in ["Name", "Quantity", "Price", "Expiry (YYYY-MM-DD)"]:
            ttk.Label(card, text=l, style="CardBody.TLabel").pack(anchor="center")
            e = ttk.Entry(card, width=30); e.pack(pady=5); entries.append(e)
        def add_d():
            v = [e.get().strip() for e in entries]
            try:
                datetime.strptime(v[3], "%Y-%m-%d")
                if v[1].isdigit(): append_data("drugs.txt", "|".join(v)); messagebox.showinfo("Success", "Added"); 
                for e in entries: e.delete(0, tk.END)
            except: messagebox.showerror("Error", "Invalid Input")
        ttk.Button(card, text="Add Drug", style="Success.TButton", command=add_d).pack(pady=20)

    def manager_sell_drug_fixed(self, tab):
        vf = ttk.Frame(tab, style="Card.TFrame", padding=20); vf.pack(fill="x", padx=20, pady=10)
        ttk.Label(vf, text="Patient Phone/SmartID:", style="CardTitle.TLabel").pack(side="left")
        pid_e = ttk.Entry(vf, width=30); pid_e.pack(side="left", padx=10)
        st_lbl = ttk.Label(vf, text="Waiting...", foreground="gray"); st_lbl.pack(side="left", padx=10)
        
        s_tree = ttk.Treeview(tab, columns=("Name", "Stock", "Price"), show="headings"); s_tree.pack(fill="both", expand=True, padx=20)
        for c in ("Name", "Stock", "Price"): s_tree.heading(c, text=c)

        def verify():
            meds = set()
            full = "".join(load_raw_lines("patients.txt"))
            valid = False; in_m = False
            for line in full.split("\n"):
                if "════" in line: valid = False
                if ("SmartID:" in line or "Phone:" in line) and pid_e.get() in line: valid = True
                if valid:
                    if "Medicines:" in line: in_m = True; continue
                    if "Tests:" in line: in_m = False; continue
                    if in_m and line.strip().startswith("•"): meds.add(line.strip()[2:].split(" - ")[0])
            
            for i in s_tree.get_children(): s_tree.delete(i)
            if meds:
                st_lbl.config(text="Verified ✅", foreground="green")
                for d in load_data("drugs.txt"):
                    if any(m.lower() in d[0].lower() or d[0].lower() in m.lower() for m in meds) and int(d[1]) > 0:
                        s_tree.insert("", "end", values=(d[0], d[1], d[2]))
            else: st_lbl.config(text="No Rx Found ❌", foreground="red")

        def sell():
            sel = s_tree.selection()
            if not sel: return
            item = s_tree.item(sel[0])["values"]
            qty = simpledialog.askinteger("Qty", f"Sell {item[0]}?", minvalue=1, maxvalue=int(item[1]))
            if qty:
                drugs = load_data("drugs.txt")
                for d in drugs:
                    if d[0] == item[0]:
                        d[1] = str(int(d[1])-qty)
                        append_data("sales.txt", f"{d[0]}|{qty}|{float(d[2])*qty}|{datetime.now().strftime('%Y-%m-%d %H:%M')}|{pid_e.get()}")
                        break
                save_data("drugs.txt", drugs); messagebox.showinfo("Sold", "Sale Recorded"); verify()

        ttk.Button(vf, text="Verify", style="Primary.TButton", command=verify).pack(side="left")
        ttk.Button(tab, text="Sell Selected", style="Success.TButton", command=sell).pack(pady=10)

    # ====================== MANAGER: SALES REPORTS (3 VIEWS) ======================
    def manager_sales_reports_full(self, tab):
        sub_nb = ttk.Notebook(tab)
        sub_nb.pack(fill="both", expand=True, padx=20, pady=20)
        all_tab = ttk.Frame(sub_nb, style="Main.TFrame"); sub_nb.add(all_tab, text="  All Sales Log  ")
        drug_tab = ttk.Frame(sub_nb, style="Main.TFrame"); sub_nb.add(drug_tab, text="  Summary (By Drug)  ")
        date_tab = ttk.Frame(sub_nb, style="Main.TFrame"); sub_nb.add(date_tab, text="  Report (By Date)  ")

        self.sales_all(all_tab)
        self.sales_by_drug(drug_tab)
        self.sales_by_date(date_tab)

    def sales_all(self, tab):
        tree = ttk.Treeview(tab, columns=("Drug", "Qty", "Total", "Time", "Patient"), show="headings", style="Treeview")
        for c in ("Drug", "Qty", "Total", "Time", "Patient"): tree.heading(c, text=c)
        tree.pack(fill="both", expand=True, padx=10, pady=10)
        lbl_total = ttk.Label(tab, text="Total: 0", font=("Segoe UI", 12, "bold")); lbl_total.pack(pady=5)
        def refresh():
            for i in tree.get_children(): tree.delete(i)
            tot = 0
            for s in load_data("sales.txt"):
                if len(s) >= 4:
                    tree.insert("", "end", values=(s[0], s[1], f"৳{float(s[2]):.2f}", format_datetime(s[3]), s[4] if len(s)>4 else "-"))
                    tot += float(s[2])
            lbl_total.config(text=f"Grand Total Sales: ৳{tot:,.2f}")
        ttk.Button(tab, text="Refresh Log", command=refresh).pack(pady=5); refresh()

    def sales_by_drug(self, tab):
        tree = ttk.Treeview(tab, columns=("Drug", "TotalQty", "TotalSales"), show="headings", style="Treeview")
        for c in ("Drug", "TotalQty", "TotalSales"): tree.heading(c, text=c)
        tree.pack(fill="both", expand=True, padx=10, pady=10)
        def refresh():
            for i in tree.get_children(): tree.delete(i)
            rep = {}
            for s in load_data("sales.txt"):
                if len(s) < 3: continue
                n, q, a = s[0], int(s[1]), float(s[2])
                rep.setdefault(n, [0, 0.0]); rep[n][0] += q; rep[n][1] += a
            for n, (q, a) in sorted(rep.items(), key=lambda x: x[1][1], reverse=True):
                tree.insert("", "end", values=(n, q, f"৳{a:,.2f}"))
        ttk.Button(tab, text="Refresh Summary", command=refresh).pack(pady=5); refresh()

    def sales_by_date(self, tab):
        ctrl = ttk.Frame(tab, style="Main.TFrame"); ctrl.pack(pady=10)
        ttk.Label(ctrl, text="Date (YYYY-MM-DD):").pack(side="left")
        
        today_str = datetime.now().strftime('%Y-%m-%d')
        e_date = ttk.Entry(ctrl, width=15)
        e_date.insert(0, today_str)
        e_date.pack(side="left", padx=5)
        
        tree = ttk.Treeview(tab, columns=("Drug", "Qty", "Total", "Time"), show="headings", style="Treeview")
        for c in ("Drug", "Qty", "Total", "Time"): tree.heading(c, text=c)
        tree.pack(fill="both", expand=True, padx=10)
        
        lbl_res = ttk.Label(tab, text="", font=("Segoe UI", 12, "bold")); lbl_res.pack(pady=5)

        def search():
            d = e_date.get().strip()
            if not d: return
            for i in tree.get_children(): tree.delete(i)
            tot = 0
            for s in load_data("sales.txt"):
                if len(s)>3 and s[3].startswith(d):
                    tree.insert("", "end", values=(s[0], s[1], f"৳{float(s[2]):.2f}", format_datetime(s[3])))
                    tot += float(s[2])
            lbl_res.config(text=f"Total for {d}: ৳{tot:,.2f}")

        ttk.Button(ctrl, text="Search", style="Primary.TButton", command=search).pack(side="left", padx=5)
        
        search()