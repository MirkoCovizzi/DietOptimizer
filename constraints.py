import tkinter as tk
import tkinter.ttk as ttk
from table import Table


class ConstraintsWindow(tk.Toplevel):

    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.title("Constraints")
        self.minsize(width=400, height=300)

        ttk.Button(self, text="Ok", command=self.ok_press).pack(side='bottom')
        self.table = Table(self, structure={'name': 'Name', 'value': 'Value'})

        week = ("monday", "tuesday", "Wednesday", "thursday", "friday", "saturday", "sunday")
        for day in week:
            day = self.table.insert("", week.index(day), day, text=day.title())
            self.table.insert(day, 0, text="Minimum Calories", values=2000)
            self.table.insert(day, 1, text="Carbohydrates (%)", values=50)
            self.table.insert(day, 2, text="Proteins (%)", values=20)
            self.table.insert(day, 3, text="Fats (%)", values=30)

    def ok_press(self):
        self.destroy()