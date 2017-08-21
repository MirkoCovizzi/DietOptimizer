import pulp
from constraints import Constraint


class Solver:
    def __init__(self, dataframe=None):
        self.foods = dataframe
        self.foods = self.foods.set_index('Name')
        self.products = pulp.LpVariable.dict("product",
                                             (food for food in self.foods.index),
                                             lowBound=0,
                                             cat=pulp.LpInteger)

    def solve(self):
        expressions_dict = Constraint.get_constraints(self.products, self.foods)
        output_dict = {}
        for name in expressions_dict.keys():
            output_dict[name] = []
            model = pulp.LpProblem("Cost minimising problem", pulp.LpMinimize)

            model += pulp.lpSum(
                [self.products[food] * float(self.foods.loc[food, 'Price']) for food in self.foods.index])
            for expressions_list in expressions_dict[name]:
                model += expressions_list

            model.solve()

            for p in self.products:
                var_output = {
                    'product': p,
                    'quantity': self.products[p].varValue,
                }
                output_dict[name].append(var_output)

            separator = {'product': '_____', 'quantity': ''}
            output_dict[name].append(separator)
            status = {'product': 'Status', 'quantity': pulp.LpStatus[model.status]}
            output_dict[name].append(status)
            calories = {'product': 'Total Calories (Kcal)', 'quantity': round(sum([self.products[p].varValue *
                                                                                          float(self.foods.loc[
                                                                                                    p, 'Calories'])
                                                                                          for p in self.products]), 2)}
            output_dict[name].append(calories)
            carbohydrates = {'product': 'Total Carbohydrates (g)',
                             'quantity': round(sum([self.products[p].varValue *
                                                           float(self.foods.loc[p, 'Carbohydrates'])
                                                           for p in self.products]), 2)}
            output_dict[name].append(carbohydrates)
            proteins = {'product': 'Total Proteins (g)', 'quantity': round(sum([self.products[p].varValue *
                                                                                       float(self.foods.loc[
                                                                                                 p, 'Proteins'])
                                                                                       for p in self.products]), 2)}
            output_dict[name].append(proteins)
            fats = {'product': 'Total Fats (g)', 'quantity': round(sum([self.products[p].varValue *
                                                                               float(self.foods.loc[p, 'Fats'])
                                                                               for p in self.products]), 2)}
            output_dict[name].append(fats)
            objective = {'product': 'Total Price (€)', 'quantity': round(pulp.value(model.objective), 2)}
            output_dict[name].append(objective)

        return output_dict
