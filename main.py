import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox
from constraints import ConstraintsWindow
from table import Table, TableWindowView, TableOpenError
import os
from solver import Solver

application_name = "Diet Optimizer"
default_file_name = "Untitled"


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
        self.table_window_solution = None
        self.constraints_window = None
        self.entryPopup = None
        self.create_ui()

    def create_ui(self):
        self.parent.title(default_file_name + ' - ' + application_name)
        self.menu_bar = tk.Menu(self)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        self.bind_all("<Control-n>", self.new_file)
        self.file_menu.add_command(label="Open...", command=self.open_file, accelerator="Ctrl+O")
        self.bind_all("<Control-o>", self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        self.bind_all("<Control-s>", self.save_file)
        self.file_menu.entryconfig('Save', state="disabled")
        self.file_menu.add_command(label="Save As...", command=self.save_as_file)
        self.file_menu.entryconfig('Save As...', state="disabled")
        self.file_menu.add_separator()

        self.constraints_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.constraints_menu.add_command(label="Constraints...", command=self.open_constraints_window)
        self.file_menu.add_cascade(label="Settings", menu=self.constraints_menu)
        self.file_menu.add_separator()

        self.file_menu.add_command(label="Exit", command=self.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="Insert New Empty Row", command=self.insert_row, accelerator="Ctrl+I")
        self.bind_all("<Control-i>", self.insert_row)
        self.edit_menu.add_command(label="Duplicate Selected Rows", command=self.duplicate_selected_rows,
                                   accelerator="Ctrl+D")
        self.edit_menu.add_command(label="Delete Selected Rows", command=self.delete_selected_rows, accelerator="Del")
        self.bind_all("<Delete>", self.delete_selected_rows)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)

        self.run_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.run_menu.add_command(label="Run Solver", command=self.run_solver, accelerator="Ctrl+R")
        self.menu_bar.add_cascade(label="Run", menu=self.run_menu)
        self.menu_bar.entryconfig('Run', state="disabled")

        self.parent.config(menu=self.menu_bar)

        self.table = Table(self.parent)

    def new_file(self, event=None):
        self.table.clear()
        self.file_name = None
        self.file_menu.entryconfig('Save', state="disabled")
        self.menu_bar.entryconfig('Run', state="disabled")
        self.parent.title(default_file_name + ' - ' + application_name)

    def open_file(self, event=None):
        self.file_name = filedialog.askopenfilename(filetypes=[("CSV files (*.csv)", "*.csv")])
        base = os.path.basename(self.file_name)
        name = os.path.splitext(base)[0]
        if self.file_name is not '':
            self.table.clear()
            try:
                self.table.load_table(self.file_name)
                self.parent.title(name + ' - ' + application_name)
                self.file_menu.entryconfig('Save', state="normal")
                self.file_menu.entryconfig('Save As...', state="normal")
                self.menu_bar.entryconfig('Run', state="normal")
            except TableOpenError:
                messagebox.showerror('Error', 'This file has a wrong table structure.')
            except ValueError:
                messagebox.showerror('Error', 'At least one table cell contains a string value instead of a float.')

    def save_file(self, event=None):
        if self.file_name is not None:
            self.table.save_table(self.file_name)

    def save_as_file(self):
        if self.file_name is not None:
            base = os.path.basename(self.file_name)
            f = os.path.splitext(base)[0]
        else:
            f = default_file_name
        save_as_file_name = filedialog.asksaveasfilename(filetypes=[("CSV files (*.csv)", "*.csv")],
                                                         initialfile=f,
                                                         defaultextension='.csv')
        if save_as_file_name is not '':
            self.table.save_table(save_as_file_name)

            base = os.path.basename(save_as_file_name)
            name = os.path.splitext(base)[0]

            self.table.clear()
            self.table.load_table(save_as_file_name)

            self.parent.title(name + ' - ' + application_name)
            self.file_menu.entryconfig('Save', state="normal")
            self.file_menu.entryconfig('Save As...', state="normal")
            self.menu_bar.entryconfig('Run', state="normal")

    def open_constraints_window(self):
        self.constraints_window = ConstraintsWindow(self, title='Constraints', button_text='OK',
                                                    structure={'text': 'Name', 'value': 'Value'})

    def insert_row(self, event=None):
        self.table.insert_row()
        self.menu_bar.entryconfig('Run', state="normal")
        self.file_menu.entryconfig('Save As...', state="normal")

    def duplicate_selected_rows(self, event=None):
        self.table.duplicate_selected_rows()

    def delete_selected_rows(self, event=None):
        self.table.delete_selected_rows()
        if not self.table.get_children():
            self.menu_bar.entryconfig('Run', state="disabled")
            self.file_menu.entryconfig('Save As...', state="disabled")

    def run_solver(self):
        s = Solver(self.table.get_dataframe())
        solution = s.solve()
        if self.table_window_solution is not None:
            self.table_window_solution.destroy()

        self.table_window_solution = TableWindowView(self, dictionary=solution, title='Solution', popup=False,
                                                     structure={'product': 'Product', 'quantity': 'Quantity'})
        self.table_window_solution.wm_attributes("-topmost", 1)


def main(name):
    root = tk.Tk()
    root.title(name)
    root.minsize(width=1300, height=500)
    Application(parent=root)
    root.mainloop()


if __name__ == '__main__':
    main(application_name)
