# Library imports
import os

# File imports
# from lambda_function import Node, LambdaFunctionCode    # check later if node is necessary

in_folder = './in/'
dictionary = {}

# Print the names of the directories in the current directory
lambda_functions = []
print('Subdirectories:')
for name in os.listdir('.'):
    if os.path.isdir(name):
        dictionary[name] = {}
        lambda_functions.append(name)
        print(name)
print()

# Print the name of the files in each subdirectory
for lambda_function in lambda_functions:
    print(f'Files in {lambda_function}:')
    for name in os.listdir(lambda_function):
        dictionary[lambda_function][name] = []
        print(f'  {name}')
    print()


# Get the list of functions in each file
function_names = [] 
for lambda_function in lambda_functions:
    print(f'Files in {lambda_function}:')
    for name in os.listdir(lambda_function):
        # find the func.py file
        if name == 'func.py':
            print(f'  {name}')
            with open(f'{lambda_function}/{name}') as f:
                code = f.read().split('\n')

                for line in code:
                    if 'def' in line and 'main' not in line:
                        new_func_name = line.split(' ')[1].split('(')[0]
                        if new_func_name not in function_names:
                            dictionary[lambda_function][name].append(new_func_name)
                            function_names.append(new_func_name)                
                        else:
                            print(f'Function {new_func_name} already exists')
print("Function names:")
print(function_names)


print("Dictionary:")
print(dictionary)
print()

# set starting function
starting_function = 'video-streaming'   # hardcoded for now
print(dictionary[starting_function])

newly_called_function = ''
buffer = ""
change_file_flag = True
eof_flag = False

while not eof_flag:
    print(f'Starting function: {starting_function}')
    if change_file_flag:
        with open(f'{starting_function}/func.py') as f:
            code = f.read().split('\n')
            change_file_flag = False

            for line in code:
                if 'import' in line.split():
                    continue
                print(line)
                buffer += line + '\n'
                if 'requests.post' in line:
                    newly_called_function = line.split('(')[1].split(',')[0].lower().replace('_', '-')
                    print(f'Newly called function: {newly_called_function}')
                    
                    # print("lfs:")
                    # print(lambda_functions)

                    # search for the function in lambda functions
                    for lf in lambda_functions:
                        if lf in newly_called_function:
                            print(f'Lambda function {lf} is called')
                            starting_function = lf
                            change_file_flag = True
                            # f.close()
                            break
                    break
            else:   # executed if the loop ended normally (no break)
                eof_flag = True
            
print("Buffer:")
print("-------------------")
print(buffer)
print("-------------------")

# OLD CODE
'''
with open(f'{starting_function}/func.py') as f:
    code = f.read().split('\n')

    # find the main function
    for line in code:
        if 'def' in line and 'main' in line:
            print("Main function found")
            print(line)
            flag = True
        
        if flag:
            if 'requests.post' in line:
                newly_called_function = line.split('(')[1].split(',')[0].lower()
                print(f'Newly called function: {newly_called_function}')
                break

            if 'return' in line:
                break

            buffer += line + '\n'
newly_called_function = newly_called_function.replace('_', '-')

eof_flag = False
while not eof_flag:
    
    for lf in lambda_functions:
        if lf in newly_called_function:
            print(f'Lambda function {lf} is called')
            break

'''