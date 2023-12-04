import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy import create_engine
from db import Base


# Validation functions
def validate_non_empty(entry):
    return entry.get().strip() != ""


def validate_department_code(entry):
    return len(entry.get().strip()) <= 4 and entry.get().strip().isalnum()


def validate_email(entry):
    # simple email validation (can be improved)
    return "@" in entry.get().strip() and "." in entry.get().strip()


def validate_course_id(entry):
    # Example validation for course ID (can be improved)
    return entry.get().strip().isalnum() and len(entry.get().strip()) == 7


def validate_section_id(entry):
    # Example validation for section ID (can be improved)
    return entry.get().strip().isdigit() and len(entry.get().strip()) <= 3


def validate_department_id(entry):
    # Add appropriate validation for department ID
    return entry.get().strip().isdigit()


def validate_person_in_charge_id(entry):
    # Add appropriate validation for person in charge ID
    return entry.get().strip().isdigit()


def validate_enrollment_count(entry):
    # Add appropriate validation for enrollment count
    print(entry.get().strip().isdigit())
    return entry.get().strip().isdigit()


def validate_semester(entry):
    # Add appropriate validation for semester (e.g., format like 'Fall 2023')
    return entry.get().strip().isalpha() and len(entry.get().strip().split()) == 2


validation_functions = {
    "Code": validate_department_code,
    "Email": validate_email,
    "ID": validate_course_id,  # Assuming this is for course ID
    "Department ID": validate_department_id,
    "Person in Charge ID": validate_person_in_charge_id,
    "Enrollment Count": validate_enrollment_count,
    "Semester": validate_semester,
    # Add other specific validations as needed
}


def set_entry_validity(entry, is_valid):
    if is_valid:
        entry.config(foreground="black")
    else:
        entry.config(foreground="red")


def check_entries(entries, submit_button):
    all_valid = True
    for field, entry in entries.items():
        is_valid = validate_non_empty(entry) and validation_functions.get(
            field, lambda e: True
        )(entry)
        set_entry_validity(entry, is_valid)
        all_valid &= is_valid
    submit_button.config(state="normal" if all_valid else "disabled")


# Handler for data submission
def handle_data_submission(entries, status_label):
    is_valid = all(validate_non_empty(entry) for entry in entries.values())
    if is_valid:
        data = {field: entry.get() for field, entry in entries.items()}
        print("Data Submitted:", data)
        status_label.config(text="Data successfully submitted.", fg="green")
    else:
        status_label.config(text="Invalid data in some fields.", fg="red")


# Function to add data fields to a tab
def add_data_fields(tab, field_names, validation_functions, status_label):
    entries = {}
    for field in field_names:
        frame = tk.Frame(tab)
        frame.pack(side="top", fill="x", padx=5, pady=5)

        label = tk.Label(frame, text=field, width=20)
        label.pack(side="left")

        entry = tk.Entry(frame, highlightthickness=1)
        entry.pack(side="right", expand=True, fill="x")
        entry.bind(
            "<KeyRelease>", lambda event, e=entry: check_entries(entries, submit_button)
        )
        entries[field] = entry

    submit_button = tk.Button(
        tab,
        text="Submit",
        state="disabled",
        command=lambda: handle_data_submission(entries, status_label),
    )
    submit_button.pack(pady=10)

    check_entries(entries, submit_button)

    return entries


