from project_classes import UserInput, SolveTransportationProblem

user_input = UserInput()
user_input.collect_data()
tr_problem = SolveTransportationProblem(user_input.S, user_input.C, user_input.D, user_input.size[0], user_input.size[1])
tr_problem.print_input_parameter_table()
result = tr_problem.transportation_problem_nw()
print(*result)
