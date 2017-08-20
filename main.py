import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import pandas
from constraints import ConstraintsWindow
from table import Table


class Application(ttk.Frame):
    def __init__(self, parent=None, **kwargs):
        ttk.Frame.__init__(self, **kwargs)
        self.parent = parent
        self.menu_bar = None
        self.file_menu = None
        self.constraints_menu = None
        self.edit_menu = None
        self.run_menu = None
        self.file_name = None
        self.tree_view = None
        self.dataframe = None
        self.table = None
        self.constraints_window = None
        self.entryPopup = None
        self.create_ui()

    def create_ui(self):
        self.menu_bar = tk.Menu(self)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New", command=(lambda: self.table.clear()))
        self.file_menu.add_command(label="Open...", command=self.load_file)
        self.file_menu.add_command(label="Save")
        self.file_menu.entryconfig('Save', state="disabled")
        self.file_menu.add_command(label="Save As...")
        self.file_menu.entryconfig('Save As...', state="disabled")
        self.file_menu.add_separator()

        self.constraints_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.constraints_menu.add_command(label="Constraints...", command=self.open_constraints_window)
        self.file_menu.add_cascade(label="Settings", menu=self.constraints_menu)
        self.file_menu.add_separator()

        self.file_menu.add_command(label="Exit", command=self.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="Insert Row...")
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.menu_bar.entryconfig('Edit', state="disabled")

        self.run_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.run_menu.add_command(label="Run Solver")
        self.menu_bar.add_cascade(label="Run", menu=self.run_menu)
        self.menu_bar.entryconfig('Run', state="disabled")

        self.parent.config(menu=self.menu_bar)
        self.table = Table(self.parent)
        # self.create_table()

    def load_file(self):
        self.file_name = filedialog.askopenfilename(filetypes=[("CSV files (*.csv)", "*.csv")])
        if self.file_name is not '':
            self.dataframe = pandas.read_csv(self.file_name)
            self.table.clear()
            self.table.load_table(self.dataframe)
            self.menu_bar.entryconfig('Run', state="normal")
            self.menu_bar.entryconfig('Edit', state="normal")

    def open_constraints_window(self):
        self.constraints_window = ConstraintsWindow(self.parent)


def main(name):
    root = tk.Tk()
    root.title(name)
    root.minsize(width=1000, height=500)
    Application(parent=root)
    root.mainloop()


if __name__ == '__main__':
    main("Diet Optimizer")
