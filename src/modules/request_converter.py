import re
import sys
import os

# Sample input code
# input_code = ""

# regex = ''
# prefix = ''
# lambda_functions = []

# prefix = 'VIDEO_'
# lambda_functions = ['video-streaming', 'video-decoder', 'video-recog']

# Regular expression to match the input code and capture relevant parts
# regex = r"(\w+) = requests.post\(os.environ\['(VIDEO_DECODER|VIDEO_RECOG)'\], json=\{\"(video|frame)\": base64.b64encode\((\w+)\).decode\(\), \"workflow_id\": workflow_id, \"workflow_depth\": workflow_depth \+ 1, \"workflow_width\": 0\}\).text"
# regex = r"(\w+) = requests.post\(os.environ\['(VIDEO_DECODER|VIDEO_RECOG)'\], json=\{\"(\w+)\": base64.b64encode\((\w+)\).decode\(\), \"workflow_id\": workflow_id, \"workflow_depth\": workflow_depth \+ 1, \"workflow_width\": 0\}\).text"
# regex = rf"(\w+) = requests.post\(os.environ\['(\w+)'\], json=\{prefix}\"(\w+)\": base64.b64encode\((\w+)\).decode\(\), \"workflow_id\": workflow_id, \"workflow_depth\": workflow_depth \+ 1, \"workflow_width\": 0\}\).text"

# regex = rf"(\w+) = requests.post\(os.environ\['{prefix}(\w+)'\], json=\{{\"(\w+)\": base64.b64encode\((\w+)\).decode\(\), \"workflow_id\": workflow_id, \"workflow_depth\": workflow_depth \+ 1, \"workflow_width\": 0\}}\).text"
# regex = r"(\w+) = requests.post\(os.environ\['VIDEO_(\w+)'\], json=\{\"(\w+)\": base64.b64encode\((\w+)\).decode\(\), \"workflow_id\": workflow_id, \"workflow_depth\": workflow_depth \+ 1, \"workflow_width\": 0\}\).text"
# regex = r"(\w+) = requests.post\(os.environ\['VIDEO_\w+'\], json=\{\"(\w+)\": base64.b64encode\((\w+)\).decode\(\), \"workflow_id\": workflow_id, \"workflow_depth\": workflow_depth \+ 1, \"workflow_width\": 0\}\).text"


def find_common_prefix():
    print("LFs: ", lambda_functions)
    common_prefix = os.path.commonprefix(lambda_functions)
    print("Common prefix: ", common_prefix)
    return common_prefix.replace('-', '_').upper()

# Function to determine the output function name based on the environment variable
def determine_function_name(env_var):
    print("--> FUNCTION CALLED BY MAIN: ", function_called_by_main_dict)
    # function_called = function_called_by_main_dict[lf]
    # print("FUNCTION CALLED: ", function_called)
    # return function_called
    return "Decode" if env_var == "VIDEO_DECODER" else "Recognise"

# Replacement function to format the output code
def replacement(match):
    # all_matches = re.findall(regex, input_code)
    # print('TEMP: ', len(all_matches))
    # print(all_matches)


    variable_name = match.group(1)
    env_var = match.group(2)

    print("<->ENV_VAR: ", env_var)
    
    json_key = match.group(3)
    encoded_value = match.group(4)
    # function_name = determine_function_name(env_var)
    
    request_name = prefix + '-' + env_var
    request_name = request_name.replace('_', '').lower()
    
    print("Request name: ", request_name)

    lf = prefix + env_var

    lf = lf.replace('_', '-').lower()

    if lf in lambda_functions:
        function_name = lf.replace('-', '_') + '_' + function_called_by_main_dict[lf]
        # function_name = lf.replace('-', '_') + '_' + request_name
        print("FOUND A MATCH!", lf)
    else:
        print("NO MATCH!", lf)
        exit()

    print("DE DAME: ", function_called_by_main_dict[lf])

    # print(f'variable_name: {variable_name}, env_var: {env_var}, json_key: {json_key}, encoded_value: {encoded_value}, function_name: {function_name}')
    return f'{variable_name} = {function_name}({{"{json_key}": base64.b64encode({encoded_value}).decode()}})'

def main(input_code='', input_functions=[], function_called_by_main={}):
    global regex, prefix, lambda_functions, function_called_by_main_dict
    print("Input functions: ", input_functions)
    print()

    lambda_functions = input_functions
    function_called_by_main_dict = function_called_by_main

    print("Lambda functions: ", lambda_functions)
    print()

    prefix = find_common_prefix()
    
    regex = rf"(\w+) = requests.post\(os.environ\['{prefix}(\w+)'\], json=\{{\"(\w+)\": base64.b64encode\((\w+)\).decode\(\), \"workflow_id\": workflow_id, \"workflow_depth\": workflow_depth \+ 1, \"workflow_width\": 0\}}\).text"

    # Perform the replacement
    output_code = re.sub(pattern=regex, repl=replacement, string=input_code)
    # output_code = re.sub(regex, replacement, input_code)

    print("\033[94mInput code:\033[0m")
    print(input_code)
    print()

    print("\033[94mOutput code:\033[0m")
    print(output_code)
    print()

    return output_code

if __name__ == "__main__":
    main()