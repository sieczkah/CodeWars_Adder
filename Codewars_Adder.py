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
        self.path = self.create_path()

    def create_path(self):
        try:
            with open('path.txt', 'r') as path_txt:
                path = path_txt.read()
                return path if os.path.exists(path) else self.ask_path()
        except FileNotFoundError:
            return self.ask_path()

    def change_path(self):
        self.path = self.ask_path()
        print(self.path)

    @staticmethod
    def ask_path(current_path=os.getcwd()):
        path = filedialog.askdirectory(initialdir=current_path)
        if os.path.exists(path):
            with open('path.txt', 'w') as path_txt:
                path_txt.write(path)
            return path

    def get_path(self):
        return self.path


class KataFile:
    path = DirPath()

    def __init__(self):
        self.link = None
        self.kata_name = None
        self.file_name = None
        self.kata_rank = None
        self.content = None

    @classmethod
    def change_path(cls):
        cls.path.change_path()

    # Getting kata info wit codewars api,
    # later is used to create file in corresponding kyu folder
    def get_kata_info(self):
        pattern = re.compile(r'(https?://)?(www\.codewars\.com/kata/\w+)')
        self.link = re.match(pattern, self.link).group()
        kata_json = requests.get(self.link + '.json').json()

        self.kata_name = kata_json['name']
        self.kata_rank = kata_json['rank']['name']
        self.file_name = re.sub(r'(?!-|\s|\(|\))\W+', ' ', self.kata_name)

    # checks if file exists If not calling func create if it exists
    # asking the user if to overwrite the File and takes action according to Yes/No answer
    @staticmethod
    def make_dir(path, directory):
        if not os.path.exists(f'{path}/{directory}'):
            os.mkdir(f'{path}/{directory}')

    @staticmethod
    def check_filepath(file_path):
        if os.path.exists(file_path):
            msg_exist = messagebox.askyesno('File Error', 'File exists want to overwrite?')
            return not msg_exist
        else:
            return True

    def create_file(self):
        file_path = f"{self.path.get_path()}/{self.kata_rank}/{self.file_name}.py"

        if self.check_filepath(file_path):
            self.make_dir(self.path.get_path(), self.kata_rank)
            with open(file_path, 'w') as file:
                file.write(f'"""{self.link}"""' + '\r\n\n' + self.content)
            messagebox.showinfo('CodeWars Adder', f'Kata Created! saved as: {self.file_name}')


class KataAdder(KataFile):

    # Init basically Creates the GUI and sets variables that will be used
    def __init__(self, master):
        self.master = master
        canvas = tk.Canvas(root, height=700, width=700)
        canvas.pack()

        super().__init__()
        self.stats = Stats(self.path.get_path())

        # Frame1 hold whole window
        frame_1_main = tk.Frame(self.master)
        frame_1_main.place(relwidth=1, relheight=1)

        # Frame 2 holds entry box for url and get button
        frame_2_url = tk.Frame(self.master, bd=5)
        frame_2_url.place(relwidth=0.9, relheight=0.1, relx=0.05, rely=0.1)
        self.e1 = tk.Entry(frame_2_url)
        self.e1.place(relwidth=1, relheight=0.5)
        get_info_button = tk.Button(frame_2_url, text='Get Kata Info', padx=10, pady=5,
                                    command=lambda: self.button_scrap(),
                                    fg='#f1ff33', activebackground='#202020', activeforeground='#f1ff33')
        get_info_button.place(rely=0.55, relx=0.5, anchor='n')

        # Frame 3 holds kata name and rank label
        frame_3_namelabel = tk.Frame(self.master)
        frame_3_namelabel.place(relwidth=0.9, relheight=0.1, relx=0.05, rely=0.2)
        self.name_label = tk.Label(frame_3_namelabel, text='Kata name and Kyu')
        self.name_label.place(rely=0.3, relx=0, relwidth=1)

        # Frame 4 hold code entry box and rightside menu
        frame_4_code_entry = tk.Frame(self.master)
        frame_4_code_entry.place(relwidth=0.9, relheight=0.5, relx=0.05, rely=0.35)

        frame_textbox = tk.Frame(frame_4_code_entry)
        frame_textbox.pack(side='left', expand=1, fill='both')
        self.e2 = tk.Text(frame_textbox, bg='#707070')
        self.e2.place(relwidth=0.99, relheight=0.98)

        frame_buttons = tk.Frame(frame_4_code_entry)
        frame_buttons.pack()

        stat_button = tk.Button(frame_buttons, text='Stats', padx=1, pady=3,
                                command=lambda: self.stats.open_statstab(), width=8,
                                fg='#2d69e0', font=16)
        stat_button.grid()

        chose_button = tk.Button(frame_buttons, text='Chose Directory', padx=1, pady=3,
                                 command=lambda: self.button_chosedir(), width=8,
                                 fg='#2d69e0', font=16, wraplength=100)
        chose_button.grid()

        # Frame 5 holds clear and save buttons
        frame_5_bottom = tk.Frame(self.master, bd=1)
        frame_5_bottom.place(width=300, height=35, relx=0.5, rely=0.9, anchor='s')

        create_button = tk.Button(frame_5_bottom, text=u'\u2713' + 'Create File', padx=20, pady=5,
                                  command=lambda: self.button_create_file(),
                                  fg='#26de58')
        create_button.place(rely=1, relx=0.3, anchor='s')

        clear_button = tk.Button(frame_5_bottom, text='X  Clear', padx=20, pady=5,
                                 command=lambda: self.clear(),
                                 fg='red')
        clear_button.place(rely=1, relx=0.75, anchor='s')

    # After Scrapping displays scrapped Kata Name and its Kyu to know with which kata we are creating
    def show_name_rank(self):
        self.name_label.configure(text=self.kata_name + '  |  ' + self.kata_rank)

    def button_chosedir(self):
        self.change_path()
        self.stats = Stats(self.path.get_path())

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
    # lstrip('\n') is used to strip the newline char that comes with get.entry
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


class Stats:

    def __init__(self, path):
        self.path = path
        self.kata_qty = self.create_stat()

    def open_statstab(self):
        window = tk.Toplevel(root, height=300, width=400)
        label = tk.Label(window, text=f'Kata done:\n{self.kata_qty}')
        label.place(relx=0.5, rely=0.1, anchor='nw')

    @staticmethod
    def is_py(directory):
        return [file for file in directory if file.endswith('.py')]

    def create_stat(self):
        directories = [f for f in os.listdir(self.path) if f.endswith('kyu')]
        dir_files = {directory: len(self.is_py(os.listdir(f'{self.path}/' + directory)))
                     for directory in directories}
        return sum(dir_files.values())


KataAdder(root)
root.mainloop()
