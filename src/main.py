# Library imports
import os
import sys

# File imports
from modules.shared_variables import in_folder
from modules.requirements_merge import main as requirements_merge
from modules.yaml_merge import main as yaml_merge
from modules.imports_merge import main as imports_merge
from modules.tree import main as tree

# Global variables
dictionary = {}

def main():
    
    # check for arguments
    if len(sys.argv) > 1:
        initial_function = sys.argv[1]
    else:
        initial_function = 'video-streaming'

    # print the current directory
    print('Current directory:', os.getcwd())

    # Print the names of the directories in the current directory
    lamda_functions = []
    directories = []
    print('Subdirectories:')
    for name in os.listdir(in_folder):
        if os.path.isdir(os.path.join(in_folder, name)):
            directories.append(name)
            lamda_functions.append(name)
            print(name)
    print()

    print("Lambda functions: ")
    print(lamda_functions)


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

    # Find the function names
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

    merged_requirements = requirements_merge()
    print("Merged requirements:")
    print(merged_requirements)

    merged_yaml = yaml_merge()
    print("Merged YAML:")
    print(merged_yaml)

    imports, from_imports, total_imports = imports_merge()
    print("Imports:")
    print(imports)
    print()
    print("From imports:")
    print(from_imports)
    print()

    buffer = tree()

    print("TOTAL IMPORTS:")
    print(total_imports)

    output = total_imports + buffer

    with open('temp.py', 'w') as f:
        # f.write(buffer)
        f.write(output)

if __name__ == '__main__':
    main()