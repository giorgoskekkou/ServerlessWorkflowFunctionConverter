from .function_merge import main as function_merge
from .request_converter import main as conv

in_folder = './benchmarks/'

function_names = []
list_of_nodes = []
function_calls = []
hierarchical_functions = {}
function_dictionary = {}
lambda_functions = []

def tokenize_line(line: str):
    tokens = []
    buffer = ''
    for char in line:
        if char in [' ', '.', '(', ')']:
            tokens.append(buffer)
            buffer = ''
        else:
            buffer += char
    return tokens

def remove_duplicates(l: list):
    new_l = []
    for item in l:
        if item not in new_l:
            new_l.append(item)
    return new_l

def is_post_request(line, lambda_functions):
    matches = []
    for lambda_function in lambda_functions:
        pattern = lambda_function.replace('-', '_').upper()
        print(pattern)
        # if lambda_function in line:
        if pattern in line:
            matches.append(lambda_function)
            print("MATCH: ", lambda_function)
    return matches

def is_function_call(line, function_names):
    # print("FUNCTION NAMES: ", function_names)
    function_matches = []
    stripped_line = line.strip()
    for name in function_names:
        tokenized_line = tokenize_line(line)
        # print("Tokenized line: ", tokenized_line)
        if name in tokenized_line and ('.' + name) not in stripped_line:
            function_matches.append(name)
    # print("Function matches: ", remove_duplicates(function_matches))
    return remove_duplicates(function_matches)
    # return function_matches

def str_in_params(str_pattern, params):
    for index, param in enumerate(params):
        if str_pattern in param:
            return index
    return None

def remove_parameters(line, params):
    print("PARAMS: ", params)
    # return line.replace("workflow_id", "workflow_id=''").replace("workflow_depth", "workflow_depth=''")
    # OLD
    
    buffer = ''
    flag = -1    # -1 : before, 0 : during, 1 : after
    write_flag = False
    
    print("Line: ", line)
    print("Params: ", params)


    for char in line:
        if char == '(':
            buffer += char
            flag = 0
        elif char == ')':
            # buffer += char
            # flag = True
            flag = 1
            

        if flag == -1:
            buffer += char
        elif flag == 0 and not write_flag:
            buffer += ','.join(params)
            write_flag = True
        elif flag == 1:
            buffer += char
        
            # line += ','.join(params)
    return buffer

def remove_arguments(line):
    buffer = ''
    arguments = ''
    flag = -1    # -1 : before, 0 : during, 1 : after
    
    print("Line: ")
    print("BEFORE: ", line)


    for char in line:
        if char == '(':
            if flag == -1:
                buffer += char
                flag = 0
                continue
            else:
                return line
        elif char == ')':
            # buffer += char
            # flag = True
            # list_of_arguments = arguments.split(',')    
            # Remove arguments
            # for arg in list_of_arguments:
            #     if 'workflow' in arg:
            #         list_of_arguments.remove(arg)
            if flag == 0:
                list_of_arguments = arguments.split(',')
                # Create a new list excluding arguments that contain 'workflow'
                list_of_arguments = [arg for arg in list_of_arguments if 'workflow' not in arg]
                
                buffer += ','.join(list_of_arguments)
                flag = 1
            else:
                return line            

        if flag == -1:
            buffer += char
        elif flag == 0:
            arguments += char
        elif flag == 1:
            buffer += char
    
    print("-________________-")
    print("Arguments: ", arguments)
    print("Split: ", arguments.split(','))
    print("-________________-")

    # list_of_arguments = arguments.split(',')    
    # # Remove arguments
    # for arg in list_of_arguments:
    #     if 'workflow' in arg:
    #         list_of_arguments.remove(arg)
    
    print("AFTER: ", buffer)

    return buffer

def check_line(line):
    if 'workflow' in line:
        return False
    return True

