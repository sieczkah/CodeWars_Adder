import requests
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import re
import os.path


root = tk.Tk()
root.title('CodeWars Adder')
root.option_readfile('options.txt')


class DirPath:
    def __init__(self):
        self.path = self.get_path_file()
        if not self.path:
            self.ask_path()

    def get_path_file(self):
        try:
            with open('path.txt', 'r') as path_txt:
                return path_txt.read()
        except FileNotFoundError:
            return self.ask_path()

    @staticmethod
    def ask_path(current_path=os.getcwd()):
        path = filedialog.askdirectory(initialdir=current_path)
        with open('path.txt', 'w') as path_txt:
            path_txt.write(path)
        return path


class KataFile:
    dir_path = DirPath()

    def __init__(self):
        self.link = None
        self.kata_name = None
        self.file_name = None
        self.kata_rank = None
        self.content = None

    # Getting kata info wit codewars api,
    # later is used to create file in corresponding kyu folder
    def get_kata_info(self):
        pattern = re.compile(r'(https?://)?(www\.codewars\.com/kata/\w+)')
        self.link = re.match(pattern, self.link).group()
        kata_json = requests.get(self.link + '.json').json()
        self.kata_name = kata_json['name']
        self.kata_rank = kata_json['rank']['name']

    # checks if file exists If not calling func create if it exists
    # asking the user if to overwrite the File and takes action according to Yes/No answer
    def path_check(self):
        self.add_file_name()
        file_path = f"{self.dir_path.path}/{self.kata_rank}/{self.file_name}.py"
        if os.path.exists(file_path):
            msg_exist = messagebox.askyesno('File Error', 'File exists want to overwrite?')
            if msg_exist:
                return file_path
            else:
                return False
        else:
            return file_path

    # creates filename from kata_name handles restricted symbols
    # and Loading Kata: prefix (that sometimes apperas when scrapping name)
    def add_file_name(self):
        self.file_name = re.sub(r'(?!-|\s|\(|\))\W+', ' ', self.kata_name)


class KataAdder(KataFile):

    # Init basically Creates the GUI and sets variables that will be used
    def __init__(self, master):
        self.master = master
        canvas = tk.Canvas(root, height=700, width=700)
        canvas.pack()

        super().__init__()

        # Frame0 is for whole window
        frame0 = tk.Frame(self.master)
        frame0.place(relwidth=1, relheight=1)

        # Frame1 holds Entry for link, and a button for scrapping
        frame1 = tk.Frame(self.master, bd=5)
        frame1.place(relwidth=0.9, relheight=0.1, relx=0.05, rely=0.1)

        self.e1 = tk.Entry(frame1)
        self.e1.place(relwidth=1, relheight=0.5)

        get_info_button = tk.Button(frame1, text='Get Kata Info', padx=10, pady=5,
                                    command=lambda: self.button_scrap(),
                                    fg='#f1ff33', activebackground='#202020', activeforeground='#f1ff33')

        get_info_button.place(rely=0.55, relx=0.5, anchor='n')

        # Frame2 holds the label for Kata name and Kyu rank
        frame2 = tk.Frame(self.master)
        frame2.place(relwidth=0.9, relheight=0.1, relx=0.05, rely=0.2)

        self.name_label = tk.Label(frame2, text='Kata name and Kyu')
        self.name_label.place(rely=0.3, relx=0, relwidth=1)

        # Frame3 HOLD CODE TEXT BOX AND BUTTONS
        frame3 = tk.Frame(self.master)
        frame3.place(relwidth=0.85, relheight=0.5, relx=0.05, rely=0.35)

        frame_textbox = tk.Frame(frame3)
        frame_textbox.pack(side='left',expand=1, fill='both')

        frame_buttons = tk.Frame(frame3)
        frame_buttons.pack()

        self.e2 = tk.Text(frame_textbox, bg='#707070')
        self.e2.place(relwidth=0.99, relheight=0.99)

        stat_button = tk.Button(frame_buttons, text='Stats', padx=1, pady=1,
                                command=StatsWindow, width=8,
                                fg='#2d69e0', font=16)
        stat_button.grid()

        # Frame 4 hold two buttons Create and Clear
        frame4 = tk.Frame(self.master, bd=1)
        frame4.place(width=300, height=35, relx=0.5, rely=0.9, anchor='s')
        # Button to create file with given content(code)
        create_button = tk.Button(frame4, text=u'\u2713' + 'Create File', padx=20, pady=5,
                                  command=lambda: self.button_create_file(),
                                  fg='#26de58')
        create_button.place(rely=1, relx=0.3, anchor='s')

        clear_button = tk.Button(frame4, text='X  Clear', padx=20, pady=5,
                                 command=lambda: self.clear(),
                                 fg='red')
        clear_button.place(rely=1, relx=0.75, anchor='s')

    # After Scrapping displays scrapped Kata Name and its Kyu to know with which kata we are creating
    def show_name_rank(self):
        self.name_label.configure(text=self.kata_name + '  |  ' + self.kata_rank)

    def button_scrap(self):
        try:
            self.link = self.e1.get()
            self.get_kata_info()
            self.show_name_rank()
        except AttributeError:
            messagebox.showerror('Wrong link', 'Wrong link provided')

    # Methods for Create File BUTTON
    def button_create_file(self):
        try:
            if not self.get_content():
                msg_blank_file = messagebox.askyesno("Warning", "No code entered. Do you want to create blank file ?")
                if msg_blank_file:
                    self.create_file()
                else:
                    pass
            else:
                self.create_file()
        except TypeError:
            messagebox.showerror('Error', 'No info provided')

    # Creates content variable that stores textBox content
    # lstrip('\n') is used to strip the newlinechar that comes with get.entry
    # in order to be able to check if the content variable is empty in buttonCreateFile method
    def get_content(self):
        self.content = self.e2.get('1.0', tk.END).lstrip('\n')
        return self.content

    # Clear all data(variables, textbox, labels)
    def clear(self):
        self.e1.delete(0, tk.END)
        self.e2.delete('1.0', tk.END)
        self.name_label.configure(text='Kata name and Kyu')
        super().__init__()

    # In the Directory D:/Codewars/... creates file kata_name.py in the folder
    # In the File writes the link to Kata and code we passed
    def create_file(self):
        path = self.path_check()
        if path:
            with open(path, 'w') as file:
                file.write(f'"""{self.link}"""' + '\r\n\n' + self.content)
            messagebox.showinfo('CodeWars Adder', f'Kata Created! saved as: {self.file_name}')
        else:
            messagebox.showerror('File exists', 'File exists')


class StatsWindow:

    def __init__(self):
        self.kata_qty = None
        self.create_stat()
        window = tk.Toplevel(root, height=300, width=400)
        label = tk.Label(window, text=f'Kata done:\n{self.kata_qty}')
        label.place(relx=0.5, rely=0.1, anchor='nw')

    @staticmethod
    def is_py(directory):
        return [file for file in directory if file.endswith('.py')]

    def create_stat(self):
        directories = [f for f in os.listdir('D:/00_CodeWars/') if f.endswith('kyu')]
        dir_files = {directory: len(self.is_py(os.listdir('D:/00_CodeWars/' + directory)))
                     for directory in directories}
        self.kata_qty = sum(dir_files.values())


KataAdder(root)
root.mainloop()
