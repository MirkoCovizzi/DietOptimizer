import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import pandas
from constraints import ConstraintsWindow


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
        self.table = None
        self.constraints_window = None
        self.entryPopup = None
        self.create_ui()

    def create_ui(self):
        self.menu_bar = tk.Menu(self)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New", command=(lambda: self.tree_view.delete(*self.tree_view.get_children())))
        self.file_menu.add_command(label="Open...", command=self.load_file)
        self.file_menu.add_command(label="Save")
        self.file_menu.add_command(label="Save As...")
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
        self.create_table()

    def create_table(self):
        tv = ttk.Treeview(self.parent, selectmode='browse')
        tv['columns'] = ('quantity', 'calories', 'carbohydrates', 'proteins', 'fats', 'price')
        tv.heading("#0", text='Name', anchor='w')
        tv.column("#0", anchor='w', width=100)
        tv.heading('quantity', text='Quantity (g)')
        tv.column('quantity', anchor='center', width=100)
        tv.heading('calories', text='Calories (Kcal)')
        tv.column('calories', anchor='center', width=100)
        tv.heading('carbohydrates', text='Carbohydrates (g)')
        tv.column('carbohydrates', anchor='center', width=150)
        tv.heading('proteins', text='Proteins (g)')
        tv.column('proteins', anchor='center', width=100)
        tv.heading('fats', text='Fats (g)')
        tv.column('fats', anchor='center', width=100)
        tv.heading('price', text='Price (€)')
        tv.column('price', anchor='center', width=100)
        self.tree_view = tv
        self.tree_view.pack(side='left', fill=tk.BOTH, expand=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.parent.grid_rowconfigure(0, weight=1)
        self.parent.grid_columnconfigure(0, weight=1)
        vsb = ttk.Scrollbar(self.parent, orient="vertical", command=self.tree_view.yview)
        vsb.pack(side='right', fill='y')
        self.tree_view.configure(yscrollcommand=vsb.set)
        self.tree_view.bind("<Double-1>", self.on_double_click)

    def load_file(self):
        self.file_name = filedialog.askopenfilename(filetypes=[("CSV files (*.csv)", "*.csv")])
        if self.file_name is not '':
            self.table = pandas.read_csv(self.file_name)
            self.tree_view.delete(*self.tree_view.get_children())
            for i in range(len(self.table)):
                self.tree_view.insert('', i, text=self.table.iloc[i]['Name'] + str(i), values=(self.table.iloc[i][1],
                                                                                               self.table.iloc[i][2],
                                                                                               self.table.iloc[i][3],
                                                                                               self.table.iloc[i][4],
                                                                                               self.table.iloc[i][5],
                                                                                               self.table.iloc[i][6]))
            self.menu_bar.entryconfig('Run', state="normal")
            self.menu_bar.entryconfig('Edit', state="normal")

    def open_constraints_window(self):
        self.constraints_window = ConstraintsWindow(self.parent)

    def on_double_click(self, event):
        x = self.master.winfo_x()
        y = self.master.winfo_y()
        rowid = self.tree_view.identify_row(event.y)
        column = self.tree_view.identify_column(event.x)

        xi, yi, width, height = self.tree_view.bbox(rowid, column)
        self.entryPopup = EntryPopup(self.tree_view, rowid, column)
        self.entryPopup.geometry('%dx%d+%d+%d' % (width, 50, x + xi - (width - width) / 2, y + yi + (50 - height) / 2))


class EntryPopup(tk.Toplevel):
    def __init__(self, master_tree_view, rowid, column, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.master_tree_view = master_tree_view
        self.rowid = rowid
        self.column = column
        s = str(self.column).replace('#', '')
        self.c = int(s)
        self.attributes("-toolwindow", 1)
        self.title("Edit")
        self.resizable(width=0, height=0)
        self.entry = None

        ttk.Button(self, text="Update", command=self.update_master_tree_view).pack(side='bottom')
        self.entry = ttk.Entry(self, justify='center')
        self.entry.focus()
        self.entry.pack(side='top', fill=tk.BOTH, expand=1)
        self.set_value(self.master_tree_view.item(rowid)['values'][self.c - 1])
        self.entry.bind("<Return>", self.update_master_tree_view)

    def set_value(self, value):
        self.entry.insert(0, value)

    def update_master_tree_view(self, event=None):
        values = self.master_tree_view.item(self.rowid)['values']
        values[self.c - 1] = self.entry.get()
        self.master_tree_view.item(self.rowid, values=values)
        self.destroy()


def main(name):
    root = tk.Tk()
    root.title(name)
    root.minsize(width=1000, height=500)
    Application(parent=root)
    root.mainloop()


if __name__ == '__main__':
    main("Diet Optimizer")
