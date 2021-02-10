from bs4 import BeautifulSoup
import requests
import tkinter as tk
from tkinter import messagebox

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

        self.scrappButton = tk.Button(master, text='Scrap from source', padx=10, pady=5, command=self.scrapping,
                                      fg='#f1ff33', bg='#3F3F3F', activebackground='#202020',
                                      activeforeground='#f1ff33')
        self.scrappButton.place(rely=0.18, relx=0.4)

        self.addContentButton = tk.Button(master, text='Create File', padx=20, pady=5,
                                          command=lambda: self.create_file(),
                                          fg='#f1ff33', bg='#3F3F3F', activebackground='#202020',
                                          activeforeground='#f1ff33')
        self.addContentButton.place(rely=0.75, relx=0.4)

        self.name_label = tk.Label(self.master, text='Kata name and Kyu',
                                   font=('ComicSans', 14), fg='#f1ff33', bg='#202020')
        self.name_label.place(rely=0.3, relx=0.2)

        self.link = None
        self.kata_name = None
        self.kata_kyu = None
        self.contents = None

    # After Scrapping displays scrapped Kata Name and its Kyu to know with which kata we are creating
    def kata_name_kyu(self):
        self.name_label.configure(text=self.kata_name + ' ' + self.kata_kyu)

    # With BeautifulSoup from the passed link scrapps the Kata Name and Kyu,
    # later is used to create file in corresponding kyu folder
    def scrapping(self):
        self.link = self.e1.get()
        source = requests.get(self.link).text
        soup = BeautifulSoup(source, 'lxml')
        self.kata_name = soup.find('div', class_='flex items-center').h4.text
        if 'Loading Kata:' in self.kata_name:
            self.kata_name = self.kata_name[14:]
        self.kata_kyu = soup.find('div', class_='flex items-center').span.text
        self.kata_name_kyu()

    # From the text box(where whe put the code) creates contents variable
    # Which stores the inputted code
    def enter_content(self):
        self.contents = self.e2.get('1.0', tk.END)

    # In the Directory D:/Codewars/... creates file kata_name.py in the folder
    # In the File writes the link to Kata and code we passed
    def create_file(self):
        self.enter_content()
        with open(f'D:/CodeWars/{self.kata_kyu}/{self.kata_name}.py', 'w') as file:
            if self.contents:
                file.write(f'"""{self.link}"""' + '\n\n' + self.contents)
            pass
        messagebox.showinfo('CodeWars Adder', 'Kata Created!')


CodewarsAdder(root)
root.mainloop()
