import tkinter as tk


# Place frame setup code here

def setup_data_entry_frame(parent, status_label):
    entry_frame = tk.Frame(parent, borderwidth=2, relief='ridge')
    entry_frame.pack(side='left', fill='both', expand=True)

    title_entry = tk.Label(entry_frame, text='Data Entry', font='Helvetica 18 bold')
    title_entry.pack()

    cmdLabel = tk.Label(entry_frame, text='Enter your command:', font='Helvetica 15')
    cmdLabel.pack()

    cmd = tk.Entry(entry_frame)
    cmd.pack()

    submit_button = tk.Button(entry_frame, text="Submit", command=lambda: submit(cmd, status_label))
    submit_button.pack()

    return entry_frame

def setup_data_query_frame(parent):
    query_frame = tk.Frame(parent, borderwidth=2, relief='ridge')
    query_frame.pack(side='right', fill='both', expand=True)

    title_query = tk.Label(query_frame, text='Data Query', font='Helvetica 18 bold')
    title_query.pack()

    return query_frame

# Database functions and user input section

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

