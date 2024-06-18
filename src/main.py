# Library imports
import os

# File imports
# from lambda_function import Node, LambdaFunctionCode    # check later if node is necessary

# Global variables
in_folder = './benchmarks/'
dictionary = {}

# print the current directory
print('Current directory:', os.getcwd())

# Print the names of the directories in the current directory
lamda_functions = []
# print('Subdirectories:')
# OLD
# for name in os.listdir('.'):
#     if os.path.isdir(name):
#         dictionary[name] = {}
#         lamda_functions.append(name)
#         print(name)
# print()

# NEW
directories = []
print('Subdirectories:')
for name in os.listdir(in_folder):
    if os.path.isdir(os.path.join(in_folder, name)):
        directories.append(name)
        lamda_functions.append(name)
        print(name)
print()

# Print the name of the files in each subdirectory
for lamda_function in lamda_functions:
    print(f'Files in {lamda_function}:')
    for name in os.listdir(in_folder + lamda_function):
        if not os.path.isdir(os.path.join(in_folder, lamda_function, name)):
            if lamda_function not in dictionary:
                dictionary[lamda_function] = {}
            dictionary[lamda_function][name] = []
            print(f'  {name}')
    print()


function_names = [] 
for lamda_function in lamda_functions:
    print(f'Files in {lamda_function}:')
    for name in os.listdir(in_folder + lamda_function):
        # find the func.py file
        if name == 'func.py':
            print(f'  {name}')
            with open(os.path.join(in_folder, lamda_function, name)) as f:
                code = f.read().split('\n')

                for line in code:
                    if 'def' in line and 'main' not in line:
                        new_func_name = line.split(' ')[1].split('(')[0]
                        if new_func_name not in function_names:
                            dictionary[lamda_function][name].append(new_func_name)
                            function_names.append(new_func_name)                
                        else:
                            print(f'Function {new_func_name} already exists')

print("Function names:")
print(function_names)


print("Dictionary:")
print(dictionary)