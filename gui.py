import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy import create_engine
from db import Base
from random import random

DB = None


# Validation functions
def validate_non_empty(entry):
    return entry.get().strip() != ""


def validate_department_code(entry):
    return len(entry.get().strip()) <= 4 and entry.get().strip().isalnum()


def validate_email(entry):
    return "@" in entry.get().strip() and "." in entry.get().strip()


def validate_course_id(entry):
    return entry.get().strip().isdigit() and len(entry.get().strip()) == 4


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
    return entry.get().strip() != "" and len(entry.get().strip(
    )) == 5 and entry.get().strip()[0:2].isdigit() and entry.get().strip(
    )[3:5].isdigit() and entry.get().strip()[2] == "-"


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
                DB.add_department(data["Name"], data["Code"])
            elif category == "Faculty":
                DB.add_faculty(data["Name"], data["Email"], data["Rank"],
                               data["Code"])
            elif category == "Programs":
                DB.add_program(data["Name"], data["Code"],
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
                if data["Choice"] == "faculty":
                    results = DB.get_department_faculty_by_name(
                        data["Department Name"])
                elif data["Choice"] == "program":
                    results = DB.get_department_programs_by_name(
                        data["Department Name"])
            elif category == "Program":
                if data["Choice"] == "courses":
                    results = DB.get_program_courses_by_name(
                        data["Program Name"])
                elif data["Choice"] == "objectives":
                    results = DB.get_program_objectives_by_name(
                        data["Program Name"])
            elif category == "Semester Program":
                if data["Choice"] == "evaluation":
                    results = DB.get_results_by_semester(
                        data["Semester"], data["Program Name"])
            elif category == "Year":
                if data["Choice"] == "evaluation":
                    results = DB.get_results_by_year(data["Year"])

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

        if field == "Choice":
            choice_var = tk.StringVar()
            choice_options = ["default"]
            if category == "Department":
                choice_options = ["faculty", "program"]
            elif category == "Program":
                choice_options = ["courses", "objectives"]
            elif category == "Semester Program":
                choice_options = ["evaluation"]
            elif category == "Year":
                choice_options = ["evaluation"]
            choice_dropdown = ttk.Combobox(frame,
                                           textvariable=choice_var,
                                           values=choice_options,
                                           state="readonly")
            choice_dropdown.set(choice_options[0])
            choice_dropdown.pack(side="right", expand=True, fill="x")
            entries[field] = choice_dropdown
        else:
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


def handle_course_program_assignment(entries, status_label):
    is_valid = all(validate_non_empty(entry) for entry in entries.values())
    if is_valid:
        data = {field: entry.get() for field, entry in entries.items()}
        try:
            DB.assign_course_to_program(data["Program ID"], data["Course ID"])
            status_label.config(
                text="Course successfully assigned to program.", fg="green")
        except Exception as e:
            status_label.config(text=str(e), fg="red")
    else:
        status_label.config(text="Invalid data in some fields.", fg="red")


def add_course_program_assignment_fields(tab, validation_functions,
                                         status_label):
    entries = {}
    fields = ["Program ID", "Course ID"]
    for field in fields:
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

    submit_button = tk.Button(tab,
                              text="Assign",
                              state="disabled",
                              command=lambda: handle_course_program_assignment(
                                  entries, status_label))
    submit_button.pack(pady=10)
    check_entries(entries, submit_button)


def handle_objective_assignment(entries, status_label):
    is_valid = all(validate_non_empty(entry) for entry in entries.values())
    if is_valid:
        data = {field: entry.get() for field, entry in entries.items()}
        try:
            DB.assign_objective_to_course(data["Course ID"],
                                          data["Objective ID"],
                                          data["Program ID"])
            status_label.config(text="Objective successfully assigned.",
                                fg="green")
        except Exception as e:
            status_label.config(text=str(e), fg="red")
    else:
        status_label.config(text="Invalid data in some fields.", fg="red")


def add_objective_assignment_fields(tab, validation_functions, status_label):
    entries = {}
    fields = ["Course ID", "Objective ID", "Program ID"]
    for field in fields:
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
        text="Assign",
        state="disabled",
        command=lambda: handle_objective_assignment(entries, status_label))
    submit_button.pack(pady=10)
    check_entries(entries, submit_button)


