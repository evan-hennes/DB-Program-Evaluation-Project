import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy import create_engine
from db import Base

DB_MANAGER = None

# Validation functions
def validate_non_empty(entry):
    return entry.get().strip() != ""


def validate_department_code(entry):
    return len(entry.get().strip()) <= 4 and entry.get().strip().isalnum()


def validate_email(entry):
    return "@" in entry.get().strip() and "." in entry.get().strip()


def validate_course_id(entry):
    return entry.get().strip().isalnum() and len(entry.get().strip()) == 7


def validate_section_id(entry):
    return entry.get().strip().isdigit() and len(entry.get().strip()) <= 3


def validate_department_id(entry):
    return entry.get().strip().isdigit()


def validate_person_in_charge_id(entry):
    return entry.get().strip().isdigit()


def validate_enrollment_count(entry):
    return entry.get().strip().isdigit()

def validate_department_name(entry):
    return entry.get().strip() != ""

def validate_program_name(entry):
    return entry.get().strip() != ""

def validate_year(entry):
    return entry.get().strip() != "" and len(entry.get().strip()) == 5 and entry.get().strip()[0:2].isdigit() and entry.get().strip()[3:5].isdigit() and entry.get().strip()[2] == "-"


validation_functions = {
    "Code": validate_department_code,
    "Email": validate_email,
    "Course ID": validate_course_id,  # Assuming this is for course ID
    "Department ID": validate_department_id,
    "Person in Charge ID": validate_person_in_charge_id,
    "Enrollment Count": validate_enrollment_count,

    "Department Name": validate_department_name,
    "Program Name": validate_program_name,
    "Year": validate_year,
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
            field, lambda e: True)(entry)
        set_entry_validity(entry, is_valid)
        all_valid &= is_valid
    submit_button.config(state="normal" if all_valid else "disabled")


def handle_data_submission(entries, status_label, category):
    is_valid = all(validate_non_empty(entry) for entry in entries.values())
    if is_valid:
        data = {field: entry.get() for field, entry in entries.items()}
        try:
            if category == "Departments":
                DB_MANAGER.add_department(data["Name"], data["Code"])
            elif category == "Faculty":
                DB_MANAGER.add_faculty(data["Name"], data["Email"],
                                       data["Rank"], data["Department ID"])
            elif category == "Programs":
                DB_MANAGER.add_program(data["Name"], data["Department ID"],
                                       data["Person in Charge ID"])
            # Add similar branches for other categories
            status_label.config(
                text=f"Data for {category} successfully submitted.",
                fg="green")
        except Exception as e:
            status_label.config(text=str(e), fg="red")
    else:
        status_label.config(text="Invalid data in some fields.", fg="red")


def add_data_fields(tab, field_names, validation_functions, status_label,
                    category):
    entries = {}
    for field in field_names:
        frame = tk.Frame(tab)
        frame.pack(side="top", fill="x", padx=5, pady=5)

        label = tk.Label(frame, text=field, width=20)
        label.pack(side="left")

        entry = tk.Entry(frame)
        entry.pack(side="right", expand=True, fill="x")
        entry.bind(
            "<KeyRelease>",
            lambda event, e=entry: check_entries(entries, submit_button))
        entries[field] = entry

    submit_button = tk.Button(
        tab,
        text="Submit",
        state="disabled",
        command=lambda: handle_data_submission(entries, status_label, category
                                               ),
    )
    submit_button.pack(pady=10)

    check_entries(entries, submit_button)

    return entries

def handle_query_submission(entries, status_label, category):
    is_valid = all(validate_non_empty(entry) for entry in entries.values())
    if is_valid:
        data = {field: entry.get() for field, entry in entries.items()}
        try:
            results = ""
            if category == "Department":
                results = DB_MANAGER.get_department_programs_by_name(data["Department Name"])
            elif category == "Program":
                print("do stuff")
            elif category == "SemesterProgram":
                Dprint("do stuff")
            elif category == "Year":
                print("do stuff")
            status_label.config(
                text=f"Query for {category} successfully submitted.\n{results}",
                fg="green")
        except Exception as e:
            status_label.config(text=str(e), fg="red")
    else:
        status_label.config(text="Invalid data in some fields.", fg="red")

