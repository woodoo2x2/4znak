import tkinter as tk
import tkinter.filedialog as fd
import zipfile, os
import json
from eps_convert import convert_eps_to_jpeg, print_label


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        btn_file = tk.Button(self, text="Выбрать файл",
                             command=self.choose_file)
        btn_print = tk.Button(self, text='Печать', command=self.exec)
        btn_file.pack(padx=60, pady=10)
        btn_print.pack(padx=60, pady=10)
        self.files = []

    def choose_file(self):
        self.files = []
        filetypes = ("zip", "*.zip"),

        filename = fd.askopenfilename(title="Открыть файл", initialdir="/",
                                      filetypes=filetypes, multiple=True)

        if type(filename) == str:
            self.files.append(filename)
        else:
            for i in filename:
                self.files.append(i)

    def exctract_zip(self, zipname):
        with zipfile.ZipFile(zipname, mode='r') as zf:
            zf.extractall()
            for file in zf.namelist():

                if file == 'attributes.json':
                    self.json_name = file
                else:
                    self.image_name = file

    def dump_json(self, json_name):
        with open(json_name, 'r', encoding='utf-8') as file:
            a = json.load(file)
            self.good_name = tuple(a['gtinProductAttributes'].items())[0][1]['name'].capitalize()
            self.good_size = tuple(a['gtinProductAttributes'].items())[0][1]['size'].capitalize()
            self.good_color = tuple(a['gtinProductAttributes'].items())[0][1]['color'].capitalize()

    def exec(self):
        for zip in self.files:
            self.exctract_zip(zip)
            self.dump_json(self.json_name)
            convert_eps_to_jpeg(self.image_name, self.good_name, self.good_color, self.good_size)
            print_label()
            os.remove(self.image_name)
            os.remove(self.json_name)
            os.remove('example.jpeg')


