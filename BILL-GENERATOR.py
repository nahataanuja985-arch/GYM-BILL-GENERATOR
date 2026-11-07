"""
Project Name: Gym Products Bill Generator
Shop Name: FITNESS HUB
Framework: Tkinter (Built-in Python GUI)
Architecture: Modular Functions with Tkinter StringVar tracking for simple viva explanations.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import random
import os

# ==========================================
# 1. FIXED PRODUCT CATALOGUE & CONFIGURATION
# ==========================================
PRODUCTS = [
    {"name": "Whey Protein (1 kg)", "price": 2499},
    {"name": "Creatine Monohydrate (250 g)", "price": 799},
    {"name": "Protein Shaker", "price": 199},
    {"name": "Gym Gloves", "price": 299},
    {"name": "Resistance Bands", "price": 399},
    {"name": "Skipping Rope", "price": 149},
]

GST_RATE = 0.18  # 18% GST

# ==========================================
# 2. APPLICATION CLASS
# ==========================================
class GymBillingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FITNESS HUB - Gym Products Billing System")
        self.root.geometry("1100x680")
        self.root.resizable(False, False)

        # Color Palette
        self.PRIMARY_COLOR = "#1f2937"    # Dark Charcoal
        self.ACCENT_COLOR = "#2563eb"     # Royal Blue
        self.BG_COLOR = "#f3f4f6"         # Light Gray background
        self.PANEL_BG = "#ffffff"         # White containers
        self.TEXT_COLOR = "#111827"

        self.root.configure(bg=self.BG_COLOR)

        # Trackers
        self.bill_no_var = tk.StringVar()
        self.date_time_var = tk.StringVar()
        self.customer_name_var = tk.StringVar()
        self.customer_mobile_var = tk.StringVar()

        self.subtotal_var = tk.StringVar(value="₹ 0.00")
        self.gst_var = tk.StringVar(value="₹ 0.00")
        self.grand_total_var = tk.StringVar(value="₹ 0.00")

        # Product row state dictionaries
        self.product_data = []

        # Build UI layout
        self._setup_header()
        self._setup_customer_frame()
        self._setup_main_area()
        self._setup_summary_and_actions()

        # Initialize defaults
        self.reset_form()

    # ---------------- UI BUILDERS ----------------

    def _setup_header(self):
        header_frame = tk.Frame(self.root, bg=self.PRIMARY_COLOR, pady=12)
        header_frame.pack(fill=tk.X)

        title = tk.Label(
            header_frame,
            text="FITNESS HUB",
            font=("Segoe UI", 20, "bold"),
            fg="#f9fafb",
            bg=self.PRIMARY_COLOR,
        )
        title.pack()

        subtitle = tk.Label(
            header_frame,
            text="Premium Supplements & Fitness Accessories Billing Counter",
            font=("Segoe UI", 10),
            fg="#9ca3af",
            bg=self.PRIMARY_COLOR,
        )
        subtitle.pack()

    def _setup_customer_frame(self):
        cust_frame = tk.LabelFrame(
            self.root,
            text=" Customer & Invoice Details ",
            font=("Segoe UI", 10, "bold"),
            bg=self.PANEL_BG,
            fg=self.PRIMARY_COLOR,
            padx=15,
            pady=10,
        )
        cust_frame.pack(fill=tk.X, padx=15, pady=8)

        # Row 1: Bill No & Date (Auto-generated & Read-only)
        tk.Label(cust_frame, text="Bill No:", font=("Segoe UI", 9, "bold"), bg=self.PANEL_BG).grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
        tk.Entry(cust_frame, textvariable=self.bill_no_var, state="readonly", width=16, font=("Segoe UI", 9), relief=tk.SOLID, bd=1).grid(row=0, column=1, padx=5, pady=3)

        tk.Label(cust_frame, text="Date & Time:", font=("Segoe UI", 9, "bold"), bg=self.PANEL_BG).grid(row=0, column=2, sticky=tk.W, padx=(25, 5), pady=3)
        tk.Entry(cust_frame, textvariable=self.date_time_var, state="readonly", width=22, font=("Segoe UI", 9), relief=tk.SOLID, bd=1).grid(row=0, column=3, padx=5, pady=3)

        # Row 2: Customer Inputs
        tk.Label(cust_frame, text="Customer Name:", font=("Segoe UI", 9, "bold"), bg=self.PANEL_BG).grid(row=1, column=0, sticky=tk.W, padx=5, pady=3)
        self.entry_name = tk.Entry(cust_frame, textvariable=self.customer_name_var, width=22, font=("Segoe UI", 9), relief=tk.SOLID, bd=1)
        self.entry_name.grid(row=1, column=1, padx=5, pady=3)

        tk.Label(cust_frame, text="Mobile Number:", font=("Segoe UI", 9, "bold"), bg=self.PANEL_BG).grid(row=1, column=2, sticky=tk.W, padx=(25, 5), pady=3)
        self.entry_mobile = tk.Entry(cust_frame, textvariable=self.customer_mobile_var, width=22, font=("Segoe UI", 9), relief=tk.SOLID, bd=1)
        self.entry_mobile.grid(row=1, column=3, padx=5, pady=3)

    def _setup_main_area(self):
        container = tk.Frame(self.root, bg=self.BG_COLOR)
        container.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        # Left Column: Product Selection Grid
        left_frame = tk.LabelFrame(
            container,
            text=" Product Catalogue & Quantities ",
            font=("Segoe UI", 10, "bold"),
            bg=self.PANEL_BG,
            fg=self.PRIMARY_COLOR,
            padx=10,
            pady=10,
        )
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Column Headers
        headers = ["Select", "Product Name", "Price (₹)", "Qty", "Item Total (₹)"]
        col_widths = [6, 24, 10, 8, 12]
        for col_idx, (heading, w) in enumerate(zip(headers, col_widths)):
            lbl = tk.Label(
                left_frame,
                text=heading,
                font=("Segoe UI", 9, "bold"),
                bg="#e5e7eb",
                fg=self.TEXT_COLOR,
                relief=tk.FLAT,
                pady=4,
                width=w,
            )
            lbl.grid(row=0, column=col_idx, padx=2, pady=4, sticky="nsew")

        # Populate rows from fixed catalog
        for idx, item in enumerate(PRODUCTS, start=1):
            is_selected = tk.BooleanVar(value=False)
            qty_var = tk.StringVar(value="0")
            item_total_var = tk.StringVar(value="0.00")

            # Checkbox
            chk = tk.Checkbutton(
                left_frame,
                variable=is_selected,
                bg=self.PANEL_BG,
                activebackground=self.PANEL_BG,
                command=self.calculate_totals,
            )
            chk.grid(row=idx, column=0, pady=3)

            # Product Name (Fixed label)
            p_name = tk.Label(
                left_frame,
                text=item["name"],
                anchor=tk.W,
                font=("Segoe UI", 9),
                bg=self.PANEL_BG,
            )
            p_name.grid(row=idx, column=1, sticky=tk.W, padx=5, pady=3)

            # Unit Price (Fixed label)
            p_price = tk.Label(
                left_frame,
                text=f"{item['price']}",
                font=("Segoe UI", 9),
                bg=self.PANEL_BG,
            )
            p_price.grid(row=idx, column=2, padx=5, pady=3)

            # Quantity Spinbox
            qty_spin = tk.Spinbox(
                left_frame,
                from_=0,
                to=99,
                width=5,
                textvariable=qty_var,
                font=("Segoe UI", 9),
                relief=tk.SOLID,
                bd=1,
                command=self.calculate_totals,
            )
            qty_spin.grid(row=idx, column=3, padx=5, pady=3)
            qty_spin.bind("<KeyRelease>", lambda event: self.calculate_totals())

            # Row Subtotal
            lbl_total = tk.Label(
                left_frame,
                textvariable=item_total_var,
                font=("Segoe UI", 9, "bold"),
                fg="#059669",
                bg=self.PANEL_BG,
            )
            lbl_total.grid(row=idx, column=4, padx=5, pady=3)

            self.product_data.append({
                "name": item["name"],
                "price": item["price"],
                "selected": is_selected,
                "qty": qty_var,
                "total": item_total_var,
            })

        # Right Column: Bill Output Preview Area
        right_frame = tk.LabelFrame(
            container,
            text=" Bill Preview ",
            font=("Segoe UI", 10, "bold"),
            bg=self.PANEL_BG,
            fg=self.PRIMARY_COLOR,
            padx=10,
            pady=10,
        )
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.bill_text_area = tk.Text(
            right_frame,
            width=46,
            height=18,
            font=("Courier New", 9),
            relief=tk.SOLID,
            bd=1,
            bg="#fdfdfd",
        )
        self.bill_text_area.pack(fill=tk.BOTH, expand=True)

    def _setup_summary_and_actions(self):
        bottom_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        bottom_frame.pack(fill=tk.X, padx=15, pady=(0, 10))

        # Calculation Metrics Display
        summary_frame = tk.Frame(bottom_frame, bg=self.PANEL_BG, relief=tk.SOLID, bd=1, padx=15, pady=8)
        summary_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        tk.Label(summary_frame, text="Subtotal:", font=("Segoe UI", 9), bg=self.PANEL_BG).grid(row=0, column=0, sticky=tk.W, padx=10)
        tk.Label(summary_frame, textvariable=self.subtotal_var, font=("Segoe UI", 9, "bold"), bg=self.PANEL_BG).grid(row=0, column=1, sticky=tk.W)

        tk.Label(summary_frame, text="GST (18%):", font=("Segoe UI", 9), bg=self.PANEL_BG).grid(row=0, column=2, sticky=tk.W, padx=(20, 10))
        tk.Label(summary_frame, textvariable=self.gst_var, font=("Segoe UI", 9, "bold"), bg=self.PANEL_BG).grid(row=0, column=3, sticky=tk.W)

        tk.Label(summary_frame, text="Grand Total:", font=("Segoe UI", 10, "bold"), fg="#b91c1c", bg=self.PANEL_BG).grid(row=0, column=4, sticky=tk.W, padx=(25, 10))
        tk.Label(summary_frame, textvariable=self.grand_total_var, font=("Segoe UI", 11, "bold"), fg="#b91c1c", bg=self.PANEL_BG).grid(row=0, column=5, sticky=tk.W)

        # Action Buttons
        btn_frame = tk.Frame(bottom_frame, bg=self.BG_COLOR)
        btn_frame.pack(side=tk.RIGHT, padx=(10, 0))

        btn_calculate = tk.Button(
            btn_frame,
            text="Recalculate",
            font=("Segoe UI", 9, "bold"),
            bg="#4b5563",
            fg="white",
            relief=tk.FLAT,
            padx=12,
            pady=5,
            command=self.calculate_totals,
        )
        btn_calculate.pack(side=tk.LEFT, padx=3)

        btn_generate = tk.Button(
            btn_frame,
            text="Generate Bill",
            font=("Segoe UI", 9, "bold"),
            bg=self.ACCENT_COLOR,
            fg="white",
            relief=tk.FLAT,
            padx=14,
            pady=5,
            command=self.generate_bill,
        )
        btn_generate.pack(side=tk.LEFT, padx=3)

        btn_save = tk.Button(
            btn_frame,
            text="Save Bill",
            font=("Segoe UI", 9, "bold"),
            bg="#059669",
            fg="white",
            relief=tk.FLAT,
            padx=12,
            pady=5,
            command=self.save_bill_file,
        )
        btn_save.pack(side=tk.LEFT, padx=3)

        btn_reset = tk.Button(
            btn_frame,
            text="Reset",
            font=("Segoe UI", 9, "bold"),
            bg="#dc2626",
            fg="white",
            relief=tk.FLAT,
            padx=12,
            pady=5,
            command=self.reset_form,
        )
        btn_reset.pack(side=tk.LEFT, padx=3)

    # ---------------- BUSINESS LOGIC ----------------

    def calculate_totals(self):
        """Calculates row totals, subtotal, 18% GST, and grand total."""
        subtotal = 0.0

        for row in self.product_data:
            qty_raw = row["qty"].get().strip()

            # Input validation: Ensure integer quantity
            if not qty_raw.isdigit():
                qty = 0
            else:
                qty = int(qty_raw)

            # If checkbox is ticked but qty is 0, bump qty to 1 for quick selection
            if row["selected"].get() and qty == 0:
                qty = 1
                row["qty"].set("1")
            elif not row["selected"].get() and qty > 0:
                # If quantity entered, auto-check the product
                row["selected"].set(True)

            row_total = row["price"] * qty if row["selected"].get() else 0.0
            row["total"].set(f"{row_total:.2f}")

            subtotal += row_total

        gst = subtotal * GST_RATE
        grand_total = subtotal + gst

        self.subtotal_var.set(f"₹ {subtotal:.2f}")
        self.gst_var.set(f"₹ {gst:.2f}")
        self.grand_total_var.set(f"₹ {grand_total:.2f}")

        return subtotal, gst, grand_total

    def generate_bill(self):
        """Validates inputs and renders formatted receipt on the Text widget."""
        name = self.customer_name_var.get().strip()
        mobile = self.customer_mobile_var.get().strip()

        # Customer validation
        if not name:
            messagebox.showwarning("Validation Error", "Please enter the Customer Name.")
            self.entry_name.focus_set()
            return

        if not mobile or not mobile.isdigit() or len(mobile) != 10:
            messagebox.showwarning("Validation Error", "Please enter a valid 10-digit mobile number.")
            self.entry_mobile.focus_set()
            return

        subtotal, gst, grand_total = self.calculate_totals()

        # Validate that at least one item was purchased
        items_to_print = []
        for row in self.product_data:
            if row["selected"].get() and int(row["qty"].get()) > 0:
                items_to_print.append({
                    "name": row["name"],
                    "qty": int(row["qty"].get()),
                    "price": row["price"],
                    "total": float(row["total"].get()),
                })

        if not items_to_print:
            messagebox.showwarning("Cart Empty", "Please select at least one product with quantity > 0.")
            return

        # Build Bill Template
        bill_lines = []
        bill_lines.append("=" * 44)
        bill_lines.append("                FITNESS HUB                 ")
        bill_lines.append("      Supplements & Accessories Store       ")
        bill_lines.append("=" * 44)
        bill_lines.append(f"Bill No : {self.bill_no_var.get():<14} Date: {self.date_time_var.get().split()[0]}")
        bill_lines.append(f"Customer: {name[:16]:<16} Time: {self.date_time_var.get().split()[1]}")
        bill_lines.append(f"Phone   : {mobile:<20}")
        bill_lines.append("-" * 44)
        bill_lines.append(f"{'Item':<18}{'Price':>7}{'Qty':>5}{'Total':>10}")
        bill_lines.append("-" * 44)

        for item in items_to_print:
            short_name = (item["name"][:16] + "..") if len(item["name"]) > 17 else item["name"]
            line = f"{short_name:<18}{item['price']:>7.0f}{item['qty']:>5}{item['total']:>10.2f}"
            bill_lines.append(line)

        bill_lines.append("-" * 44)
        bill_lines.append(f"{'Subtotal:':<30} ₹ {subtotal:>9.2f}")
        bill_lines.append(f"{'GST (18%):':<30} ₹ {gst:>9.2f}")
        bill_lines.append("=" * 44)
        bill_lines.append(f"{'GRAND TOTAL:':<30} ₹ {grand_total:>9.2f}")
        bill_lines.append("=" * 44)
        bill_lines.append("          Thank you for choosing us!        ")
        bill_lines.append("            Stay Fit, Stay Strong!          ")
        bill_lines.append("=" * 44)

        bill_content = "\n".join(bill_lines)

        # Render in text view
        self.bill_text_area.delete("1.0", tk.END)
        self.bill_text_area.insert(tk.END, bill_content)

    def save_bill_file(self):
        """Saves current receipt to a .txt file on disk."""
        content = self.bill_text_area.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Notice", "Generate a bill first before saving.")
            return

        folder = "bills"
        if not os.path.exists(folder):
            os.makedirs(folder)

        file_path = os.path.join(folder, f"{self.bill_no_var.get()}.txt")
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            messagebox.showinfo("Saved", f"Bill saved successfully to:\n{os.path.abspath(file_path)}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save bill: {str(e)}")

    def reset_form(self):
        """Clears all customer details, resets quantities, and generates a new bill ID."""
        # Auto-generate Bill ID and current Timestamp
        new_bill_id = f"FH-{random.randint(1000, 9999)}"
        self.bill_no_var.set(new_bill_id)
        self.date_time_var.set(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

        self.customer_name_var.set("")
        self.customer_mobile_var.set("")

        # Reset all product selections
        for row in self.product_data:
            row["selected"].set(False)
            row["qty"].set("0")
            row["total"].set("0.00")

        self.subtotal_var.set("₹ 0.00")
        self.gst_var.set("₹ 0.00")
        self.grand_total_var.set("₹ 0.00")

        self.bill_text_area.delete("1.0", tk.END)


# ==========================================
# 3. APPLICATION ENTRY POINT
# ==========================================
if __name__ == "__main__":
    window = tk.Tk()
    app = GymBillingApp(window)
    window.mainloop()