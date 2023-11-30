import tkinter as tk

def submit(cmdVar):
    cmdText = cmdVar.get()
    print(f'Command Entered: {cmdText}')
    # commands to implement:
    # d = enter department info
    # f = enter faculty info
    # p = enter program info
    # c = enter course info
    # s = enter section info
    # l = enter learning objective/sub-objective info
    # a = add course to program
    # A = ade (sub)objectives to (course, program) pairs
    # e = enter evaluation results for section
    # D = get department info
    # P = get program info
    # S = get evaluation results for each section given semester & program
    # Y = get evaluation results for each objective/sub-objective given academic year

if __name__ == '__main__':
    window = tk.Tk()
    title = tk.Label(text='Program Evaluation', font='Helvetica 18 bold')
    title.pack()
    cmdLabel = tk.Label(text='Enter your command:', font='Helvetica 15')
    cmdLabel.pack()
    cmd = tk.Entry()
    cmd.pack()
    submit_button = tk.Button(window, text="Submit", command=lambda: submit(cmd))
    submit_button.pack()
    window.mainloop()