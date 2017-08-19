import tkinter as tk
import tkinter.ttk as ttk


class ConstraintsWindow(tk.Toplevel):

    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.title("Constraints")
        self.minsize(width=400, height=300)

        self.tree_view = ttk.Treeview(self, columns="value")
        self.tree_view.column("value", anchor='center', width=100)
        self.tree_view.heading("value", text="Value")
        self.tree_view.heading("#0", text='Name', anchor='w')
        self.tree_view.column("#0", anchor='w', width=200)

        week = ("monday", "tuesday", "Wednesday", "thursday", "friday", "saturday", "sunday")
        for day in week:
            day = self.tree_view.insert("", week.index(day), day, text=day.title())
            self.tree_view.insert(day, 0, text="Minimum Calories", values=2000)
            self.tree_view.insert(day, 1, text="Carbohydrates (%)", values=50)
            self.tree_view.insert(day, 2, text="Proteins (%)", values=20)
            self.tree_view.insert(day, 3, text="Fats (%)", values=30)

        self.tree_view.pack(side='left', fill=tk.BOTH, expand=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree_view.yview)
        vsb.pack(side='right', fill='y')
        self.tree_view.configure(yscrollcommand=vsb.set)

