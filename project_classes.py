import numpy as np
from prettytable import PrettyTable


class UserInput:
    def __init__(self):
        self.S = None  # A vector of coefficients of supply
        self.C = None  # A matrix of coefficients of costs
        self.D = None  # A vector of coefficients of demand
        self.size = [3, 4]

    def collect_data(self):
        print("This program is designed to solve Transportation Problem that has 3 sources and 4 destinations")
        self.input_S()
        self.input_C()
        self.input_D()

    def input_S(self):
        self.S = list(map(int, input("Enter vector S (example: 12 17 11): ").split()))

    def input_C(self):
        self.C = []
        print("Enter matrix C:\nexample: 500 750 300 450\n         650 800 400 600\n         400 700 500 550")
        for i in range(self.size[0]):
            line = list(map(int, input().split()))
            self.C.append(line)

    def input_D(self):
        self.D = list(map(int, input("Enter vector D (example: 10 10 10 10): ").split()))


class SolveTransportationProblem:
    def __init__(self, S, C, D, sources, destinations):
        self.S = np.array(S, dtype=int)  # A vector of coefficients of supply
        self.C = np.array(C, dtype=int)  # A matrix of coefficients of costs
        self.D = np.array(D, dtype=int)  # A vector of coefficients of demand
        self.num_sources = sources
        self.num_destinations = destinations

    def print_input_parameter_table(self):
        table = PrettyTable()
        table.field_names = [""] + [f"D_{j + 1}" for j in range(len(self.D))]

        for i, row in enumerate(self.C):
            table.add_row([f"S_{i + 1}", *row])

        s_values = [f"{self.S[i]}" for i in range(len(self.C))]
        table.add_column("Supply", s_values, align="c")

        d_values = list(map(str, self.D))
        table.add_row(["Demand"] + d_values + [" "])

        print("\nInput Parameter Table:")
        print(table)

    def transportation_problem_nw(self):
        """
            Implementation of North-West corner method
        """

        X = np.zeros((self.num_sources, self.num_destinations), dtype=int)
        supply = np.copy(self.S)
        demand = np.copy(self.D)

        i, j = 0, 0
        while i < self.num_sources and j < self.num_destinations:
            x_ij = min(supply[i], demand[j])
            X[i][j] = x_ij
            supply[i] -= x_ij
            demand[j] -= x_ij

            if supply[i] == 0:
                i += 1
            if demand[j] == 0:
                j += 1

        return X

    def transportation_problem_vogel(self):
        """
            Implementation of Vogel’s approximation method
        """
        X = np.zeros((self.num_sources, self.num_destinations), dtype=int)
        supply = np.copy(self.S)
        demand = np.copy(self.D)
        costs = np.copy(self.C)

        while np.sum(supply) > 0 and np.sum(demand) > 0:
            max_row_diff, max_row_diff_idx = self.get_cost_differences_and_indexes(costs, axis=1)
            max_col_diff, max_col_diff_idx = self.get_cost_differences_and_indexes(costs, axis=0)

            if max_row_diff == max_row_diff_idx == max_col_diff == max_col_diff_idx:    # the last cost
                last = np.where(costs >= 0)
                i, j = last[0][0], last[1][0]
            elif max_row_diff > max_col_diff:
                i = max_row_diff_idx
                j = np.where(costs[i] >= 0)[0][np.argmin(costs[i][costs[i] >= 0])]
            else:
                j = max_col_diff_idx
                i = np.where(costs[:, j] >= 0)[0][np.argmin(costs[:, j][costs[:, j] >= 0])]

            quantity = min(supply[i], demand[j])
            X[i][j] = quantity

            supply[i] -= quantity
            demand[j] -= quantity

            zero_supply_indices = np.where(supply == 0)[0]
            zero_demand_indices = np.where(demand == 0)[0]

            for i in zero_supply_indices:
                costs[i] = -1

            for j in zero_demand_indices:
                costs[:, j] = -1

        return X

    @staticmethod
    def get_cost_differences_and_indexes(costs_matrix, axis):
        differences = []
        if axis == 0:
            sorted_by_col = np.sort(costs_matrix, axis=0)
            for col in sorted_by_col.T:
                valid_values = col[col != -1]
                if len(valid_values) == 1:
                    return -1, -1
                elif len(valid_values) == 0:
                    differences.append(-1)
                    continue
                min1, min2 = valid_values[:2]
                differences.append(abs(min2 - min1))
            max_difference_index = np.argmax(differences)
            return differences[max_difference_index], max_difference_index
        elif axis == 1:
            sorted_by_rows = np.sort(costs_matrix, axis=1)
            for row in sorted_by_rows:
                valid_values = row[row != -1]
                if len(valid_values) == 1:
                    return -1, -1
                elif len(valid_values) == 0:
                    differences.append(-1)
                    continue
                min1, min2 = valid_values[:2]
                differences.append(abs(min2 - min1))
            max_difference_index = np.argmax(differences)
            return differences[max_difference_index], max_difference_index
