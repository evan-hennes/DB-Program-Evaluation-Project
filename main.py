import tkinter as tk
from tkinter import ttk

# Place frame setup code here

def setup_data_entry_frame(parent, status_label):
    entry_frame = tk.Frame(parent, borderwidth=2, relief='ridge')
    entry_frame.pack(side='left', fill='both', expand=True)

    title_entry = tk.Label(entry_frame, text='Data Entry', font='Helvetica 18 bold')
    title_entry.pack()

    # Fields for each category
    fields = {
        'Departments': ['Name', 'Code'],
        'Faculty': ['ID', 'Name', 'Email', 'Rank'],
        'Programs': ['Name', 'Department'],
        'Courses': ['ID', 'Title', 'Description'],
        'Sections': ['ID', 'Semester'],
        'Objectives': ['Code', 'Description']
    }

    # Create a tabbed interface
    tab_control = ttk.Notebook(entry_frame)

    # Create tabs dynamically
    for tab_name, field_list in fields.items():
        tab = tk.Frame(tab_control)
        tab_control.add(tab, text=tab_name)
        add_data_fields(tab, field_list)

    tab_control.pack(expand=1, fill="both")

    return entry_frame
def setup_data_query_frame(parent):
    query_frame = tk.Frame(parent, borderwidth=2, relief='ridge')
    query_frame.pack(side='right', fill='both', expand=True)

    title_query = tk.Label(query_frame, text='Data Query', font='Helvetica 18 bold')
    title_query.pack()

    return query_frame

# Database functions and user input section

def handle_data_submission(data_entries):
    data = {field: entry.get() for field, entry in data_entries.items()}
    print("Data Submitted:", data)
    # Implement your logic for handling data submission here

def add_data_fields(parent, field_names):
    data_entries = {}
    for field in field_names:
        frame = tk.Frame(parent)
        frame.pack(side="top", fill="x", padx=5, pady=5)

        label = tk.Label(frame, text=field, width=20)
        label.pack(side="left")

        entry = tk.Entry(frame)
        entry.pack(side="right", expand=True, fill="x")
        data_entries[field] = entry

    submit_button = tk.Button(parent, text="Submit", command=lambda: handle_data_submission(data_entries))
    submit_button.pack(pady=10)

    return data_entries

def add_data(cmdText, status_label):
    status_label.config(text=f'Added Data: {cmdText}')
    print(f'Adding Data: {cmdText}')

def query_data(cmdText, status_label):
    status_label.config(text=f'Queried Data: {cmdText}')
    print(f'Querying Data: {cmdText}')

def submit(cmdVar, status_label):
    cmdText = cmdVar.get()
    status_label.config(text=f'TODO! Your input was {cmdText}')


if __name__ == '__main__':
    window = tk.Tk()
    window.title('Program Evaluation')

    # Status Label
    status_label = tk.Label(window, text='', font='Helvetica 12', fg='red')
    status_label.pack()

    # Set up frames
    entry_frame = setup_data_entry_frame(window, status_label)
    query_frame = setup_data_query_frame(window)

    window.mainloop()

