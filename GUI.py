# I acknowledge the use of Microsoft Copilot (AI) to assist me in reviewing.
# The final implementation, testing, and submission were completed independently.

import csv
import os
import tkinter as tk
from tkinter import ttk, messagebox
import sys

# Load subjects from CSV file
def load_subjects(filename):
    subjects = []
    try:
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader) # Skip the header row since it's just labels
            for row in reader:
                if len(row) >= 2:
                    # Store subject name and classmark (always uppercase for consistency)
                    subjects.append({'subject': row[0], 'classmark': row[1].upper()})
    except Exception as e:
        # Show a popup error if something goes wrong
        messagebox.showerror("Error", f"Error loading subjects: {e}")
    return subjects

# Load locations from CSV file
def load_locations(filename):
    locations = {}
    try:
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader) # Skip header row
            for row in reader:
                if len(row) >= 2:
                    # Store classmark as key and location as value
                    locations[row[0].upper()] = row[1]
    except Exception as e:
        messagebox.showerror("Error", f"Error loading locations: {e}")
    return locations

# Figure out where this script is running from
script_dir = os.path.dirname(os.path.abspath(__file__))
subjects_file = os.path.join(script_dir, 'subjects.csv')
locations_file = os.path.join(script_dir, 'locations.csv')

# Load data from CSV files
subjects = load_subjects(subjects_file)
locations = load_locations(locations_file)

# If data fails to load, stop the program politely
if not subjects or not locations:
    root_tmp = tk.Tk()
    root_tmp.withdraw()   # Hide the temporary window
    messagebox.showerror("Error", "Could not load CSV files. Make sure subjects.csv and locations.csv are in the same folder as this script.")
    root_tmp.destroy()
    sys.exit(1)

# Perform search based on current mode
def perform_search(event=None):
    query = query_entry.get().strip().lower()
    # Ignore placeholder hint if user hasn’t typed anything
    if query == hint_texts.get(current_mode, "").lower():
        query = ""   
    results_table.delete(*results_table.get_children())  # Clear previous results

    if not query:
        messagebox.showwarning("Missing Input", "Please enter a search query.")
        return

    # Save query to history if new
    if query not in search_history:
        search_history.append(query)
        update_history_listbox()

    count = 0
    for item in subjects:
        subject = item['subject']
        classmark = item['classmark']
        location = locations.get(classmark, "Unknown location")

        # Decide what to match based on mode
        match = (
            current_mode == "Subject" and query in subject.lower() or
            current_mode == "Classmark" and query == classmark.lower() or
            current_mode == "Location" and query in location.lower()
        )

        if match:
            # Alternate row colors for readability
            tag = 'evenrow' if count % 2 == 0 else 'oddrow'
            results_table.insert("", "end", values=(subject, classmark, location), tags=(tag,))
            count += 1

    # Update status label with results count
    if count == 0:
        results_table.insert("", "end", values=("No matches found", "", ""))
        status_label.config(text="0 results found.")
    else:
        status_label.config(text=f"{count} result(s) found.")

# Clear search field and results
def clear_all():
    query_entry.delete(0, tk.END)
    update_hint()
    results_table.delete(*results_table.get_children())
    status_label.config(text="")

# Exit
def exit_app():
    root.quit()

# Update placeholder hint
def update_hint():
    hint = hint_texts.get(current_mode, "")
    query_entry.delete(0, tk.END)
    query_entry.insert(0, hint)
    query_entry.config(fg="gray")

# Clear hint on focus
def clear_hint(event):
    if query_entry.cget("fg") == "gray":
        query_entry.delete(0, tk.END)
        query_entry.config(fg="black")

# Set search mode and update colours (Subject / Classmark / Location)
def set_mode(mode):
    global current_mode
    current_mode = mode
    # Highlight the active button
    for m, b in mode_buttons.items():
        if m == mode:
            b.config(bg="#2C6DA2", fg="black")
        else:
            b.config(bg="SystemButtonFace", fg="black")
    update_hint()

# Update search history listbox
def update_history_listbox():
    history_listbox.delete(0, tk.END)
    for item in reversed(search_history[-10:]):  # Show last 10 searches
        history_listbox.insert(tk.END, item)

