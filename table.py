import tkinter as tk
import tkinter.ttk as ttk
import pandas

struct = {'name': 'Name', 'quantity': 'Quantity (g)', 'calories': 'Calories (Kcal)',
          'carbohydrates': 'Carbohydrates (g)', 'proteins': 'Proteins (g)', 'fats': 'Fats (g)', 'price': 'Price (€)'}


class Table(ttk.Treeview):
    # 'structure' is an argument that, if specified, indicates a dictionary with the structure of the table
    def __init__(self, *args, structure=struct, **kwargs):
        super(Table, self).__init__(*args, **kwargs)
        self.structure = structure
        self.dataframe = None
        self.entry_popup = None
        self.disabled_first_column_popup = False
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
        self.bind("<Delete>", self.on_delete)

    def load_table(self, file_name):
        self.dataframe = pandas.read_csv(file_name)
        columns_list = list(self.dataframe)

        if columns_list != [str(x).title() for x in self.structure_keys_list]:
            print("test")
            return None
        for i in range(len(self.dataframe)):
            values = []
            for j in range(len(self.structure_keys_list) - 1):
                values.append(self.dataframe.iloc[i][j + 1])
            self.insert('', i, text=self.dataframe.iloc[i][0], values=tuple(values))

    def save_table(self, file_name):
        columns = [str(x).title() for x in self.structure_keys_list]
        names = [self.item(i)['text'] for i in self.get_children()]
        series = []
        series.append(names)
        series = series + [[self.item(i)['values'][j] for i in self.get_children()] for j in range(len(columns) - 1)]
        indices = [x for x in range(len(self.get_children()))]
        d = {col: pandas.Series(series[columns.index(col)], index=indices) for col in columns}
        self.dataframe = pandas.DataFrame(d, columns=columns)
        self.dataframe.to_csv(file_name, index=False)

    def clear(self):
        self.delete(*self.get_children())

    def insert_row(self):
        t = tuple([0 for x in range(len(self.structure_keys_list) - 1)])
        self.insert('', 'end', text='None', values=t)

    def delete_selected_rows(self):
        for item in self.selection():
            self.delete(item)

    def disable_first_column_popup(self):
        self.disabled_first_column_popup = True

    def on_double_click(self, event):
        if self.entry_popup is not None:
            self.entry_popup.destroy()
        x = self.master.winfo_x()
        y = self.master.winfo_y()
        rowid = self.identify_row(event.y)
        column = self.identify_column(event.x)  # Returns '#N', where N is the number of the column
        s = str(column).replace('#', '')  # Removes the character '#' from the column
        col = int(s)

        if rowid == '':
            return

        if col == 0:
            if self.disabled_first_column_popup:
                return
        xi, yi, width, height = self.bbox(rowid, column)
        self.entry_popup = EntryPopup(self, rowid, col)
        self.entry_popup.geometry('%dx%d+%d+%d' % (width, 50, x + xi - (width - width) / 2,
                                                   y + yi + (50 - height) / 2))

    def on_delete(self, event):
        self.delete_selected_rows()


class EntryPopup(tk.Toplevel):
    def __init__(self, parent_tree_view, rowid, column, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.parent_tree_view = parent_tree_view
        self.rowid = rowid
        self.column = column
        self.attributes("-toolwindow", 1)  # Removes Minimize and Maximize buttons
        self.title("Edit")
        self.resizable(width=0, height=0)
        self.entry = None

        ttk.Button(self, text="Update", command=self.update_parent_tree_view).pack(side='bottom')
        self.entry = ttk.Entry(self, justify='center')
        self.entry.focus()
        self.entry.pack(side='top', fill=tk.BOTH, expand=1)
        if self.column > 0:
            self.set_value(self.parent_tree_view.item(rowid)['values'][self.column - 1])
        else:
            self.set_value(self.parent_tree_view.item(rowid)['text'])
        self.entry.bind("<Return>", self.update_parent_tree_view)

    def set_value(self, value):
        self.entry.insert(0, value)

    def update_parent_tree_view(self, event=None):
        if self.column > 0:
            values = self.parent_tree_view.item(self.rowid)['values']
            values[self.column - 1] = self.entry.get()
            self.parent_tree_view.item(self.rowid, values=values)
        else:
            self.parent_tree_view.item(self.rowid, text=self.entry.get())
        self.destroy()
