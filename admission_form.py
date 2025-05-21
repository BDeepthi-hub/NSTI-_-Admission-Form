import tkinter as tk
from tkinter import ttk, messagebox
import json
import csv
import os

# Load trade details
with open("trades.json", "r") as f:
    trade_data = json.load(f)

# Load NSTI locations
with open("nsti_locations.txt", "r") as f:
    locations = [line.strip() for line in f.readlines()]

# Create CSV if it doesn't exist
csv_file = "admissions.csv"
if not os.path.exists(csv_file):
    with open(csv_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Age", "Trade", "Location"])

# Main Window
root = tk.Tk()
root.title("NSTI Admission Form")
root.geometry("500x520")
root.resizable(False, False)

tk.Label(root, text="NSTI Admission Form", font=("Arial", 16, "bold")).pack(pady=10)

# Name Entry
tk.Label(root, text="Full Name").pack()
entry_name = tk.Entry(root, width=50)
entry_name.pack(pady=5)

# Age Entry
tk.Label(root, text="Age").pack()
entry_age = tk.Entry(root, width=50)
entry_age.pack(pady=5)

# Trade Dropdown
tk.Label(root, text="Select Trade").pack()
trade_var = tk.StringVar()
trade_combo = ttk.Combobox(root, textvariable=trade_var, values=list(trade_data.keys()), state="readonly", width=47)
trade_combo.pack(pady=5)

# Show Trade Details
def show_trade_details():
    trade = trade_var.get()
    detail = trade_data.get(trade, "No details available.")
    messagebox.showinfo(f"{trade} Details", detail)

tk.Button(root, text="View Trade Details", command=show_trade_details).pack(pady=5)

# Location Dropdown
tk.Label(root, text="Select NSTI Location").pack()
location_var = tk.StringVar()
location_combo = ttk.Combobox(root, textvariable=location_var, values=locations, state="readonly", width=47)
location_combo.pack(pady=5)

# Submit Form
def submit_form():
    name = entry_name.get().strip()
    age = entry_age.get().strip()
    trade = trade_var.get()
    location = location_var.get()

    if not name or not age or not trade or not location:
        messagebox.showerror("Error", "Please fill all fields.")
        return
    if not age.isdigit() or int(age) <= 0:
        messagebox.showerror("Error", "Enter a valid age.")
        return

    with open(csv_file, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([name, age, trade, location])

    messagebox.showinfo("Success", "Form submitted successfully!")
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    trade_var.set("")
    location_var.set("")

tk.Button(root, text="Submit", command=submit_form, bg="green", fg="white", width=20).pack(pady=20)

# View Submissions
def view_submissions():
    if not os.path.exists(csv_file):
        messagebox.showinfo("No Data", "No submissions yet.")
        return

    win = tk.Toplevel(root)
    win.title("All Submissions")
    win.geometry("600x300")

    tree = ttk.Treeview(win, columns=("Name", "Age", "Trade", "Location"), show="headings")
    tree.heading("Name", text="Name")
    tree.heading("Age", text="Age")
    tree.heading("Trade", text="Trade")
    tree.heading("Location", text="Location")
    tree.pack(fill=tk.BOTH, expand=True)

    with open(csv_file, "r") as file:
        reader = csv.reader(file)
        next(reader)  # skip header
        for row in reader:
            tree.insert("", tk.END, values=row)

tk.Button(root, text="View All Submissions", command=view_submissions, bg="blue", fg="white", width=20).pack(pady=5)

# Exit
tk.Button(root, text="Exit", command=root.destroy).pack(pady=5)

root.mainloop()

