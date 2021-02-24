from bs4 import BeautifulSoup
import requests
import tkinter as tk
from tkinter import messagebox
import re
import os.path

root = tk.Tk()
root.title('CodeWars Adder')


class CodewarsAdder:

    # Init basically Creates the GUI and sets variables that will be used
    def __init__(self, master):
        self.master = master
        canvas = tk.Canvas(root, height=700, width=700, bg='#202020')
        canvas.pack()

        frame1 = tk.Frame(master, bg='#3F3F3F')
        frame1.place(relwidth=0.9, relheight=0.05, relx=0.05, rely=0.1)

        frame2 = tk.Frame(master, bg='#3F3F3F')
        frame2.place(relwidth=0.7, relheight=0.2, relx=0.15, rely=0.5)

        self.e1 = tk.Entry(frame1, bg='#707070')
        self.e1.place(relwidth=0.996, relheight=0.99, x=0.5, y=0.5)

        self.e2 = tk.Text(frame2, bg='#707070')
        self.e2.place(relwidth=0.996, relheight=0.99, x=0.5, y=0.5)

        self.scrappButton = tk.Button(master, text='Scrap from source', padx=10, pady=5,
                                      command=lambda: self.button_scrap(),
                                      fg='#f1ff33', bg='#3F3F3F', activebackground='#202020',
                                      activeforeground='#f1ff33')
        self.scrappButton.place(rely=0.18, relx=0.4)

        self.addContentButton = tk.Button(master, text='Create File', padx=20, pady=5,
                                          command=lambda: self.button_create_file(),
                                          fg='#f1ff33', bg='#3F3F3F', activebackground='#202020',
                                          activeforeground='#f1ff33')
        self.addContentButton.place(rely=0.75, relx=0.4)

        self.name_label = tk.Label(self.master, text='Kata name and Kyu',
                                   font=('ComicSans', 14), fg='#f1ff33', bg='#202020')
        self.name_label.place(rely=0.3, relx=0.2)

        self.link = None
        self.kata_name = None
        self.file_name = None
        self.kata_rank = None
        self.contents = None

    # After Scrapping displays scrapped Kata Name and its Kyu to know with which kata we are creating
    def show_name_rank(self):
        self.name_label.configure(text=self.kata_name + ' ' + self.kata_rank)

    def button_scrap(self):
        try:
            self.scrapping()
        except:
            messagebox.showerror('Wrong link', 'Wrong link provided')

    # With BeautifulSoup from the passed link scrapps the Kata Name and Kyu,
    # later is used to create file in corresponding kyu folder
    def scrapping(self):
        self.link = self.e1.get()
        source = requests.get(self.link).text
        soup = BeautifulSoup(source, 'lxml')
        scrapped_name = soup.find('div', class_='flex items-center').h4.text

        self.kata_name = re.sub(r'Loading kata: ', '', scrapped_name, count=1,
                                flags=re.I)  # handles Loading Kata: that sometimes appears
        self.kata_rank = soup.find('div', class_='flex items-center').span.text
        self.show_name_rank()

    # creates filename from kata_name handles restricted symbols
    # and Loading Kata: prefix (that sometimes apperas when scrapping name)
    def create_file_name(self):
        self.file_name = re.sub(r'(?!-|\s|\(|\))\W+', '', self.kata_name)

    # From the text box(where whe put the code) creates contents variable
    # Which stores the inputted code
    def enter_content(self):
        self.contents = self.e2.get('1.0', tk.END)

    # checks if file exists If not calling func create if it exists
    # asking the user if to overwrite the File and takes action according to Yes/No answer
    def path_check(self):
        path = f"D:/CodeWars/{self.kata_rank}/{self.file_name}.py"
        if os.path.exists(path):
            msg_exist = messagebox.askyesno('File Error', 'File exists want to overwrite?')
            if msg_exist:
                self.create_file(path)
            else:
                pass
        else:
            self.create_file(path)

    # In the Directory D:/Codewars/... creates file kata_name.py in the folder
    # In the File writes the link to Kata and code we passed
    def button_create_file(self):
        self.enter_content()
        self.create_file_name()
        self.path_check()

    def create_file(self, path):
        with open(path, 'w') as file:
            if self.contents:
                file.write(f'"""{self.link}"""' + '\n\n' + self.contents)
            pass
        messagebox.showinfo('CodeWars Adder', 'Kata Created!')


CodewarsAdder(root)
root.mainloop()