def add_query_fields(tab, field_names, validation_functions, status_label,
                    category):
    entries = {}
    for field in field_names:
        frame = tk.Frame(tab)
        frame.pack(side="top", fill="x", padx=5, pady=5)

        label = tk.Label(frame, text=field, width=20)
        label.pack(side="left")

        entry = tk.Entry(frame)
        entry.pack(side="right", expand=True, fill="x")
        entry.bind(
            "<KeyRelease>",
            lambda event, e=entry: check_entries(entries, submit_button))
        entries[field] = entry

    submit_button = tk.Button(
        tab,
        text="Submit",
        state="disabled",
        command=lambda: handle_query_submission(entries, status_label, category
                                               ),
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
            rank_var = tk.StringVar()
            rank_options = ["full", "associate", "assistant", "adjunct"]
            rank_dropdown = ttk.Combobox(frame,
                                         textvariable=rank_var,
                                         values=rank_options,
                                         state="readonly")
            rank_dropdown.set(rank_options[0])
            rank_dropdown.pack(side="right", expand=True, fill="x")
            entries[field] = rank_dropdown
        else:
            entry = tk.Entry(frame)
            entry.pack(side="right", expand=True, fill="x")
            entry.bind(
                "<KeyRelease>",
                lambda event, e=entry: check_entries(entries, submit_button))
            entries[field] = entry

    submit_button = tk.Button(tab,
                              text="Submit",
                              state="disabled",
                              command=lambda: handle_data_submission(
                                  entries, status_label, "Faculty"))
    submit_button.pack(pady=10)

    check_entries(entries, submit_button)

    return entries


def setup_data_entry_tab(notebook, status_label):
    data_entry_tab = ttk.Frame(notebook)
    notebook.add(data_entry_tab, text="Data Entry")

    data_entry_notebook = ttk.Notebook(data_entry_tab)
    data_entry_notebook.pack(expand=True, fill="both", padx=10, pady=10)

    departments_tab = ttk.Frame(data_entry_notebook)
    data_entry_notebook.add(departments_tab, text="Departments")
    department_fields = ["Name", "Code"]
    add_data_fields(departments_tab, department_fields,
                    {"Code": validate_department_code}, status_label,
                    "Departments")

    faculty_tab = ttk.Frame(data_entry_notebook)
    data_entry_notebook.add(faculty_tab, text="Faculty")
    faculty_fields = ["Name", "Email", "Rank", "Department ID"]
    add_faculty_fields(faculty_tab, faculty_fields, {"Email": validate_email},
                       status_label)

    programs_tab = ttk.Frame(data_entry_notebook)
    data_entry_notebook.add(programs_tab, text="Programs")
    program_fields = ["Name", "Department ID", "Person in Charge ID"]
    add_data_fields(programs_tab, program_fields, {}, status_label, "Programs")

    courses_tab = ttk.Frame(data_entry_notebook)
    data_entry_notebook.add(courses_tab, text="Courses")
    course_fields = ["ID", "Title", "Description", "Department ID"]
    add_data_fields(courses_tab, course_fields, {"ID": validate_course_id},
                    status_label, "Courses")

    sections_tab = ttk.Frame(data_entry_notebook)
    data_entry_notebook.add(sections_tab, text="Sections")
    section_fields = [
        "ID", "Course ID", "Semester", "Instructor ID", "Enrollment Count"
    ]
    add_data_fields(sections_tab, section_fields, {"ID": validate_section_id},
                    status_label, "Sections")

    objectives_tab = ttk.Frame(data_entry_notebook)
    data_entry_notebook.add(objectives_tab, text="Learning Objectives")
    objective_fields = ["Code", "Description", "Parent Objective Code"]
    add_data_fields(objectives_tab, objective_fields, {}, status_label,
                    "Learning Objectives")

def setup_data_query_tab(notebook, status_label):
    data_query_tab = ttk.Frame(notebook)
    notebook.add(data_query_tab, text="Data Query")

    data_query_notebook = ttk.Notebook(data_query_tab)
    data_query_notebook.pack(expand=True, fill="both", padx=10, pady=10)

    # Department Queries
    department_tab = ttk.Frame(data_query_notebook)
    data_query_notebook.add(department_tab, text="Department")
    department_fields = ["Department Name"]
    add_query_fields(department_tab, department_fields, {"Department Name": validate_department_name}, status_label, "Department")

    # Program Queries
    program_tab = ttk.Frame(data_query_notebook)
    data_query_notebook.add(program_tab, text="Program")
    program_fields = ["Program Name"]
    add_query_fields(program_tab, program_fields, {"Program Name": validate_program_name}, status_label, "Program")

    # Semester + Program Queries
    semester_program_tab = ttk.Frame(data_query_notebook)
    data_query_notebook.add(semester_program_tab, text="Semester Program")
    semester_program_fields = ["Semester", "Program Name"]
    add_query_fields(semester_program_tab, semester_program_fields, {"Program Name": validate_program_name}, status_label, "Semester Program")

    # Year Queries
    year_tab = ttk.Frame(data_query_notebook)
    data_query_notebook.add(year_tab, text="Year")
    year_fields = ["Year"]
    add_query_fields(year_tab, year_fields, {"Year": validate_year}, status_label, "Year")

def reset_database():
    DATABASE_URI = "sqlite:///university_evaluation.db"

    engine = create_engine(DATABASE_URI)

    Base.metadata.drop_all(engine)

    Base.metadata.create_all(engine)
    # messagebox.showinfo("Database Reset",
    #                     "Database has been reset/initialized.")


def initialize_gui(db_manager):
    global DB_MANAGER
    DB_MANAGER =  db_manager

    DB_MANAGER.add_department("dep", 1234)
    DB_MANAGER.add_faculty("fac", "@.", "full", 1)
    DB_MANAGER.add_program("pro", 1, 1)
    
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

    # Setup Data Query Tab
    setup_data_query_tab(main_notebook, status_label)

    window.mainloop()
