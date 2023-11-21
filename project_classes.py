import numpy as np


class UserInput:
    def init(self):
        self.S = None  # A vector of coefficients of supply
        self.C = None  # A matrix of coefficients of costs
        self.D = None  # A vector of coefficients of demand
        self.size = []
        self.max_problem = True
        self.x = None

    def collect_data(self):
        print("This program is designed to solve Transportation Problem")
        self.input_S()
        self.input_size()
        self.input_C()
        self.input_D()

    def input_size(self):
        self.size = list(map(int, input("Enter the size of matrix C (a matrix of coefficients of costs) (example: 4 5): ").split()))

    def input_S(self):
        self.S = list(map(float, input("Enter vector S (example: 2 3 4 0 0): ").split()))

    def input_C(self):
        self.C = []
        print("Enter matrix C:\nexample: 4 5 6 1 0\n         5 1 2 0 1")
        for i in range(self.size[0]):
            line = list(map(float, input().split()))
            self.C.append(line)

    def input_D(self):
        self.D = list(map(float, input("Enter vector D (example: 2 3 4 0 0): ").split()))


class SolveTransportationProblem:
    def __init__(self, S, C, D, sources, destinations):
        self.S = np.array(S).astype(np.float64)  # a A vector of coefficients of supply
        self.C = np.array(C).astype(np.float64)  # c A matrix of coefficients of costs
        self.D = np.array(D).astype(np.float64)  # b A vector of coefficients of demand
        self.num_sources = sources
        self.num_destinations = destinations

    def transportation_problem_nw(self):

        X = np.zeros((self.num_sources, self.num_destinations))

        i, j = 0, 0
        while i < self.num_sources and j < self.num_destinations:
            x_ij = min(self.S[i], self.D[j])
            X[i][j] = x_ij
            self.S[i] -= x_ij
            self.D[j] -= x_ij

            if self.S[i] == 0:
                i += 1
            if self.D[j] == 0:
                j += 1

        return X
