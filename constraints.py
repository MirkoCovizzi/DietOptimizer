import tkinter as tk
import tkinter.ttk as ttk
from table import Table
import json


class ConstraintsWindow(tk.Toplevel):

    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.title("Constraints")
        self.minsize(width=600, height=300)

        ttk.Button(self, text="Ok", command=self.ok_press).pack(side='bottom')
        self.table = Table(self, structure={'name': 'Name', 'value': 'Value'})
        self.table.disable_first_column_popup()

        with open('settings.json') as file:
            settings = json.load(file)

        name_list = list(settings.keys())
        for name in name_list:
            self.table.insert('', name.index(name), name, text=name.title())
            constraint_list = settings[name]
            for constraint in constraint_list:
                i = constraint_list.index(constraint)
                self.table.insert(name, i, text=settings[name][i]['text'], values=settings[name][i]['values'])

    def ok_press(self):
        self.destroy()