def handle_evaluation_submission(entries, status_label):
    is_valid = all(validate_non_empty(entry) for entry in entries.values())
    if is_valid:
        data = {field: entry.get() for field, entry in entries.items()}
        try:
            DB.add_section_evaluation(data["Section ID"], data["Objective ID"],
                                      data["Evaluation Method"],
                                      int(data["Students Met"]))
            status_label.config(
                text="Evaluation result successfully submitted.", fg="green")
        except Exception as e:
            status_label.config(text=str(e), fg="red")
    else:
        status_label.config(text="Invalid data in some fields.", fg="red")


def add_evaluation_fields(tab, validation_functions, status_label):
    entries = {}
    fields = [
        "Section ID", "Objective ID", "Evaluation Method", "Students Met"
    ]
    for field in fields:
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
        command=lambda: handle_evaluation_submission(entries, status_label))
    submit_button.pack(pady=10)
    check_entries(entries, submit_button)


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
    faculty_fields = ["Name", "Email", "Rank", "Code"]
    add_faculty_fields(faculty_tab, faculty_fields, {"Email": validate_email, "Code": validate_department_code },
                       status_label)

    programs_tab = ttk.Frame(data_entry_notebook)
    data_entry_notebook.add(programs_tab, text="Programs")
    program_fields = ["Name", "Code", "Person in Charge ID"]
    add_data_fields(programs_tab, program_fields, {}, status_label, "Programs")

    courses_tab = ttk.Frame(data_entry_notebook)
    data_entry_notebook.add(courses_tab, text="Courses")
    course_fields = ["ID", "Title", "Description", "Code"]
    add_data_fields(courses_tab, course_fields, {"ID": validate_course_id, "Code": validate_department_code },
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

    course_program_tab = ttk.Frame(data_entry_notebook)
    data_entry_notebook.add(course_program_tab,
                            text="Assign Course to Program")
    add_course_program_assignment_fields(course_program_tab,
                                         validation_functions, status_label)

    objective_assignment_tab = ttk.Frame(data_entry_notebook)
    data_entry_notebook.add(objective_assignment_tab, text="Assign Objectives")
    add_objective_assignment_fields(objective_assignment_tab,
                                    validation_functions, status_label)

    evaluation_tab = ttk.Frame(data_entry_notebook)
    data_entry_notebook.add(evaluation_tab, text="Section Evaluation")
    add_evaluation_fields(evaluation_tab, validation_functions, status_label)


def setup_data_query_tab(notebook, status_label):
    data_query_tab = ttk.Frame(notebook)
    notebook.add(data_query_tab, text="Data Query")

    data_query_notebook = ttk.Notebook(data_query_tab)
    data_query_notebook.pack(expand=True, fill="both", padx=10, pady=10)

    # Department Queries
    department_tab = ttk.Frame(data_query_notebook)
    data_query_notebook.add(department_tab, text="Department")
    department_fields = ["Choice", "Department Name"]
    add_query_fields(department_tab, department_fields,
                     {"Department Name": validate_department_name},
                     status_label, "Department")

    # Program Queries
    program_tab = ttk.Frame(data_query_notebook)
    data_query_notebook.add(program_tab, text="Program")
    program_fields = ["Choice", "Program Name"]
    add_query_fields(program_tab, program_fields,
                     {"Program Name": validate_program_name}, status_label,
                     "Program")

    # Semester + Program Queries
    semester_program_tab = ttk.Frame(data_query_notebook)
    data_query_notebook.add(semester_program_tab, text="Semester Program")
    semester_program_fields = ["Choice", "Semester", "Program Name"]
    add_query_fields(semester_program_tab, semester_program_fields,
                     {"Program Name": validate_program_name}, status_label,
                     "Semester Program")

    # Year Queries
    year_tab = ttk.Frame(data_query_notebook)
    data_query_notebook.add(year_tab, text="Year")
    year_fields = ["Choice", "Year"]
    add_query_fields(year_tab, year_fields, {"Year": validate_year},
                     status_label, "Year")


def reset_database():
    DATABASE_URI = "sqlite:///university_evaluation.db"

    engine = create_engine(DATABASE_URI)

    Base.metadata.drop_all(engine)

    Base.metadata.create_all(engine)


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

    # Setup Data Query Tab
    setup_data_query_tab(main_notebook, status_label)

    window.mainloop()


def initialize_db(db):
    global DB
    DB = db

    # Department
    db.add_department("Cox School of Business", "BIZ")
    db.add_department("Lyle School of Engineering", "ENG")

    # Faculty
    db.add_faculty("Vishal Ahuja", "vishal.ahuja@smu.edu", "associate", "BIZ")
    db.add_faculty("Amy Altizer", "amy.altizer@smu.edu", "adjunct", "BIZ")
    db.add_faculty("Thomas Barry", "thomas.barry@smu.edu", "full", "BIZ")
    db.add_faculty("Wendy Bradley", "wendy.bradley@smu.edu", "assistant", "BIZ")

    db.add_faculty("Frank Coyle", "frank.coyle@smu.edu", "associate", "ENG")
    db.add_faculty("Qiguo Jing", "qiguo.jing@smu.edu", "adjunct", "ENG")
    db.add_faculty("Theodore Manikas", "theodore.manikas@smu.edu", "full", "ENG")
    db.add_faculty("Corey Clark", "corey.clark@smu.edu", "assistant", "ENG")

    # Program
    db.add_program("Finance", "BIZ", 3) # 1
    db.add_program("Accounting", "BIZ", 3) # 2
    db.add_program("Marketing", "BIZ", 3) # 3

    db.add_program("Computer Science", "ENG", 7) # 4
    db.add_program("Computer Engineering", "ENG", 7) # 5
    db.add_program("Creative Computing", "ENG", 7) # 6

    # Course
    db.add_course("BIZ1000", "Intro to Business",
                  "Introduction to all things Business", "BIZ")
    # db.add_learning_objective(1, "learn le business", )
    # db.add_learning_objective(2, "how sell stuff and things", 1)
    # db.assign_course_to_program(1, "BIZ1000")
    # db.assign_objective_to_course("BIZ1000", 1)
    # db.assign_objective_to_course("BIZ1000", 2)
    # db.add_course("BIZ1100", "Intro to Marketing",
    #               "Introduction to all things Marketing", 1)
    # db.add_learning_objective(3, "learn le marketing")
    # db.add_learning_objective(4, "i mark it", 3)
    # db.assign_course_to_program(3, "BIZ1100")
    # db.assign_objective_to_course("BIZ1100", 3)
    # db.assign_objective_to_course("BIZ1100", 4)
    db.add_course("BIZ1200", "Intro to Accounting",
                  "Introduction to all things Accounting", "BIZ")
    db.add_course("BIZ2000", "Intermediate Business",
                  "Intermediate class for all things Business", "BIZ")
    db.add_course("BIZ2100", "Intermediate Marketing",
                  "Intermediate class for all things Marketing", "BIZ")
    db.add_course("BIZ2200", "Intermediate Accounting",
                  "Intermediate class for all things Accounting", "BIZ")
    db.add_course("BIZ3000", "Advanced Business",
                  "Advanced class for all things Business", "BIZ")
    db.add_course("BIZ3100", "Advanced Marketing",
                  "Advanced class for all things Marketing", "BIZ")
    db.add_course("BIZ3200", "Advanced Accounting",
                  "Advanced class for all things Accounting", "BIZ")

    db.add_course("ENG1000", "Intro to Computer Science",
                  "Introduction to all things Computer Science", "ENG")
    db.add_course("ENG1100", "Intro to Computer Engineering",
                  "Introduction to all things Computer Engineering", "ENG")
    db.add_course("ENG1200", "Intro to Creative Computing",
                  "Introduction to all things Creative Computing", "ENG")
    db.add_course("ENG2000", "Intermediate Computer Science",
                  "Intermediate class for all things Computer Science", "ENG")
    db.add_course("ENG2100", "Intermediate Computer Engineering",
                  "Intermediate class for all things Computer Engineering", "ENG")
    db.add_course("ENG2200", "Intermediate Creative Computing",
                  "Intermediate class for all things Creative Computing", "ENG")
    db.add_course("ENG3000", "Advanced Computer Science",
                  "Advanced class for all things Computer Science", "ENG")
    db.add_course("ENG3100", "Advanced Computer Engineering",
                  "Advanced class for all things Computer Engineering", "ENG")
    db.add_course("ENG3200", "Advanced Creative Computing",
                  "Advanced class for all things Creative Computing", "ENG")

    # Section
    semester = ["Fall", "Spring", "Summer"]
    year = [21, 22, 23, 24, 25]
    # db.add_section(200, "Fall", 23, "BIZ1000", 3, 40)
    # db.add_section_evaluation(1, 1, "Good", 20)
    # for i in range(0, 51, 10):
    #     db.add_section(
    #         int(random() * 10) + i, semester[int(random() * 3)],
    #         year[int(random() * 5)], "BIZ1000",
    #         int(random() * 4) + 1, int(random() * 50))
    # for i in range(0, 51, 10):
    #     db.add_section(
    #         int(random() * 10) + i, semester[int(random() * 3)],
    #         year[int(random() * 5)], "BIZ1100",
    #         int(random() * 4) + 1, int(random() * 50))
    # for i in range(0, 51, 10):
    #     db.add_section(
    #         int(random() * 10) + i, semester[int(random() * 3)],
    #         year[int(random() * 5)], "BIZ1200",
    #         int(random() * 4) + 1, int(random() * 50))
    # for i in range(0, 51, 10):
    #     db.add_section(
    #         int(random() * 10) + i, semester[int(random() * 3)],
    #         year[int(random() * 5)], "BIZ2000",
    #         int(random() * 4) + 1, int(random() * 50))
    # for i in range(0, 51, 10):
    #     db.add_section(
    #         int(random() * 10) + i, semester[int(random() * 3)],
    #         year[int(random() * 5)], "BIZ2100",
    #         int(random() * 4) + 1, int(random() * 50))
    # for i in range(0, 51, 10):
    #     db.add_section(
    #         int(random() * 10) + i, semester[int(random() * 3)],
    #         year[int(random() * 5)], "BIZ2200",
    #         int(random() * 4) + 1, int(random() * 50))
    # for i in range(0, 51, 10):
    #     db.add_section(
    #         int(random() * 10) + i, semester[int(random() * 3)],
    #         year[int(random() * 5)], "BIZ3000",
    #         int(random() * 4) + 1, int(random() * 50))
    # for i in range(0, 51, 10):
    #     db.add_section(
    #         int(random() * 10) + i, semester[int(random() * 3)],
    #         year[int(random() * 5)], "BIZ3100",
    #         int(random() * 4) + 1, int(random() * 50))
    # for i in range(0, 51, 10):
    #     db.add_section(
    #         int(random() * 10) + i, semester[int(random() * 3)],
    #         year[int(random() * 5)], "BIZ3200",
    #         int(random() * 4) + 1, int(random() * 50))
    # for i in range(0, 51, 10):
    #     db.add_section(
    #         int(random() * 10) + i, semester[int(random() * 3)],
    #         year[int(random() * 5)], "ENG1000",
    #         int(random() * 4) + 5, int(random() * 50))
    # for i in range(0, 51, 10):
    #     db.add_section(
    #         int(random() * 10) + i, semester[int(random() * 3)],
    #         year[int(random() * 5)], "ENG1100",
    #         int(random() * 4) + 5, int(random() * 50))
    # for i in range(0, 51, 10):
    #     db.add_section(
    #         int(random() * 10) + i, semester[int(random() * 3)],
    #         year[int(random() * 5)], "ENG1200",
    #         int(random() * 4) + 5, int(random() * 50))
    # for i in range(0, 51, 10):
    #     db.add_section(
    #         int(random() * 10) + i, semester[int(random() * 3)],
    #         year[int(random() * 5)], "ENG2000",
    #         int(random() * 4) + 5, int(random() * 50))
    # for i in range(0, 51, 10):
    #     db.add_section(
    #         int(random() * 10) + i, semester[int(random() * 3)],
    #         year[int(random() * 5)], "ENG2100",
    #         int(random() * 4) + 5, int(random() * 50))
    # for i in range(0, 51, 10):
    #     db.add_section(
    #         int(random() * 10) + i, semester[int(random() * 3)],
    #         year[int(random() * 5)], "ENG2200",
    #         int(random() * 4) + 5, int(random() * 50))
    # for i in range(0, 51, 10):
    #     db.add_section(
    #         int(random() * 10) + i, semester[int(random() * 3)],
    #         year[int(random() * 5)], "ENG3000",
    #         int(random() * 4) + 5, int(random() * 50))
    # for i in range(0, 51, 10):
    #     db.add_section(
    #         int(random() * 10) + i, semester[int(random() * 3)],
    #         year[int(random() * 5)], "ENG3100",
    #         int(random() * 4) + 5, int(random() * 50))
    # for i in range(0, 51, 10):
    #     db.add_section(
    #         int(random() * 10) + i, semester[int(random() * 3)],
    #         year[int(random() * 5)], "ENG3200",
    #         int(random() * 4) + 5, int(random() * 50))

    print('db initialized successfully')