def add_faculty_fields(tab, field_names, validation_functions, status_label):
    entries = {}
    for field in field_names:
        frame = tk.Frame(tab)
        frame.pack(side="top", fill="x", padx=5, pady=5)

        label = tk.Label(frame, text=field, width=20)
        label.pack(side="left")

        if field == "Rank":
            # Dropdown for Rank selection
            rank_var = tk.StringVar()
            rank_options = ["full", "associate", "assistant", "adjunct"]
            rank_dropdown = ttk.Combobox(
                frame, textvariable=rank_var, values=rank_options, state="readonly"
            )
            rank_dropdown.set(rank_options[0])  # Set default value
            rank_dropdown.pack(side="right", expand=True, fill="x")
            entries[field] = rank_dropdown
        else:
            entry = tk.Entry(frame)
            entry.pack(side="right", expand=True, fill="x")
            entry.bind(
                "<KeyRelease>",
                lambda event, e=entry: check_entries(entries, submit_button),
            )
            entries[field] = entry

    submit_button = tk.Button(
        tab,
        text="Submit",
        state="disabled",
        command=lambda: handle_data_submission(entries, status_label),
    )
    submit_button.pack(pady=10)

    check_entries(entries, submit_button)

    return entries


def setup_data_entry_tab(notebook, status_label):
    data_entry_tab = ttk.Frame(notebook)
    notebook.add(data_entry_tab, text="Data Entry")

    data_entry_notebook = ttk.Notebook(data_entry_tab)
    data_entry_notebook.pack(expand=True, fill="both", padx=10, pady=10)

    # Departments tab
    departments_tab = ttk.Frame(data_entry_notebook)
    data_entry_notebook.add(departments_tab, text="Departments")
    department_fields = ["Name", "Code"]
    add_data_fields(
        departments_tab,
        department_fields,
        {"Code": validate_department_code},
        status_label,
    )

    # Faculty tab
    faculty_tab = ttk.Frame(data_entry_notebook)
    data_entry_notebook.add(faculty_tab, text="Faculty")
    faculty_fields = ["ID", "Name", "Email", "Rank"]
    add_faculty_fields(
        faculty_tab, faculty_fields, {"Email": validate_email}, status_label
    )

    programs_tab = ttk.Frame(data_entry_notebook)
    data_entry_notebook.add(programs_tab, text="Programs")
    program_fields = ["Name", "Department ID", "Person in Charge ID"]
    add_data_fields(programs_tab, program_fields, {}, status_label)

    courses_tab = ttk.Frame(data_entry_notebook)
    data_entry_notebook.add(courses_tab, text="Courses")
    course_fields = ["ID", "Title", "Description", "Department ID"]
    add_data_fields(
        courses_tab, course_fields, {"ID": validate_course_id}, status_label
    )

    sections_tab = ttk.Frame(data_entry_notebook)
    data_entry_notebook.add(sections_tab, text="Sections")
    section_fields = [
        "ID",
        "Course ID",
        "Semester",
        "Instructor ID",
        "Enrollment Count",
    ]
    add_data_fields(
        sections_tab, section_fields, {"ID": validate_section_id}, status_label
    )

    objectives_tab = ttk.Frame(data_entry_notebook)
    data_entry_notebook.add(objectives_tab, text="Learning Objectives")
    objective_fields = ["Code", "Description", "Parent Objective Code"]
    add_data_fields(objectives_tab, objective_fields, {}, status_label)

    # Add the rest later


def reset_database():
    DATABASE_URI = "sqlite:///university_evaluation.db"

    engine = create_engine(DATABASE_URI)

    Base.metadata.drop_all(engine)

    Base.metadata.create_all(engine)
    messagebox.showinfo("Database Reset", "Database has been reset/initialized.")


def initialize_gui():
    window = tk.Tk()
    window.title("University Program Evaluation System")

    menubar = tk.Menu(window)
    window.config(menu=menubar)

    settings_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Settings", menu=settings_menu)

    settings_menu.add_command(label="Reset Database", command=reset_database)

    # status Label for showing messages
    status_label = tk.Label(window, text="", font="Helvetica 12", fg="red")
    status_label.pack(pady=(5, 10))

    main_notebook = ttk.Notebook(window)
    main_notebook.pack(expand=True, fill="both", padx=10, pady=10)

    # Setup Data Entry Tab
    setup_data_entry_tab(main_notebook, status_label)

    # Placeholder for Data Query Tab (do that later)
    data_query_tab = ttk.Frame(main_notebook)
    main_notebook.add(data_query_tab, text="Data Query")

    window.mainloop()