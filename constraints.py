import tkinter as tk
import tkinter.ttk as ttk
from table import Table
import json

settings_file = 'settings.json'


class ConstraintsWindow(tk.Toplevel):

    def __init__(self, *args, **kwargs):
        super(ConstraintsWindow, self).__init__(*args, **kwargs)
        self.title("Constraints")
        self.minsize(width=600, height=300)

        ttk.Button(self, text="Ok", command=self.ok_press).pack(side='bottom')
        self.table = Table(self, structure={'name': 'Name', 'value': 'Value'})
        self.table.disable_first_column_popup()
        self.settings = None

        with open(settings_file) as file:
            self.settings = json.load(file)

        name_list = list(self.settings.keys())
        for name in name_list:
            self.table.insert('', name.index(name), name, text=name.title())
            constraint_list = self.settings[name]
            for constraint in constraint_list:
                i = constraint_list.index(constraint)
                self.table.insert(name, i, text=self.settings[name][i]['text'], values=self.settings[name][i]['values'])

    def ok_press(self):
        name_list = self.table.get_children()
        for name in name_list:
            constraint_list = self.table.get_children(item=name)
            for constraint in constraint_list:
                i = constraint_list.index(constraint)
                self.settings[name][i]['values'] = self.table.item(constraint)['values']

        json.dump(self.settings, open(settings_file, 'w'), indent=4)
        self.destroy()
