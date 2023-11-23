from project_classes import UserInput, SolveTransportationProblem

user_input = UserInput()
user_input.collect_data()
tr_problem = SolveTransportationProblem(user_input.S, user_input.C, user_input.D, user_input.size[0], user_input.size[1])
tr_problem.print_input_parameter_table()
# North-West corner method result
print("The solution comprises 3 initial basic feasible solution vectors represented as "
      "x = [x_11, x_12, x_13, x_14, x_21, x_22, x_23, x_24, x_31, x_32, x_33, x_34].\n"
      "Here, x_ij denotes: i - the selected source number, j - the chosen destination number.\n")
print("North-West corner method:")
result = tr_problem.transportation_problem_nw()
print("x = [" + ", ".join([str(x) for x in result.flatten()]) + "]")
# Vogel’s approximation method result
print("Vogel’s approximation method:")
result = tr_problem.transportation_problem_vogel()
print("x = [" + ", ".join([str(x) for x in result.flatten()]) + "]")
