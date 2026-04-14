import pandas as pd
import tkinter as tk
from tkinter import ttk

# Load data
df = pd.read_csv(r"C:\Users\goust\PycharmProjects\Hyrox_Project\data\london_2021_2023.csv")

# Convert time columns to HH:MM:SS
for col in ["total_time", "work_time", "roxzone_time", "run_time"]:
    df[col] = df[col].apply(lambda x: str(pd.to_timedelta(x)).split()[-1])


# Functions
def filter_data():
    gender = gender_var.get()
    age_group = age_var.get()
    division = division_var.get()

    filtered = df.copy()

    if gender != "all":
        filtered = filtered[filtered["gender"].str.lower() == gender.lower()]

    if age_group != "all":
        filtered = filtered[filtered["age_group"] == age_group]

    if division != "all":
        filtered = filtered[filtered["division"].str.lower() == division.lower()]

    filtered = filtered.drop_duplicates()

    filtered["total_seconds"] = filtered["total_time"].apply(
        lambda t: sum(int(x) * 60 ** i for i, x in enumerate(reversed(t.split(":"))))
    )

    filtered = filtered.sort_values("total_seconds")
    filtered = filtered.drop(columns=["total_seconds"])

    display_data(filtered)


def display_data(filtered):
    for i in tree.get_children():
        tree.delete(i)

    for i, row in filtered.iterrows():
        tree.insert("", "end", values=[row[col] for col in columns])


def update_total(*args):
    try:
        work = pd.to_timedelta(work_entry.get())
        rox = pd.to_timedelta(rox_entry.get())
        run = pd.to_timedelta(run_entry.get())

        total_var.set(f"{(work + rox + run)}".split()[-1])
    except:
        total_var.set("")


def analyze_my_result():
    update_total()

    gender = gender_var.get()
    age_group = age_var.get()
    division = division_var.get()

    filtered = df.copy()

    if gender != "all":
        filtered = filtered[filtered["gender"].str.lower() == gender.lower()]

    if age_group != "all":
        filtered = filtered[filtered["age_group"] == age_group]

    if division != "all":
        filtered = filtered[filtered["division"].str.lower() == division.lower()]

    filtered = filtered.drop_duplicates()

    time_cols = ["total_time", "work_time", "roxzone_time", "run_time"]

    for col in time_cols:
        filtered[f"{col}_seconds"] = filtered[col].apply(
            lambda t: sum(int(x) * 60 ** i for i, x in enumerate(reversed(t.split(":"))))
        )

    try:
        my_times = {
            col: pd.to_timedelta(entry.get()).total_seconds()
            for col, entry in zip(time_cols[1:], [work_entry, rox_entry, run_entry])
        }

        my_times["total_time"] = pd.to_timedelta(total_var.get()).total_seconds()

    except:
        analysis_label.config(text="Invalid time format")
        improvement_label.config(text="")
        return

    # Analysis
    analysis_text = ""
    improvement_text = ""

    for col in time_cols:
        all_seconds = filtered[f"{col}_seconds"].tolist() + [my_times[col]]
        all_seconds_sorted = sorted(all_seconds)

        place = all_seconds_sorted.index(my_times[col]) + 1
        total_athletes = len(all_seconds_sorted)

        analysis_text += f"{entry_label(col)}: position {place} out of {total_athletes} athletes\n"

        best = min(all_seconds_sorted)
        diff_sec = my_times[col] - best

        if diff_sec > 0:
            diff_min = int(diff_sec // 60)
            diff_sec_rem = int(diff_sec % 60)

            improvement_text += (
                f"To be 1st in {entry_label(col)}, improve by {diff_min}:{diff_sec_rem:02d}\n"
            )
        else:
            improvement_text += f"You are the best in {entry_label(col)}!\n"

    analysis_label.config(text=analysis_text.strip())
    improvement_label.config(text=improvement_text.strip())


def entry_label(col):
    labels = {
        "total_time": "total",
        "work_time": "work",
        "roxzone_time": "roxzone",
        "run_time": "run"
    }
    return labels.get(col, col)


# GUI
root = tk.Tk()
root.title("Athlete Analysis")

# Filters
filter_frame = tk.Frame(root)
filter_frame.pack(pady=10)

gender_var = tk.StringVar(value="all")
tk.Label(filter_frame, text="Gender:").grid(row=0, column=0, padx=5)

gender_dropdown = ttk.Combobox(
    filter_frame,
    textvariable=gender_var,
    values=["all", "male", "female"],
    state="readonly",
    width=10
)
gender_dropdown.grid(row=0, column=1, padx=5)

age_var = tk.StringVar(value="all")
tk.Label(filter_frame, text="Age:").grid(row=0, column=2, padx=5)

age_options = ["all"] + sorted(df["age_group"].unique())
age_dropdown = ttk.Combobox(
    filter_frame,
    textvariable=age_var,
    values=age_options,
    state="readonly",
    width=10
)
age_dropdown.grid(row=0, column=3, padx=5)

division_var = tk.StringVar(value="all")
tk.Label(filter_frame, text="Division:").grid(row=0, column=4, padx=5)

division_dropdown = ttk.Combobox(
    filter_frame,
    textvariable=division_var,
    values=["all", "open", "pro"],
    state="readonly",
    width=10
)
division_dropdown.grid(row=0, column=5, padx=5)

filter_button = tk.Button(filter_frame, text="Filter", command=filter_data)
filter_button.grid(row=0, column=6, padx=10)

# Input section
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

total_var = tk.StringVar()
tk.Label(input_frame, text="Your total time:").grid(row=0, column=0, padx=5)

total_entry = tk.Entry(input_frame, textvariable=total_var, width=10, state="readonly")
total_entry.grid(row=0, column=1, padx=5)

tk.Label(input_frame, text="Your work time:").grid(row=0, column=2, padx=5)
work_entry = tk.Entry(input_frame, width=10)
work_entry.grid(row=0, column=3, padx=5)
work_entry.insert(0, "0:30:00")
work_entry.bind("<KeyRelease>", update_total)

tk.Label(input_frame, text="Your roxzone time:").grid(row=0, column=4, padx=5)
rox_entry = tk.Entry(input_frame, width=10)
rox_entry.grid(row=0, column=5, padx=5)
rox_entry.insert(0, "0:05:00")
rox_entry.bind("<KeyRelease>", update_total)

tk.Label(input_frame, text="Your run time:").grid(row=0, column=6, padx=5)
run_entry = tk.Entry(input_frame, width=10)
run_entry.grid(row=0, column=7, padx=5)
run_entry.insert(0, "0:34:00")
run_entry.bind("<KeyRelease>", update_total)

analyze_button = tk.Button(input_frame, text="Analyze", command=analyze_my_result)
analyze_button.grid(row=0, column=8, padx=10)

# Labels
analysis_label = tk.Label(root, text="", fg="blue", justify="left")
analysis_label.pack(pady=2)

improvement_label = tk.Label(root, text="", fg="green", justify="left")
improvement_label.pack(pady=2)

update_total()

# Table
columns = [
    "event_name", "gender", "nationality", "age_group", "division",
    "total_time", "work_time", "roxzone_time", "run_time"
]

tree = ttk.Treeview(root, columns=columns, show="headings", height=15)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100, anchor="center")

tree.pack(fill=tk.BOTH, expand=True)

root.mainloop()