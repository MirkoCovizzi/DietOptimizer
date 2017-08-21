from table import TableWindowView
import json
import pulp

settings_file = 'constraints.json'


class ConstraintsWindow(TableWindowView):

    def __init__(self, *args, file_name=settings_file, **kwargs):
        super(ConstraintsWindow, self).__init__(*args, **kwargs)
        self.file_name = file_name

        with open(self.file_name) as file:
            self.settings = json.load(file)

        self.dictionary = self.settings
        self.load_dictionary()
        self.table.disable_first_column_popup()

    def on_button_press(self):
        name_list = self.table.get_children()
        for name in name_list:
            constraint_list = self.table.get_children(item=name)
            for constraint in constraint_list:
                i = constraint_list.index(constraint)
                self.settings[name][i]['value'] = self.table.item(constraint)['values'][0]

        json.dump(self.settings, open(self.file_name, 'w'), indent=4)
        self.destroy()


class Constraint:

    def __init__(self, name, value, constraint_type):
        self.name = name
        self.value = value
        self.constraint_type = constraint_type

    @staticmethod
    def get_constraints(products, foods, constraints_file='constraints.json'):
        with open(constraints_file) as file:
            constraints = json.load(file)

        expressions_dict = {}
        name_list = list(constraints.keys())
        for name in name_list:
            expressions_dict[name] = []
            constraints_list = constraints[name]
            for constraint in constraints_list:
                i = constraints_list.index(constraint)
                if constraints[name][i]['constraint_type'] == 'LE':
                    expr = pulp.lpSum([products[food] * float(foods.loc[food, (constraints[name][i]['name']).title()])
                            for food in foods.index]) <= float(constraints[name][i]['value'])
                elif constraints[name][i]['constraint_type'] == 'GE':
                    expr = pulp.lpSum([products[food] * float(foods.loc[food, (constraints[name][i]['name']).title()])
                            for food in foods.index]) >= float(constraints[name][i]['value'])
                elif constraints[name][i]['constraint_type'] == 'E':
                    expr = pulp.lpSum([products[food] * float(foods.loc[food, (constraints[name][i]['name']).title()])
                            for food in foods.index]) == float(constraints[name][i]['value'])
                expressions_dict[name].append(expr)
        return expressions_dict
