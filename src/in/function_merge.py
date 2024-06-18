# Library imports
import os

# File imports
# from lambda_function import Node, LambdaFunctionCode    # check later if node is necessary
def get_function_name(full_name):
    parts = full_name.split('_')
    without_first_prefix = parts[1:]
    return '_'.join(without_first_prefix)
    
    

def main():
    in_folder = './benchmarks/'
    dictionary = {}

    functions_dictionary = {}

    # Print the names of the directories in the current directory
    lambda_functions = []

    print('Subdirectories:')
    for name in os.listdir(in_folder):
        if os.path.isdir(os.path.join(in_folder, name)):
            dictionary[name] = {}
            lambda_functions.append(name)
            print(name)
    print()

    # Print the name of the files in each subdirectory
    for lambda_function in lambda_functions:
        print(f'Files in {lambda_function}:')
        for name in os.listdir(os.path.join(in_folder, lambda_function)):
            dictionary[lambda_function][name] = []
            print(f'  {name}')
        print()


    # Get the list of functions in each file
    function_names = [] 
    for lambda_function in lambda_functions:
        print(f'Files in {lambda_function}:')
        for name in os.listdir(os.path.join(in_folder, lambda_function)):
            # find the func.py file
            if name == 'func.py':
                print(f'  {name}')
                with open(f'{in_folder}{lambda_function}/{name}') as f:
                    code = f.read().split('\n')

                    previous_function = ''
                    new_func_name = ''
                    for index, line in enumerate(code):
                        # if 'def' in line and 'main' not in line:
                        if 'def' in line:
                            previous_function = new_func_name 
                            new_func_name = f"{lambda_function}_{line.split(' ')[1].split('(')[0]}"

                            function_names.append(new_func_name)
                            dictionary[lambda_function][name].append(new_func_name)

                            functions_dictionary[new_func_name] = {
                                'directory': lambda_function,
                                'function_name': get_function_name(new_func_name),
                                'start': index + 1,
                                'end': -1,  # still unknown
                            }

                            if previous_function != '':
                                functions_dictionary[previous_function]['end'] = index - 1
                            # OLD
                            # lambda_function + line.split(' ')[1].split('(')[0]
                            # if new_func_name not in function_names:
                            #     dictionary[lambda_function][name].append(new_func_name)
                            #     function_names.append(new_func_name)

                                # number_of_instances = len(functions_dictionary[new_func_name])
                                # if number_of_instances == 0:
                                #     functions_dictionary[new_func_name] = []
                                # functions_dictionary[new_func_name].append({
                                #     'directory': lambda_function,
                                #     'start': index + 1,
                                #     'end': -1,  # still unknown
                                # })
                            #     functions_dictionary[new_func_name] = {
                            #         'directory': lambda_function,
                            #         'function_name': get_function_name(lambda_function),
                            #         'start': index + 1,
                            #         'end': -1,  # still unknown
                            #     }
                            #     if previous_function != '':
                            #         functions_dictionary[previous_function]['end'] = index - 1
                            # else:
                            #     print(f'Function {new_func_name} already exists')
                            #     function_names
                    else:
                        functions_dictionary[new_func_name]['end'] = index

    print("Function names:")
    print(function_names)
    print()

    # function_names.append('prefix_name_surname')
    for function in function_names:
        print(function)
        print(get_function_name(function))
        print()

    print("Dictionary:")
    print(dictionary)
    print()

    print("Functions dictionary:")
    print(functions_dictionary)
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
            with open(f'{in_folder}{starting_function}/func.py') as f:
                code = f.read().split('\n')
                change_file_flag = False

                for line in code:
                    if 'import' in line.split():
                        continue
                    # print(line) # for debugging 
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
    # print(buffer)
    print("-------------------")

    # TEMPORARY RETURN
    return functions_dictionary, lambda_functions

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

if __name__ == '__main__':
    main()