# Re-run search from history
def on_history_select(event):
    selected = history_listbox.curselection()
    if selected:
        query_entry.delete(0, tk.END)
        query_entry.insert(0, history_listbox.get(selected[0]))
        perform_search()

# Hint texts for each mode
hint_texts = {
    "Subject": "e.g. English",
    "Classmark": "e.g. CC",
    "Location": "e.g. Top Floor"
}



# ---------------GUI setup-----------------
root = tk.Tk()
root.title("📘 Library Book Finder")
root.geometry("850x700")
root.configure(bg="#F5F5F5")

# Styles
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))
style.configure("Treeview", font=("Segoe UI", 10), rowheight=25)
style.map("TButton", background=[("active", "#744d6007")])

# Title
title_label = tk.Label(root, text="FindMyBook", font=("Helvetica", 16, "bold"), bg="#003366", fg="white")
title_label.pack(fill=tk.X, pady=20)

# Query frame
query_frame = tk.Frame(root, bg="#fdf6f0")
query_frame.pack(pady=5)

tk.Label(query_frame, text="🔍 Enter Query:", font=("Helvetica", 11), bg="#fdf6f0").grid(row=0, column=0, padx=5)
query_entry = tk.Entry(query_frame, width=50, font=("Helvetica", 11))
query_entry.grid(row=0, column=1, padx=5)
query_entry.bind("<Return>", perform_search)
query_entry.bind("<FocusIn>", clear_hint)

search_btn = tk.Button(query_frame, text="Search", command=perform_search, font=("Helvetica", 11), bg="#26343A", fg="white")
search_btn.grid(row=0, column=2, padx=5)

# Filter buttons
filter_frame = tk.Frame(root, bg="#fdf6f0")
filter_frame.pack(pady=10)

tk.Label(filter_frame, text="Filter by:", font=("Helvetica", 11), bg="#fdf6f0").pack(side=tk.LEFT, padx=5)

mode_buttons = {}
current_mode = "Subject"
search_history = []

for mode in ["Subject", "Classmark", "Location"]:
    btn = tk.Button(filter_frame, text=mode, width=12, font=("Helvetica", 11),
                    command=lambda m=mode: set_mode(m))
    btn.pack(side=tk.LEFT, padx=5)
    mode_buttons[mode] = btn

set_mode("Subject")  # Default mode is Subject

# Results label
tk.Label(root, text="Output:", font=("Helvetica", 10, "bold"), bg="#fdf6f0").pack(pady=5)

# Results table
table_frame = tk.Frame(root)
table_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

columns = ("Subject", "Classmark", "Location")
results_table = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
for col in columns:
    results_table.heading(col, text=col)
    results_table.column(col, anchor=tk.CENTER, stretch=True)
results_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=results_table.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
results_table.configure(yscrollcommand=scrollbar.set)

results_table.tag_configure('oddrow', background='#f9f9f9')
results_table.tag_configure('evenrow', background='#e6e6e6')

# Status label
status_label = tk.Label(root, text="", font=("Helvetica", 10), bg="#fdf6f0")
status_label.pack(pady=5)

# Search History Label
tk.Label(root, text="Search History:", font=("Helvetica", 11, "bold"), bg="#fdf6f0").pack(pady=(10, 0))

# History Listbox
history_listbox = tk.Listbox(root, height=4, font=("Helvetica", 10))
history_listbox.pack(padx=10, pady=(0, 10), fill=tk.X)
history_listbox.bind("<<ListboxSelect>>", on_history_select)

# Action buttons
action_frame = tk.Frame(root, bg="#fdf6f0")
action_frame.pack(pady=15)

tk.Button(action_frame, text="Clear", command=clear_all, width=12, font=("Helvetica", 11), bg="#1F2938", fg="white").grid(row=0, column=0, padx=10)
tk.Button(action_frame, text="Exit", command=exit_app, width=12, font=("Helvetica", 11), bg="#1D2225", fg="white").grid(row=0, column=1, padx=10)

root.mainloop()
 