def main():
    function_dictionary, lambda_functions, initial_function = function_merge()

    function_names = [function_dictionary[function]['function_name'] for function in function_dictionary]

    for item in function_dictionary:
        directory = function_dictionary[item]['directory']
        function_name = function_dictionary[item]['function_name']
        if directory not in hierarchical_functions:
            hierarchical_functions[directory] = []
        hierarchical_functions[directory].append(function_name)

    print("Hierarchical functions: ", hierarchical_functions)


    print("Function names: ", function_names)

    new_function_calls = {}
    function_called_by_main = {}
    for lambda_function in lambda_functions:
        with open(f'{in_folder}{lambda_function}/func.py') as f:
            code = f.read().split('\n')
            
            # for function_element in function_dictionary:
            #     print(function_element)
            for function_element in function_dictionary:
                el = function_dictionary[function_element]
                if el['directory'] == lambda_function:
                    start = el['start']
                    end = el['end']
                    # print(f"Function: {el['function_name']} at {start} - {end} from file: {lambda_function}")
                    for index in range(start - 1, end):
                        line = code[index]
                        # print(line)
                        if line.strip().startswith('#'):
                            continue
                        # print("TEMP: ", el['function_name'])
                        # print(hierarchical_functions[lambda_function])  # see later
                        function_matches = is_function_call(line, hierarchical_functions[lambda_function])
                        # function_matches = is_function_call(line, function_names)
                        # if function_name and function_name != el['function_name']:
                        if function_matches != []:
                            # print("FUNCTION MATCES: ", function_matches)

                            for i in range(len(function_matches)):
                                if function_matches[i] != el['function_name']:
                                    print(f"Function call: {el['function_name']} -> {function_matches[i]}")
                                    function_calls.append({'src': el['function_name'], 'dst': function_matches[i] , 'lambda': lambda_function, 'line': index + 1})

                                    # Remove arguments from the function call
                                    # code[i] = remove_arguments(line)
                                    new_function_calls[index] = remove_arguments(line)
                                    # line = remove_arguments(line)
                                    
                            if el['function_name'] == 'main' and len(function_matches) == 1:
                                function_called_by_main[lambda_function] = function_matches[0]

                                    # print(f"Function call: {function_names[i]}")
                                    # function_calls.append({'src': el['function_name'], 'dst': function_names[i] , 'lambda': lambda_function, 'line': index + 1})
                            # print(f"Function call: {function_name}")
                            # function_calls.append({'src': el['function_name'], 'dst': function_name , 'lambda': lambda_function, 'line': index + 1})

    print(function_calls)
    # for key in function_calls:
    #     print(key)

    # TEST CODE to replace the function definition and calls with new function names
    buffer = ""

    print()
    print("Lambda functions: ", lambda_functions)
    print()

    # lambda_functions = ['video-streaming', 'video-decoder', 'video-recog'] # hardcoded for now
    # initial_function = lambda_functions[0] # hardcoded for now
    print("Initial function: ", initial_function)

    for lambda_function in lambda_functions:
        # buffer = ""
        with open(f'{in_folder}{lambda_function}/func.py') as f:
            code = f.read().split('\n')
            
            print(f"Lambda function: {lambda_function}")
            # for line in code:
                # print(line)
            # print()
            i = 0
            # n = len(code)
            # for i in range(len(code)):
            while i < len(code):
                line = code[i]
                if 'import' in line.split():
                    i += 1
                    continue
                
                # add prefix to the function calls 
                for function_call in function_calls:
                    if function_call['line'] == i + 1 and function_call['lambda'] == lambda_function:
                        new_func_name = f"{function_call['lambda'].replace('-', '_')}_{function_call['dst']}"
                        line = line.replace(function_call['dst'], new_func_name)
                        
                        print(line)
                
                # add prefix to the function definitions
                for key, value in function_dictionary.items():
                    skip_flag = False
                    if value['directory'] == lambda_function and value['start'] == i + 1:
                        if  value['function_name'] != 'main':
                            # new_func_name = key.replace('-', '_')
                            line = line.replace(value['function_name'], key.replace('-', '_'))
                            print("--1--")
                            print(line)

                            remove_flag = False
                            # remove workflow parameters
                            # if 'workflow_id' in value['parameters']:
                            # if str_in_params('workflow_id', value['parameters']):
                            returned_index = str_in_params('workflow_id', value['parameters'])
                            if returned_index is not None:
                                value['parameters'].pop(returned_index)
                                # value['parameters'].remove('workflow_id')
                                remove_flag = True

                            # if 'workflow_depth' in value['parameters']:
                            # if str_in_params('workflow_depth', value['parameters']):
                            returned_index = str_in_params('workflow_depth', value['parameters'])
                            if returned_index is not None:
                                # value['parameters'].remove('workflow_depth')
                                value['parameters'].pop(returned_index)
                                remove_flag = True
                            
                            
                            if remove_flag:
                                print("New parameters: ", value['parameters'])
                                print("\n88888888888")
                                print("BEF: ", line)
                                line = remove_parameters(line, value['parameters'])
                                print("AFT: ", line)
                                print("88888888888\n")

                            print("-1.5--")
                            print(line)

                        elif value['function_name'] == 'main' and lambda_function != initial_function:
                            print("--2--")
                            print(f"Function: {lambda_function} at line {i + 1}")
                            print(f"{lambda_function} - {initial_function}")
                            print(f"function name: {value['function_name']} - {key}")
                            i = value['end']
                            skip_flag = True
                            break
                        
                
                if skip_flag:
                    print("--SKIP--")
                    continue

                # find the lambda function post request call
                if 'requests.post' in line:
                    print("FOUND POST REQUEST on line: ", line)
                    lambda_function_matches =  is_post_request(line, lambda_functions)
                    print(lambda_function_matches)
                    print()
                    line = conv(line, lambda_functions, function_called_by_main)
                    
                    # print("Call conv")
                    # conv(lambda_functions, line)
                    # print('requests.post')
                elif 'partial(' in line:
                    for key, value in function_dictionary.items():
                        if value['directory'] == lambda_function:
                            line = line.replace(value['function_name'], key.replace('-', '_'))
                            print(line)


                buffer += line + '\n'
                i += 1

    # color codes
    RED = '\033[91m'
    END = '\033[0m'

    # print buffer
    print()
    print(f"{RED}THIS IS THE BUFFER: {END}")
    print(buffer)

    return buffer


if __name__ == '__main__':
    main()

