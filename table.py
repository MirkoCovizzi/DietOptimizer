import tkinter as tk
import tkinter.ttk as ttk

struct = {'name': 'Name', 'quantity': 'Quantity (g)', 'calories': 'Calories (Kcal)',
          'carbohydrates': 'Carbohydrates (g)', 'proteins': 'Proteins (g)', 'fats': 'Fats (g)', 'price': 'Price (€)'}


class Table(ttk.Treeview):
    # 'structure' is an argument that, if specified, indicates a dictionary with the structure of the table
    def __init__(self, *args, structure=struct, **kwargs):
        super(Table, self).__init__(*args, **kwargs)
        self.structure = structure
        self.dataframe = None
        self.entry_popup = None
        self.structure_keys_list = list(self.structure.keys())
        self['columns'] = tuple(self.structure_keys_list[1:])
        self.heading("#0", text=self.structure[self.structure_keys_list[0]], anchor='w')
        self.column("#0", anchor='w', width=100)
        self.pack(side='left', fill=tk.BOTH, expand=1)

        for column in self['columns']:
            self.heading(column, text=self.structure[column])
            self.column(column, anchor='center', width=100)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        scroll_bar = ttk.Scrollbar(self.master, orient="vertical", command=self.yview)
        scroll_bar.pack(side='right', fill='y')
        self.configure(yscrollcommand=scroll_bar.set)
        self.bind("<Double-1>", self.on_double_click)

    def load_table(self, dataframe):
        self.dataframe = dataframe
        columns_list = list(self.dataframe)

        if columns_list != [str(x).title() for x in self.structure_keys_list]:
            return None
        for i in range(len(self.dataframe)):
            values = []
            for j in range(len(self.structure_keys_list) - 1):
                values.append(self.dataframe.iloc[i][j + 1])
            self.insert('', i, text=self.dataframe.iloc[i][0], values=tuple(values))

    def clear(self):
        self.delete(*self.get_children())

    def on_double_click(self, event):
        if self.entry_popup is not None:
            self.entry_popup.destroy()
        x = self.master.winfo_x()
        y = self.master.winfo_y()
        rowid = self.identify_row(event.y)
        column = self.identify_column(event.x)  # Returns '#N', where N is the number of the column

        xi, yi, width, height = self.bbox(rowid, column)
        self.entry_popup = EntryPopup(self, rowid, column)
        self.entry_popup.geometry('%dx%d+%d+%d' % (width, 50, x + xi - (width - width) / 2, y + yi + (50 - height) / 2))


class EntryPopup(tk.Toplevel):
    def __init__(self, parent_tree_view, rowid, column, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.parent_tree_view = parent_tree_view
        self.rowid = rowid
        self.column = column
        s = str(self.column).replace('#', '')  # Removes the character '#' from the column
        self.c = int(s)
        self.attributes("-toolwindow", 1)  # Removes Minimize and Maximize buttons
        self.title("Edit")
        self.resizable(width=0, height=0)
        self.entry = None

        ttk.Button(self, text="Update", command=self.update_parent_tree_view).pack(side='bottom')
        self.entry = ttk.Entry(self, justify='center')
        self.entry.focus()
        self.entry.pack(side='top', fill=tk.BOTH, expand=1)
        self.set_value(self.parent_tree_view.item(rowid)['values'][self.c - 1])
        self.entry.bind("<Return>", self.update_parent_tree_view)

    def set_value(self, value):
        self.entry.insert(0, value)

    def update_parent_tree_view(self, event=None):
        values = self.parent_tree_view.item(self.rowid)['values']
        values[self.c - 1] = self.entry.get()
        self.parent_tree_view.item(self.rowid, values=values)
        self.destroy()
